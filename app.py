from pprint import pprint

from default_config import config as config_default

config_local = {}
try:
    from local_config import config as config_local  # type: ignore
except ImportError:
    print("No local config found, using default config")
finally:
    config = config_default | config_local


client = chromadb.Client()
collection = client.create_collection(name="glyphs")
