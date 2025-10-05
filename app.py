import os
import tempfile
import subprocess
import stripe
import threading
import time
from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, send_file
)
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from dotenv import load_dotenv
from chakra import CHAKRAS, PLANETS, SACRED, NOISES

# ---------- LOAD ENVIRONMENT ----------
env_file = ".env.prod" if os.getenv("FLASK_ENV") == "production" else ".env.dev"
print(f"[ENV] Loading environment file: {env_file}")
load_dotenv(env_file)

# ---------- CONFIG ----------
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devkey")

stripe.api_key = os.getenv("STRIPE_API_KEY", "")
STRIPE_PRICE_ID_PRESET = os.getenv("STRIPE_PRICE_ID_PRESET", "")
STRIPE_PRICE_ID_CUSTOM = os.getenv("STRIPE_PRICE_ID_CUSTOM", "")

PRESIGN_EXPIRE_MINUTES = 60
TMP_DIR = tempfile.gettempdir()
serializer = URLSafeTimedSerializer(app.secret_key)

# 🔧 Base directory setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TONES_DIR = os.path.join(BASE_DIR, "tones")
print(f"[INIT] Tones directory set to: {TONES_DIR}")


# ---------- UTILITIES ----------
def schedule_delete(path, delay):
    """Delete a temporary file after delay."""
    def _delete():
        time.sleep(delay)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"[CLEANUP] Deleted {path}")
            except Exception as e:
                print(f"[CLEANUP ERROR] {e}")
    threading.Thread(target=_delete, daemon=True).start()


def generate_audio_from_meta(meta):
    """Generate or retrieve tone based on metadata."""
    category = meta.get("category")
    duration = int(meta.get("duration", 360))
    duration = min(max(duration, 1), 360)
    freq = meta.get("frequency", "")
    out_path = os.path.join(TMP_DIR, f"beat_{os.getpid()}_{int(time.time())}.wav")
    gain = "-3"

    prebuilt_map = {
        "Root (256 Hz)": "Root_256.wav",
        "Sacral (288 Hz)": "Sacral_288.wav",
        "Solar Plexus (320 Hz)": "Solar_320.wav",
        "Heart (341.3 Hz)": "Heart_341.wav",
        "Throat (384 Hz)": "Throat_384.wav",
        "Third Eye (426.7 Hz)": "ThirdEye_426.wav",
        "Crown (480 Hz)": "Crown_480.wav",
        "Pi Balance (180 Hz)": "Pi_180.wav",
        "Elevation (360 Hz)": "Elevation_360.wav",
        "Pink Noise": "Pink_Noise.wav",
        "Brown Noise": "Brown_Noise.wav",
        "Planet Sun": "Planet_Sun.wav",
        "Planet Moon": "Planet_Moon.wav",
        "Planet Mercury": "Planet_Mercury.wav",
        "Planet Venus": "Planet_Venus.wav",
        "Planet Mars": "Planet_Mars.wav",
        "Planet Jupiter": "Planet_Jupiter.wav",
        "Planet Saturn": "Planet_Saturn.wav",
    }

    # ✅ Serve prebuilt tones from ./tones
    if category in prebuilt_map:
        preset = os.path.join(TONES_DIR, prebuilt_map[category])
        if os.path.exists(preset):
            subprocess.run(["cp", preset, out_path], check=True)
            return out_path

    # Custom tones
    if category == "Custom":
        freq = freq or "440"
        cmd = ["sox", "-n", out_path, "synth", str(duration), "sine", str(freq), "gain", gain]
        subprocess.run(cmd, check=True)
        return out_path

    # Planet tones fallback
    if category in PLANETS:
        freqs = [round(float(f), 2) for f in PLANETS[category]]
        temp_files = []
        for f in freqs:
            tone_path = os.path.join(TMP_DIR, f"tone_{f}_{int(time.time())}.wav")
            cmd = ["sox", "-n", tone_path, "synth", str(duration), "sine", str(f), "gain", gain]
            subprocess.run(cmd, check=True)
            temp_files.append(tone_path)
        cmd = ["sox", "-m"] + temp_files + [out_path, "gain", gain]
        subprocess.run(cmd, check=True)
        for t in temp_files:
            try:
                os.remove(t)
            except Exception:
                pass
        return out_path

    raise ValueError(f"Unknown category {category}")


# ---------- ROUTES ----------
@app.route("/")
def index():
    """Main tone selection page."""
    descriptions = {
        "Root (256 Hz)": "Grounding and physical stability.",
        "Sacral (288 Hz)": "Creativity, sensuality, and emotional flow.",
        "Solar Plexus (320 Hz)": "Confidence, energy, and self-esteem.",
        "Heart (341.3 Hz)": "Love, compassion, and forgiveness.",
        "Throat (384 Hz)": "Communication and truth expression.",
        "Third Eye (426.7 Hz)": "Intuition and mental clarity.",
        "Crown (480 Hz)": "Spiritual connection and enlightenment.",
        "Pi Balance (180 Hz)": "Centering and harmonic balance (π resonance).",
        "Elevation (360 Hz)": "Expansion, elevation, and higher focus.",
        "Pink Noise": "Soft static for relaxation or focus.",
        "Brown Noise": "Deep grounding sound for meditation or sleep.",
    }

    planet_descriptions = {
        "Sun": "Vitality, confidence, and creative power.",
        "Moon": "Emotional balance, intuition, and inner reflection.",
        "Mercury": "Focus, communication, and mental clarity.",
        "Venus": "Harmony, beauty, and relationships.",
        "Mars": "Action, drive, and personal strength.",
        "Jupiter": "Expansion, optimism, and spiritual growth.",
        "Saturn": "Discipline, grounding, and life structure.",
    }

    # ✅ Map exact preview files
    preview_files = {
        "Root (256 Hz)": "Root_256_preview.wav",
        "Sacral (288 Hz)": "Sacral_288_preview.wav",
        "Solar Plexus (320 Hz)": "Solar_320_preview.wav",
        "Heart (341.3 Hz)": "Heart_341_preview.wav",
        "Throat (384 Hz)": "Throat_384_preview.wav",
        "Third Eye (426.7 Hz)": "ThirdEye_426_preview.wav",
        "Crown (480 Hz)": "Crown_480_preview.wav",
        "Pi Balance (180 Hz)": "Pi_180_preview.wav",
        "Elevation (360 Hz)": "Elevation_360_preview.wav",
        "Pink Noise": "Pink_Noise_preview.wav",
        "Brown Noise": "Brown_Noise_preview.wav",
        "Planet Sun": "Planet_Sun_preview.wav",
        "Planet Moon": "Planet_Moon_preview.wav",
        "Planet Mercury": "Planet_Mercury_preview.wav",
        "Planet Venus": "Planet_Venus_preview.wav",
        "Planet Mars": "Planet_Mars_preview.wav",
        "Planet Jupiter": "Planet_Jupiter_preview.wav",
        "Planet Saturn": "Planet_Saturn_preview.wav",
    }

    return render_template(
        "index.html",
        chakras=CHAKRAS,
        planets=PLANETS,
        sacred=SACRED,
        noises=NOISES,
        desc=descriptions,
        planet_desc=planet_descriptions,
        previews=preview_files,
        active="build",
    )


@app.route("/faq")
def faq():
    return render_template("faq.html", active="faq")


@app.route("/download_prebuilt/<path:filename>")
def download_prebuilt(filename):
    """🎧 Serve prebuilt or preview tones from ./tones."""
    path = os.path.abspath(os.path.join(TONES_DIR, filename))
    print(f"[PREVIEW DEBUG] Looking for: {path}")

    if not path.startswith(TONES_DIR):
        return ("", 404)

    if not os.path.exists(path):
        print(f"[PREVIEW ERROR] File not found: {path}")
        return ("", 404)

    print(f"[PREVIEW OK] Streaming {path}")
    return send_file(path, mimetype="audio/wav", as_attachment=False)


@app.route("/checkout_create", methods=["POST"])
def checkout_create():
    """Stripe checkout for paid tones."""
    category = request.form.get("category")
    duration = int(request.form.get("duration", 360))
    duration = min(max(duration, 1), 360)
    frequency = request.form.get("frequency", "").strip()

    metadata = {"category": category, "duration": str(duration), "frequency": frequency}
    price_id = STRIPE_PRICE_ID_CUSTOM if category == "Custom" else STRIPE_PRICE_ID_PRESET

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{"price": price_id, "quantity": 1}],
            metadata=metadata,
            success_url=url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for("index", _external=True),
        )
        print(f"[STRIPE] Checkout created for {category}: {session.url}")
        return redirect(session.url, code=303)
    except Exception:
        app.logger.exception("Stripe session creation failed")
        flash("Payment initialization failed.", "danger")
        return redirect(url_for("index"))


@app.route("/success")
def success():
    """After successful payment: serve tone and playback."""
    session_id = request.args.get("session_id")
    if not session_id:
        flash("Missing session ID.", "danger")
        return redirect(url_for("index"))

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        flash("Unable to verify payment.", "danger")
        return redirect(url_for("index"))

    if session.payment_status != "paid":
        flash("Payment not completed.", "danger")
        return redirect(url_for("index"))

    meta = session.metadata or {}
    try:
        out_path = generate_audio_from_meta(meta)
    except Exception:
        app.logger.exception("Tone generation failed")
        flash("Failed to generate tone.", "danger")
        return redirect(url_for("index"))

    schedule_delete(out_path, PRESIGN_EXPIRE_MINUTES * 60)
    token = serializer.dumps(out_path)

    tone_name = meta.get("category", "Your Tone")
    filename = os.path.basename(out_path)

    return render_template(
        "success.html",
        download_url=url_for("download", token=token, _external=True),
        tone_name=tone_name,
        tone_file=filename,
        expires=PRESIGN_EXPIRE_MINUTES,
        active="success",
    )


@app.route("/download/<token>")
def download(token):
    """Secure, timed download link for generated tones."""
    try:
        file_path = serializer.loads(token, max_age=PRESIGN_EXPIRE_MINUTES * 60)
        if not os.path.exists(file_path):
            flash("File expired.", "danger")
            return redirect(url_for("index"))
        schedule_delete(file_path, 5)
        return send_file(file_path, as_attachment=True)
    except (BadSignature, SignatureExpired):
        flash("Download expired.", "danger")
        return redirect(url_for("index"))
    except Exception:
        flash("Error during download.", "danger")
        return redirect(url_for("index"))


@app.route("/custom")
def custom():
    return render_template("custom.html", active="custom")


if __name__ == "__main__":
    print(f"🎧 Serving tones from: {TONES_DIR}")
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=(os.getenv("FLASK_ENV") != "production")
    )
