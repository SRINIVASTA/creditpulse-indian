import json
import os

def determine_flat_penal_charge(current_outstanding: float, config_path: str = None) -> float:
    """
    RBI Compliance Gate: Restricts systems from levying percentage-based penal interest.
    Dynamically maps outstanding balances to flat cash penalty slabs.
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), '../../config/credit_policy_limits.json')
    
    if not os.path.exists(config_path):
        bal = float(current_outstanding)
        if bal <= 100: return 0.0
        elif bal <= 500: return 100.0
        elif bal <= 10000: return 500.0
        return 750.0

    with open(config_path, 'r') as f:
        config = json.load(f)
        
    slabs = config["indian_lending_compliance_profile"]["flat_penal_charge_slabs"]
    bal = float(current_outstanding)
    
    for slab in slabs:
        if slab["min_outstanding_balance_inr"] <= bal <= slab["max_outstanding_balance_inr"]:
            return float(slab["fee_inr"])
            
    return 750.00
