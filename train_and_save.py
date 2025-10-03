"""
Heart Disease Prediction Model Training Script
This script trains a classification model and saves it for deployment
"""

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    classification_report, 
    confusion_matrix, 
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare the heart disease dataset"""
    print("Loading data...")
    df = pd.read_csv('./data/heart-disease.csv')
    
    # Separate features and target
    X = df.drop('target', axis=1)
    y = df['target']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple classification models and return the best one"""
    
    print("\n" + "="*50)
    print("Training Classification Models")
    print("="*50)
    
    # Define models (FIXED: Using classifiers instead of regressors)
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'KNN': KNeighborsClassifier(),
        'Random Forest': RandomForestClassifier(random_state=42)
    }
    
    results = {}
    
    # Train and evaluate each model
    for name, model in models.items():
        print(f"\n--- {name} ---")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
        
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")
    
    return results

def hyperparameter_tuning(X_train, y_train):
    """Perform hyperparameter tuning on Random Forest"""
    
    print("\n" + "="*50)
    print("Hyperparameter Tuning with RandomizedSearchCV")
    print("="*50)
    
    # Define parameter grid
    rf_grid = {
        'n_estimators': np.arange(10, 1000, 50),
        'max_depth': [None, 3, 5, 10, 20],
        'min_samples_split': np.arange(2, 20, 2),
        'min_samples_leaf': np.arange(1, 20, 2)
    }
    
    # Perform randomized search
    np.random.seed(42)
    rs_rf = RandomizedSearchCV(
        RandomForestClassifier(random_state=42),
        param_distributions=rf_grid,
        cv=5,
        n_iter=20,
        verbose=1,
        random_state=42,
        n_jobs=-1
    )
    
    rs_rf.fit(X_train, y_train)
    
    print(f"\nBest Parameters: {rs_rf.best_params_}")
    print(f"Best CV Score: {rs_rf.best_score_:.4f}")
    
    return rs_rf.best_estimator_

def evaluate_final_model(model, X_test, y_test):
    """Evaluate the final model with comprehensive metrics"""
    
    print("\n" + "="*50)
    print("Final Model Evaluation")
    print("="*50)
    
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"\nTest Set Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"ROC AUC Score: {roc_auc:.4f}")
    
    print(f"\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc
    }

def save_model(model, filename='model.joblib'):
    """Save the trained model"""
    joblib.dump(model, filename)
    print(f"\n✓ Model saved as '{filename}'")

def main():
    """Main training pipeline"""
    
    print("="*50)
    print("Heart Disease Prediction Model Training")
    print("="*50)
    
    # Load and prepare data
    X_train, X_test, y_train, y_test = load_and_prepare_data()
    
    # Train baseline models
    results = train_models(X_train, X_test, y_train, y_test)
    
    # Hyperparameter tuning
    best_model = hyperparameter_tuning(X_train, y_train)
    
    # Final evaluation
    metrics = evaluate_final_model(best_model, X_test, y_test)
    
    # Save the model
    save_model(best_model, 'model.joblib')
    
    print("\n" + "="*50)
    print("Training Complete!")
    print("="*50)
    
    return best_model, metrics

if __name__ == "__main__":
    model, metrics = main()
