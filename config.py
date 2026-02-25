"""
ASDTS Configuration Management
Centralized configuration with environment variables and defaults
"""
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    credential_path: str = os.getenv("FIREBASE_CREDENTIAL_PATH", "firebase-credentials.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "asdts-system")
    collections: Dict[str, str] = None
    
    def __post_init__(self):
        if self.collections is None:
            self.collections = {
                "trades": "trades",
                "sentiment": "sentiment_data",
                "strategies": "trading_strategies",
                "system_logs": "system_logs",
                "market_data": "market_data"
            }

@dataclass
class TradingConfig:
    """Trading configuration"""
    exchange: str = os.getenv("TRADING_EXCHANGE", "binance")
    testnet: bool = os.getenv("TRADING_TESTNET", "True").lower() == "true"
    default_symbol: str = os.getenv("DEFAULT_SYMBOL", "BTC/USDT")
    max_position_size: float = float(os.getenv("MAX_POSITION_SIZE", "0.1"))
    stop_loss_pct: float = float(os.getenv("STOP_LOSS_PCT", "0.02"))
    take_profit_pct: float = float(os.getenv("TAKE_PROFIT_PCT", "0.03"))
    sentiment_threshold: float = float(os.getenv("SENTIMENT_THRESHOLD", "0.3"))

@dataclass
class SentimentConfig:
    """Sentiment analysis configuration"""
    sources: list = None
    update_interval: int = int(os.getenv("SENTIMENT_UPDATE_INTERVAL", "300"))
    vader_threshold: float = float(os.getenv("VADER_THRESHOLD", "0.05"))
    
    def __post_init__(self):
        if self.sources is None:
            self.sources = ["news", "twitter", "reddit"]

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    file_path: str = os.getenv("LOG_FILE", "asdts.log")
    max_size_mb: int = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))

class ASDTSConfig:
    """Main configuration class"""
    
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.sentiment = SentimentConfig()
        self.logging = LoggingConfig()
        
        # Validate critical configurations
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate critical configuration values"""
        if not os.path.exists(self.firebase.credential_path):
            logging.warning(f"Firebase credential file not found: {self.firebase.credential_path}")
        
        if self.trading.max_position_size <= 0:
            raise ValueError("MAX_POSITION_SIZE must be positive")
        
        if self.trading.stop_loss_pct <= 0:
            raise ValueError("STOP_LOSS_PCT must be positive")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for logging"""
        return {
            "firebase": {
                "project_id": self.firebase.project_id,
                "collections": self.firebase.collections
            },
            "trading": {
                "exchange": self.trading.exchange,
                "testnet": self.trading.testnet,
                "default_symbol": self.trading.default_symbol
            },
            "sentiment": {
                "sources": self.sentiment.sources,
                "update_interval": self.sentiment.update_interval
            }
        }

# Global config instance
config = ASDTSConfig()