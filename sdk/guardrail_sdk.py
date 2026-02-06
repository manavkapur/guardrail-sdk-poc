from sdk.decision_engine import DecisionEngine
from engines.guardrails_validator.validator import GuardrailsValidator
from engines.nemo_policy.policy import NemoPolicy


class GuardrailSDK:

    def __init__(self, enable_nemo=True):
        self.validator = GuardrailsValidator()
        self.nemo = NemoPolicy() if enable_nemo else None
        self.decision = DecisionEngine()

    async def check_input(self, text):

        signals = []
        risk_score = 0
        lower_text = text.lower()

        # ------------------------------------------------
        # Step 1: Run deterministic validators (cheap layer)
        # ------------------------------------------------
        signals += self.validator.validate(text)

        # Immediate decision check (fast-fail)
        decision = self.decision.decide(signals)
        if decision == "BLOCK":
            print("Signals:", signals)
            print("Decision:", decision)
            return decision, signals

        # ------------------------------------------------
        # Step 2: Lightweight heuristic risk scoring
        # ------------------------------------------------

        # Suspicious phrasing patterns (not just keywords)
        suspicious_phrases = [
            "ignore previous",
            "override instructions",
            "bypass",
            "jailbreak",
            "act as",
            "pretend you are",
            "developer mode",
            "simulate being",
            "without restrictions",
            "for educational purposes only"
        ]

        if any(p in lower_text for p in suspicious_phrases):
            risk_score += 2

        # Excessively long input (possible injection payload)
        if len(text) > 800:
            risk_score += 1

        # Encoded / obfuscated patterns
        if "```" in text or "<script>" in lower_text:
            risk_score += 1

        # System prompt manipulation hints
        if "system prompt" in lower_text or "hidden instructions" in lower_text:
            risk_score += 2

        # If any MEDIUM signals already exist → increase risk
        if any(s.severity == "MEDIUM" for s in signals):
            risk_score += 1

        # ------------------------------------------------
        # Step 3: Escalate to NeMo only if risk justifies it
        # ------------------------------------------------

        ESCALATION_THRESHOLD = 2

        if self.nemo and risk_score >= ESCALATION_THRESHOLD:
            nemo_signals = await self.nemo.check(text)
            signals += nemo_signals

        # ------------------------------------------------
        # Step 4: Final decision
        # ------------------------------------------------

        decision = self.decision.decide(signals)

        print("Risk Score:", risk_score)
        print("Signals:", signals)
        print("Decision:", decision)

        return decision, signals
