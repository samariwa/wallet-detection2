#!/usr/bin/env python3
"""
Simple System Flow Diagram for Blockchain Fraud Detection
Creates a clean, minimal flow diagram showing the essential components
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Set up the figure
fig, ax = plt.subplots(1, 1, figsize=(16, 10))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Define simple color scheme
colors = {
    'data': '#E3F2FD',      # Light blue
    'model': '#E8F5E8',     # Light green
    'api': '#FFF3E0',       # Light orange
    'ui': '#FCE4EC',        # Light pink
    'result': '#F3E5F5'     # Light purple
}

def create_simple_box(x, y, width, height, text, color, fontsize=12):
    """Create a simple rounded box with text"""
    box = FancyBboxPatch((x, y), width, height,
                        boxstyle="round,pad=0.5",
                        facecolor=color,
                        edgecolor='#333333',
                        linewidth=2)
    ax.add_patch(box)
    
    ax.text(x + width/2, y + height/2, text,
           ha='center', va='center',
           fontsize=fontsize, fontweight='bold',
           color='#333333')

def create_simple_arrow(start_x, start_y, end_x, end_y, text='', color='#333333'):
    """Create a simple arrow with optional label"""
    arrow = ConnectionPatch((start_x, start_y), (end_x, end_y), 
                           "data", "data",
                           arrowstyle="->", 
                           shrinkA=0, shrinkB=0,
                           mutation_scale=25, 
                           fc=color, ec=color,
                           linewidth=3)
    ax.add_patch(arrow)
    
    if text:
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2 + 2
        ax.text(mid_x, mid_y, text, ha='center', va='center',
               fontsize=10, fontweight='bold', color=color,
               bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor=color, linewidth=1))

# Title
ax.text(50, 90, 'Blockchain Fraud Detection System', 
        ha='center', va='center', fontsize=18, fontweight='bold', color='#333333')

# Step 1: Data & Training
create_simple_box(10, 70, 25, 12, 'DATA & TRAINING\n\n• Load Transaction Data\n• Train XGBoost Model\n• Save as Pickle Files', colors['data'], 11)

# Step 2: Model Storage
create_simple_box(65, 70, 25, 12, 'MODEL STORAGE\n\n• model.pkl\n• normalizer.pkl\n• SHAP Explainer', colors['model'], 11)

# Step 3: User Interface
create_simple_box(10, 45, 25, 12, 'USER INTERFACE\n\n• React Frontend\n• Enter Wallet Address\n• Submit Request', colors['ui'], 11)

# Step 4: API Backend
create_simple_box(40, 45, 25, 12, 'API BACKEND\n\n• Flask Server\n• Load Models\n• Process Request', colors['api'], 11)

# Step 5: Blockchain Data
create_simple_box(70, 45, 25, 12, 'BLOCKCHAIN DATA\n\n• Etherscan API\n• Fetch Transactions\n• Extract Features', colors['data'], 11)

# Step 6: Prediction & SHAP
create_simple_box(25, 20, 25, 12, 'PREDICTION\n\n• Run XGBoost Model\n• Calculate Fraud Score\n• Generate SHAP Values', colors['model'], 11)

# Step 7: Results
create_simple_box(55, 20, 25, 12, 'RESULTS\n\n• Fraud Probability\n• Feature Importance\n• Risk Assessment', colors['result'], 11)

# Arrows with labels
create_simple_arrow(35, 76, 65, 76, '1. Train & Save')
create_simple_arrow(22, 70, 22, 57, '2. User Input')
create_simple_arrow(35, 51, 40, 51, '3. API Call')
create_simple_arrow(65, 51, 70, 51, '4. Fetch Data')
create_simple_arrow(77, 70, 52, 57, '5. Load Models')
create_simple_arrow(52, 45, 37, 32, '6. Predict')
create_simple_arrow(50, 26, 55, 26, '7. Return Results')
create_simple_arrow(37, 45, 22, 32, '8. Display to User')

# Add simple workflow numbers
workflow_positions = [
    (22, 76), (77, 76), (22, 51), (52, 51), (82, 51), (37, 26), (67, 26)
]

for i, (x, y) in enumerate(workflow_positions, 1):
    circle = patches.Circle((x, y), 2, facecolor='#FF6B6B', edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, str(i), ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Simple legend
legend_items = [
    ('Data/Training', colors['data']),
    ('Model/Processing', colors['model']),
    ('API/Backend', colors['api']),
    ('User Interface', colors['ui']),
    ('Results', colors['result'])
]

ax.text(5, 10, 'Components:', fontsize=12, fontweight='bold', color='#333333')
for i, (label, color) in enumerate(legend_items):
    y_pos = 7 - i * 1.5
    legend_box = patches.Rectangle((7, y_pos-0.4), 1.5, 0.8, 
                                 facecolor=color, edgecolor='#333333')
    ax.add_patch(legend_box)
    ax.text(9, y_pos, label, fontsize=10, va='center', color='#333333')

# Simple workflow description
workflow_text = """Simple Workflow: Train Model → Save Files → User Input → API Call → Fetch Data → Predict → Return Results"""
ax.text(50, 5, workflow_text, ha='center', va='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#F5F5F5', edgecolor='#333333', linewidth=1))

plt.tight_layout()
plt.savefig('/Volumes/External/Dan Project/simple_system_flow.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✅ Simple system flow diagram saved as 'simple_system_flow.png'")
print("📊 Clean diagram showing:")
print("   • 7-step workflow from training to results")
print("   • Clear component separation")
print("   • Simple color coding")
print("   • Easy-to-follow flow arrows")
