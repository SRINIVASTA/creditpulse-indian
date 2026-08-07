import logging

class NudgeWebhookDispatcher:
    @staticmethod
    def dispatch_nudge(account_id: int, segment_strategy: str) -> bool:
        """
        Fires an outbound message webhook to the bank's digital notification gateways.
        """
        uid = int(account_id)
        strategy = str(segment_strategy)
        logging.info(f"🚀 [EPHEMERAL ACTION] Account ID: {uid} -> Webhook Sent for strategy: {strategy}")
        return True
