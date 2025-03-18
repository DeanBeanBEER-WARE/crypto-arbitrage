import os
import yaml
from dotenv import load_dotenv

class Config:
    def __init__(self, config_path="config.yaml"):
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configuration from yaml file
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Initialize exchange API keys from environment variables
        self.api_keys = {}
        for exchange in self.config['exchanges']:
            name = exchange['name'].upper()
            self.api_keys[name] = {
                'api_key': os.getenv(f'{name}_API_KEY'),
                'api_secret': os.getenv(f'{name}_API_SECRET')
            }
    
    @property
    def enabled_exchanges(self):
        return [ex['name'] for ex in self.config['exchanges'] if ex['enabled']]
    
    @property
    def trading_pairs(self):
        return self.config['trading_pairs']
    
    @property
    def min_profit_percent(self):
        return self.config['min_profit_percent']
    
    @property
    def trade_amount(self):
        return self.config['trade_amount']
    
    @property
    def max_simultaneous_trades(self):
        return self.config['max_simultaneous_trades']
    
    @property
    def polling_interval(self):
        return self.config['polling_interval_ms'] / 1000  # Convert to seconds
    
    @property
    def stop_loss_percent(self):
        return self.config['stop_loss_percent']
    
    def get_api_keys(self, exchange_name):
        return self.api_keys.get(exchange_name.upper(), {})
