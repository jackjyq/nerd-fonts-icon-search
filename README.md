# Semantic Search

![](https://img.shields.io/badge/python-3.11-yellow)

## Build database locally

```shell
# include sentence_transformers and Jupyter stuff,
#   so that you could build database locally, which is faster
pip install -r req_full.txt

# build the database (assuming that the database does NOT exist)
python app.py

# upload the local database to remote (We can build on Windows and run on Ubuntu)
scp -r .\model\chromadb\ $REMOTE_HOST:$PROJECT_PATH\model
```

Note: the `req_full.txt` file may be platform dependent. i.e. you may need to fix it if you are not using Windows. for example:

```shell
# find this line and append the following marker.
pywin32==306; platform_system=="Windows"
```

## Deploy on a server

```shell
# exclude sentence_transformers to save resources,
#   thus you must set `huggingface_api_key` in config.py
#
# Tested on both Windows and Ubuntu
pip install -r req_mini.txt

# start server (assuming that the database exist)
python app.py
```

## Moduels

![](./docs/modules.png)

## References

- [Nerdfonts Cheatsheet](https://www.nerdfonts.com/cheat-sheet)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- [ChromaDB](https://docs.trychroma.com/)
