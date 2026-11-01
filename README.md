# Plant Disease Data Analyzer

A compact NoSQL and Big Data academic project for exploring plant disease reports.

## Included features
- 1,200 synthetic demonstration reports covering 6 crops and 8 regions
- Streamlit dashboard with filters, KPIs, charts and summary table
- Add a report through the dashboard
- MongoDB import script, indexes and aggregation queries
- Optional PySpark group-by analytics
- CSV export

> Data notice: The bundled records are synthetic and illustrative. They are not real farmer reports, confirmed disease observations, or verified severity assessments. The app does not diagnose plants from images or prescribe treatment.

## Run the dashboard (fastest path; no MongoDB needed)
```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
By default, the dashboard reads the included CSV. New reports are saved to the CSV if MongoDB is unavailable.

## Enable MongoDB
Install and start MongoDB Community Server, then:
```bash
python load_to_mongodb.py
python mongodb_queries.py
```
To make the dashboard read/write MongoDB:
```bash
export MONGODB_URI="mongodb://localhost:27017/"
```
The app automatically uses MongoDB when it is reachable and contains records; otherwise it falls back to CSV.

Database: `plant_disease_db`
Collection: `disease_reports`

## Optional PySpark demo
```bash
pip install pyspark
python pyspark_analysis.py
```
PySpark setup can take time; it is optional and not required for the dashboard.

## Example MongoDB document
```json
{
  "report_id": "R00001",
  "date": "2025-04-12",
  "crop": "Tomato",
  "disease": "Early Blight",
  "region": "Mysuru",
  "severity": "Moderate",
  "affected_area_pct": 22.5,
  "report_source": "Farmer report",
  "notes": "Synthetic sample record for academic demonstration"
}
```

## NoSQL and Big Data concepts to explain
- Database and collection: `plant_disease_db.disease_reports`
- Flexible document model: each report is stored as a JSON-like document
- Indexing: indexes on crop, disease, region and date support common filters
- Aggregation: `$match`, `$group`, `$sum`, `$avg`, `$sort`
- Big Data extension: PySpark performs distributed group-by analysis for larger datasets. The bundled 1,200 rows are a demo dataset, not a large-scale benchmark.

## Suggested 3-minute demonstration
1. Open dashboard and explain KPIs.
2. Filter by crop and region.
3. Compare common disease and severity charts.
4. Add a sample report using the form.
5. Show MongoDB collection and run `mongodb_queries.py`.
6. Explain how PySpark could scale this analysis.
