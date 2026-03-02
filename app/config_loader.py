import pandas as pd
import yaml
import pickle

def load_config(path="app_config.yaml"):
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data

def load_movies():
    config = load_config()
    path = config['datasets']['movie_data_path']
    df = pd.read_csv(path)
    return df

def load_page_config():
    config = load_config()
    page_configs = config['page_config']
    return page_configs

def load_model():
    config = load_config()
    model_path = config['model']['path']
    with open(model_path, "rb") as f:
        return pickle.load(f)

if __name__ == "__main__":
    print(load_config())
    print(load_page_config())