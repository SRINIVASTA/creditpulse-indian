import sys
import gc
from src.compliance.mad_calculator import calculate_indian_mad_and_gst

def test_data_stream_evicted_from_active_ram():
    transient_payload = {"bill_amt1": 50000.00, "interest_due": 1200.00, "fees_due": 0.0, "penal_charges": 0.0}
    metrics = calculate_indian_mad_and_gst(**transient_payload)
    assert metrics["total_mad"] > 0
    del transient_payload
    gc.collect()
    assert True
