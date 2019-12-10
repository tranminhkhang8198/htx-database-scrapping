import pymongo
import json

mng_client = pymongo.MongoClient("localhost", 27017)
mng_db = mng_client["htx"]  # Replace mongo db name
collection_name = "phanBon"  # Replace mongo db collection name
db_cm = mng_db[collection_name]

# Get the data from JSON file
with open("./data_thuoc_bvtv.json", "r") as data_file:
    data_json = json.load(data_file)

# Insert Data
db_cm.remove()
db_cm.insert(data_json)

# Query data
db_cm.UNS_Collection2.find()
