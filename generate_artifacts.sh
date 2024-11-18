#!/bin/bash
#set -euo pipefail
IFS=$'\n\t'

python -m build --sdist --wheel

rm -rf /st_multimodal_chatinput_artifacts/*

mkdir -p /st_multimodal_chatinput_artifacts/st_multimodal_chatinput/frontend/build
cp -r st_multimodal_chatinput/frontend/build /st_multimodal_chatinput_artifacts/st_multimodal_chatinput/frontend/build
mv build/ /st_multimodal_chatinput_artifacts/
mv dist/ /st_multimodal_chatinput_artifacts/
mv st_multimodal_chatinput.egg-info/ /st_multimodal_chatinput_artifacts/
