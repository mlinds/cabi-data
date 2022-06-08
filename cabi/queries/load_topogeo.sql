analyze;

with joinedtable as (
    select
        station_routes.st,
        station_routes.en,
        topogeom,
        geom,
        row_number() over (
            order by
                tripdist desc
        ) as rid
    from
        station_routes
        left join routes_topogeo on station_routes.st = routes_topogeo.st
        and station_routes.en = routes_topogeo.en
),
-- get a table of rows that are in geometry but missing from topogeometry
miss_top as (
    select
        st,
        en,
        geom,
        rid
    from
        joinedtable
    where
        joinedtable.topogeom is null
)
-- write a subset of missing rows to the topo table
insert into
    routes_topogeo(st, en, topogeom)
select
    miss_top.st,
    miss_top.en,
    toTopoGeom(miss_top.geom, 'cabi_topo', 1, 0.1)
from
    miss_top
limit
    100