from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import pandas as pd
import numpy as np
import pickle
import xgboost as xgb
import shap
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Set up Etherscan API
os.environ["ETHERSCAN_API_KEY"] = "SP28UE81KFS6CVMWM7BSM28TH51T2XNTK6"
BASE_URL = "https://api.etherscan.io/api"

def fetch_wallet_transactions(address: str) -> list:
    """
    Fetches all normal transactions for an Ethereum wallet from Etherscan.
    Returns a list of transactions as dictionaries (ready for feature extraction).
    """
    try:
        url = (
            f"{BASE_URL}?module=account&action=txlist"
            f"&address={address}&startblock=0&endblock=99999999"
            f"&sort=asc&apikey={os.environ['ETHERSCAN_API_KEY']}"
        )
        response = requests.get(url)
        data = response.json()

        if data["status"] != "1":
            # If no transactions found, treat as normal account (not flagged)
            if data["message"].lower().startswith("no transactions"):
                return []
            raise ValueError(f"Error from Etherscan: {data['message']}")

        return data["result"]

    except Exception as e:
        # Only raise if not the 'no transactions found' case
        if "no transactions found" in str(e).lower():
            return []
        raise RuntimeError(f"Failed to fetch transactions: {e}")

def extract_features_from_etherscan(tx_list, address):
    """Extract features from transaction list for fraud detection"""
    if not tx_list:
        # Return default features for a new/empty account
        features = pd.DataFrame([{k: 0 for k in [
            "Avg min between sent tnx", "Avg min between received tnx", "Time Diff between first and last (Mins)",
            "Sent tnx", "Received Tnx", "Number of Created Contracts", "Unique Received From Addresses",
            "Unique Sent To Addresses", "min value received", "max value received ", "avg val received",
            "min val sent", "max val sent", "avg val sent", "min value sent to contract",
            "max val sent to contract", "avg value sent to contract", "total transactions (including tnx to create contract",
            "total Ether sent", "total ether received", "total ether balance"
        ]}])
        return features

    df = pd.DataFrame(tx_list)
    df['timestamp'] = pd.to_datetime(df['timeStamp'].astype(int), unit='s')
    df['value_eth'] = df['value'].astype(float) / 1e18
    df = df.sort_values('timestamp')

    # Basic filters
    sent = df[df['from'].str.lower() == address.lower()]
    received = df[df['to'].str.lower() == address.lower()]

    # Times
    avg_time_sent = sent['timestamp'].diff().dt.total_seconds().dropna().mean() / 60 if len(sent) > 1 else 0
    avg_time_received = received['timestamp'].diff().dt.total_seconds().dropna().mean() / 60 if len(received) > 1 else 0
    time_diff_total = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 60

    # Value stats
    min_received = received['value_eth'].min() if not received.empty else 0
    max_received = received['value_eth'].max() if not received.empty else 0
    avg_received = received['value_eth'].mean() if not received.empty else 0

    min_sent = sent['value_eth'].min() if not sent.empty else 0
    max_sent = sent['value_eth'].max() if not sent.empty else 0
    avg_sent = sent['value_eth'].mean() if not sent.empty else 0

    # Unique address counts
    uniq_received_from = received['from'].nunique()
    uniq_sent_to = sent['to'].nunique()

    # Contract interactions
    sent_contracts = sent[sent['input'] != '0x']
    avg_val_sent_to_contract = sent_contracts['value_eth'].mean() if not sent_contracts.empty else 0
    min_val_sent_to_contract = sent_contracts['value_eth'].min() if not sent_contracts.empty else 0
    max_val_sent_to_contract = sent_contracts['value_eth'].max() if not sent_contracts.empty else 0

    # Aggregates
    total_tx = len(df)
    total_eth_sent = sent['value_eth'].sum()
    total_eth_received = received['value_eth'].sum()
    total_balance = total_eth_received - total_eth_sent

    return pd.DataFrame([{
        "Avg min between sent tnx": avg_time_sent,
        "Avg min between received tnx": avg_time_received,
        "Time Diff between first and last (Mins)": time_diff_total,
        "Sent tnx": len(sent),
        "Received Tnx": len(received),
        "Number of Created Contracts": sum((sent['to'] == '') | (sent['to'].isna())),
        "Unique Received From Addresses": uniq_received_from,
        "Unique Sent To Addresses": uniq_sent_to,
        "min value received": min_received,
        "max value received ": max_received,
        "avg val received": avg_received,
        "min val sent": min_sent,
        "max val sent": max_sent,
        "avg val sent": avg_sent,
        "min value sent to contract": min_val_sent_to_contract,
        "max val sent to contract": max_val_sent_to_contract,
        "avg value sent to contract": avg_val_sent_to_contract,
        "total transactions (including tnx to create contract": total_tx,
        "total Ether sent": total_eth_sent,
        "total ether received": total_eth_received,
        "total ether balance": total_balance
    }])

def predict_scam(features):
    """
    Predict if wallet is fraudulent using trained model
    Returns: verdict and SHAP explanations
    """
    try:
        # If all features are zero, treat as normal (not flagged)
        if (features == 0).all(axis=None):
            return 'not flagged', [], 0.0

        # Load the saved model and normalizer
        with open('scam_normalizer.pkl', 'rb') as f:
            norm = pickle.load(f)
        with open('scam_model.pkl', 'rb') as f:
            xgb_model = pickle.load(f)

        # Normalize features
        norm_features = norm.transform(features)
        
        # Make prediction
        prediction = xgb_model.predict(norm_features)[0]
        prediction_proba = xgb_model.predict_proba(norm_features)[0]
        confidence = float(max(prediction_proba))  # Convert to Python float

        verdict = 'flagged' if prediction == 1 else 'not flagged'
        
        # Get SHAP explanations for flagged addresses
        top_features = []
        if verdict == 'flagged':
            try:
                explainer = shap.TreeExplainer(xgb_model)
                shap_values = explainer.shap_values(norm_features)
                feature_contributions = dict(zip(features.columns, shap_values[0]))
                sorted_contrib = sorted(feature_contributions.items(), key=lambda x: abs(x[1]), reverse=True)
                # Convert SHAP values to Python floats
                top_features = [(feature, float(impact)) for feature, impact in sorted_contrib[:3]]
            except Exception as e:
                print(f"SHAP explanation error: {e}")
                top_features = []

        return verdict, top_features, confidence

    except Exception as e:
        print(f"Prediction error: {e}")
        return 'error', [], 0.0

def predict_address_scam(address: str):
    """
    Main function to analyze an Ethereum address for fraud
    """
    try:
        # Fetch transactions
        transactions = fetch_wallet_transactions(address)
        
        # Extract features
        features = extract_features_from_etherscan(transactions, address)
        
        # Make prediction
        verdict, explanations, confidence = predict_scam(features)
        
        # Convert numpy types to Python native types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, np.float32) or isinstance(obj, np.float64):
                return float(obj)
            elif isinstance(obj, np.int32) or isinstance(obj, np.int64):
                return int(obj)
            elif isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif isinstance(obj, tuple):
                return tuple(convert_numpy_types(item) for item in obj)
            return obj
        
        # Convert features to regular Python types
        features_dict = {}
        if not features.empty:
            features_dict = {k: convert_numpy_types(v) for k, v in features.iloc[0].to_dict().items()}
        
        # Convert explanations to regular Python types
        explanations_converted = []
        for feature, impact in explanations:
            explanations_converted.append([feature, float(impact)])
        
        return {
            'address': address,
            'verdict': verdict,
            'confidence': float(confidence),
            'explanations': explanations_converted,
            'transaction_count': len(transactions),
            'features': features_dict
        }
    
    except Exception as e:
        return {
            'address': address,
            'verdict': 'error',
            'error': str(e),
            'confidence': 0.0
        }

@app.route('/')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Blockchain Fraud Detection API is running',
        'endpoints': {
            'analyze': '/api/analyze',
            'health': '/'
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_address():
    """Analyze a wallet address for fraud"""
    try:
        data = request.get_json()
        
        if not data or 'address' not in data:
            return jsonify({
                'error': 'Missing address in request body'
            }), 400
        
        address = data['address'].strip()
        
        # Basic address validation
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({
                'error': 'Invalid Ethereum address format'
            }), 400
        
        # Analyze the address
        result = predict_address_scam(address)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/analyze/<address>', methods=['GET'])
def analyze_address_get(address):
    """Analyze a wallet address for fraud via GET request"""
    try:
        # Basic address validation
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({
                'error': 'Invalid Ethereum address format'
            }), 400
        
        # Analyze the address
        result = predict_address_scam(address)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting Blockchain Fraud Detection API...")
    print("Make sure you have trained the model first by running the Jupyter notebook!")
    print("API will be available at: http://localhost:5001")
    print("Health check: http://localhost:5001")
    print("Analyze endpoint: http://localhost:5001/api/analyze")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
