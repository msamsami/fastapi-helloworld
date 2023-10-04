"""
 Contact me:
   e-mail:   enrique@enriquecatala.com 
   Linkedin: https://www.linkedin.com/in/enriquecatala/
   Web:      https://enriquecatala.com
   Twitter:  https://twitter.com/enriquecatala
   Support:  https://github.com/sponsors/enriquecatala
   Youtube:  https://www.youtube.com/enriquecatala
   
"""
import os
from os import environ
import json
from typing import Optional
from loguru import logger

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hello")
def read_root():
    if "HELLOWORLD_ENV" in environ:
        txt = environ.get('HELLOWORLD_ENV')
    else:
        txt = "HELLOWORLD_ENV not found!"
    return {"HELLOWORLD_ENV: {}".format(txt): "from /one/hello"}


@app.get("/aws_access")
def read_root():
    if "AWS_ACCESS" in environ:
        txt = environ.get('AWS_ACCESS')
    else:
        txt = "AWS_ACCESS not found!"
    return {"AWS_ACCESS: {}".format(txt): "from /aws_access"}


@app.get("/get_api_key")
def read_api_key():
    api_key = ""    
    
    try:
        with open('/app/secrets/appconfig.conf') as f:
            js = json.load(f)
            api_key = js["api_key"]
            # Do something with the file
    except Exception as e:
        logger.exception(e)
        print("/app/secrets/appconfig.conf not accessible")

    return {"API_KEY: {}".format(api_key)}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    print("Starting webserver ...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        log_level=os.getenv('LOG_LEVEL', "info"),
        proxy_headers=True
    )
