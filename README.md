# Nerd Fonts Icon Search

A multilingual semantic search engine for nerd fonts icons

## Architecture

![](./docs/modules.png)

- **Frontend**: [Material UI](https://mui.com/)
- **App server**: [FastAPI](https://fastapi.tiangolo.com/)
- **Model**: [ChromaDB](https://docs.trychroma.com/)

## Frontend

see [`./frontend/README.md`](./frontend/README.md)

## Backend

### Dependencies

![](https://img.shields.io/badge/python-3.11-yellow)

```shell
# essential packages to run cloud embedding function
pip install -r requirement.txt

# additional packages to run local embedding function
pip install sentence-transformers

# additional packages to use cuda to run local embedding function
# see https://pytorch.org/
```

see [`./docs/benchmark.md`](./docs/benchmark.md) about the performance of embedding functions

### Configuration

create `config.py` with the following lines and edit

```python
from default_config import Config

USER_CONFIG = Config(
    # you can get one for free at https://huggingface.co/
    huggingface_api_key =
)
```

see `default_config.py` for detail

### Build database locally

It is recommended to compute the embeddings of all input data locally and upload the database to the server.

```shell
# build the database locally
#   assuming that the database `./model/chromadb` does NOT exist
python app.py

# upload the local database to remote server
scp -r .\model\chromadb\ $REMOTE_HOST:$PROJECT_PATH\model
```

It is OK to build database on Windows 11 and upload to Ubuntu

### Run on a server

```shell
# start server
#   assuming that the database `./model/chromadb` has already been uploaded
#   also, you need to set up an valid `huggingface_api_key`
python app.py
```

## References

- [Nerdfonts Cheatsheet](https://www.nerdfonts.com/cheat-sheet)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
