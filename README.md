# Nerd Iconic Font Search

小呆字体图标搜索

a multilingual semantic search engine for nerd fonts glyphs

![](https://img.shields.io/badge/python-3.11-yellow)

## Dependencies

```shell
# essential packages to run cloud embedding function
pip install -r requirement.txt

# additional packages to run local embedding function
pip install sentence-transformers

# additional packages to use cuda to run local embedding function
# see https://pytorch.org/
```

## Configuration

create `config.py` with the following content and edit

```python
from default_config import Config

USER_CONFIG = Config(
    # you can get one for free at https://huggingface.co/
    huggingface_api_key =
)
```

## Build locally

```shell
# build the database locally
#   assuming that the database `./model/chromadb` does NOT exist
python app.py

# upload the local database to remote server
#   We can build on Windows and upload to Ubuntu
scp -r .\model\chromadb\ $REMOTE_HOST:$PROJECT_PATH\model
```

## Run on server

```shell
# start server
#   assuming that the database `./model/chromadb` has already been uploaded
python app.py
```

## Architecture

![](./docs/modules.png)

## References

- [Nerdfonts Cheatsheet](https://www.nerdfonts.com/cheat-sheet)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- [Nodejs on Windows](https://learn.microsoft.com/zh-cn/windows/dev-environment/javascript/nodejs-on-windows)
- [ChromaDB](https://docs.trychroma.com/)
