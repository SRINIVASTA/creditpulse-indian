from src.stream_ingestor import EphemeralStreamIngestor
from src.western_to_rbi_transformer import WesternToRbiDataTransformer
from src.analytical_engines.risk_classifier import execute_priority_waterfall
from src.actions.ledger_poster import EphemeralLedgerPoster
from src.actions.nudge_dispatcher import NudgeWebhookDispatcher

class CorePlatformOrchestrator:
    def __init__(self):
        self.ingestor = EphemeralStreamIngestor()
        self.transformer = WesternToRbiDataTransformer()
        self.ledger_poster = EphemeralLedgerPoster()
        self.nudge_dispatcher = NudgeWebhookDispatcher()

    def step_execution_pipeline(self, raw_csv_row_payload: dict, ml_threshold: float = 0.70, velocity_cap: float = 5.0) -> dict:
        sanitized_input = self.ingestor.sanitize_raw_stream_input(raw_csv_row_payload)
        if not sanitized_input:
            return {"status": "SKIPPED_ANOMALY"}

        transformed_record = self.transformer.transform_payload(sanitized_input)
        strategy = execute_priority_waterfall(transformed_record, ml_threshold, velocity_cap)
        transformed_record["STRATEGY_SEGMENT"] = strategy

        if "ALERT" in strategy or "BLOCK" in strategy:
            self.nudge_dispatcher.dispatch_nudge(transformed_record["ID"], strategy)

        posted_successfully = self.ledger_poster.post_to_cbs(transformed_record)
        return {
            "account_id": transformed_record["ID"],
            "segment_assigned": strategy,
            "posted_successfully": posted_successfully
        }
