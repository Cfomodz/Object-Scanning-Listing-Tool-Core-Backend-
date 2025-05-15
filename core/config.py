from dotenv import load_dotenv
import os

def load_core_env():
    """
    Load the core .env file from the project root.
    """
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_path = os.path.join(root_dir, '.env')
    load_dotenv(dotenv_path=env_path) 