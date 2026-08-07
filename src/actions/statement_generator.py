import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ClientStatementGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle('DocTitle', parent=self.styles['Heading1'], fontSize=18, leading=22, textColor=colors.HexColor('#0f172a'), spaceAfter=4)
        self.h2_style = ParagraphStyle('SectionHeader', parent=self.styles['Heading2'], fontSize=11, leading=15, textColor=colors.HexColor('#1e293b'), spaceBefore=10, spaceAfter=4)
        self.body_style = ParagraphStyle('BodyTextCustom', parent=self.styles['BodyText'], fontSize=9, leading=13, textColor=colors.HexColor('#475569'))
        self.bold_body = ParagraphStyle('BodyBold', parent=self.body_style, fontName='Helvetica-Bold')

    def generate_single_client_pdf(self, client_metrics: dict) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []

        # Securely read the active sidebar engine selection passed down from app.py
        engine_mode_text = client_metrics.get('ENGINE_MODE', '📌 100% Rules-Based (Original Production)')

        story.append(Paragraph("CREDITPULSE FINANCIAL SERVICES (NBFC)", self.title_style))
        story.append(Paragraph(f"<b>Statement Run:</b> {datetime.utcnow().strftime('%d-%b-%Y')} | 🚨 Confidential Regulatory Output", self.body_style))
        story.append(Paragraph(f"<b>Core Audit Track:</b> {engine_mode_text}", self.body_style))
        story.append(Spacer(1, 10))

        account_info_data = [
            [Paragraph("<b>Account ID:</b>", self.body_style), Paragraph(str(client_metrics['ID']), self.body_style),
             Paragraph("<b>Sanctioned Limit:</b>", self.body_style), Paragraph(f"₹{client_metrics['LIMIT_BAL']:,.2f}", self.body_style)],
            [Paragraph("<b>Account Strategy:</b>", self.body_style), Paragraph(f"<b>{client_metrics['STRATEGY_SEGMENT']}</b>", self.body_style),
             Paragraph("<b>Utilization Rate:</b>", self.body_style), Paragraph(f"{client_metrics['UTIL_RATE']*100:.1f}%", self.body_style)]
        ]
        account_table = Table(account_info_data, colWidths=[100, 160, 110, 150])
        account_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        story.append(account_table)
        story.append(Spacer(1, 12))

        story.append(Paragraph("Multi-Bucket Itemized Verification Ledger", self.h2_style))
        principal_due = client_metrics['BILL_AMT1']
        penal_charge = client_metrics['PENAL_CHARGES']
        gst_charge = client_metrics['GST_COMP']
        total_mad = client_metrics['TOTAL_MAD']
        
        ledger_data = [
            [Paragraph("Balance Component", self.bold_body), Paragraph("Amount (₹)", self.bold_body), Paragraph("RBI Regulatory Processing Rules Applied", self.bold_body)],
            [Paragraph("Core Principal Balance", self.body_style), f"₹{principal_due:,.2f}", "Outstanding transactional balances carried from current billing loop."],
            [Paragraph("Flat Penal Charge", self.body_style), f"₹{penal_charge:,.2f}", "Assigned via non-compounding statutory balance slabs."],
            [Paragraph("Statutory GST Remittance", self.body_style), f"₹{gst_charge:,.2f}", "Mandatory 18% GST (9% CGST + 9% SGST) applied onto fees."],
            [Paragraph("Minimum Amount Due (MAD)", self.bold_body), f"₹{total_mad:,.2f}", "Calculated as 5% of Core Principal + Fees + Flat Penal + GST."]
        ]
        
        ledger_table = Table(ledger_data, colWidths=[140, 100, 280])
        ledger_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('PADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#f8f9fa')]),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f1f5f9')),
        ]))
        for idx in range(3):
            ledger_table.setStyle(TableStyle([('TEXTCOLOR', (idx,0), (idx,0), colors.whitesmoke)]))
            
        story.append(ledger_table)
        story.append(Spacer(1, 15))

        story.append(Paragraph("System Strategy Allocation Logic", self.h2_style))
        
        # 🌟 FIXED CRITICAL LINK: Separate narrative routing based on the active sidebar toggle engine 🌟
        if "Predictive ML Engine" in engine_mode_text:
            if "GROWTH" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account is flagged for <b>Growth Optimization via Machine Learning Models</b> because your multi-dimensional transaction habits, low card utilization, and repayment signals match low-risk default behavior clusters. You are eligible for automated credit limit upgrades."
            elif "RISK" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account has entered a <b>Critical Predictive Risk Block</b> assigned dynamically via background logistic regression stress models."
            elif "VELOCITY" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account is under an adaptive <b>Predictive Security Lock</b> due to structural spending anomalies found within the stream processor matrix."
            else:
                strategy_explanation = "Stable portfolio balance configuration confirmed via active algorithmic runtime checks."
        else:
            # Reverts safely to your original default rule-based sentences
            strategy_explanation = "Stable portfolio configuration. Standard revolving interest parameters apply."
            if "GROWTH" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account is flagged for <b>Growth Optimization</b> because your repayment records are clean and your credit line utilization is low. You are eligible for automated credit limit upgrades."
            elif "RISK" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account has entered a <b>Risk Overrides</b> state because your current card utilization has crossed the critical 90% boundary while an overdue status exists."
            elif "VELOCITY" in client_metrics['STRATEGY_SEGMENT']:
                strategy_explanation = "Your account is under a temporary <b>Security Lock</b> because your current spending volume surged by over 5.0x compared to your historical baseline."

        story.append(Paragraph(strategy_explanation, self.body_style))
        story.append(Spacer(1, 20))
        story.append(Paragraph("<font color='#94a3b8'>Electronic compliance artifact processed in-memory as per DPDP Act 2026. No physical logs written to local server disk storage hierarchies.</font>", self.body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer
