import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE = "http://api.exchangeratesapi.io/v1/latest"
API_KEY = os.getenv("EXCHANGERATES_API_KEY")

def get_latest_rates():
    params = {"access_key": API_KEY}
    response = requests.get(API_BASE, params=params)
    data = response.json()
    if not data.get("success", False):
        return {"error": data.get("error", "Unknown error")}
    return {
        "success": True,
        "rates": data.get("rates"),
        "base": data.get("base", "EUR"),
        "date": data.get("date")
    }

def convert_currency(from_currency, to_currency, amount, date=None):
    rates_data = get_latest_rates()
    if "error" in rates_data:
        return {"error": rates_data["error"], "from": from_currency, "to": to_currency, "amount": amount}

    rates = rates_data["rates"]
    if from_currency not in rates or to_currency not in rates:
        return {"error": f"Currency {from_currency} or {to_currency} not supported", "from": from_currency, "to": to_currency, "amount": amount}

    rate = rates[to_currency] / rates[from_currency]
    result = float(amount) * rate

    return {
        "from": from_currency,
        "to": to_currency,
        "amount": amount,
        "result": result,
        "rate": rate,
        "date": rates_data["date"]
    }

exchange_rate_tool_schema = {
    "name": "convert_currency",
    "description": ( "Convert any amount from one currency to another using Exchangerates API. "
        "Trigger this tool for ANY query about currency conversion, e.g. 'convert', 'in', '=', currency pairs (like USD to INR, 200 USD in INR, INR to EUR), or any question about exchange rate or conversion. "
        "This tool only handles one-step conversion per call."
        "Call this tool multiple times in a loop in case of chain convertion requests."),
    "input_schema": {
        "type": "object",
        "properties": {
            "from_currency": {"type": "string", "description": "Source currency code (e.g. 'INR')"},
            "to_currency": {"type": "string", "description": "Target currency code (e.g. 'USD')"},
            "amount": {"type": "number", "description": "Amount to convert"},
            "date": {"type": "string", "description": "Optional date for historical rates (YYYY-MM-DD)"}
        },
        "required": ["from_currency", "to_currency", "amount"]
    }
}
