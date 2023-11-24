#################################### read config #######################################
import sys

try:
    from config import USER_CONFIG  # type: ignore
except ModuleNotFoundError:
    with open("./config.py", "w") as f:
        f.write(
            """from default_config import Config

USER_CONFIG = Config()
"""
        )
    print("Please edit `config.py` and try again\n")
    sys.exit()
########################################################################################

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

import model.input_data
from model.model import Model, SearchResults

#################################### initialization ####################################
model = Model(input_data=model.input_data.glyphs)

app = FastAPI(
    title="Nerd Iconic Font Search API Documentation",
    # Disable default docs
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=USER_CONFIG.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#################################### API endpoints #####################################
@app.get("/api")
def get_this_docs_page():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Semantic Search",
    )


@app.get("/api/search")
def search(
    q: Annotated[str, Query(title="query text", max_length=50)],
    num_results: Annotated[
        int, Query(title="max number of results", gt=0, le=100)
    ] = 10,
) -> SearchResults:
    return model.search(query_texts=q, n_results=num_results)


#################################### start server ######################################
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        workers=1,
        host=USER_CONFIG.backend_host,
        port=USER_CONFIG.backend_port,
    )
