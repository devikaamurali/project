from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

# Database initialization
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.commit()
    conn.close()

# Generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(6))

# Home page (serves the frontend)
@app.route("/")
def home():
    return render_template("index.html")

# API endpoint to shorten a URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()

    # Save to database
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code),
    )
    conn.commit()
    conn.close()

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

# Redirect to the original URL
@app.route("/<short_code>")
def redirect_to_url(short_code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)