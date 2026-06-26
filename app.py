import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)
application = app  # <--- Add this line right here to satisfy Vercel's fallback finder

# ... (rest of your model loading code and HTML template) ...

@app.route('/', methods=['GET', 'POST'])
def home():
    # ... (your route logic) ...
    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text, inputs=inputs)

# Vercel reads the file as a module; this block is only for local testing
if __name__ == '__main__':
    app.run(debug=True)
