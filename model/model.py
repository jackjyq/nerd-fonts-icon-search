import functools
import time

import chromadb
from chromadb.api.types import EmbeddingFunction
from chromadb.utils import embedding_functions
from pydantic import BaseModel
from tqdm import tqdm

from config import USER_CONFIG


class SearchResult(BaseModel):
    font_name: str
    series: str | None
    group: str | None
    unicode: str | None
    description: str


class SearchResults(BaseModel):
    results: list[SearchResult]
    num_results: int
    execution_time: float


def timer(func):
    """Print the start and finish message of the decorated function

    Refs:
        https://realpython.com/primer-on-python-decorators/#timing-functions
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        print(f"Starting {func.__name__!r}...")

        result = func(*args, **kwargs)

        run_time = time.perf_counter() - start_time
        print(f"Finished {func.__name__!r} in {run_time:.2f} secs")
        return result

    return wrapper


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
            coll_name: collection name to identify the collection, default is the model name
                       you could specify another collection name to test the same model on different input data

            input_data: (dict) the data to populate the collection
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
                embedding_function=self._load_cloud_embedding_function(),
            )
            if USER_CONFIG.huggingface_api_key
            else self._client.get_collection(
                # otherwise, use local embedding function
                self._coll_name,
                embedding_function=self._load_local_embedding_function(),
            )
        )

    ############################# private methods ######################################
    def _exist_coll(self) -> bool:
        return any(
            coll.name == self._coll_name for coll in self._client.list_collections()
        )

    @timer
    def _load_local_embedding_function(self) -> EmbeddingFunction:
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            device=USER_CONFIG.device,
        )

    @timer
    def _load_cloud_embedding_function(self) -> EmbeddingFunction:
        assert (
            USER_CONFIG.huggingface_api_key
        ), "Failed because huggingface_api_key is None"

        return embedding_functions.HuggingFaceEmbeddingFunction(
            model_name=USER_CONFIG.huggingface_model,
            api_key=USER_CONFIG.huggingface_api_key,
        )

    ############################## public methods ######################################
    def build_coll(self, input_data: dict[str, str] | None):
        """create and populate the collection with input data, existing data will be overwritten

        Raises:
            will raise exception when input_data is None
        """
        # load or create collection with local embedding function
        assert input_data, "Fail to build collection, because the input data is empty"
        coll = self._client.get_or_create_collection(
            self._coll_name,
            embedding_function=self._load_local_embedding_function(),
        )

        # extract data from input_data
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

        # populate the collection
        for item in tqdm(output_data):
            coll.upsert(**item)

    def search(self, query_texts: str, n_results: int) -> SearchResults:
        """search database

        Args:
            query_texts: query text
            n_results: max number of results

        Return:
            SearchResults
        """
        start_time = time.perf_counter()

        results = []
        if query_result := self._coll.query(
            query_texts=[query_texts],
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

        return SearchResults(
            results=results,
            num_results=len(results),
            execution_time=time.perf_counter() - start_time,
        )
