from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

def get_codeforces_rating():
    """Fetches Codeforces rating for user 'ps2006'."""
    url = "https://codeforces.com/api/user.info?handles=ps2006"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        return {"rating": data["result"][0].get("rating", "N/A")}
    return {"error": "User not found"}

def get_leetcode_data():
    """Fetches LeetCode problems solved and rating for user 'psinfinity'."""
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }
    query = {
        "query": """
        query getLeetcodeData($username: String!) {
          matchedUser(username: $username) {
            submitStats {
              totalSubmissionNum {
                count
              }
            }
          }
          userContestRanking(username: $username) {
            rating
          }
        }
        """,
        "variables": {"username": "psinfinity"}
    }

    response = requests.post(url, json=query, headers=headers)
    data = response.json()

    if "data" in data and data["data"]["matchedUser"]:
        problems_solved = data["data"]["matchedUser"]["submitStats"]["totalSubmissionNum"][0]["count"]
        rating = data["data"]["userContestRanking"]["rating"]
        return {"problems_solved": problems_solved, "rating": round(rating)}
    
    return {"error": "User not found"}

@app.route("/")
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>ps2006 Stats</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Orbitron', sans-serif;
                background: #0a0a0a;
                color: #ddd;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            .background {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle, rgba(0,0,0,0.1) 10%, transparent 80%);
                animation: moveBackground 10s linear infinite;
            }
            @keyframes moveBackground {
                0% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0); }
            }
            h1 {
                font-size: 28px;
                margin-bottom: 20px;
                color: #fff;
                text-transform: uppercase;
                letter-spacing: 3px;
            }
            .container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 70%;
                max-width: 900px;
            }
            .stat {
                font-size: 50px;
                font-weight: bold;
                padding: 25px;
                min-width: 200px;
                text-align: center;
                border-radius: 10px;
                transition: transform 0.2s ease-in-out;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.15);
            }
            .stat .label {
                font-size: 16px;
                display: block;
                margin-top: 5px;
                opacity: 0.8;
            }
            .codeforces {
                background: rgba(0, 116, 204, 0.25);
                color: #00aaff;
                border: 2px solid #0074cc;
            }
            .leetcode {
                background: rgba(255, 161, 22, 0.25);
                color: #ffa116;
                border: 2px solid #ffa116;
            }
            .middle {
                background: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                border: 2px solid #ffffff;
            }
            .buttons {
                margin-top: 20px;
                display: flex;
                gap: 15px;
            }
            .btn {
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                transition: all 0.3s;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }
            .cf-btn {
                background: rgba(0, 116, 204, 0.25);
                color: #00aaff;
                border: 2px solid #0074cc;
            }
            .lc-btn {
                background: rgba(255, 161, 22, 0.25);
                color: #ffa116;
                border: 2px solid #ffa116;
            }
            .btn:hover {
                opacity: 0.8;
                transform: scale(1.05);
            }
            @media (max-width: 768px) {
                .container { flex-direction: column; gap: 15px; }
                .buttons { flex-direction: column; }
            }
            canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; }
        </style>
    </head>
    <body>
        
        <canvas id="particleCanvas"></canvas>
        <h1>ps2006</h1>
        <div class=\"container\">
            <div class=\"stat codeforces"><span id=\"cfRating\">Loading...</span><span class=\"label\">Codeforces Rating</span></div>
            <div class=\"stat middle"><span id=\"lcSolved\">Loading...</span><span class=\"label\">LC Problems Solved</span></div>
            <div class=\"stat leetcode"><span id=\"lcRating\">Loading...</span><span class=\"label\">LeetCode Rating</span></div>
        </div>
        <div class="buttons">
            <a href="https://codeforces.com/profile/ps2006" class="btn cf-btn" rel="noopener noreferrer">
                View Codeforces
            </a>
            <a href="https://leetcode.com/psinfinity/" class="btn lc-btn" rel="noopener noreferrer">
                View LeetCode
            </a>
        </div>

                        

        <script>
            function fetchStats() {
                fetch("/stats").then(response => response.json()).then(data => {
                    document.getElementById("cfRating").innerText = data.codeforces.rating || 0;
                    document.getElementById("lcSolved").innerText = data.leetcode.problems_solved || 0;
                    document.getElementById("lcRating").innerText = data.leetcode.rating || 0;
                });
            }
            window.onload = fetchStats;
                                  
        </script>
                <script>
            const canvas = document.getElementById("particleCanvas");
            const ctx = canvas.getContext("2d");
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const particles = [];
            class Particle {
                constructor() {
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 5 + 1;
                    this.speedX = Math.random() * 3 - 1.5;
                    this.speedY = Math.random() * 3 - 1.5;
                }
                update() {
                    this.x += this.speedX;
                    this.y += this.speedY;
                }
                draw() {
                    ctx.fillStyle = "rgba(255, 255, 255, 0.5)";
                    ctx.beginPath();
                    ctx.fillRect(this.x, this.y, this.size, this.size);
                    ctx.fill();
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(this.x, this.y);
                    ctx.lineTo(this.x - this.speedX * 5, this.y - this.speedY * 5);
                    ctx.stroke();
                }
            }
            function init() {
                for (let i = 0; i < 100; i++) {
                    particles.push(new Particle());
                }
            }
            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                particles.forEach(p => { p.update(); p.draw(); });
                requestAnimationFrame(animate);
            }
            init();
            animate();
        </script>

    </body>
    </html>
    """)

@app.route("/stats")
def get_stats():
    cf_data = get_codeforces_rating()
    lc_data = get_leetcode_data()
    return jsonify({"codeforces": cf_data, "leetcode": lc_data})

if __name__ == "__main__":
    app.run(debug=True)
