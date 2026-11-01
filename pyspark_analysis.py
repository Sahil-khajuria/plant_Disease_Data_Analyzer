# Optional Big Data demonstration: pip install pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import count, avg, desc

spark=SparkSession.builder.appName("PlantDiseaseAnalytics").getOrCreate()
df=spark.read.option("header",True).option("inferSchema",True).csv("data/plant_disease_reports.csv")
print("Total records:",df.count())
print("Disease reports by crop and disease:")
df.filter(df.disease!="Healthy").groupBy("crop","disease").agg(
 count("*").alias("report_count"),
 avg("affected_area_pct").alias("avg_affected_area")
).orderBy(desc("report_count")).show(30,truncate=False)
print("Severity by region:")
df.groupBy("region","severity").count().orderBy(desc("count")).show(truncate=False)
spark.stop()
