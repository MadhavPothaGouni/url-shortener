from flask import Flask, jsonify, request, redirect
from app.models import save_url_mapping, get_original_url, get_url_stats, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400

    original_url = data['url']

    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    short_code = save_url_mapping(original_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    })

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    url = get_original_url(short_code)
    if url:
        return redirect(url)
    return jsonify({"error": "Short code not found"}), 404

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    data = get_url_stats(short_code)
    if data:
        return jsonify({
            "url": data["url"],
            "clicks": data["clicks"],
            "created_at": data["created_at"]
        })
    return jsonify({"error": "Short code not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
