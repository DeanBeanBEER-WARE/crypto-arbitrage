import asyncio
from loguru import logger
import sys
import os
from datetime import datetime

from config import Config
from exchange import ExchangeManager
from arbitrage import ArbitrageTrader

def setup_logging(config):
    """Configure logging settings"""
    # Remove default logger
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        level=config.config['logging']['level'],
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file handler
    log_file = config.config['logging']['file']
    logger.add(
        log_file,
        rotation="1 day",
        retention="7 days",
        level=config.config['logging']['level']
    )

async def shutdown(exchange_manager):
    """Gracefully shutdown the application"""
    logger.info("Shutting down...")
    await exchange_manager.close()

async def main():
    try:
        # Load configuration
        config = Config()
        
        # Setup logging
        setup_logging(config)
        
        logger.info("Starting crypto arbitrage bot...")
        
        # Initialize exchange manager
        exchange_manager = ExchangeManager(config)
        
        # Initialize arbitrage trader
        trader = ArbitrageTrader(config, exchange_manager)
        
        # Handle graceful shutdown
        try:
            await trader.run()
        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        finally:
            await shutdown(exchange_manager)
            
        # Generate final report
        report = trader.generate_trade_report()
        if not report.empty:
            # Save report to CSV
            report_file = f"trade_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            report.to_csv(report_file)
            logger.info(f"Trade report saved to {report_file}")
            
            # Print summary
            total_profit = report['profit'].sum()
            total_trades = len(report)
            successful_trades = len(report[report['profit'] > 0])
            
            logger.info(f"""
Trading Summary:
---------------
Total Trades: {total_trades}
Successful Trades: {successful_trades}
Success Rate: {(successful_trades/total_trades)*100:.2f}%
Total Profit: {total_profit:.8f}
            """)
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Create event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
