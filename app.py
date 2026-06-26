import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

# 1. DEFINE BOTH APP ENTRIES FOR VERCEL TO AUTOMATICALLY DETECT
app = Flask(__name__)
application = app 

# --- Keep your exact model loading code here ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'Laptop_model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    model_load_error = str(e)

# --- Keep your HTML_TEMPLATE code here ---

@app.route('/', methods=['GET', 'POST'])
def home():
    # --- Keep your routine processing code here ---
    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text, error_text=error_text, inputs=inputs)

# 2. SEPARATE VERCEL SERVER FROM LOCAL TESTING
if __name__ == '__main__':
    app.run(debug=True)
