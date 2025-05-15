# main.py (refactored for plugin-based architecture)
from core.config import load_core_env
from core.plugin import PluginRegistry
import sys

# Load core environment variables
load_core_env()

# Example: CLI entrypoint for processing items with a specified plugin
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <item_type> [args...]")
        sys.exit(1)
    item_type = sys.argv[1]
    plugin = PluginRegistry.available_types().get(item_type)
    if not plugin:
        print(f"No plugin registered for type '{item_type}'")
        sys.exit(1)
    # Further CLI logic would go here (e.g., process images, create listings, etc.)
    print(f"Plugin for '{item_type}' loaded: {plugin}")

if __name__ == "__main__":
    main()
