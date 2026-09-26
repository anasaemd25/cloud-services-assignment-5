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
    try:
        views = cache.incr('page_views')
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weekly Assignment 5 - Redis Cache</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; background-color: #f4f7f6; color: #333; }}
                .container {{ max-width: 900px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #27ae60; padding-bottom: 10px; margin-top: 0; }}
                h2 {{ color: #34495e; margin-top: 25px; }}
                .badge {{ background-color: #27ae60; color: white; padding: 5px 10px; border-radius: 4px; font-size: 0.9em; }}
                .card {{ background: #e8f8f5; border-left: 5px solid #27ae60; padding: 20px; margin: 20px 0; border-radius: 4px; }}
                .counter {{ font-size: 2.2em; color: #27ae60; font-weight: bold; font-family: monospace; }}
                .info-box {{ background: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                ul {{ line-height: 1.8; }}
                a {{ color: #2980b9; text-decoration: none; font-weight: bold; }}
                a:hover {{ text-decoration: underline; }}
                img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; margin-top: 15px; display: block; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Assignment 5: Redis Cache Extension <span class="badge">Live</span></h1>
                
                <div class="card">
                    <h2>In-Memory Visit Counter</h2>
                    <p>This endpoint interacts directly with an independent <strong>Redis key-value store</strong> running in OpenShift/Rahti.</p>
                    <p class="counter">Total Hits: {views}</p>
                </div>

                <div class="info-box">
                    <h3>Architecture Overview</h3>
                    <p>Unlike the primary MySQL database from Week 4 which persists structured tabular data to disk, Redis stores this counter in RAM for ultra-fast read/write operations, bypassing database query overhead.</p>
                    <ul>
                        <li><strong>Component Type:</strong> Standalone Deployment & Service (<code>redis-service:6379</code>)</li>
                        <li><strong>Data Pattern:</strong> Ephemeral key-value counter (<code>INCR page_views</code>)</li>
                        <li><strong>Main App Baseline:</strong> <a href="/">Return to Week 4 MySQL Main Page</a></li>
                    </ul>
                </div>

                <h2>Implementation Evidence</h2>
                <div class="info-box">
                    <h3>1. Cluster Status (OpenShift Pods & Services)</h3>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/Evidence-Pod-Services.png" alt="OpenShift Status">
                    
                    <h3>2. Week 4 Baseline Verification (MySQL Database)</h3>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/Week4-Evidence.png" alt="Week 4 Baseline">

                    <h3>3. Live Redis Cache Endpoint Verification</h3>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/redis-web.png" alt="Redis Endpoint Verification">
                </div>
            </div>
        </body>
        </html>
        """

    except Exception as e:
        return jsonify({"error": "Redis connection failed", "details": str(e)}), 500    except Exception as e:
        return jsonify({"error": "Redis connection failed", "details": str(e)}), 500
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)