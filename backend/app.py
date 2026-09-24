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
    # Incrementa un contador en memoria cada vez que se visita la ruta
    views = cache.incr('visitas_cache')
    return f"<h1>Prueba de Redis Cache</h1><p>Esta página se ha visitado {views} veces usando Redis en memoria.</p>"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)