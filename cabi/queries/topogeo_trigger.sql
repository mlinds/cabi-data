create or replace function trig_geo2topogeo() returns trigger as $$
begin
    IF (TG_OP = 'DELETE') THEN
            delete from routes_topogeo
            where OLD.st = routes_topogeo.st and Old.en = routes_topogeo.en;
        ELSIF (TG_OP = 'UPDATE') THEN
            update routes_topogeo
                set topogeom = toTopoGeom(NEW.geom,'cabi_topo',1,0.1);

        ELSIF (TG_OP = 'INSERT') THEN
            insert into routes_topogeo(st, en, topogeom)
            select NEW.st,
                NEW.en,
                toTopoGeom(NEW.geom, 'cabi_topo2', 1, 0.1);
        END IF;
	return NULL;
end;
$$ language plpgsql;


create or replace trigger update_topogeo after
insert
or
update
or
delete on route_geometry
for each row execute procedure trig_geo2topogeo();