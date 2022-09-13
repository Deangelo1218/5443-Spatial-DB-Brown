from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse,HTMLResponse 

import psycopg2
import json



class DatabaseCursor(object):
    """https://stackoverflow.com/questions/32812463/setting-schema-for-all-queries-of-a-connection-in-psycopg2-getting-race-conditi
    https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
    """

    def __init__(self, conn_config_file):
        with open(conn_config_file) as config_file:
            self.conn_config = json.load(config_file)

    def __enter__(self):
        self.conn = psycopg2.connect(
            "dbname='"
            + self.conn_config["dbname"]
            + "' "
            + "user='"
            + self.conn_config["user"]
            + "' "
            + "host='"
            + self.conn_config["host"]
            + "' "
            + "password='"
            + self.conn_config["password"]
            + "' "
            + "port="
            + self.conn_config["port"]
            + " "
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SET search_path TO " + self.conn_config["schema"])

        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # some logic to commit/rollback

        self.conn.commit()
        self.conn.close()


description = """🚀
## Are you having a road trip with your family?
### Why not check out some UFO sighting on your tour!!!!
"""

app = FastAPI(
    title="UFO Sighting near you",
    description=description,
    version="0.0.1",
    terms_of_service="http://killzonmbieswith.us/worldleterms/",
    contact={
        "name": "Deangelo Brown",
        "url": "https://github.com/Deangelo1218/5443-Spatial-DB-Brown",
        "email": "deangelobrown808@gmail.com",
    },
    license_info={
        "name": "Postgres",
        "url": "https://www.postgresql.org/?&",
    },
)


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")


@app.get("/home")
async def root(request: Request):
    return {
        #"Listing of all routes": request.url_for("routes"),
        "URL for 'findAll'": request.url_for("all"),
        "URL for ''findCity'": request.url_for("findCity", **{"city": "Louisville"}),
        "URL for ''findState'": request.url_for("findState", **{"state": "TX"}),
        #"URL for ''closest' pass params from url": request.url_for("closest":"?lng=-98&lat=33"),
    }

##Find all Route

@app.get("/findAll", name="all" )
async def ufo():
    sql = "select * from aliens ORDER BY id OFFSET 100;"

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchall()
        response = {
        "Question": 'Where are all the ufo sightings?',
        "Query": sql,
        "Results": answer
        }

        return response


##Select one ufo sighting e.g = 'Waynesboro'
##Find a single ufo sighting for city

@app.get("/findCity/{city}")
async def findCity(city):
    sql = f"""SELECT * from aliens 
              WHERE city = '{city}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchone()
        response = {
            "Question": 'Where can I find just one ufo sighting in my city?',
            "Query": sql,
            "Results": answer
        }
        return response

#Find single ufo sighting for state

@app.get("/findState/{state}")
async def findState(state):
    sql = f"""SELECT * from aliens 
              WHERE state = '{state}'"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchone()
        response = {
            "Question": 'Where can I find just one ufo sighting in my State?',
            "Query": sql,
            "Results": answer
        }
        return response

#'http://127.0.0.1:8080/closest/?ufo=Waynesboro'    

#SELECT * FROM ufo WHERE  lat = 38.0652286 AND lng = -78.90588756;


#Pass in latitude and longitude and search for all locations 

@app.get("/closest/")
async def findClosest(lat: float , lng: float):
    sql = f"""SELECT *, ST_Distance('SRID=4326;POINT({lng} {lat})'::geometry, location) 
                        FROM aliens
                        ORDER BY id LIMIT 10;"""

    with DatabaseCursor(".config.json") as cur:
        cur.execute(sql)
        answer = cur.fetchall()
        response = {
            "Question": 'Where can I find all the neighboring ufo sightings from my given location?',
            "Query": sql,
            "Results": answer
        }
        return response


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8080, log_level="debug", reload=True)