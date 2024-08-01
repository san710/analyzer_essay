from flask import Flask, render_template, request, jsonify
import time
from analyze_essay import analyze_essay

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')
    context = data.get('context', '')

    analysis = analyze_essay(text, context)

    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)
