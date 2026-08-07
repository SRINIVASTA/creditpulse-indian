# app.py
import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

from src.western_to_rbi_transformer import WesternToRbiDataTransformer
from src.analytical_engines.risk_classifier import execute_priority_waterfall
from src.actions.ledger_poster import EphemeralLedgerPoster
from src.actions.statement_generator import ClientStatementGenerator

st.set_page_config(page_title="CreditPulse CC: Single Client Query Engine", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #0f172a; color: white; border-radius: 6px; width: 100%;}
    .metric-card {background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ CreditPulse-AI: Single Client Compliance Processor")
st.caption("🚨 RBI Master Directions & DPDP Act 2026 Compliant | Lazy Real-Time Processing")

# 1. CORE SOURCE DATA ENTRY GATES
uploaded_file = st.file_uploader("📥 Step 1: Load Base Database File Stream (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the data file cleanly into memory
    if uploaded_file.name.endswith('.csv'):
        base_df = pd.read_csv(uploaded_file)
    else:
        base_df = pd.read_excel(uploaded_file)
        
    st.success(f"Successfully connected to portfolio registry file. Total available rows: {len(base_df)}")
    
    st.write("---")
    st.subheader("🔍 Step 2: Target Single Account Ingestion")
    
    # User Input to find one exact target client ID
    target_id = st.number_input("Enter Specific Client ID to Process:", min_value=int(base_df['ID'].min()), max_value=int(base_df['ID'].max()), value=int(base_df['ID'].min()), step=1)
    
    # 2. RUN LAZY ISOLATION LIFE CYCLE
    if st.button("⚡ Run Regulatory Transformation Engine"):
        # Instantly filter and find that single row in memory
        matched_row = base_df[base_df['ID'] == target_id]
        
        if matched_row.empty:
            st.error(f"Account ID {target_id} not found inside the loaded dataset.")
        else:
            with st.spinner("Processing zero-storage conversion metrics..."):
                # Extract the raw row dictionary
                raw_client_dict = matched_row.iloc[0].to_dict()
                
                # Run the multi-bucket RBI transformer on just this one client record
                transformer = WesternToRbiDataTransformer()
                transformed = transformer.transform_payload(raw_client_dict)
                
                # Execute strategy categorization waterfall
                strategy = execute_priority_waterfall(transformed, ml_threshold=0.70, velocity_cap=5.0)
                transformed['STRATEGY_SEGMENT'] = strategy
                
                # Post out to core ledger streaming pipeline instantly (Zero-Storage rule)
                EphemeralLedgerPoster.post_to_cbs(transformed)
                
            # 3. RENDER METRIC METRICS FOR THIS SINGLE CLIENT
            st.write("### 📊 Real-Time Compliance Output Summary")
            
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown(f"<div class='metric-card'><b>Assigned Strategy</b><h3 style='color:#0f172a;'>{transformed['STRATEGY_SEGMENT']}</h3></div>", unsafe_allow_html=True)
            with kpi2:
                st.markdown(f"<div class='metric-card'><b>Computed Minimum Amount Due (MAD)</b><h2>₹{transformed['TOTAL_MAD']:.2f}</h2></div>", unsafe_allow_html=True)
            with kpi3:
                st.markdown(f"<div class='metric-card'><b>18% GST Component Remitted</b><h2>₹{transformed['GST_COMP']:.2f}</h2></div>", unsafe_allow_html=True)
                
            st.write("#### Itemized Balance Sheets Details")
            display_df = pd.DataFrame([transformed])
            st.dataframe(display_df[['ID', 'LIMIT_BAL', 'UTIL_RATE', 'SPENDING_JUMP', 'PENAL_CHARGES', 'TOTAL_MAD', 'GST_COMP']], use_container_width=True)
            
            # 4. TARGET REPORTLAB PDF COMPILATION AND DOWNLOAD TRIGGER
            st.write("---")
            st.subheader("🖨️ Step 3: Print Audit Statement")
            
            with st.spinner("Compiling ReportLab PDF context on-the-fly..."):
                pdf_factory = ClientStatementGenerator()
                pdf_stream = pdf_factory.generate_single_client_pdf(transformed)
                
            st.download_button(
                label=f"💾 Download Official PDF Statement for Client {target_id}",
                data=pdf_stream,
                file_name=f"Statement_Client_{target_id}.pdf",
                mime="application/pdf"
            )
else:
    st.info("Ingest your portfolio dataset schema file above to enable the single-client query lookup dashboard.")
