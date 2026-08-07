import pytest
import os
from src.western_to_rbi_transformer import WesternToRbiDataTransformer

def test_provided_portfolio_rows_map_exactly_to_rbi_rules():
    transformer = WesternToRbiDataTransformer()
    
    # Testing Row 1002 (Delinquent High Spender)
    row_1002 = {"ID": 1002, "LIMIT_BAL": 150000, "PAY_0": 2, "BILL_AMT1": 85000, "BILL_AMT2": 12000, "PAY_AMT1": 0}
    tx_1002 = transformer.transform_payload(row_1002)
    assert tx_1002["PENAL_CHARGES"] == 750.00
    assert tx_1002["GST_COMP"] > 0.0

    # Testing Row 1003 (Low balance floor trigger validation)
    row_1003 = {"ID": 1003, "LIMIT_BAL": 200000, "PAY_0": 0, "BILL_AMT1": 5000, "BILL_AMT2": 25000, "PAY_AMT1": 5000}
    tx_1003 = transformer.transform_payload(row_1003)
    assert tx_1003["TOTAL_MAD"] == 250.00
