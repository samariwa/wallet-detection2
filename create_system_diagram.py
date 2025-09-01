#!/usr/bin/env python3
"""
System Architecture Diagram Generator for Blockchain Fraud Detection System
Creates a comprehensive flow diagram showing model training, UI interaction, and SHAP interpretation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the figure with high DPI for crisp PNG output
plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Define colors
colors = {
    'data': '#E3F2FD',          # Light blue for data
    'training': '#FFF3E0',       # Light orange for training
    'model': '#E8F5E8',         # Light green for models
    'api': '#F3E5F5',           # Light purple for API
    'ui': '#FCE4EC',            # Light pink for UI
    'storage': '#FFF8E1',       # Light yellow for storage
    'interpretation': '#E0F2F1', # Light teal for SHAP
    'process': '#F5F5F5'        # Light gray for processes
}

# Define box style
box_style = "round,pad=0.3"

def create_box(x, y, width, height, text, color, fontsize=10, text_color='black'):
    """Create a rounded rectangle box with text"""
    box = FancyBboxPatch((x, y), width, height,
                        boxstyle=box_style,
                        facecolor=color,
                        edgecolor='gray',
                        linewidth=1.5)
    ax.add_patch(box)
    
    # Add text
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center',
           fontsize=fontsize, fontweight='bold',
           color=text_color,
           wrap=True)

def create_arrow(start_x, start_y, end_x, end_y, text='', offset=0, color='black'):
    """Create an arrow between two points with optional label"""
    arrow = ConnectionPatch((start_x, start_y), (end_x, end_y), 
                           "data", "data",
                           arrowstyle="->", 
                           shrinkA=0, shrinkB=0,
                           mutation_scale=20, 
                           fc=color, ec=color,
                           linewidth=2)
    ax.add_patch(arrow)
    
    if text:
        mid_x = (start_x + end_x) / 2 + offset
        mid_y = (start_y + end_y) / 2
        ax.text(mid_x, mid_y, text, ha='center', va='center',
               fontsize=8, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))

# Title
ax.text(50, 95, 'Blockchain Fraud Detection System Architecture', 
        ha='center', va='center', fontsize=20, fontweight='bold')

# ========== DATA LAYER ==========
# Raw Data
create_box(5, 80, 15, 8, 'Transaction\nDataset\n(CSV)', colors['data'], 10)

# Data Processing
create_box(25, 80, 15, 8, 'Data\nPreprocessing\n& Cleaning', colors['process'], 10)

# Normalized Data
create_box(45, 80, 15, 8, 'Normalized\nFeatures\n(PowerTransformer)', colors['data'], 10)

# Oversampling
create_box(65, 80, 15, 8, 'Balanced Dataset\n(BorderlineSMOTE)', colors['process'], 10)

# Data flow arrows
create_arrow(20, 84, 25, 84, 'Load & Explore')
create_arrow(40, 84, 45, 84, 'Transform')
create_arrow(60, 84, 65, 84, 'Oversample')

# ========== MODEL TRAINING LAYER ==========
# Cross-validation
create_box(5, 65, 18, 8, 'K-Fold Cross\nValidation\n(6 Models)', colors['training'], 10)

# Individual Models
create_box(28, 65, 12, 8, 'XGBoost\n(Selected)', colors['model'], 9)
create_box(42, 65, 12, 8, 'CatBoost', colors['model'], 9)
create_box(56, 65, 12, 8, 'TabNet\n(PyTorch)', colors['model'], 9)
create_box(70, 65, 12, 8, 'Deep Learning\n(TensorFlow)', colors['model'], 9)

# Model evaluation
create_box(85, 65, 12, 8, 'Model\nEvaluation\n& Selection', colors['training'], 9)

# Training flow arrows
create_arrow(72, 80, 15, 73, 'Split & Validate')
create_arrow(72, 80, 34, 73, 'Train')
create_arrow(72, 80, 48, 73, 'Train')
create_arrow(72, 80, 62, 73, 'Train')
create_arrow(72, 80, 76, 73, 'Train')
create_arrow(76, 69, 85, 69, 'Compare')

# ========== MODEL STORAGE ==========
# Pickle Storage
create_box(5, 48, 15, 8, 'Model Storage\n(Pickle Files)\nmodel.pkl\nnorm.pkl', colors['storage'], 9)

# SHAP Setup
create_box(25, 48, 15, 8, 'SHAP Explainer\nSetup & Training', colors['interpretation'], 9)

# Storage arrows
create_arrow(34, 65, 12, 56, 'Save XGBoost')
create_arrow(34, 65, 32, 56, 'Configure SHAP')

# ========== API LAYER ==========
# Flask Backend
create_box(5, 30, 20, 12, 'Flask Backend API\n\n• Load Models\n• Feature Extraction\n• Prediction\n• SHAP Analysis', colors['api'], 10)

# Blockchain Integration
create_box(30, 30, 18, 12, 'Blockchain Integration\n\n• Etherscan API\n• Real-time Data\n• Transaction Fetching', colors['api'], 10)

# API arrows
create_arrow(12, 48, 15, 42, 'Load Models')
create_arrow(32, 48, 39, 42, 'Load SHAP')

# ========== PROCESSING LAYER ==========
# Feature Extraction
create_box(55, 35, 18, 8, 'Feature Extraction\nfrom Blockchain\nTransactions', colors['process'], 9)

# Prediction Engine
create_box(55, 22, 18, 8, 'Prediction Engine\n& SHAP Analysis', colors['interpretation'], 9)

# Processing arrows
create_arrow(48, 36, 55, 39, 'Extract Features')
create_arrow(64, 35, 64, 30, 'Process')

# ========== UI LAYER ==========
# React Frontend
create_box(5, 8, 25, 12, 'React Frontend UI\n\n• Address Input\n• Results Display\n• SHAP Visualizations\n• User Dashboard', colors['ui'], 11)

# User Interaction
create_box(35, 8, 20, 12, 'User Experience\n\n• Enter Wallet Address\n• View Fraud Score\n• See Explanations\n• Download Reports', colors['ui'], 10)

# Results Display
create_box(60, 8, 25, 12, 'Results & Insights\n\n• Fraud Probability\n• Feature Importance\n• SHAP Values\n• Risk Assessment', colors['interpretation'], 10)

# UI flow arrows
create_arrow(15, 30, 17, 20, 'API Calls')
create_arrow(30, 14, 35, 14, 'User Input')
create_arrow(55, 14, 60, 14, 'Display Results')

# ========== DETAILED PROCESS FLOWS ==========
# User Journey
create_arrow(45, 14, 55, 26, 'Send Address', offset=2, color='blue')
create_arrow(64, 22, 72, 14, 'Return Results', offset=2, color='green')

# Backend Processing
create_arrow(25, 36, 30, 36, 'API Request', color='purple')
create_arrow(73, 35, 73, 30, 'Process', color='purple')

# ========== LEGEND ==========
legend_y = 2
ax.text(2, legend_y, 'Legend:', fontsize=12, fontweight='bold')

legend_items = [
    ('Data Layer', colors['data']),
    ('Training', colors['training']),
    ('Models', colors['model']),
    ('API/Backend', colors['api']),
    ('UI/Frontend', colors['ui']),
    ('Storage', colors['storage']),
    ('Interpretation', colors['interpretation']),
    ('Processing', colors['process'])
]

for i, (label, color) in enumerate(legend_items):
    x_pos = 10 + (i % 4) * 20
    y_pos = legend_y - 2 if i >= 4 else legend_y
    
    # Small colored box
    legend_box = patches.Rectangle((x_pos, y_pos-0.5), 2, 1, 
                                 facecolor=color, edgecolor='gray')
    ax.add_patch(legend_box)
    ax.text(x_pos + 3, y_pos, label, fontsize=9, va='center')

# ========== WORKFLOW ANNOTATIONS ==========
# Add workflow numbers
workflow_steps = [
    (12, 84, '1'),
    (32, 84, '2'),
    (52, 84, '3'),
    (72, 84, '4'),
    (15, 69, '5'),
    (91, 69, '6'),
    (12, 52, '7'),
    (32, 52, '8'),
    (15, 36, '9'),
    (39, 36, '10'),
    (64, 39, '11'),
    (64, 26, '12'),
    (17, 14, '13'),
    (47, 14, '14'),
    (72, 14, '15')
]

for x, y, num in workflow_steps:
    circle = patches.Circle((x, y), 1.5, facecolor='red', edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, num, ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Workflow description
workflow_text = """
Workflow Steps:
1-4: Data Pipeline  5-6: Model Training & Selection  7-8: Model Storage & SHAP Setup
9-10: API & Blockchain Integration  11-12: Real-time Processing  13-15: User Interface & Results
"""

ax.text(50, -2, workflow_text, ha='center', va='top', fontsize=10,
        bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.8))

# Add timestamp and project info
ax.text(95, 1, 'Generated: August 30, 2025\nBlockchain Fraud Detection System', 
        ha='right', va='bottom', fontsize=8, style='italic')

# Save the diagram
plt.tight_layout()
plt.savefig('/Volumes/External/Dan Project/system_architecture_diagram.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("System architecture diagram saved as 'system_architecture_diagram.png'")
print("Diagram shows complete flow from data to user results including:")
print("   • Data preprocessing and model training pipeline")
print("   • Model storage and SHAP configuration")
print("   • Flask API and React UI integration")
print("   • Real-time blockchain data processing")
print("   • User interaction and results delivery")
