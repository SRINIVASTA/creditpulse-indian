# 💳 CreditPulse-AI: Revolving Credit Card Analytics Platform
### 🚨 RBI Master Directions & DPDP Act 2026 Compliant Enterprise Portfolio Risk Engine

CreditPulse-AI is a high-utility, B2B SaaS portfolio optimization and risk underwriting application built tailored for Indian Non-Banking Financial Companies (NBFCs), Microfinance Institutions (MFIs), and Digital Lending Startups. 

🌐 **Live Interactive Web App:** [Launch Live Streamlit Dashboard](https://creditpulse-indian-aplrf7swwheadhpqhouazq.streamlit.app/)

The platform deploys a unique **Dual-Engine Architecture** that isolates deterministic accounting logic from predictive machine learning behaviors, allowing lenders to safely uncover trapped credit line revenue while proactively screening for Gross Non-Performing Assets (GNPAs).

---

## 🕹️ Core System Capabilities

### 1. Dual-Track Risk Processing Engine
* **📌 100% Rules-Based Track (Original Production):** Executes a rigid, auditable priority waterfall mapping static policy thresholds to protect invoicing, interest calculation, and statutory fees from variance.
* **🤖 Predictive ML Track (Parallel Track):** Deploys an in-memory Scikit-Learn machine learning classifier that simultaneously cross-evaluates card utilization, payment lag (`PAY_0`), and spending velocity to uncover hidden default vectors and re-route credit allocations.

### 2. Full Portfolio Segment Distribution
The processing engine streams and segregates unstructured incoming data sets instantly across a 5-Tier Strategic Matrix:
* **🛑 AI Risk Blocked:** Flagged critical default profiles before 90-day delinquency milestones.
* **⚠️ Velocity Blocked:** Automated line freezes triggered by sudden transactional velocity surges.
* **🟡 Nudge Due Alerts:** Early collection mapping isolating transient repayment delays.
* **🟢 Growth Targets:** Safely flags low-risk, low-utilization accounts eligible for automated credit limit upgrades.
* **✅ Stable Accounts:** Baselines solid credit asset accounts maintaining programmatic balance stability.

### 3. Financial Reconciliation Matrix Summary
* **Statutory Compliance:** Automatically audits the core credit card statement math (`Minimum Amount Due` = 5% of Core Principal + Fees + Flat Penalties + GST).
* **GST Automation:** Instantly calculates and bundles the mandatory 18% GST (9% CGST + 9% SGST) over fee-bearing components for downstream corporate remittance reporting.

### 4. Target On-Demand Client Statement Generator
Generates an unalterable, print-ready document using **ReportLab** straight out of the active memory stream. The PDF dynamically updates its system strategy allocation logic text depending on which backend engine was running the simulation on your screen.

---

## 🛡️ Statutory Regulatory Compliance

* **RBI Master Directions (2022-2026 Credit Card Issuance & Conduct):** Guarantees zero automated blind decisioning by leaving the threshold gates under strict human control via interactive sidebar policy sliders. Restricts penalties to flat, non-compounding statutory ledger charges.
* **DPDP Act 2026 (Data Minimization & Ephemeral Core Architecture):** Operates on an entirely volatile, zero-storage runtime footprint. Personal portfolio data and streaming variables are processed completely in-memory and permanently wiped the moment the application session is closed, insulating the NBFC from data leakage liability.

---

## 🛠️ Project Directory Tree

```text
creditpulse-indian/
├── .github/workflows/       # Automated CI/CD execution setups
├── .streamlit/              # UI deployment layout styles
├── src/
│   ├── western_to_rbi_transformer.py   # Maps western base features to RBI schema
│   ├── analytical_engines/
│   │   └── risk_classifier.py          # Traditional rule-waterfall logic script
│   └── actions/
│       ├── ledger_poster.py            # Feeds transaction entries to core banking adapters
│       └── statement_generator.py      # ReportLab factory for compiling statements
├── app.py                   # Main interactive Streamlit SaaS platform file
├── requirements.txt         # Package dependency records
└── credit_data.csv          # 322-Row Baseline Sample Credit Portfolio
```

---

## 🚀 Quick Local Installation & Running Guide

### 1. Clone the Codebase Workspace
```bash
git clone https://github.com
cd creditpulse-indian
```

### 2. Configure Your Virtual Environment Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Execute the Streamlit Server Platform
```bash
streamlit run app.py
```

---

## 📊 Commercial SaaS Pilot Framework (B2B GTM Playbook)
CreditPulse-AI enters markets via a zero-integration **30-Day Sandbox Pilot Track**:
1. **The Ingest Phase:** Target client uploads a historical, anonymized portfolio data file up to 10,000 rows.
2. **The Measurement Phase:** The engine quantifies *Return on Trust* (proving how many weeks earlier the ML track flags defaults) and *Return on Experience* (unlocking an average of 15% hidden growth accounts stuck in rigid rules).
3. **The Audit Phase:** Verifies exact financial ledger reconciliation down to a single paisa before generating target customer statements.

## 📄 License & Copyright

> ⚠️ **IMPORTANT COPYRIGHT NOTICE**
> 
> **All Rights Reserved © 2026 T A Srinivas.**
> This repository is strictly for portfolio viewing purposes. **DO NOT COPY, CLONE, OR REDISTRIBUTE** this code. Stolen copies or unauthorized forks will be reported immediately for a GitHub copyright takedown.

* **Lead Architect & Developer:** [Srinivasta](https://github.com/SRINIVASTA)

### 🌐 Let’s Connect

- [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/srinivas-t-a-557637119/)  
- [![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/srinivasta)  
- [![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tasrinivass@gmail.com)  
- [![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/srinivasta)
- [![Website](https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=website&logoColor=white)](https://srinivasta.github.io)

