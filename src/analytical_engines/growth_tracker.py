from decimal import Decimal

class EphemeralGrowthTracker:
    @staticmethod
    def assess_wallet_acceleration(spend_current_month: float, spend_previous_month: float) -> float:
        """
        Calculates the real-time velocity shift ratio to identify high-spending profiles.
        """
        b1 = Decimal(str(spend_current_month))
        b2 = Decimal(str(spend_previous_month))
        
        if b2 <= 0:
            return 1.0
            
        velocity_jump = b1 / b2
        return float(velocity_jump.quantize(Decimal('0.01')))
