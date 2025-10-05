

# 🪐 Chakra & Planetary Beats

### *A Flask-based binaural & monaural beat generator with Stripe payments and cosmic design*

![screenshot](https://via.placeholder.com/800x350/000000/ffffff?text=Chakra+Beats+Preview)

---

## 🌌 Overview

**Chakra & Planetary Beats** is a self-hosted web app that generates and sells **binaural, monaural, and noise-based meditation tones**.
Built with **Flask**, **SoX**, and **Stripe Checkout**, the app allows users to:

* Stream 5-second tone previews.
* Purchase full 6-minute versions securely.
* Generate **custom tones** on a separate page (premium option).
* Experience an **animated starfield UI** with **flippable Chakra cards**.

---

## 🧠 Features

| Feature                               | Description                                                   |
| ------------------------------------- | ------------------------------------------------------------- |
| 🎵 **Prebuilt Chakra tones**          | Root → Crown, each 6-minute SoX-generated tone                |
| 💳 **Stripe integration**             | Secure payments for prebuilt ($2) & custom ($5) tones         |
| 🎧 **Binaural & monaural generation** | Powered by `sox` inside the container                         |
| 💫 **Animated design**                | Moving star background, 3D flippable cards, responsive layout |
| 📱 **Mobile friendly**                | Fully responsive Bootstrap 5 interface                        |
| 🐳 **Dockerized**                     | One-command deploy with Docker Compose                        |
| ⚙️ **Environment isolation**          | `.env.dev` (sandbox) & `.env.prod` (live) modes               |
| 🔐 **Secure file handling**           | Automatic cleanup of generated tone files after download      |

---

## 🗂️ Folder Structure

```
/home/wisdom/MONEY/
├── app.py
├── chakra.py
├── templates/
│   ├── index.html
│   ├── custom.html
│   └── success.html
├── tones/
│   ├── Root_256.wav
│   ├── Root_256_preview.wav
│   └── ...
├── .env.dev
├── .env.prod
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Requirements

* Python 3.10+
* SoX (audio synthesis tool)
* Docker (for deployment)
* Stripe account + API keys

---

## 🧩 Environment Setup

### 1️⃣ Development (Stripe Sandbox)

Create **`.env.dev`**:

```bash
FLASK_ENV=development
SECRET_KEY=dev_secret_key
STRIPE_API_KEY=sk_test_...
STRIPE_PRICE_ID_PRESET=price_1SEwucJCNqGNTrOCyi5S5o7p
STRIPE_PRICE_ID_CUSTOM=price_1SExGrJCNqGNTrOC6MrRGPn9
PORT=5000
```

### 2️⃣ Production (Live Stripe)

Create **`.env.prod`**:

```bash
FLASK_ENV=production
SECRET_KEY=super_secret_key_replace
STRIPE_API_KEY=sk_live_your_real_key
STRIPE_PRICE_ID_PRESET=price_live_preset_id_here
STRIPE_PRICE_ID_CUSTOM=price_live_custom_id_here
PORT=5000
```

### 3️⃣ `.gitignore`

Make sure you have:

```
.env
.env.*
tones/*.wav
__pycache__/
venv/
```

---

## 🧭 Switching Environments

### 🔹 Local Development

```bash
export FLASK_ENV=development
python3 app.py
```

or use the helper script:

```bash
./switch_env.sh dev
```

### 🔹 Production

```bash
export FLASK_ENV=production
python3 app.py
```

or with the helper:

```bash
./switch_env.sh prod
```

---

## 🐳 Docker Deployment

### Build & Run (Development)

```bash
docker compose build
docker compose up
```

### Switch to Production

Edit `docker-compose.yml`:

```yaml
env_file:
  - .env.prod
environment:
  - FLASK_ENV=production
```

Then:

```bash
docker compose down
docker compose up --build -d
```

App runs on `http://0.0.0.0:5000`

---

## 💳 Stripe Integration

### Pricing IDs

| Type     | Price ID                         | Description         |
| -------- | -------------------------------- | ------------------- |
| Prebuilt | `price_1SEwucJCNqGNTrOCyi5S5o7p` | $2 Chakra tones     |
| Custom   | `price_1SExGrJCNqGNTrOC6MrRGPn9` | $5 custom generator |

### Test Card

For sandbox mode, use:

```
Card: 4242 4242 4242 4242
Date: Any future
CVC: 123
ZIP: 12345
```

---

## 🎨 Design Details

* **Framework:** Bootstrap 5
* **Animation:** CSS keyframes (starfield background)
* **Cards:** CSS 3D transforms, flippable on hover/tap
* **Audio Players:** Native HTML5
* **Color Palette:** Deep blue gradient with cyan glow
* **Navbar:** Sticky, transparent, mobile collapsible

---

## 🔉 Tones Overview

| Chakra       | Frequency | Element   | Focus                 |
| ------------ | --------- | --------- | --------------------- |
| Root         | 256 Hz    | Earth     | Grounding & Security  |
| Sacral       | 288 Hz    | Water     | Creativity & Pleasure |
| Solar Plexus | 320 Hz    | Fire      | Power & Will          |
| Heart        | 341 Hz    | Air       | Love & Healing        |
| Throat       | 384 Hz    | Ether     | Communication         |
| Third Eye    | 426 Hz    | Light     | Intuition             |
| Crown        | 480 Hz    | Spirit    | Enlightenment         |
| Pi           | 180 Hz    | Balance   | Centering             |
| Elevation    | 360 Hz    | Ascension | Higher Awareness      |

All tones are generated with SoX and mixed with binaural or pink/brown noise variants.

---

## ⚠️ Disclaimer

These sounds are designed for **meditation and relaxation**.
They are **not medical devices** and should not replace professional care.
Use responsibly, ideally with headphones in a quiet space.

---

## 🔍 Health Check (optional)

Add a simple route in `app.py` for monitoring:

```python
@app.route("/healthz")
def healthz():
    return {"status": "ok"}, 200
```

Then in `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/healthz"]
  interval: 30s
  timeout: 10s
  retries: 3
```

---

## ✨ Future Enhancements

* 🌠 Parallax star depth
* 🌈 Chakra-based gradient animations
* 🔊 Layered sound previews
* 🪙 Wallet payments or PayPal integration
* 🧘 User-saved meditation sessions

---

## 👨‍💻 Author

**Jeremy Franklin (Richmack Studios)**
🛰️ *Building meditative & AI-driven tools for creative consciousness*
🔗 GitHub: [iamrichmack111](https://github.com/iamrichmack111)

---

