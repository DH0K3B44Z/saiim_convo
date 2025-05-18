#!/data/data/com.termux/files/usr/bin/bash

clear
echo ""
echo "--------- S A I I M  -  M E N U ---------"
echo ""
echo "1. Fill Files (Configure)"
echo "2. Launch Tool"
echo "3. View Console (Live Logs)"
echo "4. Stop Tool"
echo "5. Contact Admin"
echo "6. Exit"
echo "7. Check Your Tokens"
echo ""

read -p "Choose an option [1-7]: " opt

case $opt in
  1)
    clear
    python convo.py
    ;;
  2)
    echo "[*] Launching sender.py in background..."
    nohup python sender.py > output.log 2>&1 &
    echo "[+] Tool started. Logs in output.log"
    ;;
  3)
    echo "--- Live Logs (Press Ctrl+C to stop) ---"
    tail -f output.log
    ;;
  4)
    pkill -f sender.py
    echo "[-] Tool stopped successfully."
    ;;
  5)
    termux-open-url https://wa.me/919999999999
    ;;
  6)
    echo "Bye!"
    exit 0
    ;;
  7)
    echo "--- Tokens in your file ---"
    if [ -f "$(jq -r .token_file config.json)" ]; then
      cat "$(jq -r .token_file config.json)"
    else
      echo "Token file not found!"
    fi
    ;;
  *)
    echo "Invalid option."
    ;;
esac
