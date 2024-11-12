# Simple Discord Giveaway Bot

This is a very simple discord giveaway bot written in python, follow the guide below for installation.
## Run Locally

Download requirements

```bash
pip install requirements.txt
```
Make an env variable with bot token

#### Windows:
```bash
setx GIVEAWAYS_TOKEN "TOKEN HERE"
```
#### Linux:
``` bash
export GIVEAWAYS_TOKEN="TOKEN HERE"
```
Start the bot

```bash
python main.py
```


## Host on a VPS

#### Docker
```bash
docker pull foregroundeclipse/giveawaysbot
docker run -d --name yourname-e GIVEAWAYS_TOKEN=TOKEN foregroundeclipse/giveawaysbot:latest
```
#### Daemon

Download requirements 

```bash
pip install path/to/requirements.txt
```
Make an env variable with bot token

``` bash
export GIVEAWAYS_TOKEN="TOKEN HERE"
```
Make the daemon config

```bash
nano /etc/systemd/system/servicename.service
```
In opened menu paste in
```bash
[Unit]
Description = description
After = network.target

[Service]
ExecStart = python3 /path/to/main.py
Restart = on-failure
RestartSec = 5s

[Install]
WantedBy = multi-user.target
```
Save by clicking ctrl+x and run the following commands in terminal
```bash
systemctl daemon-reload
systemctl start servicename
systemctl status servicename
```


