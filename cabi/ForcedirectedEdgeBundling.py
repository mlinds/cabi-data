from numba import jit, prange, float64, njit
from numba.experimental import jitclass
from numba.typed import List
from numba.types import ListType, int64, uint8
from tqdm.auto import tqdm
import math

# Hyper-parameters
#
# global bundling constant controlling edge stiffness
K = 1.
# initial distance to move points
S_initial = 0.01
# initial subdivision number
P_initial = 1
# subdivision rate increase
P_rate = 2
# number of cycles to perform
C = 6
# initial number of iterations for cycle
I_initial = 70
# rate at which iteration number decreases i.e. 2/3
I_rate = 0.6666667

compatibility_threshold = 0.7
eps = 1e-6

# Execution settings
FASTMATH = False
PARALLEL = False # On usage.ipynb benchmark went from 4min 35s to 4min 41s (slightly worse)
NOGIL = False # On usage.ipynb benchmark went from 4min 38s to 4min 35s (nano improve, thus ignored)


@jitclass([('x', float64), ('y', float64)])
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@jitclass([('source', Point.class_type.instance_type), ('target', Point.class_type.instance_type)])
class Edge:
    def __init__(self, source, target):
        self.source = source
        self.target = target


ForceFactors = Point


@jit(Point.class_type.instance_type(Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def edge_as_vector(edge):
    return Point(edge.target.x - edge.source.x, edge.target.y - edge.source.y)


@jit(float64(Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def edge_length(edge):
    # handling nodes that are the same location, so that K / edge_length != Inf
    if (abs(edge.source.x - edge.target.x)) < eps and (abs(edge.source.y - edge.target.y)) < eps:
        return eps

    return math.sqrt(math.pow(edge.source.x - edge.target.x, 2) + math.pow(edge.source.y - edge.target.y, 2))


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def angle_compatibility(edge, oedge):
    v1 = edge_as_vector(edge)
    v2 = edge_as_vector(oedge)
    dot_product = v1.x * v2.x + v1.y * v2.y
    return max(0.0, dot_product / (edge_length(edge) * edge_length(oedge)))
    #return math.fabs(dot_product / (edge_length(edge) * edge_length(oedge)))


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def scale_compatibility(edge, oedge):
    lavg = (edge_length(edge) + edge_length(oedge)) / 2.0
    return 2.0 / (lavg/min(edge_length(edge), edge_length(oedge)) + max(edge_length(edge), edge_length(oedge))/lavg)


@jit(float64(Point.class_type.instance_type, Point.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def euclidean_distance(source, target):
    return math.sqrt(math.pow(source.x - target.x, 2) + math.pow(source.y - target.y, 2))


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def position_compatibility(edge, oedge):
        lavg = (edge_length(edge) + edge_length(oedge)) / 2.0
        midP = Point((edge.source.x + edge.target.x) / 2.0,
                (edge.source.y + edge.target.y) / 2.0)
        midQ = Point((oedge.source.x + oedge.target.x) / 2.0,
                     (oedge.source.y + oedge.target.y) / 2.0)

        return lavg / (lavg + euclidean_distance(midP, midQ))


@jit(Point.class_type.instance_type(Point.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def project_point_on_line(point, edge):
    L = math.sqrt(math.pow(edge.target.x - edge.source.x, 2) + math.pow((edge.target.y - edge.source.y), 2))
    r = ((edge.source.y - point.y) * (edge.source.y - edge.target.y) - (edge.source.x - point.x) * (edge.target.x - edge.source.x)) / math.pow(L, 2)
    return Point((edge.source.x + r * (edge.target.x - edge.source.x)),
                 (edge.source.y + r * (edge.target.y - edge.source.y)))


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def edge_visibility(edge, oedge):
    # send actual edge points positions
    I0 = project_point_on_line(oedge.source, edge)
    I1 = project_point_on_line(oedge.target, edge)
    divisor = euclidean_distance(I0, I1)
    divisor = divisor if divisor != 0 else eps

    midI = Point((I0.x + I1.x) / 2.0, (I0.y + I1.y) / 2.0)

    midP = Point((edge.source.x + edge.target.x) / 2.0,
                 (edge.source.y + edge.target.y) / 2.0)

    return max(0, 1 - 2 * euclidean_distance(midP, midI) / divisor)


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=True)
def visibility_compatibility(edge, oedge):
    return min(edge_visibility(edge, oedge), edge_visibility(oedge, edge))


@jit(float64(Edge.class_type.instance_type, Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH, nogil=NOGIL)
def are_compatible(edge, oedge):
    angles_score = angle_compatibility(edge, oedge)
    scales_score = scale_compatibility(edge, oedge)
    positi_score = position_compatibility(edge, oedge)
    visivi_score = visibility_compatibility(edge, oedge)

    score = (angles_score * scales_score * positi_score * visivi_score)

    return score >= compatibility_threshold


# No numba, so we have tqdm
def compute_compatibility_list(edges):
    compatibility_list = List()
    for _ in edges:
        compatibility_list.append(List.empty_list(int64))

    total_edges = len(edges)
    for e_idx in tqdm(range(total_edges - 1), unit='Edges'):
        compatibility_list = compute_compatibility_list_on_edge(edges, e_idx, compatibility_list, total_edges)

    return compatibility_list


@jit(ListType(ListType(int64))(ListType(Edge.class_type.instance_type), int64, ListType(ListType(int64)), int64), nopython=True)
def compute_compatibility_list_on_edge(edges, e_idx, compatibility_list, total_edges):
    for oe_idx in range(e_idx + 1, total_edges):
        if are_compatible(edges[e_idx], edges[oe_idx]):
            compatibility_list[e_idx].append(oe_idx)
            compatibility_list[oe_idx].append(e_idx)
    return compatibility_list


# Need to set types on var (they are not available inside a jit function)
pt_cls = Point.class_type.instance_type
list_of_pts = ListType(pt_cls)
@jit(ListType(ListType(Point.class_type.instance_type))(ListType(Edge.class_type.instance_type), uint8), nopython=True)
def build_edge_subdivisions(edges, P_initial=1):
    subdivision_points_for_edge = List.empty_list(list_of_pts)
    for i in range(len(edges)):
        subdivision_points_for_edge.append(List.empty_list(pt_cls))

        #if P_initial != 1:
        subdivision_points_for_edge[i].append(edges[i].source)
        subdivision_points_for_edge[i].append(edges[i].target)

    return subdivision_points_for_edge


@jit(nopython=True, fastmath=FASTMATH, parallel=PARALLEL)
def compute_divided_edge_length(subdivision_points_for_edge, edge_idx):
    length = 0.
    for i in prange(1, len(subdivision_points_for_edge[edge_idx])): 
        segment_length = euclidean_distance(subdivision_points_for_edge[edge_idx][i],
                                            subdivision_points_for_edge[edge_idx][i - 1])
        length += segment_length

    return length


@jit(Point.class_type.instance_type(Edge.class_type.instance_type), nopython=True, fastmath=FASTMATH)
def edge_midpoint(edge):
    middle_x = (edge.source.x + edge.target.x) / 2
    middle_y = (edge.source.y + edge.target.y) / 2

    return Point(middle_x, middle_y)


@jit(nopython=True, fastmath=True)
def update_edge_divisions(edges, subdivision_points_for_edge, P):
    for edge_idx in range(len(edges)):
        divided_edge_length = compute_divided_edge_length(subdivision_points_for_edge, edge_idx)
        segment_length = divided_edge_length / (P + 1)
        current_node = Point(edges[edge_idx].source.x, edges[edge_idx].source.y)
        new_subdivision_points = List()
        number_subdiv_points = 0
        new_subdivision_points.append(Point(current_node.x, current_node.y)) # revisar que no se cambie si cambio el source
        number_subdiv_points += 1
        current_segment_length = segment_length
        i = 1
        finished = False
        while not finished:
            old_segment_length = euclidean_distance(subdivision_points_for_edge[edge_idx][i],current_node)
            # direction is a vector of length = 1
            direction_x = (subdivision_points_for_edge[edge_idx][i].x - current_node.x)/old_segment_length
            direction_y = (subdivision_points_for_edge[edge_idx][i].y - current_node.y)/old_segment_length
            if current_segment_length > old_segment_length:
                current_segment_length -= old_segment_length 
                current_node = Point(subdivision_points_for_edge[edge_idx][i].x, subdivision_points_for_edge[edge_idx][i].y)
                i += 1
            else: 
                current_node.x += current_segment_length * direction_x
                current_node.y += current_segment_length * direction_y
                new_subdivision_points.append(Point(current_node.x, current_node.y))
                number_subdiv_points += 1
                current_segment_length = segment_length
            finished = number_subdiv_points == P+1
        new_subdivision_points.append(Point(edges[edge_idx].target.x, edges[edge_idx].target.y)) 

        subdivision_points_for_edge[edge_idx] = new_subdivision_points

    return subdivision_points_for_edge


@jit(nopython=True, fastmath=FASTMATH, nogil=NOGIL)
def apply_spring_force(subdivision_points_for_edge, edge_idx, i, kP):
    prev = subdivision_points_for_edge[edge_idx][i - 1]
    next_ = subdivision_points_for_edge[edge_idx][i + 1]
    crnt = subdivision_points_for_edge[edge_idx][i]
    x = prev.x - crnt.x + next_.x - crnt.x
    x = x if x >= 0 else 0.
    y = prev.y - crnt.y + next_.y - crnt.y
    y = y if y >= 0 else 0.

    x *= kP
    y *= kP

    return ForceFactors(x, y)


@jit(nopython=True, fastmath=FASTMATH, nogil=NOGIL)
def custom_edge_length(edge):
    return math.sqrt(math.pow(edge.source.x - edge.target.x, 2) + math.pow(edge.source.y - edge.target.y, 2))


@jit(ForceFactors.class_type.instance_type(ListType(ListType(Point.class_type.instance_type)), ListType(ListType(int64)), int64, int64, ListType(float64)), nopython=True, fastmath=FASTMATH) #
def apply_electrostatic_force(subdivision_points_for_edge, compatibility_list_for_edge, edge_idx, i, weights):
    sum_of_forces_x = 0.0
    sum_of_forces_y = 0.0
    compatible_edges_list = compatibility_list_for_edge[edge_idx]
    use_weights = True if len(weights) > 0 else False

    for oe in range(len(compatible_edges_list)):
        if use_weights:
            force = ForceFactors((subdivision_points_for_edge[compatible_edges_list[oe]][i].x - subdivision_points_for_edge[edge_idx][i].x)  * weights[oe],
                                 (subdivision_points_for_edge[compatible_edges_list[oe]][i].y - subdivision_points_for_edge[edge_idx][i].y)  * weights[oe]
                                 )
        else:
            force = ForceFactors((subdivision_points_for_edge[compatible_edges_list[oe]][i].x - subdivision_points_for_edge[edge_idx][i].x),
                                 (subdivision_points_for_edge[compatible_edges_list[oe]][i].y - subdivision_points_for_edge[edge_idx][i].y)
                                 )

        if (math.fabs(force.x) > eps) or (math.fabs(force.y) > eps):
            divisor = custom_edge_length(Edge(subdivision_points_for_edge[compatible_edges_list[oe]][i], subdivision_points_for_edge[edge_idx][i]))
            diff = (1 / divisor)

            sum_of_forces_x += force.x * diff
            sum_of_forces_y += force.y * diff

    return ForceFactors(sum_of_forces_x, sum_of_forces_y)


@jit(nopython=True, fastmath=FASTMATH)
def apply_resulting_forces_on_subdivision_points(edges, subdivision_points_for_edge, compatibility_list_for_edge, edge_idx, K, P, S, weights):
    # kP = K / | P | (number of segments), where | P | is the initial length of edge P.
    kP = K / (edge_length(edges[edge_idx]) * (P + 1))

    # (length * (num of sub division pts - 1))
    resulting_forces_for_subdivision_points = List()
    resulting_forces_for_subdivision_points.append(ForceFactors(0.0, 0.0))

    for i in range(1, P + 1): # exclude initial end points of the edge 0 and P+1
        spring_force = apply_spring_force(subdivision_points_for_edge, edge_idx, i, kP)
        electrostatic_force = apply_electrostatic_force(subdivision_points_for_edge, compatibility_list_for_edge, edge_idx, i, weights)

        resulting_force = ForceFactors(S * (spring_force.x + electrostatic_force.x),
                                       S * (spring_force.y + electrostatic_force.y))

        resulting_forces_for_subdivision_points.append(resulting_force)


    resulting_forces_for_subdivision_points.append(ForceFactors(0.0, 0.0))

    return resulting_forces_for_subdivision_points

# No numba, so we have tqdm
def forcebundle(edges, weights = List.empty_list(float64)):
    S = S_initial
    I = I_initial
    P = P_initial

    subdivision_points_for_edge = build_edge_subdivisions(edges, P_initial)
    print(len(subdivision_points_for_edge))
    compatibility_list_for_edge = compute_compatibility_list(edges)
    subdivision_points_for_edge = update_edge_divisions(edges, subdivision_points_for_edge, P)

    for _cycle in tqdm(range(C), unit='cycle'):
        subdivision_points_for_edge, S, P, I = apply_forces_cycle(edges, subdivision_points_for_edge, compatibility_list_for_edge, K, P, P_rate, I, I_rate, S, weights)

    return subdivision_points_for_edge


@jit(nopython=True, fastmath=True)
def apply_forces_cycle(edges, subdivision_points_for_edge, compatibility_list_for_edge, K, P, P_rate, I, I_rate, S, weights):
    for _iteration in range(math.ceil(I)):
        forces = List()
        for edge_idx in range(len(edges)):
            forces.append(apply_resulting_forces_on_subdivision_points(edges, subdivision_points_for_edge,
                                                                            compatibility_list_for_edge, edge_idx, K, P,
                                                                            S, weights))
        for edge_idx in range(len(edges)):
            for i in range(P + 1): # We want from 0 to P
                subdivision_points_for_edge[edge_idx][i] = Point(
                    subdivision_points_for_edge[edge_idx][i].x + forces[edge_idx][i].x,
                    subdivision_points_for_edge[edge_idx][i].y + forces[edge_idx][i].y
                )



    # prepare for next cycle
    S = S / 2
    P = P * P_rate
    I = I * I_rate

    subdivision_points_for_edge = update_edge_divisions(edges, subdivision_points_for_edge, P)

    return subdivision_points_for_edge, S, P, I


# Helpers
@jit(nopython=True, fastmath=FASTMATH)
def is_long_enough(edge):
    # Zero length edges
    if (edge.source.x == edge.target.x) or (edge.source.y == edge.target.y):
        return False
    # No EPS euclidean distance
    raw_lenght = math.sqrt(math.pow(edge.target.x - edge.source.x, 2) + math.pow(edge.target.y - edge.source.y, 2))
    if raw_lenght < (eps * P_initial * P_rate * C):
        return False
    else:
        return True


# Need to set types on var (they are not available inside a jit function)
edge_class = Edge.class_type.instance_type
@jit(nopython=True)
def get_empty_edge_list():
    return List.empty_list(edge_class)


def net2edges(network, positions):
    edges = get_empty_edge_list()
    for edge in network.edges:
        source = Point(positions[edge[0]][0], positions[edge[0]][1])
        target = Point(positions[edge[1]][0], positions[edge[1]][1])
        edge = Edge(source, target)
        if is_long_enough(edge):
            edges.append(edge)

    return edges


# TODO: add a edges2net method
# Should do the networkx import at function? (so networkx it's only needed if function is used)


@jit(nopython=True)
def array2edges(flat_array):
    edges =  get_empty_edge_list()
    valid_edges = List()
    for edge_idx in range(len(flat_array)):
        source = Point(flat_array[edge_idx][0], flat_array[edge_idx][1])
        target = Point(flat_array[edge_idx][2], flat_array[edge_idx][3])
        edge = Edge(source, target)
        if is_long_enough(edge):
            edges.append(edge)
            valid_edges.append(edge_idx)

    return edges, valid_edges


@jit(nopython=True)
def edges2lines(edges):
    lines = List()
    for edge in edges:
        line = List()
        line.append(Point(edge.source.x, edge.source.y))
        line.append(Point(edge.target.x, edge.target.y))
        lines.append(line)
    return lines
