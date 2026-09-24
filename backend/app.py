from flask import Flask, jsonify
import mysql.connector
import os
import redis

app = Flask(__name__)

# Redis conection
cache = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis-service'),
    port=6379,
    decode_responses=True
)

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'database'),
        user=os.environ.get('DB_USER', 'appuser'),
        password=os.environ.get('DB_PASSWORD', 'changeme'),
        database=os.environ.get('DB_NAME', 'appdb')
    )

@app.route('/api')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Automatically create table if missing
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # WRITE operation
        cursor.execute("INSERT INTO visitors () VALUES ()")
        conn.commit()
        
        # READ 1 operation
        cursor.execute("SELECT COUNT(*) FROM visitors")
        visitor_count = cursor.fetchone()[0]
        
        # READ 2 operation
        cursor.execute("SELECT NOW()")
        db_time = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "message": "Connected to Database Successfully!",
            "visitor_count": visitor_count,
            "db_time": str(db_time)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/cache')
def cache_demo():
    # Increment counter in memory
    views = cache.incr('page_views')
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Weekly Assignment 5 - Redis Cache</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; max-width: 800px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }}
            .card {{ background: #eef9f1; border-left: 5px solid #28a745; padding: 15px; margin: 20px 0; }}
            .info-box {{ background: #f8f9fa; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }}
            a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>Weekly Assignment 5 - Redis Cache Extension</h1>
        
        <div class="card">
            <h2>Redis In-Memory Counter</h2>
            <p style="font-size: 1.2em;">This page has been visited <strong>{views}</strong> times using Redis cache!</p>
        </div>

        <div class="info-box">
            <h3>Project Links & Resources</h3>
            <ul>
                <li><strong>GitHub Repository:</strong> <a href="https://github.com/anasaemd25/cloud-services-assignment-5" target="_blank">anasaemd25/cloud-services-assignment-5</a></li>
                <li><strong>Main Application (Week 4 Baseline):</strong> <a href="/">View Main Page (MySQL Database)</a></li>
            </ul>
        </div>

        <h3>Part B - Implementation Summary</h3>
        <p>This extension runs an independent <code>redis:alpine</code> container and service inside CSC Rahti on port 6379 alongside the Nginx frontend, Flask backend, and MySQL database.</p>
    </body>
    </html>
    """
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)