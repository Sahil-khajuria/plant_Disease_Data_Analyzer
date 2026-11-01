from pymongo import MongoClient, DESCENDING
client=MongoClient("mongodb://localhost:27017/")
col=client["plant_disease_db"]["disease_reports"]

print("\n1. Most reported diseases")
pipeline=[
 {"$match":{"disease":{"$ne":"Healthy"}}},
 {"$group":{"_id":"$disease","reports":{"$sum":1}}},
 {"$sort":{"reports":-1}}
]
for x in col.aggregate(pipeline): print(x)

print("\n2. Crop-wise report count")
pipeline=[
 {"$group":{"_id":"$crop","reports":{"$sum":1}}},
 {"$sort":{"reports":-1}}
]
for x in col.aggregate(pipeline): print(x)

print("\n3. High severity reports by region")
pipeline=[
 {"$match":{"severity":"High"}},
 {"$group":{"_id":"$region","high_severity_reports":{"$sum":1}}},
 {"$sort":{"high_severity_reports":-1}}
]
for x in col.aggregate(pipeline): print(x)

client.close()
