try:
    from local_config import CONFIG  # type: ignore
except ImportError:
    print("No local config found, using default config")
    from default_config import CONFIG

import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm

from model.data import GLYPHS


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
    def __init__(self) -> None:
        self._client = chromadb.PersistentClient(path="./database")
        self._collection_name = CONFIG["model_name"].replace("-", "_")
        try:
            self._collection = self._load_collection_with_api_embedding_function()

        except ValueError:
            self._collection = self._create_collection_with_local_embedding_function()
            self._populate()

    ############################# private methods ######################################
    def _load_collection_with_api_embedding_function(self) -> chromadb.Collection:
        """use embedding function through API
        Raise:
            ValueError: if collection does not exist
        """
        return self._client.get_collection(
            name=self._collection_name,
            embedding_function=embedding_functions.HuggingFaceEmbeddingFunction(
                api_key=CONFIG["huggingface_api_key"],
                model_name=CONFIG["model_name"],
            ),
        )

    def _create_collection_with_local_embedding_function(self) -> chromadb.Collection:
        """use embedding function locally"""
        return self._client.create_collection(
            name=self._collection_name,
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=CONFIG["model_name"],
                device=CONFIG["device"],
            ),
        )

    def _populate(self):
        """populate database by GLYPHS"""
        datas = []
        for glyph_name, unicode in GLYPHS.items():
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
            self._collection.add(**data)

    ############################## public methods ######################################
    def query(self, query: str, n_results: int) -> list[dict]:
        """query database

        Args:
            query: query string
            n_results: top k results

        Return:
            list of dict, each dict contains:
                ids: glyph name
                metadatas: dict, contains series, group, unicode
                score: float
        """
        query_result = self._collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["metadatas"],
        )

        for metadata in query_result["metadatas"]:
            ...

        return result
