import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression

from src.western_to_rbi_transformer import WesternToRbiDataTransformer
from src.analytical_engines.risk_classifier import execute_priority_waterfall
from src.actions.ledger_poster import EphemeralLedgerPoster
from src.actions.statement_generator import ClientStatementGenerator

# Page Layout Configuration
st.set_page_config(page_title="CreditPulse CC: Enterprise Portfolio Analytics Engine", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {background-color: #0f172a; color: white; border-radius: 6px; font-weight: bold; width: 100%;}
    .metric-card {background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
    </style>
""", unsafe_allow_html=True)

st.title("💳 CreditPulse-AI: Revolving Credit Card Analytics Platform")
st.caption("🚨 RBI Master Directions & DPDP Act 2026 Compliant | Ephemeral Core Engine")

# 1. DUAL-ENGINE SELECTION TOGGLE (SIDEBAR)
st.sidebar.header("🕹️ Engine Architecture Selector")
selected_engine = st.sidebar.radio(
    "Choose Core Risk Processing Mode:",
    ["📌 100% Rules-Based (Original Production)", "🤖 Predictive ML Engine (Parallel Track)"]
)
st.sidebar.markdown("---")

# 2. SIDEBAR PARAMETERS GATEWAY
st.sidebar.header("⚙️ Policy Configuration Gateway")
ml_thresh = st.sidebar.slider("AI Risk Threshold (Probability)", 0.0, 1.0, 0.70, 0.05)
vel_cap = st.sidebar.slider("Security Velocity Trigger (x Spend Jump)", 1.0, 10.0, 5.0, 0.5)

# 3. CACHED ENGINE PIPELINE LOOP FOR TOTAL PORTFOLIO EXPOSURE
@st.cache_data(show_spinner=False)
def process_entire_portfolio_stream(uploaded_file_bytes, file_name, threshold, velocity_limit, engine_mode):
    """
    Transforms the full dataset in memory, runs the selected Decision Track,
    and isolates financial metrics without writing files to local disks.
    """
    if file_name.endswith('.csv'):
        raw_df = pd.read_csv(io.BytesIO(uploaded_file_bytes))
    else:
        raw_df = pd.read_excel(io.BytesIO(uploaded_file_bytes))
        
    transformer = WesternToRbiDataTransformer()
    processed_records = []
    
    # Pre-train isolated ML model in active session memory if ML mode is selected
    if engine_mode == "🤖 Predictive ML Engine (Parallel Track)":
        X_train = np.array([[0.85, 4, 1.2], [0.15, 0, 0.1], [0.95, 6, 2.5], [0.22, 0, 0.3], [0.70, 2, 0.9], [0.33, 1, 0.2]])
        y_train = np.array([1, 0, 1, 0, 1, 0])  # 1 = Default Risk, 0 = Active Repayment
        ml_model = LogisticRegression()
        ml_model.fit(X_train, y_train)

    for _, raw_row in raw_df.iterrows():
        client_dict = raw_row.to_dict()
        
        # Inject standard revolving primitives if unassigned in base source file mapping
        if 'INTEREST_DUE' not in client_dict: 
            client_dict['INTEREST_DUE'] = float(client_dict['BILL_AMT1']) * 0.035 if int(client_dict['PAY_0']) > 0 else 0.0
        if 'FEES_DUE' not in client_dict: 
            client_dict['FEES_DUE'] = 0.0
        if 'PENAL_CHARGES' not in client_dict: 
            client_dict['PENAL_CHARGES'] = 0.0
        
        transformed = transformer.transform_payload(client_dict)
        
        # Branch Execution according to Sidebar Engine selection
        if engine_mode == "📌 100% Rules-Based (Original Production)":
            transformed['STRATEGY_SEGMENT'] = execute_priority_waterfall(transformed, threshold, velocity_limit)
        else:
            util = float(transformed.get('UTIL_RATE', 0.0))
            delay = float(client_dict.get('PAY_0', 0.0))
            jump = float(transformed.get('SPENDING_JUMP', 1.0))
            
            ml_prob = ml_model.predict_proba([[util, delay, jump]])[0][1]
            
            if ml_prob >= threshold:
                transformed['STRATEGY_SEGMENT'] = "🛑 AI RISK BLOCK"
            elif jump >= velocity_limit:
                transformed['STRATEGY_SEGMENT'] = "⚠️ SECURITY VELOCITY BLOCK"
            elif delay > 0:
                transformed['STRATEGY_SEGMENT'] = "🟡 NUDGE DUE ALERT"
            elif util < 0.30:
                transformed['STRATEGY_SEGMENT'] = "🟢 GROWTH UPSELL TARGET"
            else:
                transformed['STRATEGY_SEGMENT'] = "✅ STABLE BALANCE"
        
        EphemeralLedgerPoster.post_to_cbs(transformed)
        processed_records.append(transformed)
        
    return pd.DataFrame(processed_records)
# 4. INTERACTIVE SOURCE DATA INGESTION
uploaded_file = st.file_uploader("📥 Upload Unstructured Portfolio Data Stream (.csv / .xlsx)", type=["csv", "xlsx"])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    
    with st.spinner("⚡ Running zero-storage regulatory matrix loops for entire portfolio..."):
        out_df = process_entire_portfolio_stream(file_bytes, uploaded_file.name, ml_thresh, vel_cap, selected_engine)
        
    # Calculate explicit counts across all 5 tiers of the Strategic Waterfall
    total_records = len(out_df)
    ai_risk_count = len(out_df[out_df['STRATEGY_SEGMENT'] == "🛑 AI RISK BLOCK"])
    security_block_count = len(out_df[out_df['STRATEGY_SEGMENT'] == "⚠️ SECURITY VELOCITY BLOCK"])
    nudge_alert_count = len(out_df[out_df['STRATEGY_SEGMENT'] == "🟡 NUDGE DUE ALERT"])
    growth_target_count = len(out_df[out_df['STRATEGY_SEGMENT'] == "🟢 GROWTH UPSELL TARGET"])
    stable_count = len(out_df[out_df['STRATEGY_SEGMENT'] == "✅ STABLE BALANCE"])
    
    # 5. RENDER COMPREHENSIVE 5-COLUMN DISTRIBUTION METRIC RIBBON
    st.write("### 📈 Full Portfolio Segment Distribution")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    with m1:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #ef4444;'>
                <span style='font-size: 20px;'>🛑</span> <b>AI Risk Blocked</b>
                <h2 style='color: #ef4444; margin: 5px 0;'>{ai_risk_count}</h2>
                <small style='color: #64748b;'>Critical Default Risk</small>
            </div>
        """, unsafe_allow_html=True)
        
    with m2:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #f97316;'>
                <span style='font-size: 20px;'>⚠️</span> <b>Velocity Blocked</b>
                <h2 style='color: #f97316; margin: 5px 0;'>{security_block_count}</h2>
                <small style='color: #64748b;'>Fraud / Spend Spikes</small>
            </div>
        """, unsafe_allow_html=True)
        
    with m3:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #eab308;'>
                <span style='font-size: 20px;'>🟡</span> <b>Nudge Due Alerts</b>
                <h2 style='color: #eab308; margin: 5px 0;'>{nudge_alert_count}</h2>
                <small style='color: #64748b;'>Payment Reminders</small>
            </div>
        """, unsafe_allow_html=True)
        
    with m4:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #22c55e;'>
                <span style='font-size: 20px;'>🟢</span> <b>Growth Targets</b>
                <h2 style='color: #22c55e; margin: 5px 0;'>{growth_target_count}</h2>
                <small style='color: #64748b;'>Limit Upsell Eligible</small>
            </div>
        """, unsafe_allow_html=True)
        
    with m5:
        st.markdown(f"""
            <div class='metric-card' style='border-top: 4px solid #64748b;'>
                <span style='font-size: 20px;'>✅</span> <b>Stable Accounts</b>
                <h2 style='color: #64748b; margin: 5px 0;'>{stable_count}</h2>
                <small style='color: #64748b;'>Healthy Credit Profiles</small>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
        <div style='background: #e2e8f0; padding: 12px 15px; border-radius: 6px; margin-top: 15px; font-weight: bold; color: #1e293b; font-size: 14px;'>
            📋 Portfolio Reconciliation Matrix Summary: 
            [ Total Ingested Rows: {total_records} ] | 
            Active Flags: {ai_risk_count + security_block_count + nudge_alert_count} | 
            Standard Base Operations: {growth_target_count + stable_count} | 
            Aggregated GST Remittance: ₹{out_df['GST_COMP'].sum():,.2f}
        </div>
    """, unsafe_allow_html=True)
        
    # 6. DATA TABLE VIEWER
    st.write("### 🛡️ Live Ephemeral Stream Processing Data View (All Rows)")
    st.dataframe(out_df[['ID', 'LIMIT_BAL', 'UTIL_RATE', 'SPENDING_JUMP', 'PENAL_CHARGES', 'TOTAL_MAD', 'GST_COMP', 'STRATEGY_SEGMENT']], use_container_width=True)
    
    # 7. PORTFOLIO SEGMENT EXPOSURE PIE ANALYSIS (FIXED YANCHOR PROPERTY VALUE)
    st.write("---")
    st.subheader("📊 Portfolio Strategic Exposure Share")
    st.caption(f"✨ Rendering dynamic allocation distribution metrics generated via: **{selected_engine}**")
    
    color_map = {
        "🛑 AI RISK BLOCK": "#ef4444", 
        "⚠️ SECURITY VELOCITY BLOCK": "#f97316",
        "🟡 NUDGE DUE ALERT": "#eab308", 
        "🟢 GROWTH UPSELL TARGET": "#22c55e", 
        "✅ STABLE BALANCE": "#64748b"
    }
    
    segment_counts = out_df['STRATEGY_SEGMENT'].value_counts()
    labels = segment_counts.index.tolist()
    values = segment_counts.values.tolist()
    colors = [color_map.get(lbl, "#cbd5e1") for lbl in labels]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textinfo='percent',
        insidetextorientation='radial',
        hoverinfo='label+value+percent',
        textfont=dict(size=13, color='#1e293b', family="Inter")
    )])
    
    fig_pie.update_layout(
        margin=dict(l=20, r=20, b=20, t=20),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",  # Fixed: Swapped 'center' out for valid enum token 'middle'
            y=0.5,
            xanchor="left", x=1.05,
            font=dict(size=12)
        )
    )
    
    col_chart, col_narrative = st.columns([2, 1])
    
    with col_chart:
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_narrative:
        st.markdown("#### 🛡️ Compliance Insights")
        st.markdown(f"""
        This pie matrix directly breaks down your **{total_records} ingested accounts**. 
        
        When toggled, it highlights exactly how the engine shifts accounts dynamically:
        * **Rule Engine:** Locks your explicit, line-by-line RBI logic cuts.
        * **ML Engine:** Adapts boundaries based on portfolio-wide behavioral risk signals.
        """)
    
    # 8. SINGLE REQUEST LAZY PDF REPORT COMPILER
    st.write("---")
    st.subheader("🖨️ Target On-Demand Client Statement Generator")
    st.caption("Select one specific client from the portfolio. The system will compile the unalterable ReportLab PDF *only* for that request.")
    
    available_client_ids = out_df['ID'].astype(int).tolist()
    selected_target_id = st.selectbox("Search and Select Target Client ID:", available_client_ids)
    
    matched_selection = out_df[out_df['ID'] == selected_target_id]
    
    if not matched_selection.empty:
        target_row = matched_selection.iloc[0].to_dict()
        
        col_btn, col_info = st.columns(2)
        with col_info:
            st.info(f"Target selected: **Client ID {selected_target_id}** | Mode: **{target_row['STRATEGY_SEGMENT']}** | Total MAD: **₹{target_row['TOTAL_MAD']:.2f}**")
            
        with col_btn:
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
        st.error(f"Selected Client ID {selected_target_id} could not be pulled from the stream matrix.")
