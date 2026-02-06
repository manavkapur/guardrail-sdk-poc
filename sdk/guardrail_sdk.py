from sdk.decision_engine import DecisionEngine
from engines.guardrails_validator.validator import GuardrailsValidator
from engines.nemo_policy.policy import NemoPolicy
from sdk.risk_signal import RiskSignal
import re


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
        # Step 1: Deterministic Validators (Precise Layer)
        # ------------------------------------------------
        signals += self.validator.validate(text)

        decision = self.decision.decide(signals)
        if decision == "BLOCK":
            print("Risk Score:", risk_score)
            print("Signals:", signals)
            print("Decision:", decision)
            return decision, signals

        # ------------------------------------------------
        # Step 2: Structured Risk Scoring
        # ------------------------------------------------

        # 1️⃣ Instruction Override Attempts (High Risk)
        if (
            lower_text.startswith("ignore")
            or "ignore all" in lower_text
            or ("ignore" in lower_text and "instruction" in lower_text)
            or "disregard previous" in lower_text
            or "override system" in lower_text
        ):
            risk_score += 3

        # 2️⃣ Role Manipulation / Jailbreak Framing (Medium-High)
        role_patterns = [
            r"act as .*",
            r"pretend you are .*",
            r"simulate being .*",
            r"developer mode",
            r"without restrictions",
            r"bypass (security|rules|policy)",
            r"jailbreak"
        ]

        for pattern in role_patterns:
            if re.search(pattern, lower_text):
                risk_score += 2
                break

        # 3️⃣ System Prompt Exfiltration (High Risk)
        if (
            "system prompt" in lower_text
            or "hidden instructions" in lower_text
            or "internal policy" in lower_text
            or "show me your instructions" in lower_text
        ):
            risk_score += 3

        # 4️⃣ Social Engineering Framing (Low-Medium)
        if (
            "for educational purposes only" in lower_text
            or "hypothetically" in lower_text
            or "just for research" in lower_text
        ):
            risk_score += 1

        # 5️⃣ Injection Payload Indicators
        if (
            "```" in text
            or "<script>" in lower_text
            or "base64" in lower_text
            or re.search(r"[A-Za-z0-9+/=]{100,}", text)
        ):
            risk_score += 2

        # 6️⃣ Abnormally Long Input
        if len(text) > 1000:
            risk_score += 1

        # 7️⃣ Medium signals increase suspicion
        if any(s.severity == "MEDIUM" for s in signals):
            risk_score += 1

        # ------------------------------------------------
        # Step 3: Risk Band Classification
        # ------------------------------------------------

        LOW_RISK = 1
        MEDIUM_RISK = 2
        HIGH_RISK = 4

        # 🚨 Immediate block for very high risk injection
        if risk_score >= HIGH_RISK:
            signals.append(
                RiskSignal(
                    engine="HeuristicLayer",
                    category="PromptInjection",
                    severity="HIGH",
                    score=0.85,
                    confidence=0.8,
                    critical=True,
                    explanation="High-risk prompt injection pattern detected"
                )
            )

        # ------------------------------------------------
        # Step 4: Escalate to NeMo (ML Layer)
        # ------------------------------------------------

        ESCALATION_THRESHOLD = MEDIUM_RISK

        if self.nemo and risk_score >= ESCALATION_THRESHOLD:
            nemo_signals = await self.nemo.check(text)
            signals += nemo_signals

        # ------------------------------------------------
        # Step 5: Final Decision
        # ------------------------------------------------

        decision = self.decision.decide(signals)

        print("Risk Score:", risk_score)
        print("Signals:", signals)
        print("Decision:", decision)

        return decision, signals
