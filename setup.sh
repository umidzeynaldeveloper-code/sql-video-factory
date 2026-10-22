#!/bin/bash
# Prepares a fresh workspace to render videos. Run from repo root.
set -e
pip install -q --break-system-packages sherpa-onnx soundfile pillow numpy
which ffmpeg >/dev/null || (apt-get update -q && apt-get install -y -q ffmpeg fonts-dejavu-core)
# Kokoro TTS model (sherpa-onnx format) shipped inside an npm package
mkdir -p /home/claude/tts_dl/n && cd /home/claude/tts_dl/n
[ -f package/kokoro-int8-en-v0_19/model.int8.onnx ] || (npm pack n8n-nodes-ttsbro@0.1.6 -q && tar xzf n8n-nodes-ttsbro-0.1.6.tgz)
# scripts expect to live in /home/claude
cd - >/dev/null
cp common.py vhelp.py make_video*.py make_music*.py /home/claude/
mkdir -p /home/claude/en && cp en/*.py /home/claude/en/
echo "ready"
