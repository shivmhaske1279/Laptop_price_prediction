import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)
application = app

# Load the pickle model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'Laptop_model.pkl')
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    model = None
    model_load_error = str(e)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Laptop Price Predictor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.08);
            --accent-primary: #6366f1;
            --accent-hover: #4f46e5;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background: var(--bg-gradient); color: var(--text-main); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem 1rem; }
        .container { width: 100%; max-width: 650px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 24px; padding: 2.5rem; backdrop-filter: blur(16px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); }
        .header { text-align: center; margin-bottom: 2.5rem; }
        .header h1 { font-size: 2.25rem; font-weight: 700; background: linear-gradient(to right, #a5b4fc, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem; }
        .header p { color: var(--text-muted); font-size: 0.95rem; }
        .grid-form { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; }
        @media (max-width: 500px) { .grid-form { grid-template-columns: 1fr; } }
        .form-group { display: flex; flex-direction: column; gap: 0.5rem; }
        label { font-size: 0.85rem; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }
        input, select { background: rgba(255, 255, 255, 0.05); border: 1px solid var(--card-border); border-radius: 12px; padding: 0.85rem 1rem; color: var(--text-main); font-size: 1rem; outline: none; }
        input:focus, select:focus { border-color: var(--accent-primary); }
        select option { background: #1e1b4b; color: var(--text-main); }
        .btn-submit { grid-column: span 2; background: var(--accent-primary); color: white; border: none; border-radius: 12px; padding: 1rem; font-size: 1rem; font-weight: 600; cursor: pointer; margin-top: 1rem; }
        @media (max-width: 500px) { .btn-submit { grid-column: span 1; } }
        .result-container { margin-top: 2.5rem; padding: 1.5rem; background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 16px; text-align: center; }
        .error-container { margin-top: 2.5rem; padding: 1.5rem; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 16px; color: #fca5a5; font-family: monospace; font-size: 0.9rem; text-align: left; overflow-x: auto; }
        .result-title { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; color: #a5b4fc; margin-bottom: 0.25rem; }
        .result-val { font-size: 2rem; font-weight: 700; color: #ffffff; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Laptop Valuation Engine</h1>
        <p>Configure specifications to approximate custom market pricing models</p>
    </div>

    <form method="POST" action="/" class="grid-form">
        <div class="form-group">
            <label for="brand">Brand</label>
            <select name="Brand" id="brand" required>
                <option value="0" {% if inputs and inputs['Brand'] == '0' %}selected{% endif %}>ASUS</option>
                <option value="1" {% if inputs and inputs['Brand'] == '1' %}selected{% endif %}>Acer</option>
                <option value="2" {% if inputs and inputs['Brand'] == '2' %}selected{% endif %}>Apple</option>
                <option value="3" {% if inputs and inputs['Brand'] == '3' %}selected{% endif %}>Dell</option>
                <option value="4" {% if inputs and inputs['Brand'] == '4' %}selected{% endif %}>HP</option>
                <option value="5" {% if inputs and inputs['Brand'] == '5' %}selected{% endif %}>Lenovo</option>
            </select>
        </div>

        <div class="form-group">
            <label for="processor">Processor Speed (GHz)</label>
            <input type="number" step="0.1" name="Processor_Speed" id="processor" min="1.0" max="5.0" value="{{ inputs['Processor_Speed'] if inputs else '2.5' }}" required>
        </div>

        <div class="form-group">
            <label for="ram">RAM Size (GB)</label>
            <select name="RAM_Size" id="ram" required>
                <option value="4" {% if inputs and inputs['RAM_Size'] == '4' %}selected{% endif %}>4 GB</option>
                <option value="8" {% if inputs and inputs['RAM_Size'] == '8' %}selected{% endif %}>8 GB</option>
                <option value="16" {% if inputs and inputs['RAM_Size'] == '16' %}selected{% endif %}>16 GB</option>
                <option value="32" {% if
