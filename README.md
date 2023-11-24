# Iconic Font Search

![](https://img.shields.io/badge/python-3.11-yellow)

## Dependencies

```shell
# packages to run cloud embedding function
pip install -r requirement.txt

# additional packages to run local embedding function
pip install sentence-transformers

# additional to use cuda to run local embedding function
# see https://pytorch.org/
```

## Build locally

```shell
# build the database locally
#   assuming that the database on `./model/chromadb` does NOT exist
python app.py

# upload the local database to remote server
#   We can build on Windows and upload to Ubuntu
scp -r .\model\chromadb\ $REMOTE_HOST:$PROJECT_PATH\model
```

## Run on server

```shell
# start server
#   assuming that the database on `./model/chromadb` has already been uploaded
python app.py
```

## Design

![](./docs/modules.png)

## References

- [Nerdfonts Cheatsheet](https://www.nerdfonts.com/cheat-sheet)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- [ChromaDB](https://docs.trychroma.com/)
