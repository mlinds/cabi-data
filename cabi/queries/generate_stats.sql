truncate table cabi_network_stats;

with jointtab as
    ( select pp.st,
             pp.en,
             pp.popularity as pop,
             topogeom
     from route_stats as pp -- get all routes we have both route statistics and the topogeo for

     inner join routes_topogeo as tp on pp.st = tp.st
     and pp.en = tp.en), -- of these routes, join all that share the same topological elements
statsums as
    ( select count(jointtab.st) as trip_count,
             sum(jointtab.pop) as total_trips,
             (topelem) [1] as edge_id
     from jointtab, -- return one row for each unique topo element in the route
 getTopoGeomElements(jointtab.topogeom) as topelem -- aggregate on the element ID

     group by topelem) -- for each topoID, get the actual geometry from the topo schema, combine it with the stats, write the results to the new table

insert into cabi_network_stats(route_count, popularity, geom)
select trip_count,
       total_trips,
       geom
from statsums
left join cabi_topo.edge_data on statsums.edge_id = cabi_topo.edge_data.edge_id