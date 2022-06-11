create or replace function trig_geo2topogeo()

returns trigger as $$
begin
update routes_topogeo 
    set topogeom = toTopoGeom(NEW.geom,'cabi_topo',1,0.1)

end;
language plpgsql;

create trigger update_topogeo 
    after insert or update on route_geometry
    for row 
    execute procedure 