import os
from flask import Flask, jsonify

app = Flask(__name__)


@app.get('/api/health')
def health_check():
    """Simple endpoint to verify backend is running and env vars are loaded."""
    return jsonify({
        "status": "ok",
        "service": "backend",
        "database": {
            "host": os.getenv("DB_HOST", "not-set"),
            "port": os.getenv("DB_PORT", "not-set"),
            "name": os.getenv("DB_NAME", "not-set"),
            "user": os.getenv("DB_USER", "not-set"),
        },
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
