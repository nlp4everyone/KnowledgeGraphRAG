"""Configuration loader for TOML files."""
import logging
from typing import Dict, Any
import os, toml

class TomlConfigLoader:
    """Utility class to load and manage TOML configuration files."""
    
    def __init__(self):
        """Initialize the TOML config loader.

        Args:
        """
        # Get the project root directory (3 levels up from this file)
        self._dir_path = os.getcwd()
    
    def _load(self,
              toml_filename :str,
              config_dir :str = "config") -> Dict[str, Any]:
        """Load configuration from TOML file.
        
        Returns:
            Dictionary containing configuration values.
            
        Raises:
            FileNotFoundError: If config file doesn't exist.
            toml.TomlDecodeError: If config file is malformed.
        """
        # Define config path
        config_path = os.path.join(self._dir_path, config_dir,toml_filename)
        # Check existance
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Load the config
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = toml.load(f)
        
        return self._config
    
    def get_chunking_config(self) -> Dict[str, Any]:
        """Get chunking configuration section.

        Returns:
            Dictionary containing chunking parameters.
        """
        return self._load(toml_filename = "chunking_config.toml")

    def get_pdfparser_config(self):
        """Get pdf parser configuration section.
        Returns:
            Dictionary containing chunking parameters.
        """
        return self._load(toml_filename="pdfparser_config.toml")
    
    def get_llm_config(self):
        """Get LLM configuration section.
        Returns:
            Dictionary containing LLM parameters.
        """
        return self._load(toml_filename="llm_config.toml")
