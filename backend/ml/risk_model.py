import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Features for risk prediction
FEATURES = [
    'commit_count',
    'lines_added',
    'lines_deleted',
    'files_modified',
    'code_churn',
    'bug_count',
    'modification_frequency'
]


def generate_training_data() -> pd.DataFrame:
    """Generate synthetic training data for risk model"""
    np.random.seed(42)
    n_samples = 500
    
    data = {
        'commit_count': np.random.randint(1, 100, n_samples),
        'lines_added': np.random.randint(10, 1000, n_samples),
        'lines_deleted': np.random.randint(5, 800, n_samples),
        'files_modified': np.random.randint(1, 30, n_samples),
        'bug_count': np.random.randint(0, 20, n_samples),
    }
    
    data['code_churn'] = data['lines_added'] + data['lines_deleted']
    data['modification_frequency'] = np.random.uniform(0.1, 10, n_samples)
    
    df = pd.DataFrame(data)
    
    # Calculate risk labels based on rules
    def calculate_risk(row):
        score = 0
        score += min(30, row['commit_count'] * 0.3)
        score += min(20, row['code_churn'] / 50)
        score += min(25, row['files_modified'] * 0.8)
        score += min(25, row['bug_count'] * 2)
        
        if score < 30:
            return 'Low'
        elif score < 60:
            return 'Medium'
        else:
            return 'High'
    
    df['risk_level'] = df.apply(calculate_risk, axis=1)
    
    return df


def train_model() -> tuple:
    """Train the risk prediction model"""
    # Generate training data
    df = generate_training_data()
    
    X = df[FEATURES]
    y = df['risk_level']
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_scaled, y)
    
    return model, scaler


def calculate_risk_score(proba: np.ndarray, classes: np.ndarray) -> float:
    """Calculate risk score (0-100) from probabilities"""
    # Weight the probabilities: High=100, Medium=50, Low=0
    weights = {'High': 100, 'Medium': 50, 'Low': 0}
    score = 0
    for i, cls in enumerate(classes):
        score += proba[i] * weights[cls]
    return round(score, 2)


def predict_risk(
    commit_count: int,
    lines_added: int,
    lines_deleted: int,
    files_modified: int,
    bug_count: int,
    modification_frequency: float = 1.0
) -> dict:
    """Predict risk for a module"""
    # Try to load existing model, otherwise train new one
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
    
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
    else:
        model, scaler = train_model()
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
    
    # Prepare input
    code_churn = lines_added + lines_deleted
    X = np.array([[
        commit_count,
        lines_added,
        lines_deleted,
        files_modified,
        code_churn,
        bug_count,
        modification_frequency
    ]])
    
    X_scaled = scaler.transform(X)
    
    # Predict
    risk_level = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]
    classes = model.classes_
    risk_score = calculate_risk_score(proba, classes)
    
    # Generate factors and recommendations
    factors = []
    if commit_count > 50:
        factors.append("High commit count")
    if code_churn > 500:
        factors.append("High code churn")
    if files_modified > 10:
        factors.append("Many files modified")
    if bug_count > 5:
        factors.append("High bug count")
    if modification_frequency > 5:
        factors.append("High modification frequency")
    
    if not factors:
        factors.append("No significant risk factors detected")
    
    # Generate recommendation
    if risk_level == 'High':
        recommendation = "Immediate attention required. Consider code review and additional testing."
    elif risk_level == 'Medium':
        recommendation = "Monitor closely. Implement regular code reviews and regression testing."
    else:
        recommendation = "Module appears stable. Continue normal maintenance."
    
    # Add specific recommendations based on factors
    if "High modification frequency" in factors:
        recommendation += " Consider breaking down this module into smaller components."
    if "High bug count" in factors:
        recommendation += " Increase test coverage and address technical debt."
    
    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "factors": factors,
        "recommendation": recommendation
    }


# Initialize model on module load
if __name__ != "__main__":
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.joblib')
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        model, scaler = train_model()
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        print("Model trained and saved successfully")
