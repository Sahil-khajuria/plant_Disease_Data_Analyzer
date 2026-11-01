import os
from datetime import date
import pandas as pd
import streamlit as st
import plotly.express as px
from pymongo import MongoClient
from pymongo.errors import PyMongoError

st.set_page_config(page_title="Plant Disease Data Analyzer", page_icon="🌿", layout="wide")
st.title("🌿 Plant Disease Data Analyzer")
st.caption("Agricultural disease reporting • MongoDB • Data analytics")

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "plant_disease_reports.csv")
FIELDS = ["report_id","date","crop","disease","region","severity","affected_area_pct","report_source","notes"]
CROP_OPTIONS = ["Tomato", "Potato", "Grape", "Maize", "Apple", "Chilli"]

def mongo_collection():
    uri=os.getenv("MONGODB_URI","mongodb://localhost:27017/")
    client=MongoClient(uri, serverSelectionTimeoutMS=1200)
    client.admin.command("ping")
    return client, client["plant_disease_db"]["disease_reports"]

def read_records():
    try:
        client, col = mongo_collection()
        docs=list(col.find({}, {"_id":0}))
        client.close()
        if docs:
            df=pd.DataFrame(docs)
            df["date"]=pd.to_datetime(df["date"])
            return df, "MongoDB"
    except Exception:
        pass
    df=pd.read_csv(CSV_PATH)
    df["date"]=pd.to_datetime(df["date"])
    return df, "CSV demo dataset"

df, source=read_records()
st.sidebar.success(f"Data source: {source}")
st.sidebar.markdown("### Filter reports")
crops=sorted(df["crop"].dropna().unique())
regions=sorted(df["region"].dropna().unique())
selected_crops=st.sidebar.multiselect("Crop", crops, default=crops)
selected_regions=st.sidebar.multiselect("Region", regions, default=regions)
selected_severity=st.sidebar.multiselect("Severity", ["Low","Moderate","High"], default=["Low","Moderate","High"])

filtered=df[df["crop"].isin(selected_crops) & df["region"].isin(selected_regions) & df["severity"].isin(selected_severity)].copy()
if filtered.empty:
    st.warning("No reports match the selected filters.")
    st.stop()

total=len(filtered)
disease_only=filtered[filtered["disease"].str.lower()!="healthy"]
common = disease_only["disease"].value_counts().index[0] if not disease_only.empty else "No disease reports"
high=int((filtered["severity"]=="High").sum())
avg_area=float(disease_only["affected_area_pct"].mean()) if not disease_only.empty else 0

k1,k2,k3,k4=st.columns(4)
k1.metric("Reports analysed", f"{total:,}")
k2.metric("Disease reports", f"{len(disease_only):,}")
k3.metric("Most reported disease", common)
k4.metric("High severity reports", f"{high:,}")

st.divider()
left,right=st.columns(2)
with left:
    counts=disease_only["disease"].value_counts().rename_axis("Disease").reset_index(name="Reports")
    fig=px.bar(counts, x="Disease", y="Reports", title="Most frequently reported diseases")
    fig.update_layout(xaxis_tickangle=-25)
    st.plotly_chart(fig, use_container_width=True)
with right:
    crop_counts=disease_only["crop"].value_counts().rename_axis("Crop").reset_index(name="Reports")
    fig=px.pie(crop_counts, names="Crop", values="Reports", title="Disease reports by crop", hole=.35)
    st.plotly_chart(fig, use_container_width=True)

left,right=st.columns(2)
with left:
    region_counts=disease_only["region"].value_counts().rename_axis("Region").reset_index(name="Reports")
    fig=px.bar(region_counts, x="Region", y="Reports", title="Reports by region")
    st.plotly_chart(fig, use_container_width=True)
with right:
    sev=filtered["severity"].value_counts().reindex(["Low","Moderate","High"],fill_value=0).rename_axis("Severity").reset_index(name="Reports")
    fig=px.bar(sev, x="Severity", y="Reports", color="Severity", title="Severity distribution")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Crop-wise disease summary")
summary=disease_only.groupby("crop").agg(
    disease_reports=("report_id","count"),
    average_affected_area=("affected_area_pct","mean"),
    high_severity=("severity",lambda s:int((s=="High").sum()))
).reset_index()
if not summary.empty:
    summary["average_affected_area"]=summary["average_affected_area"].round(1)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("📝 Add a disease report")
with st.form("new_report", clear_on_submit=True):
    a,b,c=st.columns(3)
    with a:
        new_crop=st.selectbox("Crop", CROP_OPTIONS)
        new_disease=st.text_input("Disease name", placeholder="e.g. Early Blight")
        new_region=st.selectbox("Region", regions)
    with b:
        new_severity=st.selectbox("Severity", ["Low","Moderate","High"])
        new_area=st.number_input("Estimated affected area (%)", min_value=0.0, max_value=100.0, value=10.0)
        new_date=st.date_input("Report date", value=date.today())
    with c:
        new_source=st.selectbox("Report source", ["Farmer report","Field survey","Demo entry"])
        new_notes=st.text_area("Notes", "Initial field observation")
    submitted=st.form_submit_button("Save report")
    if submitted:
        record={
            "report_id":"R"+pd.Timestamp.now().strftime("%y%m%d%H%M%S"),
            "date":new_date.isoformat(),"crop":new_crop,"disease":new_disease.strip() or "Unspecified",
            "region":new_region,"severity":new_severity,"affected_area_pct":float(new_area),
            "report_source":new_source,"notes":new_notes
        }
        saved=False
        try:
            client,col=mongo_collection()
            col.insert_one(record)
            client.close()
            saved=True
            st.success("Report saved to MongoDB. Refresh the page to see updated analytics.")
        except Exception:
            # Offline fallback: append to CSV
            existing=pd.read_csv(CSV_PATH)
            pd.concat([existing,pd.DataFrame([record])],ignore_index=True).to_csv(CSV_PATH,index=False)
            st.success("MongoDB not connected: report saved to local CSV for this demo. Refresh the page.")

with st.expander("View report records"):
    view=filtered.copy()
    view["date"]=view["date"].dt.strftime("%Y-%m-%d")
    st.dataframe(view, use_container_width=True, hide_index=True)

csv=filtered.copy()
csv["date"]=csv["date"].dt.strftime("%Y-%m-%d")
st.download_button("⬇️ Download filtered reports", csv.to_csv(index=False).encode("utf-8"),
                   "plant_disease_filtered_reports.csv","text/csv")

st.info("Academic demo: included records are synthetic sample data. Reports and severity values are illustrative, not verified diagnoses or agronomic advice.")
