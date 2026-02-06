from sqlalchemy import text
from sdk.decision_engine import DecisionEngine
from engines.guardrails_validator.validator import GuardrailsValidator
from engines.nemo_policy.policy import NemoPolicy
import asyncio

class GuardrailSDK:

    def __init__(self):

        self.validator = GuardrailsValidator()
        self.nemo = NemoPolicy()
        self.decision = DecisionEngine()

    async def check_input(self, text):

        signals = []

        signals += self.validator.validate(text)
        signals += await self.nemo.check(text)

        decision = self.decision.decide(signals)
        print("Signals:", signals)
        print("Decision:", decision)


        return decision, signals
