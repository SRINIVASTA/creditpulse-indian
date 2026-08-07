# src/western_to_rbi_transformer.py
from datetime import datetime
from src.compliance.penal_charge_guard import determine_flat_penal_charge
from src.compliance.mad_calculator import calculate_indian_mad_and_gst

class WesternToRbiDataTransformer:
    def transform_payload(self, row: dict) -> dict:
        """
        Ingests a dictionary snapshot for a single client.
        Enforces defensive types validation to prevent runtime payload errors.
        """
        # Defensive Data Typing Gates
        id_val = int(float(str(row['ID'])))
        limit_bal = float(row['LIMIT_BAL'])
        pay_0 = int(float(str(row['PAY_0'])))
        bill_amt1 = float(row['BILL_AMT1'])
        bill_amt2 = float(row['BILL_AMT2'])
        
        # Core Feature Engineering Calculations
        util_rate = bill_amt1 / max(1.0, limit_bal)
        spending_jump = bill_amt1 / bill_amt2 if bill_amt2 > 0 else 1.0
        
        # Pull derived metrics from the compliance gates
        penal_charges = determine_flat_penal_charge(bill_amt1) if pay_0 > 0 else 0.0
        
        # Simulating unbilled accrued interest on dynamic revolving balances
        interest_due = bill_amt1 * 0.035 if pay_0 > 0 else 0.0
        fees_due = 0.0
        
        # Compute Indian MAD and Tax components
        mad_metrics = calculate_indian_mad_and_gst(bill_amt1, interest_due, fees_due, penal_charges)
        
        return {
            "ID": id_val,
            "LIMIT_BAL": limit_bal,
            "UTIL_RATE": util_rate,
            "SPENDING_JUMP": spending_jump,
            "PENAL_CHARGES": penal_charges,
            "TOTAL_MAD": mad_metrics["total_mad"],
            "GST_COMP": mad_metrics["gst_component"],
            "PAY_0": pay_0,
            "BILL_AMT1": bill_amt1, # Required by Statement Generator Table mapping
            "TIMESTAMP": datetime.utcnow().isoformat() + "Z"
        }
