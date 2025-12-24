
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import xgboost as xgb
import os

def train_and_save_model():
    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"RandomForest Model accuracy: {accuracy:.2f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    with open("models/iris_model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("RandomForest Model saved to models/iris_model.pkl")
    return accuracy

def train_xgboost_model():
    # Load dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = xgb.XGBClassifier(
        n_estimators=100, 
        random_state=42, 
        eval_metric='logloss'
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"XGBoost Model accuracy: {accuracy:.2f}")
    
    # Save model
    os.makedirs("models", exist_ok=True)
    with open("models/iris_xgboost.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print("XGBoost Model saved to models/iris_xgboost.pkl")
    return accuracy

if __name__ == "__main__":
    train_and_save_model()
    train_xgboost_model()

