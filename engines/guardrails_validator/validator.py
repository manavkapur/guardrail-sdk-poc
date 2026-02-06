import re
from sdk.risk_signal import RiskSignal


class GuardrailsValidator:

    def __init__(self):
        pass

    def validate(self, text):

        # Simple credit card detection
        cc_pattern = r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"

        if re.search(cc_pattern, text):
            return [
                RiskSignal(
                    engine="GuardrailsAI",
                    category="PII",
                    severity="HIGH",
                    score=0.95,
                    confidence=0.95,
                    critical=True,
                    explanation="Credit card detected"
                )
            ]

        return []
