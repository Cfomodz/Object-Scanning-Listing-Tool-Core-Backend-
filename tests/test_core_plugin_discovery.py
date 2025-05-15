import os
import importlib
import pytest

def test_plugin_tests_run():
    plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        tests_path = os.path.join(plugin_path, 'tests')
        if os.path.isdir(tests_path):
            # Import all test modules in the plugin's tests dir
            for fname in os.listdir(tests_path):
                if fname.startswith('test_') and fname.endswith('.py'):
                    mod_name = f'plugins.{plugin_name}.tests.{fname[:-3]}'
                    importlib.import_module(mod_name)
    # Optionally, run pytest programmatically (not needed if using pytest CLI)
    # pytest.main([tests_path]) 