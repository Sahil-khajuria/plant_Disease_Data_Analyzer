import os
from datetime import date
from PIL import Image
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from disease_classifier import analyze_leaf_image, DISEASE_KNOWLEDGE_BASE

st.set_page_config(page_title="Plant Disease Data Analyzer", page_icon="🌿", layout="wide")
st.title("🌿 Plant Disease Data Analyzer & Diagnostic Engine")
st.caption("AI Leaf Disease Detection • Agricultural Reporting • MongoDB • Big Data Analytics")

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "plant_disease_reports.csv")
FIELDS = ["report_id", "date", "crop", "disease", "region", "severity", "affected_area_pct", "report_source", "notes"]
CROP_OPTIONS = ["Tomato", "Potato", "Grape", "Maize", "Apple", "Chilli"]

def mongo_collection():
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri, serverSelectionTimeoutMS=1200)
    client.admin.command("ping")
    return client, client["plant_disease_db"]["disease_reports"]

def read_records():
    try:
        client, col = mongo_collection()
        docs = list(col.find({}, {"_id": 0}))
        client.close()
        if docs:
            df = pd.DataFrame(docs)
            df["date"] = pd.to_datetime(df["date"])
            return df, "MongoDB"
    except Exception:
        pass
    df = pd.read_csv(CSV_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df, "CSV demo dataset"

def save_report_record(record):
    """Saves a new record to MongoDB if available, otherwise appends to CSV."""
    try:
        client, col = mongo_collection()
        col.insert_one(record)
        client.close()
        return "MongoDB"
    except Exception:
        existing = pd.read_csv(CSV_PATH)
        pd.concat([existing, pd.DataFrame([record])], ignore_index=True).to_csv(CSV_PATH, index=False)
        return "CSV demo dataset"

df, source = read_records()

# Navigation Tabs
tab_diag, tab_dash, tab_entry = st.tabs([
    "📸 Image Disease Detector", 
    "📊 Analytics Dashboard", 
    "📝 Add & Export Reports"
])

# ==========================================
# TAB 1: IMAGE DISEASE DIAGNOSIS FEATURE
# ==========================================
with tab_diag:
    st.subheader("🔍 Automated Crop Disease Detection from Leaf Image")
    st.markdown(
        "Upload a photo of an affected plant leaf or take a snapshot with your camera. "
        "The computer vision diagnostic engine analyzes foliar lesions, chlorosis, and discoloration "
        "to identify the plant disease, calculate affected leaf area, and prescribe treatments."
    )

    col_up, col_info = st.columns([1, 1], gap="medium")

    with col_up:
        input_method = st.radio("Choose image source:", ["Sample Test Image", "File Upload", "Camera Snapshot"], horizontal=True)
        uploaded_file = None
        leaf_img = None

        if input_method == "Sample Test Image":
            sample_choices = {
                "Tomato - Early Blight (Blight lesions & halo)": ("sample_images/tomato_early_blight.png", "Tomato"),
                "Tomato - Healthy Leaf (Uniform green)": ("sample_images/tomato_healthy.png", "Tomato"),
                "Potato - Late Blight (Water-soaked decay)": ("sample_images/potato_late_blight.png", "Potato"),
                "Grape - Black Rot (Necrotic circular spots)": ("sample_images/grape_black_rot.png", "Grape"),
                "Maize - Common Rust (Cinnamon pustules)": ("sample_images/maize_common_rust.png", "Maize"),
            }
            sample_name = st.selectbox("Select a demonstration sample leaf:", list(sample_choices.keys()))
            sample_path, sample_crop = sample_choices[sample_name]
            full_sample_path = os.path.join(os.path.dirname(__file__), sample_path)
            if os.path.exists(full_sample_path):
                leaf_img = Image.open(full_sample_path)
            default_crop_index = CROP_OPTIONS.index(sample_crop) if sample_crop in CROP_OPTIONS else 0
        elif input_method == "File Upload":
            uploaded_file = st.file_uploader(
                "Upload a clear photo of the crop leaf", 
                type=["jpg", "jpeg", "png", "webp"],
                help="Supported crops: Tomato, Potato, Grape, Apple, Chilli, Maize"
            )
            if uploaded_file is not None:
                leaf_img = Image.open(uploaded_file)
            default_crop_index = 0
        else:
            uploaded_file = st.camera_input("Take a photo of the plant leaf")
            if uploaded_file is not None:
                leaf_img = Image.open(uploaded_file)
            default_crop_index = 0

        sel_crop = st.selectbox(
            "Select Crop Type", 
            CROP_OPTIONS, 
            index=default_crop_index, 
            help="Specify the crop being analyzed for targeted disease diagnosis"
        )
        diag_region = st.selectbox(
            "Observation Region (for logging)", 
            sorted(df["region"].dropna().unique()), 
            index=0
        )

    with col_info:
        if leaf_img is not None:
            st.image(leaf_img, caption="Leaf Image Under Analysis", use_container_width=True)
            
            with st.spinner("Analyzing foliar morphology and lesion patterns..."):
                result = analyze_leaf_image(leaf_img, selected_crop=sel_crop)

            # Display Diagnosis Card
            st.divider()
            diag_disease = result["disease"]
            confidence = result["confidence"]
            severity = result["severity"]
            area_pct = result["affected_area_pct"]

            if diag_disease == "Healthy":
                st.success(f"### Result: 🌿 {sel_crop} is Healthy ({confidence}% Confidence)")
            else:
                st.error(f"### Diagnosis: ⚠️ {diag_disease} ({confidence}% Confidence)")

            m1, m2, m3 = st.columns(3)
            m1.metric("Predicted Disease", diag_disease)
            m2.metric("Severity Level", severity)
            m3.metric("Affected Leaf Area", f"{area_pct}%")

            st.caption(f"**Causal Pathogen:** *{result['pathogen']}*")

            # Symptoms & Treatments
            st.markdown("#### 🩺 Symptoms Identified")
            for symptom in result["symptoms"]:
                st.markdown(f"- {symptom}")

            st.markdown("#### 💊 Recommended Treatment Plan")
            for treat in result["treatments"]:
                st.markdown(f"- {treat}")

            with st.expander("🛡️ Preventive Cultural Practices"):
                for prev in result["prevention"]:
                    st.markdown(f"- {prev}")

            with st.expander("🔬 View Computer Vision Colorimetry Metrics"):
                c_m = result["metrics"]
                st.write({
                    "Healthy Green Foliage (%)": c_m["green_tissue_pct"],
                    "Yellowing / Chlorosis (%)": c_m["chlorosis_yellow_pct"],
                    "Necrotic / Brown Spots (%)": c_m["necrotic_brown_pct"],
                    "Dark Lesions (%)": c_m["dark_lesion_pct"],
                    "Rust Pustules (%)": c_m["rust_pustule_pct"]
                })

            st.markdown("---")
            # Action: Save to Database
            if st.button("💾 Log This Diagnosis to Disease Reports Database", type="primary", use_container_width=True):
                new_rec = {
                    "report_id": "IMG" + pd.Timestamp.now().strftime("%y%m%d%H%M%S"),
                    "date": date.today().isoformat(),
                    "crop": sel_crop,
                    "disease": diag_disease,
                    "region": diag_region,
                    "severity": severity,
                    "affected_area_pct": float(area_pct),
                    "report_source": "Leaf Image Detection",
                    "notes": f"Automated CV diagnosis ({confidence}% conf). Pathogen: {result['pathogen']}"
                }
                dest = save_report_record(new_rec)
                st.success(f"✅ Report saved to {dest}! Open the 'Analytics Dashboard' tab to view updated metrics.")
                st.rerun()
        else:
            st.info("👆 Upload an image or use your camera to diagnose plant leaf diseases in real-time.")
            st.markdown("#### Supported Crop Diagnoses:")
            for crop_name, diseases in DISEASE_KNOWLEDGE_BASE.items():
                disease_list = [d for d in diseases.keys() if d != "Healthy"]
                st.markdown(f"- **{crop_name}:** {', '.join(disease_list)} + Healthy")


# ==========================================
# TAB 2: ANALYTICS DASHBOARD
# ==========================================
with tab_dash:
    st.sidebar.success(f"Data source: {source}")
    st.sidebar.markdown("### Filter reports")
    crops = sorted(df["crop"].dropna().unique())
    regions = sorted(df["region"].dropna().unique())
    selected_crops = st.sidebar.multiselect("Crop", crops, default=crops)
    selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
    selected_severity = st.sidebar.multiselect("Severity", ["Low", "Moderate", "High"], default=["Low", "Moderate", "High"])

    filtered = df[df["crop"].isin(selected_crops) & df["region"].isin(selected_regions) & df["severity"].isin(selected_severity)].copy()
    if filtered.empty:
        st.warning("No reports match the selected filters.")
    else:
        total = len(filtered)
        disease_only = filtered[filtered["disease"].str.lower() != "healthy"]
        common = disease_only["disease"].value_counts().index[0] if not disease_only.empty else "No disease reports"
        high = int((filtered["severity"] == "High").sum())
        avg_area = float(disease_only["affected_area_pct"].mean()) if not disease_only.empty else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Reports analysed", f"{total:,}")
        k2.metric("Disease reports", f"{len(disease_only):,}")
        k3.metric("Most reported disease", common)
        k4.metric("High severity reports", f"{high:,}")

        st.divider()
        left, right = st.columns(2)
        with left:
            counts = disease_only["disease"].value_counts().rename_axis("Disease").reset_index(name="Reports")
            fig = px.bar(counts, x="Disease", y="Reports", title="Most frequently reported diseases", color="Reports", color_continuous_scale="Viridis")
            fig.update_layout(xaxis_tickangle=-25)
            st.plotly_chart(fig, use_container_width=True)
        with right:
            crop_counts = disease_only["crop"].value_counts().rename_axis("Crop").reset_index(name="Reports")
            fig = px.pie(crop_counts, names="Crop", values="Reports", title="Disease reports by crop", hole=.35)
            st.plotly_chart(fig, use_container_width=True)

        left, right = st.columns(2)
        with left:
            region_counts = disease_only["region"].value_counts().rename_axis("Region").reset_index(name="Reports")
            fig = px.bar(region_counts, x="Region", y="Reports", title="Reports by region", color="Reports", color_continuous_scale="Teal")
            st.plotly_chart(fig, use_container_width=True)
        with right:
            sev = filtered["severity"].value_counts().reindex(["Low", "Moderate", "High"], fill_value=0).rename_axis("Severity").reset_index(name="Reports")
            fig = px.bar(sev, x="Severity", y="Reports", color="Severity", title="Severity distribution")
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📊 Crop-wise disease summary")
        summary = disease_only.groupby("crop").agg(
            disease_reports=("report_id", "count"),
            average_affected_area=("affected_area_pct", "mean"),
            high_severity=("severity", lambda s: int((s == "High").sum()))
        ).reset_index()
        if not summary.empty:
            summary["average_affected_area"] = summary["average_affected_area"].round(1)
        st.dataframe(summary, use_container_width=True, hide_index=True)


# ==========================================
# TAB 3: ADD & EXPORT REPORTS
# ==========================================
with tab_entry:
    st.subheader("📝 Add a disease report manually")
    with st.form("new_report", clear_on_submit=True):
        a, b, c = st.columns(3)
        with a:
            new_crop = st.selectbox("Crop", CROP_OPTIONS, key="manual_crop")
            new_disease = st.text_input("Disease name", placeholder="e.g. Early Blight")
            new_region = st.selectbox("Region", regions, key="manual_region")
        with b:
            new_severity = st.selectbox("Severity", ["Low", "Moderate", "High"], key="manual_sev")
            new_area = st.number_input("Estimated affected area (%)", min_value=0.0, max_value=100.0, value=10.0)
            new_date = st.date_input("Report date", value=date.today())
        with c:
            new_source = st.selectbox("Report source", ["Farmer report", "Field survey", "Demo entry", "Image diagnosis"])
            new_notes = st.text_area("Notes", "Initial field observation")
        submitted = st.form_submit_button("Save report")
        if submitted:
            record = {
                "report_id": "R" + pd.Timestamp.now().strftime("%y%m%d%H%M%S"),
                "date": new_date.isoformat(),
                "crop": new_crop,
                "disease": new_disease.strip() or "Unspecified",
                "region": new_region,
                "severity": new_severity,
                "affected_area_pct": float(new_area),
                "report_source": new_source,
                "notes": new_notes
            }
            target_store = save_report_record(record)
            st.success(f"Report saved to {target_store}. Refresh the page or view the Analytics tab.")
            st.rerun()

    with st.expander("View report records"):
        view = filtered.copy() if not filtered.empty else df.copy()
        view["date"] = pd.to_datetime(view["date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(view, use_container_width=True, hide_index=True)

    csv_data = (filtered if not filtered.empty else df).copy()
    csv_data["date"] = pd.to_datetime(csv_data["date"]).dt.strftime("%Y-%m-%d")
    st.download_button(
        "⬇️ Download filtered reports", 
        csv_data.to_csv(index=False).encode("utf-8"),
        "plant_disease_filtered_reports.csv", 
        "text/csv"
    )

st.info("Academic demo: included records and CV analysis are for illustrative purposes. Consult agricultural extension officers for verified field treatments.")
