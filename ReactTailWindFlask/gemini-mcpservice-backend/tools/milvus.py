from pymilvus import connections, list_collections, Collection
connections.connect("default", host="localhost", port="19530")
print(list_collections())
collection = Collection("Singtel_PDF")
collection.load()
print(collection.schema)


