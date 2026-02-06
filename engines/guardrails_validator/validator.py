from guardrails import Guard
from guardrails.hub import DetectPII
from guardrails.errors import ValidationError
from sdk.risk_signal import RiskSignal


class GuardrailsValidator:

    def __init__(self):

        self.guard = Guard().use(
            DetectPII(on_fail="exception")
        )

    def validate(self, text):

        try:
            self.guard.validate(text)
            return []

        except ValidationError as e:

            return [
                RiskSignal(
                    engine="GuardrailsAI",
                    category="PII",
                    severity="HIGH",
                    score=0.95,
                    confidence=0.95,
                    critical=True,
                    explanation=str(e)
                )
            ]
