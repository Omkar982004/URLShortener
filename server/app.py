from flask import Flask, request, redirect, jsonify
import sqlite3
import random
import string

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE,
        long_url TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

# Generate short code
def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.json
    long_url = data.get("url")
    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)", (short_code, long_url))
    conn.commit()
    conn.close()
    
    return jsonify({"short_url": f"https://yourdomain.com/{short_code}"})

@app.route("/<short_code>")
def redirect_url(short_code):
    conn = sqlite3.connect("urls.db")
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return redirect(result[0])
    else:
        return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
