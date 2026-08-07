from decimal import Decimal, ROUND_HALF_UP

def calculate_indian_mad_and_gst(bill_amt1: float, interest_due: float, fees_due: float, penal_charges: float, floor_mad_inr: float = 250.00) -> dict:
    """
    Computes Indian Minimum Amount Due (MAD) cleanly in Decimal space.
    Formula: 5% of Principal (BILL_AMT1) + Interest + Fees + Penal Charges + 18% GST on charges.
    Ensures late fees and interest are isolated from compounding into principal balance.
    """
    b_amt = Decimal(str(bill_amt1))
    i_due = Decimal(str(interest_due))
    f_due = Decimal(str(fees_due))
    p_chg = Decimal(str(penal_charges))
    floor_limit = Decimal(str(floor_mad_inr))
    
    principal_portion = (b_amt * Decimal('0.05')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    raw_mad = principal_portion + i_due + f_due + p_chg
    
    # 18% GST applied strictly on processing fees, accrued interest, and penal charges
    gst_component = ((i_due + f_due + p_chg) * Decimal('0.18')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_mad_final = raw_mad + gst_component
    
    total_outstanding = b_amt + i_due + f_due + p_chg + gst_component
    
    if total_outstanding <= floor_limit:
        total_mad_final = total_outstanding
    else:
        total_mad_final = max(total_mad_final, floor_limit)
        
    return {
        "total_mad": float(total_mad_final.quantize(Decimal('0.01'))),
        "gst_component": float(gst_component),
        "principal_repayment_portion": float(principal_portion)
    }
