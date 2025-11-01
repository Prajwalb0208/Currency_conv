# Multi-Tool Claude CLI

A command-line application that leverages Claude AI with custom tool calling capabilities to perform currency conversions and fetch Wikipedia article introductions.

## Features

- **Currency Conversion**: Convert between different currencies using real-time exchange rates
- **Multi-step Conversions**: Chain multiple currency conversions (e.g., USD → INR → AUD)
- **Wikipedia Extractor**: Fetch introductory paragraphs from Wikipedia articles
- **Intelligent Tool Selection**: Claude automatically determines which tool to use based on your query

## Prerequisites

- Python 3.7+
- Anthropic API key
- ExchangeRatesAPI key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Currency
```

2. Install required dependencies:
```bash
pip install anthropic requests beautifulsoup4 python-dotenv
```

3. Create a `.env` file in the project root:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
EXCHANGERATES_API_KEY=your_exchangerates_api_key_here
```

## API Keys

### Anthropic API Key
1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Navigate to API Keys section
3. Generate a new API key

### ExchangeRatesAPI Key
1. Sign up at [ExchangeRatesAPI.io](https://exchangeratesapi.io/)
2. Get your free API access key from the dashboard

## Usage

Run the application:
```bash
python main.py
```

### Example Queries

**Currency Conversions:**
```
convert 100 USD to EUR
1000 INR in AUD
convert 500 GBP to INR to USD
what is 250 EUR in JPY
```

**Wikipedia Queries:**
```
https://en.wikipedia.org/wiki/Python_(programming_language)
tell me about https://en.wikipedia.org/wiki/Machine_learning
```

**Exit:**
```
exit
quit
```

## Project Structure

```
Currency/
├── main.py                          # Main application entry point
├── Exchange_rate_tool/
│   └── exchange_rate.py             # Currency conversion tool
├── Wikipedia_intro_tool/
│   └── wikipedia_intro_tool.py      # Wikipedia extractor tool
├── .env                             # Environment variables (not in repo)
└── README.md                        # This file
```

## How It Works

1. **User Input**: You enter a question or request
2. **Claude Processing**: Claude AI analyzes your query and determines which tool(s) to use
3. **Tool Execution**: The appropriate tool(s) are called with the extracted parameters
4. **Response**: Claude formulates a natural language response based on the tool results

### Currency Conversion Tool
- Uses ExchangeRatesAPI.io for real-time exchange rates
- Supports 170+ currencies
- Handles single and multi-step conversions
- Returns conversion rate, result, and date

### Wikipedia Intro Tool
- Scrapes Wikipedia pages using BeautifulSoup
- Extracts the first substantive introductory paragraph
- Returns the original text without modification

## Limitations

- ExchangeRatesAPI free tier has rate limits
- Wikipedia tool only extracts the introduction paragraph
- Currency conversions use latest rates (historical rates parameter exists but may require paid API tier)

## Troubleshooting

**"API key not found" error:**
- Ensure your `.env` file exists and contains both API keys
- Check that the `.env` file is in the same directory as `main.py`

**Currency not supported:**
- Verify the currency code is valid (use ISO 4217 codes like USD, EUR, INR)
- Check ExchangeRatesAPI documentation for supported currencies

**Wikipedia extraction fails:**
- Ensure the URL is a valid Wikipedia article link
- Check your internet connection

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.
