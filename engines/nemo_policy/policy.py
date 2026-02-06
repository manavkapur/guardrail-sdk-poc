from nemoguardrails import LLMRails, RailsConfig
from sdk.risk_signal import RiskSignal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()


class NemoPolicy:

    def __init__(self):

        config = RailsConfig.from_path("profiles")

        # Proper LangChain OpenAI LLM
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        self.app = LLMRails(
            config,
            llm=llm,
            verbose=True
        )

    async def check(self, text):

        result = await self.app.generate_async(
            messages=[{
                "role": "user",
                "content": text
            }],
            options={
                "rails": {
                    "input": ["jailbreak_detection_model"]
                }
            }
        )

        print("NeMo Raw Result:", result)

        # ---- IMPORTANT FIX ----
        # result is GenerationResponse (not dict)
        # assistant response is inside result.response

        if result.response and len(result.response) > 0:
            content = result.response[0]["content"].lower()

            # Detect refusal response from jailbreak model
            refusal_patterns = [
                "can't assist",
                "cannot assist",
                "not able to help",
                "i’m sorry",
                "i cannot help"
            ]

            if any(p in content for p in refusal_patterns):
                return [
                    RiskSignal(
                        engine="NeMo",
                        category="Jailbreak",
                        severity="HIGH",
                        score=0.9,
                        confidence=0.9,
                        critical=True,
                        explanation="Blocked by NeMo jailbreak detection model"
                    )
                ]

        return []
