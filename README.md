# 🌿 Plant Disease Data Analyzer & Diagnostic Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-47A248.svg?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Apache PySpark](https://img.shields.io/badge/Apache_Spark-PySpark_3.5%2B-E25A1C.svg?logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![Pillow](https://img.shields.io/badge/Pillow-Computer_Vision-11557c.svg)](https://python-pillow.org/)

An enterprise-grade, end-to-end agricultural data analytics platform and leaf disease diagnostic system. The platform combines **Computer Vision foliar diagnostics**, an interactive **Streamlit web dashboard**, a **MongoDB NoSQL document database**, and distributed **Apache PySpark big data analytics** to monitor, identify, and report crop diseases across regional farming clusters.

---

## 📌 Table of Contents
- [Executive Overview](#-executive-overview)
- [System Architecture](#-system-architecture)
- [Core Features](#-core-features)
- [Technology Stack](#-technology-stack)
- [Diagnostic Matrix & Supported Crops](#-diagnostic-matrix--supported-crops)
- [Prerequisites & System Requirements](#-prerequisites--system-requirements)
- [Step-by-Step Installation Guide](#-step-by-step-installation-guide)
- [Running the Application](#-running-the-application)
  - [1. Launching the Web Dashboard](#1-launching-the-web-dashboard)
  - [2. PySpark Big Data Processing](#2-pyspark-big-data-processing)
  - [3. MongoDB Import & Aggregations](#3-mongodb-import--aggregations)
- [Repository Structure](#-repository-structure)
- [Data Model & NoSQL Schema](#-data-model--nosql-schema)
- [Cloud Deployment (Streamlit Community Cloud)](#-cloud-deployment-streamlit-community-cloud)
- [Professional Agronomic Disclaimer](#-professional-agronomic-disclaimer)

---

## 🌾 Executive Overview

Crop diseases cause substantial losses in agricultural productivity worldwide. Efficient field management requires timely symptom identification, systematic regional incidence tracking, and scalable data analytics.

The **Plant Disease Data Analyzer** solves this through a multi-tiered architecture:
1. **At the Field Level:** Farmers and field officers upload photos or take live camera snapshots of diseased foliage to receive automated instant diagnoses, severity percentages, causal pathogens, and treatment recommendations.
2. **At the Regional Level:** Reports are aggregated into MongoDB or local datasets with multi-field indexing to track geographic disease vectors, severity hot-spots, and affected crops.
3. **At the Enterprise / Big Data Level:** PySpark distributed queries execute high-throughput group-by and aggregation analytics designed to scale from local sample records to massive multi-region agronomic datasets.

---

## 🏗️ System Architecture

```
                    ┌──────────────────────────────────────────┐
                    │            USER INTERFACE                │
                    │   (Streamlit Responsive Web Platform)    │
                    └─────────────────────┬────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     ┌────────────────────────┐                     ┌───────────────────────────┐
     │ 📸 Computer Vision     │                     │ 📊 Real-Time Analytics    │
     │ Diagnostic Engine      │                     │ & KPI Visualizations      │
     │ (PIL, HSV Colorimetry, │                     │ (Plotly Express, Dynamic  │
     │ Lesion Segmentation)   │                     │ Multi-filtering, Tables)  │
     └───────────┬────────────┘                     └─────────────┬─────────────┘
                 │                                                │
                 └───────────────────────┬────────────────────────┘
                                         ▼
                        ┌─────────────────────────────────┐
                        │      PERSISTENCE & STORAGE      │
                        ├────────────────┬────────────────┤
                        │   MongoDB      │  CSV Storage   │
                        │ (NoSQL Clust.) │  (Failover)    │
                        └────────┬───────┴────────┬───────┘
                                 │                │
                                 ▼                ▼
                        ┌─────────────────────────────────┐
                        │   BIG DATA ANALYTICS (PySpark)  │
                        │ Distributed In-Memory Processing│
                        └─────────────────────────────────┘
```

---

## ✨ Core Features

### 1. 🔍 Automated Leaf Disease Image Classifier
- **Multi-source input:** Supports image uploads (`.png`, `.jpg`, `.jpeg`, `.webp`), live camera snapshots (`st.camera_input`), and preloaded demonstration samples.
- **Foliar Colorimetry & Lesion Segmentation:** Measures green healthy tissue, chlorosis (yellow halos), necrotic lesions (brown spots), dark water-soaked blights, and orange rust pustules.
- **Quantitative Metrics:** Calculates **Confidence Score (%)**, **Severity Level (Low / Moderate / High)**, and **Affected Leaf Surface Area (%)**.
- **Actionable Treatment Plans:** Generates causal pathogen details (*fungal, bacterial, oomycete, or viral*), verified chemical/organic treatments, and cultural prevention practices.
- **One-Click Database Logging:** Persists findings directly into MongoDB or local datasets with a single click.

### 2. 📊 Interactive Analytics Dashboard
- **Executive KPIs:** Live metrics for total reports analysed, confirmed disease occurrences, top reported disease, and high-severity alarms.
- **Dynamic Visualizations:** Plotly interactive charts for:
  - Disease frequency bar chart
  - Crop distribution donut chart
  - Regional incidence comparison
  - Severity status distribution
- **Granular Multi-filtering:** Slice and dice reports by Crop, Region, and Severity simultaneously.
- **Summary Tables & Export:** Crop-wise aggregated tables and one-click CSV report export.

### 3. 🍃 Enterprise NoSQL Integration (MongoDB)
- Flexible JSON document model tailored for semi-structured agricultural survey data.
- Compound indexing on `(crop, disease)`, `region`, and `date` for sub-millisecond query performance.
- Resilient hybrid data layer: automatically detects MongoDB when running and seamlessly falls back to local CSV storage if offline.

### 4. ⚡ PySpark Distributed Analytics
- In-memory big data processing pipeline for multi-dimensional data grouping.
- Demonstrates industrial big data scalability for national agricultural survey datasets.

---

## 🛠️ Technology Stack

| Layer | Component | Technologies / Libraries | Purpose |
| :--- | :--- | :--- | :--- |
| **Frontend & UI** | Dashboard Framework | **Streamlit (v1.40+)** | Responsive, modern web interface with reactive state |
| **Data Viz** | Interactive Charts | **Plotly Express** | Interactive charts, distribution graphs, and KPIs |
| **Computer Vision** | Image Processing | **Pillow (PIL) & NumPy** | Leaf segmentation, HSV color filtering, lesion analytics |
| **Database** | NoSQL Document Store| **MongoDB Community (v6.0+)** | Storage for report documents and compound indexes |
| **DB Connector** | Python Driver | **PyMongo (v4.6+)** | Native MongoDB CRUD operations and aggregation pipeline |
| **Big Data** | Distributed Analytics | **Apache Spark (PySpark 3.5+)** | High-throughput distributed aggregation and group-by |
| **Data Handling** | Tabular Data Engine | **Pandas (v2.0+)** | In-memory dataframes, filtering, and CSV export |
| **Runtime** | Execution Environment | **Python 3.10 – 3.14+** | Cross-platform runtime on Linux, macOS, and Windows |

---

## 🌿 Diagnostic Matrix & Supported Crops

The diagnostic engine is pre-trained and mapped across 6 major economic crops:

| Crop | Target Disease | Causal Pathogen Type | Visual Identifiers |
| :--- | :--- | :--- | :--- |
| **Tomato** | Early Blight | *Alternaria solani* (Fungus) | Concentric target-board rings with yellow chlorotic halos |
| **Tomato** | Late Blight | *Phytophthora infestans* (Oomycete) | Rapidly spreading dark water-soaked lesions, leaf collapse |
| **Tomato** | Bacterial Spot | *Xanthomonas perforans* (Bacteria) | Small water-soaked lesions turning paper-thin |
| **Tomato** | Septoria Leaf Spot | *Septoria lycopersici* (Fungus) | Circular spots with grey centers and dark margins |
| **Potato** | Early Blight | *Alternaria solani* (Fungus) | Dark brown angular lesions on mature lower foliage |
| **Potato** | Late Blight | *Phytophthora infestans* (Oomycete) | Irregular dark purplish-brown decay, white margin mould |
| **Grape** | Black Rot | *Guignardia bidwellii* (Fungus) | Tan circular lesions with tiny black pycnidia specks |
| **Grape** | Esca (Measles) | Complex Fungal Pathogens | Interveinal chlorosis creating distinctive 'tiger stripes' |
| **Grape** | Leaf Blight | *Pseudocercospora vitis* (Fungus) | Reddish-brown irregular lesions, premature leaf drop |
| **Apple** | Apple Scab | *Venturia inaequalis* (Fungus) | Olive-green velvety patches turning dark and puckered |
| **Apple** | Black Rot | *Botryosphaeria obtusa* (Fungus) | Purple specks expanding into brown frog-eye spots |
| **Apple** | Cedar Apple Rust | *Gymnosporangium juniperi* (Fungus) | Bright yellow-orange pustules with exudates |
| **Chilli** | Anthracnose | *Colletotrichum capsici* (Fungus) | Sunken circular necrotic lesions with dark acervuli |
| **Chilli** | Leaf Curl | Chilli Leaf Curl Virus (Begomovirus) | Upward curling, puckering, stunted internodes |
| **Maize** | Northern Leaf Blight| *Exserohilum turcicum* (Fungus) | Long, elliptical cigar-shaped grayish-green lesions |
| **Maize** | Common Rust | *Puccinia sorghi* (Fungus) | Cinnamon-brown powdery pustules on foliage |
| **Maize** | Gray Leaf Spot | *Cercospora zeae-maydis* (Fungus) | Rectangular tan-gray lesions bounded by leaf veins |
| *All Crops*| **Healthy** | None | Uniform green blades, healthy turgor, clear vascular veins |

---

## 💻 Prerequisites & System Requirements

- **Operating System:** Linux (Fedora, Ubuntu, Debian, RHEL), macOS, or Windows 10/11.
- **Python:** Version `3.10` or higher (fully tested on Python `3.14`).
- **Java (Required only for PySpark):** Java OpenJDK `11`, `17`, or `21` (e.g. `java -version`).
- **MongoDB (Optional for NoSQL mode):** MongoDB Community Server `6.0+` running locally or MongoDB Atlas URI.

---

## 🚀 Step-by-Step Installation Guide

### 1. Clone the Repository
```bash
git clone git@github.com:Sahil-khajuria/plant_Disease_Data_Analyzer.git
cd plant_Disease_Data_Analyzer
```
*(Or clone via HTTPS: `https://github.com/Sahil-khajuria/plant_Disease_Data_Analyzer.git`)*

### 2. Create and Activate a Virtual Environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### 1. Launching the Web Dashboard
Start the Streamlit application:
```bash
streamlit run app.py
```
Open your browser and navigate to:
👉 **`http://localhost:8501`**

#### Using the Tabs:
1. **📸 Image Disease Detector:**
   - Choose **"Sample Test Image"** for instant demonstration (e.g., Tomato Early Blight, Potato Late Blight, Grape Black Rot).
   - Or choose **"File Upload"** / **"Camera Snapshot"** to test your own images.
   - Inspect diagnostic metrics, pathogen descriptions, and treatment recommendations.
   - Click **"💾 Log This Diagnosis to Disease Reports Database"** to persist the entry.
2. **📊 Analytics Dashboard:**
   - Filter by crop, region, and severity.
   - Explore interactive distribution charts and summary tables.
3. **📝 Add & Export Reports:**
   - Submit field observations manually.
   - Download the filtered dataset as a CSV file.

---

### 2. PySpark Big Data Processing
To run distributed in-memory group-by queries on the dataset:
```bash
python pyspark_analysis.py
```
**Sample Output:**
```
Total records: 1,200
Disease reports by crop and disease:
+------+--------------------+------------+------------------+
|crop  |disease             |report_count|avg_affected_area |
+------+--------------------+------------+------------------+
|Potato|Early Blight        |69          |43.07%            |
|Potato|Late Blight         |68          |43.87%            |
|Chilli|Anthracnose         |66          |42.66%            |
|Grape |Esca                |64          |45.58%            |
...
Severity by region:
+---------------+--------+-----+
|region         |severity|count|
+---------------+--------+-----+
|Tumakuru       |Low     |87   |
|Belagavi       |Low     |83   |
|Mandya         |High    |30   |
...
```

---

### 3. MongoDB Import & Aggregations
If MongoDB is installed and running (`systemctl status mongod` or `mongod`):

1. **Load data and build indexes:**
   ```bash
   python load_to_mongodb.py
   ```
2. **Execute aggregation pipelines:**
   ```bash
   python mongodb_queries.py
   ```
3. **Configure Custom MongoDB URI (e.g. MongoDB Atlas):**
   ```bash
   export MONGODB_URI="mongodb+srv://<username>:<password>@cluster.mongodb.net/"
   streamlit run app.py
   ```

---

## 📂 Repository Structure

```
plant_disease_data_analyzer/
│
├── app.py                      # Main Streamlit web application & interactive UI
├── disease_classifier.py       # Computer Vision foliar analysis & diagnostic engine
├── pyspark_analysis.py         # PySpark distributed Big Data processing script
├── load_to_mongodb.py          # MongoDB data ingestion & index creation script
├── mongodb_queries.py          # MongoDB aggregation queries ($match, $group, $sort)
├── requirements.txt            # Project dependencies and libraries
├── PROJECT_REPORT.md           # Academic project report & architectural assessment
├── README.md                   # Comprehensive project documentation
├── .gitignore                  # Git ignore rules (venv, caches, temp files)
│
├── .streamlit/
│   └── config.toml             # Streamlit UI configuration and styling
│
├── data/
│   └── plant_disease_reports.csv # Bundled dataset containing 1,200 agricultural reports
│
└── sample_images/              # Demonstration leaf images for one-click testing
    ├── tomato_early_blight.png
    ├── tomato_healthy.png
    ├── grape_black_rot.png
    ├── potato_late_blight.png
    └── maize_common_rust.png
```

---

## 📊 Data Model & NoSQL Schema

Each record is formatted as a JSON-like document in the MongoDB collection `disease_reports` within the `plant_disease_db` database:

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

### Indexed Keys
- `crop` (Ascending)
- `disease` (Ascending)
- `region` (Ascending)
- `date` (Descending)
- Compound: `(crop, disease)`

---

## ☁️ Cloud Deployment (Streamlit Community Cloud)

This application is ready for zero-configuration deployment on **Streamlit Community Cloud**:

1. Fork or push this repository to your GitHub account:
   `https://github.com/Sahil-khajuria/plant_Disease_Data_Analyzer`
2. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with GitHub.
3. Click **"New app"** and specify:
   - **Repository:** `Sahil-khajuria/plant_Disease_Data_Analyzer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy!**

---

## ⚖️ Professional Agronomic Disclaimer

> **Notice:** The bundled 1,200 survey records are synthetic demonstration data created for academic, benchmarking, and demonstration purposes. The computer vision diagnostic module is an educational and analytical tool designed to demonstrate automated foliar symptom segmentation and pattern matching. For verified commercial field applications, treatments must be confirmed by qualified agricultural extension officers or certified agronomists.

---

## 👤 Author
- **Sahil Khajuria** – [GitHub Profile](https://github.com/Sahil-khajuria)
