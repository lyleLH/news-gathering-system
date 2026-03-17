from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Serve static frontend files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Example API endpoint
@app.route('/api/inspirations')
def get_inspirations():
    # Future: Fetch data from database and return as JSON
    return jsonify({"data": ["行业新闻灵感", "热门话题灵感", "竞品分析灵感", "UGC洞察灵感"]})

def run_system():
    print("News Gathering System started.")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_system()