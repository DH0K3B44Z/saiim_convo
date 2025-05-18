#!/data/data/com.termux/files/usr/bin/bash

clear
echo ""
echo "--------- S A I I M LAUNCH TOOL ---------"
echo ""
echo "(1) Fill files (run convo.py)"
echo "(2) Launch tool (start sender.py)"
echo "(3) View console (tail logs)"
echo "(4) Stop tool (kill sender.py)"
echo "(5) Contact admin (WhatsApp)"
echo "(6) Exit"
echo "(7) Check your tokens"
echo ""
read -p "Choose an option [1-7]: " opt

case "$opt" in
  1)
    # Run convo.py to create/update config.json
    python convo.py
    ;;
  2)
    # Start sender.py in background, redirect logs
    nohup python sender.py > output.log 2>&1 &
    echo "Tool started in background. Logs saved to output.log"
    ;;
  3)
    # View logs live
    if [ -f output.log ]; then
      echo "--- Live Logs (press Ctrl+C to stop) ---"
      tail -f output.log
    else
      echo "Log file output.log not found."
    fi
    ;;
  4)
    # Stop sender.py by killing process
    pkill -f sender.py && echo "Tool stopped." || echo "Tool was not running."
    ;;
  5)
    # Open WhatsApp link (Termux only)
    termux-open-url https://wa.me/919999999999
    ;;
  6)
    echo "Exiting..."
    exit 0
    ;;
  7)
    # Check tokens inside config.json and display them
    if [ -f config.json ]; then
      token_file=$(python -c "import json; print(json.load(open('config.json')).get('token_file',''))")
      if [ -f "$token_file" ]; then
        echo "Tokens in $token_file:"
        cat "$token_file"
      else
        echo "Token file '$token_file' not found or empty."
      fi
    else
      echo "config.json not found."
    fi
    ;;
  *)
    echo "Invalid option."
    ;;
esac
