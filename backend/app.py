from flask import Flask, jsonify
import mysql.connector
import os
import redis

app = Flask(__name__)

# Redis connection setup
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("INSERT INTO visitors () VALUES ()")
        conn.commit()
        
        cursor.execute("SELECT COUNT(*) FROM visitors")
        visitor_count = cursor.fetchone()[0]
        
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
            <title>Weekly Assignment 5 - Cloud Services</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; background-color: #f4f7f6; color: #333; line-height: 1.6; }}
                .container {{ max-width: 950px; margin: 0 auto; background: #fff; padding: 35px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #27ae60; padding-bottom: 12px; margin-top: 0; }}
                h2 {{ color: #34495e; margin-top: 30px; border-bottom: 2px solid #27ae60; padding-bottom: 8px; }}
                h3 {{ color: #2e7d32; margin-top: 20px; }}
                .badge {{ background-color: #27ae60; color: white; padding: 6px 12px; border-radius: 4px; font-size: 0.85em; vertical-align: middle; }}
                .card {{ background: #e8f8f5; border-left: 5px solid #27ae60; padding: 20px; margin: 20px 0; border-radius: 4px; }}
                .counter {{ font-size: 2.2em; color: #27ae60; font-weight: bold; font-family: monospace; margin: 10px 0 0 0; }}
                .info-box {{ background: #f8f9fa; border: 1px solid #e9ecef; padding: 20px; border-radius: 6px; margin-bottom: 25px; }}
                .qa-card {{ background: #fafafa; border: 1px solid #e0e0e0; padding: 18px; border-radius: 6px; margin-bottom: 15px; }}
                .qa-card h4 {{ margin: 0 0 8px 0; color: #1a5276; font-size: 1.05em; }}
                .evidence-section {{ background: #ffffff; border: 1px solid #dcdfe6; padding: 20px; border-radius: 6px; margin-bottom: 30px; }}
                .evidence-desc {{ background: #f4f6f8; padding: 12px 15px; border-left: 4px solid #3498db; margin: 10px 0 15px 0; font-size: 0.95em; }}
                ul {{ line-height: 1.8; }}
                a {{ color: #2980b9; text-decoration: none; font-weight: bold; }}
                a:hover {{ text-decoration: underline; }}
                img {{ max-width: 100%; height: auto; border: 1px solid #ccc; border-radius: 6px; margin-top: 10px; display: block; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weekly Assignment 5: Cloud Services <span class="badge">Live</span></h1>
                
                <div class="card">
                    <h2>Part B - Redis In-Memory Counter</h2>
                    <p>This endpoint interacts directly with an independent <strong>Redis key-value store</strong> running in OpenShift/Rahti.</p>
                    <p class="counter">Total Hits: {views}</p>
                </div>

                <div class="info-box">
                    <h3>Architecture & Extension Overview</h3>
                    <p>This page extends the 3-tier architecture built during Week 4 (Nginx frontend, Flask backend, MySQL database) by introducing an isolated, high-performance caching layer using Redis.</p>
                    <ul>
                        <li><strong>Component Type:</strong> Independent Kubernetes Deployment and Service (<code>redis-service:6379</code>)</li>
                        <li><strong>Data Pattern:</strong> Ephemeral key-value counter (<code>INCR page_views</code>)</li>
                        <li><strong>Main Application (Week 4 Baseline):</strong> <a href="/">Return to Week 4 MySQL Main Page</a></li>
                        <li><strong>GitHub Repository:</strong> <a href="https://github.com/anasaemd25/cloud-services-assignment-5" target="_blank">anasaemd25/cloud-services-assignment-5</a></li>
                    </ul>
                </div>

                <h2>Part A - Theory Questions & Answers</h2>

                <div class="qa-card">
                    <h4>1. What is YAML and why has it become the default configuration format for Kubernetes/Rahti manifests? Compare it briefly to JSON.</h4>
                    <p>YAML (YAML Ain't Markup Language) is a human readable data serialization standard commonly used for configuration files. It became the default option for Kubernetes and Rahti because its clean structure relies on line indentation rather than brackets or commas, making the complex cluster definitions easier to read and maintain. Unlike JSON, YAML supports comments and has a minimal syntax. Behind the scenes, Kubernetes converts YAML manifests into JSON before applying them.</p>
                </div>

                <div class="qa-card">
                    <h4>2. What is a Web Application Firewall (WAF) and what kinds of attacks does it defend against? Where would you place one in the three-container architecture built in Week 4?</h4>
                    <p>A Web Application Firewall inspects and filters incoming HTTP/HTTPS traffic to block malicious exploits before they reach the web application. It defends against OWASP top threats like SQL Injection, Cross-Site Scripting (XSS), and automated bot attacks. In the Week 4 architecture (<code>Route → Frontend → Backend → Database</code>), a WAF would be placed at the edge of the network, right before or integrated into the public Route/Frontend, protecting Nginx and Flask from direct application layer attacks.</p>
                </div>

                <div class="qa-card">
                    <h4>3. Explain the difference between SAML and OAuth. When would a company choose one over the other?</h4>
                    <p>Security Assertion Markup Language (SAML) is an XML based framework focused on <strong>Authentication</strong> (verifying identity) for Enterprise Single Sign-On (SSO). OAuth is an open standard focused on <strong>Authorization</strong> (for granting access permissions without sharing user credentials). A company chooses SAML for internal corporate login systems across employee software, but OAuth is chosen when building web applications that allow users to sign in via 3rd party providers (like Microsoft or Google) or when managing API access tokens.</p>
                </div>

                <div class="qa-card">
                    <h4>4. What are open data portals and why does choosing the right open-data format matter for reuse?</h4>
                    <p>Open data portals are public platforms that store freely accessible datasets provided by governments and public figures. Choosing standard, machine readable formats like JSON, CSV, or GeoJSON is important for reuse, because software applications can parse and process data automatically. Unstructured formats like PDFs or images block automation and require manual extraction.</p>
                </div>

                <h2>Part B - Implementation Evidence</h2>

                <div class="evidence-section">
                    <h3>1. Cluster Status Verification (OpenShift Pods & Services)</h3>
                    <div class="evidence-desc">
                        <strong>Explanation:</strong> This terminal screenshot proves that the Redis extension runs as a distinct, standalone pod alongside the original Week 4 services. It also demonstrates that <code>redis-service</code> correctly exposes port <code>6379</code> internally to the cluster.
                    </div>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/Evidence-Pod-Services.png" alt="OpenShift Status Verification">
                </div>

                <div class="evidence-section">
                    <h3>2. Week 4 Baseline Verification (MySQL Application)</h3>
                    <div class="evidence-desc">
                        <strong>Explanation:</strong> This screenshot confirms that adding the Redis caching extension did not break or disrupt the original Week 4 core application. The primary frontend continues to communicate with the Flask API and the persistent MySQL database seamlessly.
                    </div>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/Week4-Evidence.png" alt="Week 4 Baseline Application">
                </div>

                <div class="evidence-section">
                    <h3>3. Live Endpoint & Cache Verification</h3>
                    <div class="evidence-desc">
                        <strong>Explanation:</strong> This screenshot verifies the live web interface of the <code>/api/cache</code> route. It shows the real-time incrementing counter powered by Redis in-memory storage.
                    </div>
                    <img src="https://raw.githubusercontent.com/anasaemd25/cloud-services-assignment-5/main/screenshots/redis-web.png" alt="Redis Web Interface Verification">
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return jsonify({"error": "Redis connection failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)