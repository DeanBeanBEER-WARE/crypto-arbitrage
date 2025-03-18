from typing import List, Dict, Tuple
from loguru import logger
import asyncio
from datetime import datetime
import pandas as pd

class ArbitrageTrader:
    def __init__(self, config, exchange_manager):
        self.config = config
        self.exchange_manager = exchange_manager
        self.active_trades = 0
        self.daily_pl = 0.0
        self.trade_history = []
        self.start_time = datetime.now()
    
    async def find_arbitrage_opportunities(self) -> List[Dict]:
        """Find arbitrage opportunities across exchanges"""
        opportunities = []
        
        for symbol in self.config.trading_pairs:
            # Get tickers from all exchanges
            tickers = {}
            for exchange in self.config.enabled_exchanges:
                ticker = await self.exchange_manager.get_ticker(exchange, symbol)
                if ticker:
                    tickers[exchange] = ticker
            
            # Find arbitrage opportunities
            for buy_ex in tickers:
                for sell_ex in tickers:
                    if buy_ex != sell_ex:
                        buy_price = tickers[buy_ex]['ask']
                        sell_price = tickers[sell_ex]['bid']
                        
                        # Calculate profit percentage
                        profit_percent = ((sell_price - buy_price) / buy_price) * 100
                        
                        if profit_percent > self.config.min_profit_percent:
                            opportunities.append({
                                'symbol': symbol,
                                'buy_exchange': buy_ex,
                                'sell_exchange': sell_ex,
                                'buy_price': buy_price,
                                'sell_price': sell_price,
                                'profit_percent': profit_percent,
                                'timestamp': datetime.now()
                            })
        
        return opportunities

    async def execute_arbitrage(self, opportunity: Dict) -> bool:
        """Execute arbitrage trades for a given opportunity"""
        if self.active_trades >= self.config.max_simultaneous_trades:
            logger.warning("Maximum simultaneous trades reached")
            return False

        try:
            # Place buy order
            buy_order = await self.exchange_manager.create_order(
                exchange_name=opportunity['buy_exchange'],
                symbol=opportunity['symbol'],
                side='buy',
                amount=self.config.trade_amount,
                price=opportunity['buy_price']
            )

            if not buy_order:
                logger.error("Failed to place buy order")
                return False

            # Place sell order
            sell_order = await self.exchange_manager.create_order(
                exchange_name=opportunity['sell_exchange'],
                symbol=opportunity['symbol'],
                side='sell',
                amount=self.config.trade_amount,
                price=opportunity['sell_price']
            )

            if not sell_order:
                logger.error("Failed to place sell order")
                # TODO: Implement order cancellation for buy order
                return False

            # Record the trade
            trade_record = {
                **opportunity,
                'buy_order_id': buy_order['id'],
                'sell_order_id': sell_order['id'],
                'amount': self.config.trade_amount,
                'profit': (opportunity['sell_price'] - opportunity['buy_price']) * self.config.trade_amount
            }
            self.trade_history.append(trade_record)
            
            # Update daily P&L
            self.daily_pl += trade_record['profit']
            self.active_trades += 1

            logger.info(f"Successfully executed arbitrage trade: {trade_record}")
            return True

        except Exception as e:
            logger.error(f"Error executing arbitrage trade: {str(e)}")
            return False

    def check_risk_limits(self) -> bool:
        """Check if risk limits have been exceeded"""
        # Check daily loss limit
        if self.daily_pl < -(self.config.trade_amount * self.config.daily_loss_limit_percent / 100):
            logger.warning("Daily loss limit exceeded")
            return False
        
        # Check stop loss
        if self.daily_pl < -(self.config.trade_amount * self.config.stop_loss_percent / 100):
            logger.warning("Stop loss triggered")
            return False
        
        return True

    def generate_trade_report(self) -> pd.DataFrame:
        """Generate a report of trading activity"""
        if not self.trade_history:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.trade_history)
        df['datetime'] = pd.to_datetime(df['timestamp'])
        df.set_index('datetime', inplace=True)
        
        return df

    async def run(self):
        """Main arbitrage trading loop"""
        logger.info("Starting arbitrage trading...")
        
        while True:
            try:
                # Check risk limits
                if not self.check_risk_limits():
                    logger.warning("Risk limits exceeded. Stopping trading.")
                    break

                # Find opportunities
                opportunities = await self.find_arbitrage_opportunities()
                
                for opportunity in opportunities:
                    if self.active_trades < self.config.max_simultaneous_trades:
                        await self.execute_arbitrage(opportunity)
                    
                # Wait for polling interval
                await asyncio.sleep(self.config.polling_interval)
                
            except Exception as e:
                logger.error(f"Error in arbitrage loop: {str(e)}")
                await asyncio.sleep(self.config.polling_interval)
