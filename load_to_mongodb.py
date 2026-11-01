import os
import pandas as pd
from pymongo import MongoClient, ASCENDING, DESCENDING

uri=os.getenv("MONGODB_URI","mongodb://localhost:27017/")
path=os.path.join(os.path.dirname(__file__),"data","plant_disease_reports.csv")
df=pd.read_csv(path)
client=MongoClient(uri)
col=client["plant_disease_db"]["disease_reports"]
col.delete_many({})
docs=df.to_dict("records")
if docs:
    col.insert_many(docs, ordered=False)
col.create_index([("crop",ASCENDING)])
col.create_index([("disease",ASCENDING)])
col.create_index([("region",ASCENDING)])
col.create_index([("date",DESCENDING)])
col.create_index([("crop",ASCENDING),("disease",ASCENDING)])
print(f"Loaded {col.count_documents({})} reports into plant_disease_db.disease_reports")
print("Indexes created for crop, disease, region, date and crop+disease.")
client.close()
