from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    data = request.json
    url = data['url']
    replace_patterns = str(data['replacePatterns']).lower()
    compress_images = str(data['compressImages']).lower()
    
    try:
        result = subprocess.run(['python', 'crawler.py', url, replace_patterns, compress_images], 
                                capture_output=True, text=True, check=True)
        return jsonify({"status": "success", "message": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": e.stderr}), 500

if __name__ == '__main__':
    app.run(debug=True)