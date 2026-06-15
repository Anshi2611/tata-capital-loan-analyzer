import streamlit as st
import traceback

from parser import (
    extract_zip,
    process_json_files
)

from excel_generator import (
    generate_excel
)

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Tata Capital Loan Data Transformation Suite",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    color: #0F4C81;
}

.metric-title {
    font-size: 16px;
    color: #666666;
}

.footer {
    text-align:center;
    color:gray;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------

st.markdown("""
<div style="
background: linear-gradient(90deg,#0F4C81,#1A73E8);
padding:25px;
border-radius:15px;
margin-bottom:25px;
">

<h1 style="color:white;margin:0;">
🏦 Tata Capital Loan Data Transformation Suite
</h1>

<p style="color:white;font-size:18px;">
Automated JSON Processing • Data Validation • Excel Reporting
</p>

</div>
""", unsafe_allow_html=True)

# -----------------------------
# UPLOAD
# -----------------------------

st.markdown("### 📂 Upload Loan Application Archive")

uploaded_file = st.file_uploader(
    "Upload ZIP / 7Z File",
    type=["zip", "7z"]
)

# -----------------------------
# PROCESS
# -----------------------------

if uploaded_file:

    try:

        with st.spinner("Processing files..."):

            json_files = extract_zip(
                uploaded_file
            )

            df = process_json_files(
                json_files
            )

        st.success(
            f"Successfully processed {len(json_files)} files"
        )

        # -----------------------------
        # DEBUG INFO
        # -----------------------------

        st.write("Data Shape:", df.shape)
        st.write("Total Columns:", len(df.columns))

        # -----------------------------
        # KPI CARDS
        # -----------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">
                    {len(json_files)}
                </div>
                <div class="metric-title">
                    Files Processed
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">
                    {len(df)}
                </div>
                <div class="metric-title">
                    Records Generated
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="metric-value">
                    {len(df.columns)}
                </div>
                <div class="metric-title">
                    Data Fields
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # -----------------------------
        # PREVIEW
        # -----------------------------

        st.markdown("""
        <div style="
        background:white;
        padding:15px;
        border-radius:12px;
        box-shadow:0px 2px 10px rgba(0,0,0,0.08);
        ">
        <h3>📊 Application Data Preview</h3>
        </div>
        """, unsafe_allow_html=True)

        safe_df = df.fillna("").astype(str)

        st.dataframe(
            safe_df.head(100),
            use_container_width=True,
            height=450
        )

        # -----------------------------
        # EXCEL GENERATION
        # -----------------------------

        st.write("Generating Excel...")

        excel_file = generate_excel(
            safe_df
        )

        st.success("Excel generated successfully")

        # -----------------------------
        # DOWNLOAD
        # -----------------------------

        st.download_button(
            label="📥 Download Excel Report",
            data=excel_file,
            file_name="Tata_Capital_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # -----------------------------
        # FOOTER
        # -----------------------------

        st.markdown("""
        <div class="footer">
        <hr>
        Tata Capital Loan Analyzer |
        JSON Processing • Analytics • Reporting
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

        st.code(
            traceback.format_exc()
        )