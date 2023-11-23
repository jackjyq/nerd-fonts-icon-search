#################################### read config #######################################
import sys

try:
    from config import USER_CONFIG  # type: ignore
except ImportError:
    with open("./config.py", "w") as f:
        f.write(
            """from default_config import Config

USER_CONFIG = Config()
"""
        )
    print("Please edit `config.py` and try again\n")
    sys.exit()
########################################################################################

import chromadb
from chromadb.api.types import EmbeddingFunction
from chromadb.utils import embedding_functions
from pydantic import BaseModel
from tqdm import tqdm

from model import data_subset


class SearchResult(BaseModel):
    font_name: str
    series: str | None
    group: str | None
    unicode: str | None
    description: str


class SearchResults(BaseModel):
    results: list[SearchResult]


def parse_font_name(name: str) -> tuple[str, str, str]:
    """
    Args:
        name, such as "nf-cod-arrow_small_left"

    Return:
        series, group, description, such as:
             ("nf", "code", "arrow small left")
    """
    series, group, raw_description = name.split("-")
    description = raw_description.replace("_", " ")

    return series, group, description


class Model:
    def __init__(
        self,
        coll_name: str = USER_CONFIG.huggingface_model,
        input_data: dict[str, str] | None = None,
    ) -> None:
        """initialize database model

        Args:
            coll_name: collection name to identify the collection
            input_data: (dict) the raw data to populate the collection
                        (None) when the collection exist, the input_data is not needed
                               however, you can still call self.build_coll(input_data)
                               to rebuild the collection
        """
        self._client = chromadb.PersistentClient(path="./model/chromadb")
        self._coll_name = coll_name

        # build collection with input data if not exist
        if not self._exist_coll():
            self.build_coll(input_data)

        # load collection based on config
        self._coll = (
            self._client.get_collection(
                # use cloud embedding function whenever possible
                self._coll_name,
                embedding_function=self._get_cloud_emb_fun(),
            )
            if USER_CONFIG.huggingface_api_key
            else self._client.get_collection(
                # otherwise, use local embedding function
                self._coll_name,
                embedding_function=self._get_local_emb_fun(),
            )
        )

    ############################# private methods ######################################
    def _exist_coll(self) -> bool:
        return any(
            coll.name == self._coll_name for coll in self._client.list_collections()
        )

    def _get_local_emb_fun(self) -> EmbeddingFunction:
        print(f"Loading local embedding function {self._coll_name}...", end=" ")
        emb_fun = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            device=USER_CONFIG.device,
        )
        print("ok!")
        return emb_fun

    def _get_cloud_emb_fun(self) -> EmbeddingFunction:
        print(f"Loading cloud embedding function {self._coll_name}...", end=" ")
        assert (
            USER_CONFIG.huggingface_api_key
        ), "Fail to load because huggingface_api_key is None"

        emb_fun = embedding_functions.HuggingFaceEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            api_key=USER_CONFIG.huggingface_api_key,
        )
        print("ok!")
        return emb_fun

    ############################## public methods ######################################
    def build_coll(self, input_data: dict[str, str] | None):
        """populate the collection with input data, existing data will be overwritten

        Raises:
            will raise exception when input_data is None
        """
        assert input_data, "Fail to build collection, because the input data is empty"

        # create collection with local embedding function
        coll = self._client.get_or_create_collection(
            self._coll_name,
            embedding_function=self._get_local_emb_fun(),
        )

        print("Transforming input data...")
        output_data = []
        for font_name, unicode in input_data.items():
            series, group, description = parse_font_name(font_name)
            if group != "mdi":  # icons in the mdi group have been removed
                output_data.append(
                    {
                        "ids": font_name,
                        "metadatas": {
                            "series": series,
                            "group": group,
                            "unicode": unicode,
                        },
                        "documents": description,
                    }
                )

        print(f"Populating database by {USER_CONFIG.device}...")
        for item in tqdm(output_data):
            coll.upsert(**item)

    def search(self, query: str, n_results: int) -> SearchResults:
        """search database

        Args:
            query: query text
            n_results: top n results

        Return:
            SearchResults
        """
        results = []
        if query_result := self._coll.query(
            query_texts=[query],
            n_results=n_results,
            include=["metadatas", "documents"],
        ):
            for i, font_name in enumerate(query_result["ids"][0]):
                results.append(
                    SearchResult(
                        font_name=font_name,
                        series=query_result["metadatas"][0][i]["series"],  # type: ignore
                        group=query_result["metadatas"][0][i]["group"],  # type: ignore
                        unicode=query_result["metadatas"][0][i]["unicode"],  # type: ignore
                        description=query_result["documents"][0][i],  # type: ignore
                    )
                )

        return SearchResults(results=results)
