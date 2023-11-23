# load config
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
    print("please edit `config.py` and try again\n")
    sys.exit()
else:
    print("load config.py\n")
    print(USER_CONFIG)


import chromadb
from chromadb.api.types import EmbeddingFunction
from chromadb.utils import embedding_functions
from tqdm import tqdm

from model import data_subset
from pydantic import BaseModel

class SearchResult(BaseModel):
    ...




def parse_glyph_name(name: str) -> tuple[str, str, str]:
    """
    Args:
        glyph_name, such as "nf-cod-arrow_small_left"

    Return:
        series, group, description, such as:
             ("nf", "code", "arrow small left")
    """
    series, group, raw_description = name.split("-")
    description = raw_description.replace("_", " ")

    return series, group, description


class Model:
    def __init__(self, coll_name: str = USER_CONFIG.huggingface_model) -> None:
        self._client = chromadb.PersistentClient(path="./model/chromadb")
        self._coll_name = coll_name

        # use local embedding function to create the collection and  populate data
        if not self._exist_coll():
            self._coll = self._client.create_collection(
                coll_name, embedding_function=self._get_local_emb_fun()
            )
            self._populate_coll(data_subset.glyphs)

        # switch to cloud embedding function to query whenever possible
        if USER_CONFIG.huggingface_api_key:
            self._coll = self._client.get_collection(
                coll_name, embedding_function=self._get_cloud_emb_fun()
            )

    ############################# private methods ######################################
    def _exist_coll(self) -> bool:
        return any(
            coll.name == self._coll_name for coll in self._client.list_collections()
        )

    def _get_local_emb_fun(self) -> EmbeddingFunction:
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            device=USER_CONFIG.device,
        )

    def _get_cloud_emb_fun(self) -> EmbeddingFunction:
        assert USER_CONFIG.huggingface_api_key, "huggingface_api_key is None"

        return embedding_functions.HuggingFaceEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            api_key=USER_CONFIG.huggingface_api_key,
        )

    def _populate_coll(self, glyphs: dict[str, str]):
        """populate database by glyphs"""
        datas = []
        for glyph_name, unicode in glyphs.items():
            series, group, description = parse_glyph_name(glyph_name)
            if group != "mdi":  # icons in the mdi group have been removed
                datas.append(
                    {
                        "ids": glyph_name,
                        "metadatas": {
                            "series": series,
                            "group": group,
                            "unicode": unicode,
                        },
                        "documents": description,
                    }
                )

        for data in tqdm(datas):
            self._coll.add(**data)

    ############################## public methods ######################################
    def search(self, query: str, n_results: int) -> list[dict]:
        """query database

        Args:
            query: query string
            n_results: top k results

        Return:
            list of dict, each dict contains:
                glyph_name (which is id)
                series
                group
                unicode
                document (which is description)
        """
        result = []
        if query_result := self._coll.query(
            query_texts=[query],
            n_results=n_results,
            include=["metadatas", "documents"],
        ):
            for glyph_name in query_result["ids"]:

            if query_result["metadatas"]:
                for metadata in query_result["metadatas"]:
                    result.append(metadata)

        return result
