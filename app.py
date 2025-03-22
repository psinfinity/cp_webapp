from flask import Flask, jsonify, render_template_string
import requests
import webbrowser

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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

            h1 {
                font-size: 28px;
                margin-bottom: 30px;
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
                position: relative;
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.15);
            }

            .stat:hover {
                transform: scale(1.08);
            }

            .codeforces {
                background: rgba(0, 116, 204, 0.25);
                color: #00aaff;
                border: 2px solid #0074cc;
                text-shadow: 0 0 10px rgba(0, 174, 255, 0.7);
            }

            .leetcode {
                background: rgba(255, 161, 22, 0.25);
                color: #ffa116;
                border: 2px solid #ffa116;
                text-shadow: 0 0 10px rgba(255, 161, 22, 0.7);
            }

            .middle {
                background: rgba(255, 255, 255, 0.2);
                color: #ffffff;
                border: 2px solid #ffffff;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
            }

            .animated-bg {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                background: linear-gradient(-45deg, #1a1a1a, #0a0a0a, #222, #111);
                background-size: 400% 400%;
                animation: gradientShift 6s infinite alternate ease-in-out;
            }

            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                100% { background-position: 100% 50%; }
            }

            .particle {
                position: absolute;
                background: rgba(255, 255, 255, 0.2);
                width: 5px;
                height: 5px;
                border-radius: 50%;
                pointer-events: none;
                opacity: 0;
                animation: floatParticles linear infinite;
            }

            @keyframes floatParticles {
                from {
                    transform: translateY(100vh) translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(-10vh) translateX(calc(10vw - 5vw * random()));
                    opacity: 0;
                }
            }


            .label {
                font-size: 18px;
                font-weight: normal;
                margin-top: 5px;
                opacity: 0.8;
            }

            .profile-buttons {
                margin-top: 20px;
            }

            .profile-btn {
                display: inline-block;
                padding: 12px 24px;
                font-size: 18px;
                font-weight: bold;
                border-radius: 10px;
                text-decoration: none;
                transition: all 0.3s ease-in-out;
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.15);
            }

            .cf-btn {
                background: rgba(0, 116, 204, 0.25);
                color: #00aaff;
                border: 2px solid #0074cc;
                text-shadow: 0 0 10px rgba(0, 174, 255, 0.7);
            }

            .cf-btn:hover {
                background: rgba(0, 116, 204, 0.5);
            }

            .lc-btn {
                background: rgba(255, 161, 22, 0.25);
                color: #ffa116;
                border: 2px solid #ffa116;
                text-shadow: 0 0 10px rgba(255, 161, 22, 0.7);
            }

            .lc-btn:hover {
                background: rgba(255, 161, 22, 0.5);
            }


        </style>
    </head>
    <body>

        <div class="animated-bg"></div>
        
        <h1> ps2006 </h1>

        <div class="container">
            <div class="stat codeforces">
                <span id="cfRating">Loading...</span>
                <div class="label">Codeforces Rating</div>
            </div>

            <div class="stat middle">
                <span id="lcSolved">Loading...</span>
                <div class="label">LC Problems Solved</div>
            </div>

            <div class="stat leetcode">
                <span id="lcRating">Loading...</span>
                <div class="label">LeetCode Rating</div>
            </div>
        </div>

        <div class="profile-buttons">
            <a href="https://codeforces.com/profile/ps2006" class="profile-btn cf-btn" target="_blank">View Codeforces</a>
            <a href="https://leetcode.com/psinfinity/" class="profile-btn lc-btn" target="_blank">View LeetCode</a>
        </div>

        <script>
            function animateNumber(id, target) {
                let element = document.getElementById(id);
                let start = 0;
                
                let speed = Math.max(1, Math.floor(target / 50)); 
                let duration = 500; 
                let stepTime = Math.max(10, duration / target);

                let timer = setInterval(() => {
                    start += speed;
                    if (start >= target) {
                        start = target;
                        clearInterval(timer);
                    }
                    element.innerText = start;
                }, stepTime);
            }

            function fetchStats() {
                fetch("/stats")
                    .then(response => response.json())
                    .then(data => {
                        let cfRating = data.codeforces.rating || 0;
                        let lcSolved = data.leetcode.problems_solved || 0;
                        let lcRating = data.leetcode.rating || 0;

                        animateNumber("cfRating", cfRating);
                        animateNumber("lcSolved", lcSolved);
                        animateNumber("lcRating", lcRating);
                    })
                    .catch(error => console.error("Error fetching stats:", error));
            }

            window.onload = fetchStats;

            function createParticles() {
                const numParticles = 20; 
                for (let i = 0; i < numParticles; i++) {
                    let particle = document.createElement("div");
                    particle.classList.add("particle");
                    document.body.appendChild(particle);

                    let size = Math.random() * 6 + 2; 
                    particle.style.width = `${size}px`;
                    particle.style.height = `${size}px`;

                    // Randomize starting position
                    particle.style.left = `${Math.random() * 100}vw`;
                    particle.style.top = `${Math.random() * 100}vh`;

                    // Make movement diagonal instead of stuck in one place
                    let randomXMove = Math.random() * 20 - 10; // Moves left or right slightly
                    particle.style.animation = `floatParticles ${Math.random() * 4 + 3}s linear infinite`;

                    setTimeout(() => particle.remove(), 5000);
                }
            }

            setInterval(createParticles, 1000);


            setInterval(createParticles, 1000); // Create particles every second

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
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)