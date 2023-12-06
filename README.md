# Nerd Fonts Icon Search

A multilingual semantic search engine for nerd fonts icons

## Architecture

![](./docs/modules.png)

- **Frontend**: [Material UI](https://mui.com/)
- **App server**: [FastAPI](https://fastapi.tiangolo.com/)
- **Model**: [ChromaDB](https://docs.trychroma.com/)

## Frontend

![](https://img.shields.io/badge/nodejs-20.10%20LTS-green)

### quick start

```shell
# in `$PROJECT_ROOT/frontend` folder
npm install

npm start
```

### deploy

copy `.env` to `.env.local` and edit

```env
REACT_APP_BACKEND_SERVER= ...
```

build and upload static files

```shell
# in localhost `$PROJECT_ROOT/frontend` folder
npm run build

# upload build dir to remote server
scp -r .\frontend\build\ $REMOTE_HOST:$PROJECT_PATH\frontend\build
```

set up Nginx to serve static content

## Backend

![](https://img.shields.io/badge/python-3.11-yellow)

### quick start

```shell
# essential packages to run cloud embedding function
pip install -r requirement.txt

# additional packages to run local embedding function
pip install sentence-transformers

# (optional) additional packages to use cuda to run local embedding function
# see https://pytorch.org/

# start server
#   on the first run, it build the database on ./model/chromadb
python main.py
```

### deploy

on localhost, upload the database to remote

```shell
scp -r .\model\chromadb\ $REMOTE_HOST:$PROJECT_PATH\model
```

on remote host, create `config.py` with the following lines and edit

```python
from default_config import Config

USER_CONFIG = Config(
    huggingface_api_key=...
)
```

on remote host, install the dependencies and start the server

```shell
# on remote host, only install the essential packages
pip install -r requirement.txt

# assuming that the database `./model/chromadb` has already been uploaded
#   also, you need to set up an valid `huggingface_api_key`
python main.py
```

set up uvicorn and Nginx to serve the backend

## References

- [Nerdfonts Cheatsheet](https://www.nerdfonts.com/cheat-sheet)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- [Nodejs on Windows](https://learn.microsoft.com/zh-cn/windows/dev-environment/javascript/nodejs-on-windows)
- [Adding Custom Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/#what-other-env-files-can-be-used)
