# app.py
import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.graph_objects as go

from src.western_to_rbi_transformer import WesternToRbiDataTransformer
from src.analytical_engines.risk_classifier import execute_priority_waterfall
from src.actions.ledger_poster import EphemeralLedgerPoster
from src.actions.statement_generator import ClientStatementGenerator

# Page Layout Configuration
st.set_page_config(page_title="CreditPulse CC: Enterprise Portfolio Analytics Engine", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #0f172a; color: white; border-radius: 6px; font-weight: bold;}
    .metric-card {background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    </style>
""", unsafe_allow_html=True)

st.title("💳 CreditPulse-AI: Revolving Credit Card Analytics Platform")
st.caption("🚨 RBI Master Directions & DPDP Act 2026 Compliant | Ephemeral Core Engine")

# 1. SIDEBAR PARAMETERS GATEWAY
st.sidebar.header("⚙️ Policy Configuration Gateway")
ml_thresh = st.sidebar.slider("AI Risk Threshold (Probability)", 0.0, 1.0, 0.70, 0.05)
vel_cap = st.sidebar.slider("Security Velocity Trigger (x Spend Jump)", 1.0, 10.0, 5.0, 0.5)

# 2. CACHED ENGINE PIPELINE LOOP FOR TOTAL PORTFOLIO EXPOSURE
@st.cache_data(show_spinner=False)
def process_entire_portfolio_stream(uploaded_file_bytes, file_name, threshold, velocity_limit):
    """
    Transforms the full dataset in memory, runs the 5-Tier Decision Waterfall,
    and isolates financial metrics without writing files to local disks.
    """
    if file_name.endswith('.csv'):
        raw_df = pd.read_csv(io.BytesIO(uploaded_file_bytes))
    else:
        raw_df = pd.read_excel(io.BytesIO(uploaded_file_bytes))
        
    transformer = WesternToRbiDataTransformer()
    processed_records = []
    
    for _, raw_row in raw_df.iterrows():
        # Inject mock variables into streaming snapshots if unassigned in base file
        client_dict = raw_row.to_dict()
        if 'INTEREST_DUE' not in client_dict: client_dict['INTEREST_DUE'] = float(client_dict['BILL_AMT1']) * 0.035 if int(client_dict['PAY_0']) > 0 else 0.0
        if 'FEES_DUE' not in client_dict: client_dict['FEES_DUE'] = 0.0
        if 'PENAL_CHARGES' not in client_dict: client_dict['PENAL_CHARGES'] = 0.0
        
        transformed = transformer.transform_payload(client_dict)
        transformed['STRATEGY_SEGMENT'] = execute_priority_waterfall(transformed, threshold, velocity_limit)
        
        # Stream directly to core ledger network adapters (Zero-Storage requirement)
        EphemeralLedgerPoster.post_to_cbs(transformed)
        processed_records.append(transformed)
        
    return pd.DataFrame(processed_records)

# 3. INTERACTIVE SOURCE DATA INGESTION
uploaded_file = st.file_uploader("📥 Upload Unstructured Portfolio Data Stream (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    with st.spinner("⚡ Running zero-storage regulatory matrix loops for entire portfolio..."):
        out_df = process_entire_portfolio_stream(file_bytes, uploaded_file.name, ml_thresh, vel_cap)
        
    # Render KPI Metric Ribbon
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"<div class='metric-card'><b>🚨 System Actions Triggered</b><h2>{len(out_df[out_df['STRATEGY_SEGMENT'] != '✅ STABLE BALANCE'])}</h2></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div class='metric-card'><b>🛑 Accounts Risk Blocked</b><h2>{len(out_df[out_df['STRATEGY_SEGMENT'] == '🛑 AI RISK BLOCK'])}</h2></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='metric-card'><b>💰 Accumulated Pipeline GST Remittance</b><h2>₹{out_df['GST_COMP'].sum():,.2f}</h2></div>", unsafe_allow_html=True)
        
    st.write("### 🛡️ Live Ephemeral Stream Processing Data View (All Rows)")
    st.dataframe(out_df[['ID', 'LIMIT_BAL', 'UTIL_RATE', 'SPENDING_JUMP', 'PENAL_CHARGES', 'TOTAL_MAD', 'GST_COMP', 'STRATEGY_SEGMENT']], use_container_width=True)
    
    # 4. COMPREHENSIVE 3D PLOTLY RISK MATRIX SPREAD (ALL DATA ONSCREEN)
    st.write("---")
    st.subheader("📊 3D Portfolio Exposure & Stress Analytics Mesh")
    
    color_map = {
        "🛑 AI RISK BLOCK": "#ef4444", "⚠️ SECURITY VELOCITY BLOCK": "#f97316",
        "🟡 NUDGE DUE ALERT": "#eab308", "🟢 GROWTH UPSELL TARGET": "#22c55e", "✅ STABLE BALANCE": "#64748b"
    }
    out_df['COLOR_MARKER'] = out_df['STRATEGY_SEGMENT'].map(color_map)
    
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=out_df['UTIL_RATE'] * 100, y=out_df['SPENDING_JUMP'], z=out_df['PENAL_CHARGES'],
        mode='markers',
        marker=dict(size=6, color=out_df['COLOR_MARKER'], opacity=0.85, line=dict(color='#0f172a', width=0.5)),
        text=out_df['ID'].apply(lambda uid: f"Account ID: {uid}"), hoverinfo='text'
    )])
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Utilization Rate (%)', 
            yaxis_title='Spend Jump Velocity (x)', 
            zaxis_title='Flat Penal Charges (₹)'
        ),
        margin=dict(l=0, r=0, b=0, t=0), height=550
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # 5. SINGLE REQUEST LAZY PDF REPORT COMPILER (ON-DEMAND TARGET)
    st.write("---")
    st.subheader("🖨️ Target On-Demand Client Statement Generator")
    st.caption("Select one specific client from the portfolio. The system will compile the unalterable ReportLab PDF *only* for that request.")
    
    # Render search selectors populated with live streaming account IDs
    available_client_ids = out_df['ID'].astype(int).tolist()
    selected_target_id = st.selectbox("Search and Select Target Client ID:", available_client_ids)
    
    # Extract that single client's processed snapshot out of the master collection matrix
    target_row = out_df[out_df['ID'] == selected_target_id].iloc[0].to_dict()
    
    col_btn, col_info = st.columns([1, 3])
    with col_info:
        st.info(f"Target selected: **Client ID {selected_target_id}** | Mode: **{target_row['STRATEGY_SEGMENT']}** | Total MAD: **₹{target_row['TOTAL_MAD']:.2f}**")
        
    with col_btn:
        # The ReportLab PDF is generated ONLY when this button is pressed
        if st.button(f"⚡ Compile Statement PDF"):
            with st.spinner(f"Compiling ReportLab layout context for Client {selected_target_id}..."):
                pdf_factory = ClientStatementGenerator()
                pdf_stream = pdf_factory.generate_single_client_pdf(target_row)
                
            st.success(f"Statement generated in-memory!")
            st.download_button(
                label=f"💾 Save Client {selected_target_id} PDF Statement",
                data=pdf_stream,
                file_name=f"Statement_Client_{selected_target_id}.pdf",
                mime="application/pdf"
            )
else:
    st.info("Ingest your portfolio dataset stream above to view all account records, run the 3D Plotly mesh, and compile targeted statements.")
