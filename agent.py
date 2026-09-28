import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from agent_framework import Agent, Content, Message
from agent_framework.foundry import FoundryChatClient, FoundryChatOptions
from azure.identity import AzureCliCredential


# ---------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------

load_dotenv()

FOUNDRY_PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

MODEL_DEPLOYMENT = os.getenv(
    "FOUNDRY_MODEL",
    "gpt-5.6-sol-1",
)

VECTOR_STORE_ID = os.environ["VECTOR_STORE_ID"]


# ---------------------------------------------------------
# 2. Load stable prompt content from project files
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

AGENT_INSTRUCTIONS = (
    BASE_DIR / "agent-instructions.md"
).read_text(encoding="utf-8")

RISK_ADVISORY_METHODOLOGY = (
    BASE_DIR / "risk-advisory-methodology.md"
).read_text(encoding="utf-8")


# Combine both files into ONE stable cached prefix.
#
# As long as neither file changes, this content remains
# identical across requests and can be reused from cache.

STABLE_CONTEXT = f"""
# Agent Instructions

{AGENT_INSTRUCTIONS}

# Risk Advisory Methodology

{RISK_ADVISORY_METHODOLOGY}
""".strip()


# ---------------------------------------------------------
# 3. Create Microsoft Foundry model client
# ---------------------------------------------------------

client = FoundryChatClient[FoundryChatOptions](
    project_endpoint=FOUNDRY_PROJECT_ENDPOINT,
    model=MODEL_DEPLOYMENT,
    credential=AzureCliCredential(),
)


# ---------------------------------------------------------
# 4. Configure File Search
# ---------------------------------------------------------

file_search = client.get_file_search_tool(
    vector_store_ids=[VECTOR_STORE_ID]
)


# ---------------------------------------------------------
# 5. Create the Risk Advisor agent
# ---------------------------------------------------------

# We intentionally do NOT use Agent(instructions=...)
# here.
#
# Instead, the instructions and methodology are supplied
# as a system Message below. That lets us attach an explicit
# prompt-cache breakpoint to the stable content.

agent = Agent[FoundryChatOptions](
    client=client,
    name="risk-advisor-copilot",
    tools=[file_search],
)


# ---------------------------------------------------------
# 6. Prompt caching configuration
# ---------------------------------------------------------

CACHE_OPTIONS: FoundryChatOptions = {
    # Same key for all requests that use this exact
    # instructions + methodology prefix.
    "prompt_cache_key": "risk-advisor-methodology-v1",

    # Only cache where WE explicitly place a breakpoint.
    "prompt_cache_options": {
        "mode": "explicit",
        "ttl": "30m",
    },
}


# ---------------------------------------------------------
# 7. Build each request
# ---------------------------------------------------------

def build_messages(question: str) -> list[Message]:
    """
    Stable:
        Agent instructions
        Risk-advisory methodology

    Dynamic:
        Client profile retrieved through File Search
        User question
    """

    return [
        Message(
            role="system",
            contents=[
                Content.from_text(
                    STABLE_CONTEXT,

                    # Everything through this Content block
                    # becomes the reusable cached prefix.
                    additional_properties={
                        "prompt_cache_breakpoint": {
                            "mode": "explicit"
                        }
                    },
                )
            ],
        ),
        Message(
            role="user",
            contents=[
                Content.from_text(question)
            ],
        ),
    ]


# ---------------------------------------------------------
# 8. Run one question
# ---------------------------------------------------------

async def run_question(
    question: str,
    options: FoundryChatOptions | None = None,
) -> tuple[str, dict[str, int]]:
    response = await agent.run(
        build_messages(question),
        options=options or CACHE_OPTIONS,
    )

    usage = {
        key: int(value)
        for key, value in (response.usage_details or {}).items()
        if isinstance(value, (int, float))
    }
    return response.text, usage


async def ask(question: str) -> None:
    print("\n" + "=" * 70)
    print(f"USER: {question}")
    print("=" * 70)

    response_text, usage = await run_question(question)

    print(f"\nAGENT:\n{response_text}")

    # Agent Framework normalizes prompt-cache usage into
    # these fields when the provider returns them.
    cache_write = usage.get(
        "cache_creation_input_token_count",
        0,
    )

    cache_read = usage.get(
        "cache_read_input_token_count",
        0,
    )

    print("\n--- Prompt Cache Usage ---")
    print(f"Cache write tokens: {cache_write}")
    print(f"Cache read tokens:  {cache_read}")


# ---------------------------------------------------------
# 9. Demo
# ---------------------------------------------------------

async def main() -> None:

    questions = [
        (
            "Summarize the top three enterprise risks for "
            "Tailspin Toys and cite the supporting details "
            "from the client profile."
        ),
        (
            "What risk interdependencies should an advisor "
            "be most concerned about for Tailspin Toys?"
        ),
        (
            "What questions should the advisor ask Tailspin "
            "Toys during the next client risk discussion?"
        ),
    ]

    for question in questions:
        await ask(question)

        # A newly created cache entry can take a moment to
        # become readable. Microsoft's Agent Framework sample
        # uses a short pause between requests for this reason.
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())