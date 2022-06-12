create or replace function trig_geo2topogeo()

returns trigger as $$
begin

    IF (TG_OP = 'DELETE') THEN
            delete from routes_topogeo_test
            where old.st = routes_topogeo.st and old.en = routes_topogeo.en;
        ELSIF (TG_OP = 'UPDATE') THEN
            update routes_topogeo_test
                set topogeom = toTopoGeom(NEW.geom,'cabi_topo',1,0.1);

        ELSIF (TG_OP = 'INSERT') THEN
                    
            insert into routes_topogeo_test(st, en, topogeom)
            select miss_top.st,
                miss_top.en,
                toTopoGeom(miss_top.geom, 'cabi_topo', 9, 0.1);
        END IF;

end;
$$
language plpgsql;

create trigger update_topogeo 
    after insert or update on route_geometry
    for each row
    execute procedure trig_geo2topogeo();