import requests
import json
import os

TOKEN_FILE = "tokens.txt"  # Aap apni token file ka naam yahan set kar sakte hain
OUTPUT_FILE = "valid_tokens.txt"

def load_tokens(path):
    if not os.path.isfile(path):
        print(f"[x] Token file '{path}' not found!")
        exit(1)
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_token(token):
    url = "https://graph.facebook.com/v15.0/me"
    params = {"access_token": token}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        if "error" in data:
            return False, data["error"].get("message", "Unknown error")
        else:
            return True, data  # data contains id, name etc.
    except Exception as e:
        return False, str(e)

def main():
    tokens = load_tokens(TOKEN_FILE)
    valid_tokens = []

    print(f"Checking {len(tokens)} tokens...\n")

    for i, token in enumerate(tokens, 1):
        print(f"Checking token {i} / {len(tokens)} ...")
        valid, data = check_token(token)
        if valid:
            print(f"✅ Valid token: {data.get('name')} (ID: {data.get('id')})")
            valid_tokens.append(token)
        else:
            print(f"❌ Invalid token: {data}")

    if valid_tokens:
        with open(OUTPUT_FILE, "w") as f:
            for t in valid_tokens:
                f.write(t + "\n")
        print(f"\nValid tokens saved to '{OUTPUT_FILE}'")
    else:
        print("\nNo valid tokens found.")

if __name__ == "__main__":
    main()
