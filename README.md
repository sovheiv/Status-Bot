# Status Bot
A bot specifically for Ukrainian servers showing whether a server has electricity now

### Server setup
1. `mkdir programs/Status-Bot`
1. `nano programs/Status-Bot/docker-compose.yml`
1. `nano programs/Status-Bot/.env`
1. `sudo nano //etc/systemd/system/status-bot.service`
1. `sudo systemctl daemon-reload`
1. `sudo systemctl enable status-bot.service`
1. `sudo systemctl start status-bot.service`
1. `sudo systemctl status status-bot.service`

### Dev setup
1. Optional PowerShell permitions: `Set-ExecutionPolicy unrestricted`
1. `python -m venv venv`
1. `.\venv\Scripts\activate`
1. `pip install -r .\requirements.txt`
1. Create `.env` file
