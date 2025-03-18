# Cryptocurrency Arbitrage Trading Bot

A high-frequency cryptocurrency arbitrage trading bot that monitors price differences across multiple exchanges and automatically executes trades when profitable opportunities are detected.

## Features

- Real-time price monitoring across multiple exchanges (Binance, Kraken, Coinbase)
- Automated arbitrage opportunity detection
- Configurable trading parameters
- Risk management with stop-loss and daily loss limits
- Detailed trade logging and reporting
- Asynchronous execution for optimal performance
- Secure API key management

## Prerequisites

- Python 3.8 or higher
- Valid API keys for the exchanges you want to trade on

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crypto-arbitrage
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your exchange API keys:
```
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_api_secret
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_API_SECRET=your_kraken_api_secret
COINBASE_API_KEY=your_coinbase_api_key
COINBASE_API_SECRET=your_coinbase_api_secret
```

## Configuration

The bot's behavior can be configured through the `config.yaml` file. Key parameters include:

- Trading pairs
- Minimum profit percentage
- Trade amount
- Maximum simultaneous trades
- Stop loss percentage
- Polling interval
- Risk management parameters

Example configuration:
```yaml
trading_pairs:
  - "BTC/USDT"
  - "ETH/USDT"

min_profit_percent: 0.5
trade_amount: 0.01
max_simultaneous_trades: 3
```

## Usage

1. Review and adjust the configuration in `config.yaml` according to your trading strategy.

2. Start the bot:
```bash
python src/main.py
```

3. The bot will:
   - Initialize connections to configured exchanges
   - Monitor prices in real-time
   - Execute trades when profitable opportunities are found
   - Log all activities and generate trade reports

4. To stop the bot, press Ctrl+C. It will gracefully shutdown and generate a final trade report.

## Trade Reports

The bot generates detailed CSV reports of all trading activity, including:
- Buy/Sell exchanges
- Trading pairs
- Prices
- Profit/Loss
- Timestamps

Reports are saved as `trade_report_YYYYMMDD_HHMMSS.csv` in the project directory.

## Risk Management

The bot includes several risk management features:
- Maximum simultaneous trades limit
- Daily loss limit
- Stop-loss trigger
- Maximum trade amount per pair

Configure these parameters in `config.yaml` according to your risk tolerance.

## Logging

Detailed logs are maintained in `arbitrage.log`, including:
- Trade executions
- Errors and warnings
- System events
- Performance metrics

## Security Considerations

- Never commit your `.env` file containing API keys
- Use API keys with trading permissions only (no withdrawal rights)
- Monitor the bot's activity regularly
- Start with small trade amounts while testing

## Disclaimer

This software is for educational purposes only. Cryptocurrency trading carries significant risks. Use at your own risk. The authors are not responsible for any financial losses incurred while using this software.

## License

MIT License. See LICENSE file for details.
