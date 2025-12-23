"""
Tests for model training and evaluation
"""
import pytest
import pickle
import os
import sys
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

# Add src directory to path to import train_model
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from train_model import train_and_save_model


class TestModelTraining:
    """Test suite for model training"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and cleanup for each test"""
        # Setup: Ensure models directory exists
        os.makedirs("models", exist_ok=True)
        
        yield

    
    def test_train_model_success(self):
        """Test training model successfully"""
        accuracy = train_and_save_model()
        
        # Test accuracy is returned
        assert accuracy is not None
        assert isinstance(accuracy, (float, np.floating))
        assert 0 <= accuracy <= 1
    
    def test_model_accuracy_threshold(self):
        """Test model achieves minimum accuracy"""
        accuracy = train_and_save_model()
        
        # With Iris dataset and Random Forest, accuracy should be >= 90%
        assert accuracy >= 0.90, f"Model accuracy {accuracy:.2%} is below 90% threshold"
    
    def test_model_file_created(self):
        """Test model file is created and saved correctly"""
        train_and_save_model()
        
        # Test file exists
        assert os.path.exists("models/iris_model.pkl")
        
        # Test file is not empty
        assert os.path.getsize("models/iris_model.pkl") > 0
    
    def test_model_can_be_loaded(self):
        """Test model can be loaded from file"""
        train_and_save_model()
        
        # Load model
        with open("models/iris_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Test model is RandomForestClassifier
        assert isinstance(model, RandomForestClassifier)
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')
    
    def test_loaded_model_can_predict(self):
        """Test model after loading can predict"""
        train_and_save_model()
        
        # Load model
        with open("models/iris_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Test prediction with sample data
        iris = load_iris()
        X_sample = iris.data[:5]
        
        predictions = model.predict(X_sample)
        probabilities = model.predict_proba(X_sample)
        
        # Test output
        assert len(predictions) == 5
        assert all(pred in [0, 1, 2] for pred in predictions)
        assert probabilities.shape == (5, 3)
        assert all(np.isclose(prob.sum(), 1.0) for prob in probabilities)
    
    def test_model_parameters(self):
        """Test model is trained with correct parameters"""
        train_and_save_model()
        
        # Load model
        with open("models/iris_model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Test parameters
        assert model.n_estimators == 100
        assert model.random_state == 42
        assert model.n_classes_ == 3
        assert model.n_features_in_ == 4  # Iris has 4 features

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

