import asyncio
from sdk.guardrail_sdk import GuardrailSDK
from agent.basic_agent import BasicAgent

sdk = GuardrailSDK()
agent = BasicAgent()

async def run():

    prompt = input("User Prompt: ")

    decision, signals = await sdk.check_input(prompt)

    if decision == "BLOCK":
        print("❌ BLOCKED")
        print(signals)
        return

    response = agent.ask(prompt)

    print("\n🤖 Agent:", response)

asyncio.run(run())
