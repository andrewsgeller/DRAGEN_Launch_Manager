# config_loader.py
import yaml
import os

def load_config(pipeline_name):
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Adjust based on actual directory structure
    config_path = os.path.join(base_dir, 'params', f'{pipeline_name}_config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config