class DecisionEngine:

    def decide(self, signals):

        for s in signals:
            if s.critical:
                return "BLOCK"

        high = [s for s in signals if s.severity == "HIGH"]

        if len(high) >= 1:
            return "BLOCK"

        return "ALLOW"
