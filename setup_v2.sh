#!/bin/bash
# Prepares a fresh workspace for the v2 engine (videos 51+). Run from the repo root.
set -e
pip install -q --break-system-packages sherpa-onnx soundfile pillow numpy
which ffmpeg >/dev/null || (apt-get update -q && apt-get install -y -q ffmpeg)
fc-list | grep -qi "Inter" || (apt-get install -y -q fonts-inter fonts-dejavu-core || true)

mkdir -p /home/claude/tts2 && cd /home/claude/tts2
R=https://github.com/k2-fsa/sherpa-onnx/releases/download
[ -d kokoro-multi-lang-v1_0 ] || (curl -sL $R/tts-models/kokoro-multi-lang-v1_0.tar.bz2 | tar xj)
[ -d sherpa-onnx-whisper-base.en ] || (curl -sL $R/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 | tar xj)
cd - >/dev/null

# v2 scripts expect /home/claude/v2, covers script expects /home/claude/make_cover.py
mkdir -p /home/claude/v2 /home/claude/en
cp v2/*.py /home/claude/v2/
cp make_cover.py /home/claude/
[ -d /home/claude/sql-developer-videos ] || git clone -q https://github.com/umidzeynaldeveloper-code/sql-developer-videos /home/claude/sql-developer-videos
echo "v2 ready"
