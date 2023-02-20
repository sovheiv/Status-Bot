#!/bin/bash
cd /home/ubuntu/programs/Status-Bot
git fetch
git reset origin/main --hard
source venv/bin/activate
python main.py
