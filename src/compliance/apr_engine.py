from decimal import Decimal

class RegulatoryAprEngine:
    @staticmethod
    def compute_annualized_percentage_rate(base_interest_rate_monthly: float, annualized_upfront_fees: float, loan_tenure_months: int) -> float:
        """
        Calculates the Annual Percentage Rate (APR) to show the true cost of credit.
        """
        r_monthly = Decimal(str(base_interest_rate_monthly))
        tenure = Decimal(str(loan_tenure_months))
        fees = Decimal(str(annualized_upfront_fees))
        
        nominal_annual_rate = r_monthly * Decimal('12.0')
        fee_loading_premium = (fees / tenure) * Decimal('12.0') / Decimal('100000.0')
        
        apr_calculated = nominal_annual_rate + fee_loading_premium
        return float(apr_calculated.quantize(Decimal('0.0001')))
