from typing import Dict, Type
from core.base import ItemScanner, ListingBuilder

class PluginRegistry:
    """
    Registry for item scanner and listing builder plugins.
    """
    _scanners: Dict[str, Type[ItemScanner]] = {}
    _builders: Dict[str, Type[ListingBuilder]] = {}

    @classmethod
    def register_scanner(cls, type_name: str, scanner_cls: Type[ItemScanner]):
        """
        Register an ItemScanner plugin for a given type.
        """
        cls._scanners[type_name] = scanner_cls

    @classmethod
    def register_builder(cls, type_name: str, builder_cls: Type[ListingBuilder]):
        """
        Register a ListingBuilder plugin for a given type.
        """
        cls._builders[type_name] = builder_cls

    @classmethod
    def get_scanner(cls, type_name: str) -> Type[ItemScanner]:
        """
        Retrieve the ItemScanner class for a given type.
        """
        return cls._scanners[type_name]

    @classmethod
    def get_builder(cls, type_name: str) -> Type[ListingBuilder]:
        """
        Retrieve the ListingBuilder class for a given type.
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