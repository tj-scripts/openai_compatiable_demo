"""
Configuration management module.

Author: tj-scripts
Email: tangj1984@gmail.com
Date: 2024-03-21
"""

import tomli
from pathlib import Path
from typing import Dict, Any, Optional, Union

class ConfigError(Exception):
    """Configuration error base class"""
    pass

class ConfigFileNotFoundError(ConfigError):
    """Configuration file not found error"""
    pass

class ConfigLoadError(ConfigError):
    """Configuration load error"""
    pass

class Config:
    """Configuration management class"""
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to the configuration file
            
        Raises:
            ConfigFileNotFoundError: If config file is not found
            ConfigLoadError: If config file cannot be loaded
        """
        self.config: Dict[str, Any] = {}
        self.config_path = Path(config_path) if config_path else Path("config.toml")
        self._load_config()
    
    def _load_config(self) -> None:
        """
        Load configuration from file.
        
        Raises:
            ConfigFileNotFoundError: If config file is not found
            ConfigLoadError: If config file cannot be loaded
        """
        if not self.config_path.exists():
            raise ConfigFileNotFoundError(
                f"Config file not found at {self.config_path}. "
                "Please copy config.toml.example to config.toml and configure it."
            )
        
        try:
            with open(self.config_path, "rb") as f:
                self.config = tomli.load(f)
        except tomli.TOMLDecodeError as e:
            raise ConfigLoadError(f"Failed to parse config file: {str(e)}")
        except Exception as e:
            raise ConfigLoadError(f"Failed to load config file: {str(e)}")
        
        # Validate required sections
        if "api" not in self.config:
            raise ConfigLoadError("Missing required section: [api]")
        if "openai" not in self.config["api"]:
            raise ConfigLoadError("Missing required section: [api.openai]")
        if "logging" not in self.config:
            raise ConfigLoadError("Missing required section: [logging]")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
            
        Returns:
            Configuration value
        """
        return self.config.get(section, {}).get(key, default)
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get an entire configuration section.
        
        Args:
            section: Configuration section
            
        Returns:
            Configuration section dictionary
        """
        return self.config.get(section, {})

# Create global config instance
config = Config() 