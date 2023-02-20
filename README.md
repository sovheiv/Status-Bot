# Status Bot
A bot specifically for Ukrainian servers showing whether a server has electricity now

### Setup server
1. connect `ssh ubuntu@192.168.31.114`
1. set pass `passwd`
1. gen key `ssh-keygen -t ed25519 -C "rpi"`
1. add to config
1. `ssh-copy-id -i ~/.ssh/id_rsa.pub -p 6576 ubuntu@192.168.0.1`
1. `sudo apt update`
1. `sudo apt full-upgrade`
1. `sudo apt-get install -y python3-venv`

### Setup app
1. git clone
1. move .sh file to ..
1. move .service file to //etc/systemd/system
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. `python3 -m venv venv`
1. `sudo chmod 644 //etc/systemd/system/<service>`
1. `sudo chmod 744 <sh>`
1. `sudo systemctl enable <service>`
1. `sudo systemctl start <service>`
1. `sudo systemctl status <service>`
1. if update `systemctl daemon-reload`
