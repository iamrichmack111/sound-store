mkdir -p tones && \
# Chakra tones (6 minutes each)
sox -n tones/Root_256.wav synth 360 sine 256 gain -3 && \
sox -n tones/Sacral_288.wav synth 360 sine 288 gain -3 && \
sox -n tones/Solar_320.wav synth 360 sine 320 gain -3 && \
sox -n tones/Heart_341.wav synth 360 sine 341.3 gain -3 && \
sox -n tones/Throat_384.wav synth 360 sine 384 gain -3 && \
sox -n tones/ThirdEye_426.wav synth 360 sine 426.7 gain -3 && \
sox -n tones/Crown_480.wav synth 360 sine 480 gain -3 && \
# Sacred tones
sox -n tones/Pi_180.wav synth 360 sine 180 gain -3 && \
sox -n tones/Elevation_360.wav synth 360 sine 360 gain -3 && \
# Planetary multi-tones (mixed)
sox -m "|sox -n -p synth 360 sine 256" "|sox -n -p synth 360 sine 320" "|sox -n -p synth 360 sine 384" "|sox -n -p synth 360 sine 480" tones/Planet_Sun.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 288" "|sox -n -p synth 360 sine 341.3" "|sox -n -p synth 360 sine 426.7" tones/Planet_Moon.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 384" "|sox -n -p synth 360 sine 480" "|sox -n -p synth 360 sine 288" tones/Planet_Mercury.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 341.3" "|sox -n -p synth 360 sine 426.7" "|sox -n -p synth 360 sine 256" tones/Planet_Venus.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 320" "|sox -n -p synth 360 sine 384" "|sox -n -p synth 360 sine 480" tones/Planet_Mars.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 288" "|sox -n -p synth 360 sine 341.3" "|sox -n -p synth 360 sine 426.7" "|sox -n -p synth 360 sine 256" tones/Planet_Jupiter.wav gain -3 && \
sox -m "|sox -n -p synth 360 sine 256" "|sox -n -p synth 360 sine 303" "|sox -n -p synth 360 sine 384" tones/Planet_Saturn.wav gain -3 && \
# Noise tones
sox -n tones/Pink_Noise.wav synth 360 noise pink vol -20dB gain -3 && \
sox -n tones/Brown_Noise.wav synth 360 noise brown vol -20dB gain -3
