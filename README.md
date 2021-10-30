# ngrok-telegram-notifier
Notify via Telegram bot the ngrok endpoint

## How to install and configure ngrok
``` https://gist.github.com/Mk555/6dea79c74fb26fe92774e9067dfe7222 ```

## Init
```pip install python-telegram-bot python-dotenv requests```

## Env file : 
File named ```.env``` in the ```<install_dir>``` of the script
```bash
TOKEN="<token_telegram>"
LIST_ID="<telegramID_01|telegramID_02>"
```

## Run the script : 
```bash
python daemon.py
```

## Add to systemd
Configure and copy ```ngrok-telegram-notifier.service``` in ```/etc/systemd/system/```

Run : 
```systemctl enable ngrok-telegram-notifier.service && systemctl start ngrok-telegram-notifier.service```