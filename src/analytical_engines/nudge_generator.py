class EphemeralNudgeScheduler:
    @staticmethod
    def evaluate_grace_period_eligibility(days_until_due_date: int, has_repaid_minimum: bool) -> dict:
        """
        Monitors accounts moving through the strict 3-day grace period.
        """
        days = int(days_until_due_date)
        repaid = bool(has_repaid_minimum)
        
        if repaid:
            return {"action": "SUPPRESS_ALL_ALERTS", "grace_period_active": False}
            
        if days == 0:
            return {"action": "TRIGGER_SOFT_WHATSAPP_NUDGE", "grace_period_active": True}
        elif -3 <= days < 0:
            return {"action": "TRIGGER_CRITICAL_GRACE_WINDOW_NUDGE", "grace_period_active": True}
        elif days < -3:
            return {"action": "ROUTE_TO_LEGAL_COLLECTIONS_ENGINE", "grace_period_active": False}
            
        return {"action": "STANDARD_STATEMENT_DISPATCH", "grace_period_active": False}
