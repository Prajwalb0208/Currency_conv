from anthropic import Anthropic
from Exchange_rate_tool.exchange_rate import convert_currency, exchange_rate_tool_schema
from Wikipedia_intro_tool.wikipedia_intro_tool import fetch_wikipedia_intro, wiki_intro_tool_schema
import os
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL_NAME = "claude-sonnet-4-5"

tools = [exchange_rate_tool_schema, wiki_intro_tool_schema]

def process_tool_call(tool_name, tool_input):
    if tool_name == "convert_currency":
        return convert_currency(
            tool_input["from_currency"],
            tool_input["to_currency"],
            tool_input["amount"],
            tool_input.get("date")
        )
    elif tool_name == "wiki_intro_extractor":
        return fetch_wikipedia_intro(tool_input["url"])
    return {"error": "Unknown tool"}

def get_system_prompt():
    return (
        "You are a toolcalling assistant. "
        "Always use convert_currency for ANY currency conversion questions (amount, source, target, date), including single or multi-step. "
        "Do NOT use web search for currency/conversion queries if the tool is available. "
        "For Wikipedia introductions, use wiki_intro_extractor. "
        "Only use web search if NO tool matches the request."
    )

def chat_with_claude(user_message):
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": user_message}
    ]
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=1024,
        system=get_system_prompt()
        messages=messages,
        tools=tools,
    )

    if message.stop_reason == "tool_use":
        tool_uses = [block for block in message.content if block.type == "tool_use"]
        tool_results = []
        for tool_use in tool_uses:
            tool_name = tool_use.name
            tool_input = tool_use.input
            tool_result = process_tool_call(tool_name, tool_input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": str(tool_result),
            })

        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=1024,
            messages=messages +
            [{"role": "assistant", "content": message.content}] +
            [{"role": "user", "content": tool_results}],
            tools=tools,
        )
        final_response = next((block.text for block in response.content if hasattr(block, "text")), None)
        print("\nFinal Response:", final_response)
        return final_response
    else:
        content = next((block.text for block in message.content if hasattr(block, "text")), None)
        print("\nResponse:", content)
        return content

if __name__ == "__main__":
    print("Multi-Tool Claude CLI (Currency + Wikipedia)")
    query = input("Enter your question (currency or wikipedia): ")
    chat_with_claude(query)
