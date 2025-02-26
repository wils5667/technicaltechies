from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)

@app.before_request
def initialize_alcohol_items():
    if 'alcohol_items' not in session:
        session['alcohol_items'] = [
            {"name": "Jack Daniel's Old No. 7", "serial": "JD001", "expiration": "2025-12-15", "quantity": 120},
            {"name": "Jack Daniel's Old No. 7", "serial": "JD001", "expiration": "2025-12-15", "quantity": 120},
            {"name": "Jack Daniel's Old No. 7", "serial": "JD001", "expiration": "2025-12-15", "quantity": 120}
        ]
"""
@app.route('/')
def base():
    return render_template('base.html')
"""