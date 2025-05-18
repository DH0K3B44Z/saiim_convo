#!/data/data/com.termux/files/usr/bin/bash

while true; do
    clear
    echo ""
    echo "--------- S A I I M MULTI-TOOL ---------"
    echo ""
    echo "1. Fill Files (convo.py)"
    echo "2. Launch Tool (sender.py)"
    echo "3. View Console"
    echo "4. Stop Tool"
    echo "5. Contact Admin"
    echo "6. Exit"
    echo "7. Check Your Tokens"
    echo ""
    read -p "Choose an option [1-7]: " opt

    case $opt in
        1)
            python convo.py
            read -p "Press Enter to return to menu..."
            ;;
        2)
            nohup python sender.py > output.log 2>&1 &
            echo "Tool started in background. Logs saved to output.log"
            read -p "Press Enter to return to menu..."
            ;;
        3)
            echo "--- Live Logs (press Ctrl+C to stop) ---"
            tail -f output.log
            ;;
        4)
            pkill -f sender.py
            echo "Tool stopped."
            read -p "Press Enter to return to menu..."
            ;;
        5)
            termux-open-url https://wa.me/919999999999
            ;;
        6)
            echo "Exiting..."
            exit 0
            ;;
        7)
            echo "Tokens in token file:"
            cat $(jq -r .token_file config.json)
            read -p "Press Enter to return to menu..."
            ;;
        *)
            echo "Invalid option. Try again."
            read -p "Press Enter to continue..."
            ;;
    esac
done
