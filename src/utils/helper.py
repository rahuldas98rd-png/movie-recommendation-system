import pickle

def save_object(obj, path):
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print("✅ Model saved successfully")

def load_object(path):
    with open(path, "rb") as f:
        return pickle.load(f)
    print("✅ Model loaded successfully")