import ccxt.async_support as ccxt
from loguru import logger
import asyncio
from typing import Dict, Optional

class ExchangeManager:
    def __init__(self, config):
        self.config = config
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self.initialize_exchanges()
    
    def initialize_exchanges(self):
        """Initialize connection to all enabled exchanges"""
        for exchange_name in self.config.enabled_exchanges:
            try:
                # Get exchange class from ccxt
                exchange_class = getattr(ccxt, exchange_name)
                
                # Get API keys from config
                api_keys = self.config.get_api_keys(exchange_name)
                
                # Initialize exchange
                exchange = exchange_class({
                    'apiKey': api_keys.get('api_key'),
                    'secret': api_keys.get('api_secret'),
                    'enableRateLimit': True,
                })
                
                self.exchanges[exchange_name] = exchange
                logger.info(f"Initialized exchange: {exchange_name}")
                
            except Exception as e:
                logger.error(f"Failed to initialize exchange {exchange_name}: {str(e)}")
    
    async def get_ticker(self, exchange_name: str, symbol: str) -> Optional[Dict]:
        """Get current ticker data for a symbol from an exchange"""
        try:
            exchange = self.exchanges.get(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange {exchange_name} not initialized")
            
            ticker = await exchange.fetch_ticker(symbol)
            return {
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'timestamp': ticker['timestamp']
            }
        except Exception as e:
            logger.error(f"Error fetching ticker for {symbol} on {exchange_name}: {str(e)}")
            return None
    
    async def create_order(self, exchange_name: str, symbol: str, side: str, amount: float, price: float):
        """Create a new order on the specified exchange"""
        try:
            exchange = self.exchanges.get(exchange_name)
            if not exchange:
                raise ValueError(f"Exchange {exchange_name} not initialized")
            
            order = await exchange.create_limit_order(
                symbol=symbol,
                side=side,
                amount=amount,
                price=price
            )
            
            logger.info(f"Created {side} order on {exchange_name}: {order}")
            return order
            
        except Exception as e:
            logger.error(f"Error creating order on {exchange_name}: {str(e)}")
            return None
    
    async def close(self):
        """Close all exchange connections"""
        for exchange_name, exchange in self.exchanges.items():
            try:
                await exchange.close()
                logger.info(f"Closed connection to {exchange_name}")
            except Exception as e:
                logger.error(f"Error closing connection to {exchange_name}: {str(e)}")
