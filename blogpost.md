# What i did

## Steps to recreating this analysis

### Downloading CaBi Trip data
1. Download all CSV data of the trips
2. Write python functions to parse the data, count the number of trips between station pairs, and return a summary of the data

### Visualizing the popularity of trips between stations
1. Create a visualization using altair
2. Compile the altair to vega using the vegalite web viewer
3. Add the vega to a leaflet map and host it from github

## Create a docker app to contain the various app
1. get PostGIS image
2. get valhalla image
3. get get pgadmin image

### Setting up Valhalla server
1. download the GeoFabrik files for Virginia Maryland, and DC
2. Use OSMconvert to merge the files

```shell
sudo apt install osmctools
osmconvert VA.pbf --out-o5m -b=-77.3724,38.7685,-76.8474,39.1599 \
 | osmconvert - MD.pbf --out-o5m -b=-77.3724,38.7685,-76.8474,39.1599 \
 | osmconvert - DC.pbf --out-o5m -b=-77.3724,38.7685,-76.8474,39.599 -o=all_dc_area.pbf
```
3. Point the vahalla docker file to this directory
4. On the first run, build the tiles. It will take a really long time depending on the area

### Setting up postgis database
1. Create the following tables:
   - capital bikeshare stations
        ```sql
        create table cabi_stations
        (
            short_name bigint,
            name text,
            lat double precision,
            lon double precision,
            tripcount bigint,
            roundtrips double precision,
            -- use MD State Plane Meters
            geometry geometry(Point,26985)
        );
        ```
    - Table showing the number of trips between stations
        ```sql
        create table station_popularity
        (
            index bigint,
            start_st_id integer,
            end_st_id integer,
            pop bigint
        );
        ```
    - Empty Table with geometry between stations
        ```sql
        create table station_routes
        (
            st bigint,
            en bigint,
            popularity bigint,
            geom geometry(LineString,26985)
        );
        ```
2. Set up PostGIS topology
   
   To use topology, you first have to load the expression using 
   ```sql
    CREATE EXTENSION postgis_topology;
   ```
    The next step is to create an empty topology, that we will later fill
    ```sql
    -- allowing a tolerance of 0.15 to account for coordinate conversion
    SELECT topology.CreateTopology('cabi_topo',26985,0.15);
    ```

###  Run every trip through the routing model using a python script

This could also be done in a point-and-click GIS like QGIS using the valhalla extension. However, we will use the valhalla python API. 

To get realistic routing, the costing parameters need to be set. I played with different configurations for a while until the results looked *the most similar* to the route I would take based on my many years biking in DC. 

```json
"costing_options": {
            "bicycle": {
                "bicycle_type": "hybrid",
                "use_roads": 0.1,
                "use_hills": 0.1,
                "use_ferry": 0,
            }
        },
```

When riding a heavy, slow CaBi bike, you're more inclined to avoid hills, and I assumed many cabi users are casual cyclists who try to avoid traffic to the extent possible, so I chose the parameters to **strongly** prefer bike trail over roads. Also, I don't know anyone in DC who might casually hop on a ferry to cross the Potomac, so I set the costing model avoid any ferry crossings. The final results look very realistic based on my judgement of areas i've spot-checked. A few major caveats apply:

- I based this on my judgement, you might prefer a different route
- I only routed the trips one way, then for the reverse trip I used the same route. For most cases, this will result in no or a very small diference. There might be edge cases where the route in one direction is significantly different than another.
- I don't claim that these routes are anywhere near 100% accurate. They are a rough simulation, and we have no idea what route the trip actually took. I think that on the aggregate, they do give a good estimate of how much CaBi Bike traffic follows a particular street. They are probably more realistic in areas with a high density of trips. 


### adding topology to geodatabase

```sql
select CreateTopology('cabi_topo', 26985, 0.1);
create table routes_topogeo
(
	rid serial primary key,
	st integer,
	en integer
);
select AddTopoGeometryColumn('cabi_topo', 'public', 'routes_topogeo', 'topogeom', 'LINE');
```

Once the topology information is created, the trips can be loaded in. This is a very slow operation because topology operations require many reads/writes to the topology table. I've found it is best down in chunks with an ANALYZE in between. I sorted them by distance first, with my thinking being that the longer trips would take longer to add to the topology tables, and that after I got the longest trips loaded I could make the chunk size a lot bigger. There might be a more efficient way to sort them - this requires a little more investigation.

The query to load the trips in chunks is:

```sql
analyze;
-- add a subquery that sorts by distance and then adds the row number
with 
aa as (
select st,en,geom,row_number() over (order by tripdist desc) as rid from station_routes
)
insert into routes_topogeo(rid,st,en,topogeom)
select aa.rid,aa.st,aa.en,toTopoGeom(aa.geom,'cabi_topo',1,0.1) from aa where aa.rid >10000 and aa.rid<=15000
```

This could be written using python and psychopg2, and possibly optimized to run in parallel. Right now the operation is extremely slow, so there is a lot of room for improvement.

Some other possible improvements:
- create a unique ID for each station combo, maybe add a serial field to 

