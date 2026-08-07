def execute_priority_waterfall(row: dict, ml_threshold: float = 0.70, velocity_cap: float = 5.0) -> str:
    """
    5-Tier Decision Waterfall Engine: Scans streaming data and flags profiles 
    instantly at the first rule breach to ensure real-time transaction switch overrides.
    """
    util_rate = float(row['UTIL_RATE'])
    spending_jump = float(row['SPENDING_JUMP'])
    pay_0 = int(row['PAY_0'])
    
    risk_prob = 0.1 + (pay_0 * 0.2) + (util_rate * 0.3)
    risk_prob = min(1.0, max(0.0, risk_prob))
    
    if risk_prob >= ml_threshold:
        return "🛑 AI RISK BLOCK"
    elif spending_jump >= velocity_cap:
        return "⚠️ SECURITY VELOCITY BLOCK"
    elif pay_0 > 0:
        return "🟡 NUDGE DUE ALERT"
    elif pay_0 == 0 and util_rate < 0.25:
        return "🟢 GROWTH UPSELL TARGET"
    else:
        return "✅ STABLE BALANCE"
