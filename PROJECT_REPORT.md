# Plant Disease Data Analyzer
## Activity-Based Assessment Report

### Abstract
The Plant Disease Data Analyzer is a small agricultural reporting and analytics application developed using Python, MongoDB and Streamlit. It stores plant disease reports as flexible NoSQL documents and summarizes disease frequency by crop, region and severity. The dashboard provides filters, charts, a crop-wise summary table and a form for entering new reports. An optional PySpark program demonstrates how the same analysis can be extended to distributed processing.

**Data note:** The bundled 1,200 records are synthetic demonstration records. They are not real field observations or confirmed diagnoses.

### 1. Introduction
Plant disease reporting can generate information about affected crops, locations, dates and severity. Organizing these records makes it easier to review patterns and prioritize field inspections. A document database is suitable for this demonstration because each report can contain flexible descriptive fields.

### 2. Problem Statement
Agricultural disease reports may be stored in different formats and can be difficult to summarize manually. The project provides a simple system to store, filter and analyse reports by crop, disease, region and severity.

### 3. Objectives
1. Store plant disease reports in MongoDB.
2. Search and filter reports by crop, disease, region and severity.
3. Identify frequently reported diseases and affected crops.
4. Visualize regional and severity patterns.
5. Demonstrate aggregation queries and optional PySpark processing.

### 4. Proposed System
The system has four layers:
- Data layer: CSV sample reports and user-entered records.
- NoSQL layer: MongoDB database `plant_disease_db`, collection `disease_reports`.
- Processing layer: Python and Pandas; optional PySpark.
- Presentation layer: Streamlit dashboard with Plotly charts.

### 5. Document Structure
Each document includes `report_id`, `date`, `crop`, `disease`, `region`, `severity`, `affected_area_pct`, `report_source` and `notes`. MongoDB indexes are created on crop, disease, region, date and crop+disease.

### 6. Key Features
- Dashboard KPIs: reports analysed, disease reports, most reported disease and high severity reports.
- Disease frequency bar chart.
- Crop-wise disease distribution.
- Region-wise report comparison.
- Severity distribution chart.
- Crop-wise summary table.
- Add report form and CSV export.

### 7. NoSQL Aggregation
MongoDB aggregation uses `$match` to filter records, `$group` to group by disease/crop/region, `$sum` to count reports, `$avg` to calculate average affected area and `$sort` to rank results.

### 8. Big Data Extension
The optional PySpark script reads the CSV and groups reports by crop, disease, region and severity. Spark is designed for distributed processing on larger datasets. The included 1,200 records are for demonstration and do not constitute a production-scale Big Data workload.

### 9. Limitations
- Sample records are synthetic and cannot establish real disease prevalence.
- The application does not perform image-based disease diagnosis.
- Severity and affected-area values are illustrative.
- Recommendations or pesticide treatment advice are outside the scope.

### 10. Future Enhancements
- Connect field reporting from a mobile application.
- Add verified agricultural extension officer review.
- Integrate a validated image-classification model.
- Add GPS mapping and seasonal trend analysis.
- Connect weather and soil datasets for contextual analysis.

### 11. Conclusion
The project demonstrates how MongoDB and Python can organize and analyse agricultural disease reports. The dashboard makes crop, disease, regional and severity patterns easier to explore, while the PySpark extension introduces distributed data processing concepts.

### References
1. Mohanty, S. P., Hughes, D. P., and Salathé, M. (2016). Using Deep Learning for Image-Based Plant Disease Detection. *Frontiers in Plant Science*, 7. https://doi.org/10.3389/fpls.2016.01419
2. PlantVillage Dataset repository: https://github.com/spMohanty/PlantVillage-Dataset
3. MongoDB Manual: https://www.mongodb.com/docs/manual/
4. Streamlit documentation: https://docs.streamlit.io/
