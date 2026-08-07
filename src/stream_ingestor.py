import logging

class EphemeralStreamIngestor:
    @staticmethod
    def sanitize_raw_stream_input(raw_row_data: dict) -> dict:
        try:
            required_keys = ['ID', 'LIMIT_BAL', 'PAY_0', 'BILL_AMT1', 'BILL_AMT2', 'PAY_AMT1']
            for key in required_keys:
                if key not in raw_row_data or raw_row_data[key] is None:
                    return {}
            return {
                "ID": int(raw_row_data["ID"]),
                "LIMIT_BAL": float(raw_row_data["LIMIT_BAL"]),
                "PAY_0": int(raw_row_data["PAY_0"]),
                "BILL_AMT1": float(raw_row_data["BILL_AMT1"]),
                "BILL_AMT2": float(raw_row_data["BILL_AMT2"]),
                "PAY_AMT1": float(raw_row_data["PAY_AMT1"])
            }
        except (ValueError, TypeError):
            return {}
