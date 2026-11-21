# v2.1 prototype — measured results (2026-11-21, 2 vCPU / 7.8 GB, no GPU)

| Metric | v2 (current) | v2.1 final preset |
|---|---|---|
| Demo length | 17.0 s | 17.1 s |
| Full render, cold TTS (wall) | 34.7 s | 115.1 s (video stage 99.7 s) |
| Re-render, TTS cached (wall) | — | 103.9 s |
| Peak RAM (largest process) | 843 MB | 626–1148 MB |
| Seconds per frame, 1 process | — | 0.35 (ss=2) · 0.12 (ss=1) · 0.37 (4K canvas) |
| Loudness I / TP / LRA | -14.0 / -1.5 / 1.8 | -14.0 / -1.4 / 1.7 (2-pass) |
| Resampling out-of-band energy (24 kHz sweep) | -23.1 dB (np.interp) | -53.2 dB (resample_poly) |
| Audio | 44.1 kHz, mono voice dup. | 48 kHz, stereo SFX + atmos |
| video51 SCENES unchanged | — | renders, same layout (6 frames compared) |

Smoothness proxy (mean abs frame diff, 270x480 gray): v2 58.6 % moving frames, v2.1 83.8 % (camera, particles, parallax).
Word-level subtitles are ESTIMATED (pause detection + syllables): Kokoro and local Whisper return no timestamps.
Google TTS provider = interface only, never called (no SDK, no credentials, host blocked by proxy).
