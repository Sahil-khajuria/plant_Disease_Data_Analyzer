# Plant Disease Data Analyzer & Diagnostic System
## Activity-Based Project Assessment & Technical Report

### Abstract
The **Plant Disease Data Analyzer & Diagnostic System** is an end-to-end agricultural reporting, computer vision diagnostic, and big data analytics platform developed using Python, MongoDB, Apache PySpark, and Streamlit. The application allows users to upload crop leaf imagery or capture real-time camera snapshots to automatically identify plant diseases, calculate affected surface areas, and retrieve targeted agronomic treatment plans. Observations are persisted as flexible NoSQL documents in MongoDB and summarized using dynamic interactive visual dashboards. An Apache PySpark big data extension demonstrates how multi-regional agronomic data can be processed using distributed in-memory compute clusters.

---

### 1. Introduction
Early detection and systematic tracking of plant pathogens are critical to ensuring agricultural productivity and food security. Agricultural disease surveillance generates heterogeneous information regarding host crops, pathogens, regional incidence, severity levels, and field treatments. Organizing and analyzing these records requires:
1. **Intelligent Edge Diagnostics:** Rapid image-based preliminary classification of foliar diseases.
2. **Flexible Storage:** A scalable document database capable of ingesting diverse field reports without rigid relational schema constraints.
3. **Interactive Reporting:** Business intelligence dashboards for agricultural extension officers and regional administrators.
4. **Big Data Processing:** Scalable frameworks like Apache Spark capable of handling large-scale regional disease vector tracking.

---

### 2. Problem Statement
Agricultural disease records are often fragmented across disparate formats, making them difficult to aggregate, visualize, and analyze in real-time. Furthermore, field workers often lack immediate access to expert plant pathologists to confirm foliar symptoms on-site. This project addresses these challenges by integrating an automated computer vision diagnostic engine with a NoSQL database and an interactive analytics dashboard.

---

### 3. Objectives
1. Implement a computer vision diagnostic engine to classify plant leaf diseases and estimate foliar lesion severity.
2. Provide automated agronomic recommendations, causal pathogen details, and cultural prevention practices.
3. Store and index disease report documents in a MongoDB database with automated failover to local storage.
4. Deliver an interactive Streamlit web dashboard with multi-criteria filtering, KPI cards, and Plotly visualizations.
5. Provide distributed group-by analytics and aggregation using Apache PySpark.

---

### 4. System Architecture
The platform is organized into a four-tier architecture:

1. **Presentation & Diagnostic Layer (Streamlit & Computer Vision):**
   - Responsive web interface featuring three functional modules: Leaf Image Disease Detector, Analytics Dashboard, and Report Management.
   - PIL and NumPy colorimetric pipeline for leaf segmentation, HSV color space masking, chlorosis/necrosis ratio measurement, and severity grading.
2. **Data & Persistence Layer (MongoDB & CSV Failover):**
   - MongoDB database `plant_disease_db`, collection `disease_reports`.
   - Compound and single-field B-tree indexes for accelerated filtering.
   - Seamless offline fallback to CSV storage when database clusters are unreachable.
3. **Processing & Big Data Layer (Pandas & PySpark):**
   - In-memory dataframe transformation and filtering via Pandas.
   - Distributed SparkSession executing parallelized groupBy transformations.
4. **Demonstration & Testing Suite:**
   - Bundled 1,200 survey reports covering 6 crops and 8 administrative regions.
   - Demonstration sample images for one-click diagnostic evaluation.

---

### 5. Document Structure & NoSQL Data Model
Each disease report document in MongoDB encapsulates comprehensive field metadata:

```json
{
  "report_id": "IMG261102014522",
  "date": "2026-11-02",
  "crop": "Tomato",
  "disease": "Early Blight",
  "region": "Mysuru",
  "severity": "Moderate",
  "affected_area_pct": 20.1,
  "report_source": "Leaf Image Detection",
  "notes": "Automated CV diagnosis (84.3% conf). Pathogen: Alternaria solani"
}
```

#### MongoDB Indexing Strategy
- Single indexes: `crop` (ASC), `disease` (ASC), `region` (ASC), `date` (DESC).
- Compound index: `(crop: 1, disease: 1)` to accelerate multi-attribute disease queries.

---

### 6. Key Features
- **Computer Vision Foliar Classifier:** Upload leaf images or capture photos via webcam to diagnose diseases across Tomato, Potato, Grape, Apple, Chilli, and Maize crops.
- **Severity & Affected Area Assessment:** Quantifies necrotic spots, chlorosis halos, and orange rust pustules into Low, Moderate, or High severity levels.
- **One-Click Diagnostic Logging:** Automatically saves image diagnosis records into the MongoDB survey collection.
- **Real-Time KPIs:** Live metric cards showing total reports analysed, confirmed diseases, top pathogen, and high-severity alarms.
- **Interactive Plotly Visualizations:** Disease frequency, crop distribution pie charts, regional incidence comparisons, and severity distributions.
- **CSV Export & Manual Ingestion:** Manual field survey entry form and filtered dataset export.

---

### 7. NoSQL Aggregation Pipelines
MongoDB aggregation queries are executed via PyMongo using native pipeline stages:
- `$match`: Filters out healthy controls or isolates specific severity bands.
- `$group`: Groups records by crop, pathogen, or administrative region.
- `$sum` & `$avg`: Calculates total incidences and mean leaf surface damage.
- `$sort`: Ranks diseases and regions in descending order of incidence.

---

### 8. Big Data Extension (Apache PySpark)
The PySpark module (`pyspark_analysis.py`) initializes a local or cluster `SparkSession` to process large-scale agricultural records:
- Evaluates Spark DataFrame schemas dynamically.
- Performs parallel aggregations across partitions for high-throughput reporting.

---

### 9. Limitations
- Bundled survey records are synthetic records created for benchmarking.
- The computer vision engine uses colorimetric segmentation and morphological heuristics; extreme lighting variations or novel unseen diseases may require deep neural network re-training.
- Suggested treatments are guidelines and should be corroborated by certified agricultural extension specialists.

---

### 10. Future Enhancements
- Integration of deep convolutional neural network backbones (MobileNetV3 / EfficientNet) fine-tuned on the full PlantVillage dataset.
- Geolocation GPS tagging with interactive satellite mapping.
- IoT soil moisture and atmospheric microclimate sensor integration.

---

### 11. Conclusion
The Plant Disease Data Analyzer & Diagnostic System successfully demonstrates how computer vision, NoSQL document databases, and distributed big data frameworks combine to solve real-world agricultural problems. The system provides an end-to-end workflow from field-level leaf diagnosis to regional analytics and enterprise data processing.

---

### References
1. Mohanty, S. P., Hughes, D. P., and Salathé, M. (2016). *Using Deep Learning for Image-Based Plant Disease Detection.* Frontiers in Plant Science, 7.
2. Hughes, D. and Salathé, M. (2015). *An open access repository of images on plant health to enable the development of mobile disease diagnostics.* arXiv:1511.08060.
3. MongoDB Corporation. (2024). *MongoDB Manual and Aggregation Framework.*
4. Apache Software Foundation. (2024). *Apache Spark: Unified Engine for Large-Scale Data Processing.*
