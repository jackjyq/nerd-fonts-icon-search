import chromadb

client = chromadb.Client()
collection = client.create_collection(name="glyphs")
