CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
create table cabi_stations
(
    short_name bigint,
    name text,
    lat double precision,
    lon double precision,
    geometry geometry(Point,4326)
);
create table route_stats
(
    index bigint,
    start_st_id integer,
    end_st_id integer,
    pop bigint
);
create table route_geometry
(
    id serial PRIMARY KEY,
    st bigint,
    en bigint,
    triptime double precision,
    tripdist double precision,
    geom geometry(LineString,26985)
);
SELECT topology.CreateTopology('cabi_topo',26985,0.15);
create table routes_topogeo
(
	rid serial primary key,
	st integer,
	en integer
);
select AddTopoGeometryColumn('cabi_topo', 'public', 'routes_topogeo', 'topogeom', 'LINE');
create table cabi_network_stats
(
	fid serial primary key,
	route_count integer,
	popularity integer,
    geom geometry(LineString,26985)

);
