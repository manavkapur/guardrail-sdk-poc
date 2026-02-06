from dataclasses import dataclass

@dataclass
class RiskSignal:
    engine: str
    category: str
    severity: str
    score: float
    confidence: float
    critical: bool
    explanation: str
