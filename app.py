import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.western_to_rbi_transformer import WesternToRbiDataTransformer
from src.analytical_engines.risk_classifier import execute_priority_waterfall
from src.actions.ledger_poster import EphemeralLedgerPoster
from src.actions.statement_generator import ClientStatementGenerator

st.set_page_config(page_title="CreditPulse CC: Indian Bank Analytics Engine", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #0f172a; color: white; border-radius: 6px;}
    .metric-card {background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    </style>
""", unsafe_allow_html=True)

st.title("💳 CreditPulse-AI: Revolving Credit Card Analytics Engine")
st.caption("🚨 RBI Master Directions & DPDP Act 2026 Compliant | Zero-Storage Ephemeral Pipeline")

st.sidebar.header("⚙️ Policy Configuration Gateway")
ml_thresh = st.sidebar.slider("AI Risk Threshold (Probability)", 0.0, 1.0, 0.70, 0.05)
vel_cap = st.sidebar.slider("Security Velocity Trigger (x Spend Jump)", 1.0, 10.0, 5.0, 0.5)

uploaded_file = st.file_uploader("📥 Upload Card Portfolio Data Stream (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    
    transformer = WesternToRbiDataTransformer()
    processed_records = []
    
    for _, raw_row in raw_df.iterrows():
        transformed = transformer.transform_payload(raw_row.to_dict())
        transformed['STRATEGY_SEGMENT'] = execute_priority_waterfall(transformed, ml_thresh, vel_cap)
        EphemeralLedgerPoster.post_to_cbs(transformed)
        processed_records.append(transformed)
        
    out_df = pd.DataFrame(processed_records)
    
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.markdown(f"<div class='metric-card'><b>🚨 System Actions Triggered</b><h2>{len(out_df[out_df['STRATEGY_SEGMENT'] != '✅ STABLE BALANCE'])}</h2></div>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<div class='metric-card'><b>🛑 Accounts Risk Blocked</b><h2>{len(out_df[out_df['STRATEGY_SEGMENT'] == '🛑 AI RISK BLOCK'])}</h2></div>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<div class='metric-card'><b>💰 Total GST Remittance</b><h2>₹{out_df['GST_COMP'].sum():,.2f}</h2></div>", unsafe_allow_html=True)
        
    st.write("### 🛡️ Live Ephemeral Stream Processing Data View")
    st.dataframe(out_df[['ID', 'LIMIT_BAL', 'UTIL_RATE', 'SPENDING_JUMP', 'PENAL_CHARGES', 'TOTAL_MAD', 'GST_COMP', 'STRATEGY_SEGMENT']], use_container_width=True)
    
    # On-Demand Individual ReportLab Statement Segment Actions
    st.write("---")
    st.subheader("🖨️ On-Demand Client Statement Generator")
    pdf_factory = ClientStatementGenerator()
    
    for index, row in out_df.iterrows():
        col1, col2, col3 = st.columns([1, 3, 2])
        with col1:
            st.write(f"`Client ID: {int(row['ID'])}`")
        with col2:
            st.caption(f"Strategy: **{row['STRATEGY_SEGMENT']}** | Computed MAD: **₹{row['TOTAL_MAD']:.2f}**")
        with col3:
            pdf_stream = pdf_factory.generate_single_client_pdf(row.to_dict())
            st.download_button(label="📥 Download PDF Statement", data=pdf_stream, file_name=f"Statement_Client_{int(row['ID'])}.pdf", mime="application/pdf", key=f"dl_{int(row['ID'])}")

    # 3D Vector Surface Graphing Component
    st.write("---")
    st.subheader("📊 3D Portfolio Exposure & Stress Analytics Mesh")
    color_map = {"🛑 AI RISK BLOCK": "#ef4444", "⚠️ SECURITY VELOCITY BLOCK": "#f97316", "🟡 NUDGE DUE ALERT": "#eab308", "🟢 GROWTH UPSELL TARGET": "#22c55e", "✅ STABLE BALANCE": "#64748b"}
    out_df['COLOR_MARKER'] = out_df['STRATEGY_SEGMENT'].map(color_map)
    
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=out_df['UTIL_RATE'] * 100, y=out_df['SPENDING_JUMP'], z=out_df['PENAL_CHARGES'],
        mode='markers',
        marker=dict(size=8, color=out_df['COLOR_MARKER'], opacity=0.85, line=dict(color='#0f172a', width=1)),
        text=out_df['ID'].apply(lambda uid: f"Account ID: {uid}"), hoverinfo='text'
    )])
    fig_3d.update_layout(scene=dict(xaxis_title='Utilization Rate (%)', yaxis_title='Spend Jump Velocity (x)', zaxis_title='Flat Penal Charges (₹)'), margin=dict(l=0, r=0, b=0, t=0), height=500)
    st.plotly_chart(fig_3d, use_container_width=True)
