from dotenv import load_dotenv
import os
from typing import Dict, Type

def load_core_env():
    """
    Load the core .env file from the project root.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(root_dir, '.env')
    load_dotenv(dotenv_path=env_path)

class PluginRegistry:
    """
    Registry for item scanner and listing builder plugins.
    """
    _scanners: Dict[str, Type] = {}
    _builders: Dict[str, Type] = {}

    @classmethod
    def register_scanner(cls, type_name: str, scanner_cls: Type):
        """
        Register a scanner plugin for a given type.
        """
        cls._scanners[type_name] = scanner_cls

    @classmethod
    def register_builder(cls, type_name: str, builder_cls: Type):
        """
        Register a builder plugin for a given type.
        """
        cls._builders[type_name] = builder_cls

    @classmethod
    def get_scanner(cls, type_name: str) -> Type:
        """
        Retrieve the scanner class for a given type.
        """
        return cls._scanners[type_name]

    @classmethod
    def get_builder(cls, type_name: str) -> Type:
        """
        Retrieve the builder class for a given type.
        """
        return cls._builders[type_name]

    @classmethod
    def available_types(cls) -> Dict[str, Dict[str, Type]]:
        """
        List all registered types and their associated scanner and builder classes.
        """
        return {
            type_name: {
                'scanner': cls._scanners.get(type_name),
                'builder': cls._builders.get(type_name)
            }
            for type_name in set(cls._scanners) | set(cls._builders)
        } 