import pytest
from src.compliance.penal_charge_guard import determine_flat_penal_charge

def test_late_fees_comply_with_flat_slab_caps():
    assert determine_flat_penal_charge(50.00) == 0.0
    assert determine_flat_penal_charge(4500.00) == 500.0
    assert determine_flat_penal_charge(85000.00) == 750.0
