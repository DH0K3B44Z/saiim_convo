#!/data/data/com.termux/files/usr/bin/bash

while true; do
    clear
    echo "--------- S A I I M LAUNCH TOOL ---------"
    echo ""
    echo "1. Fill Files"
    echo "2. Launch Tool"
    echo "3. View Console"
    echo "4. Stop Tool"
    echo "5. Contact Admin"
    echo "6. Exit"
    echo "7. Check Your Tokens"
    echo "9. Setup/Install Termux Environment"
    echo ""
    read -p "Choose an option [1-7,9]: " opt

    if [ "$opt" == "1" ]; then
        python convo.py
        echo ""
        read -p "Press Enter to return to menu..."
    elif [ "$opt" == "2" ]; then
        nohup python sender.py > output.log 2>&1 &
        echo ""
        echo "Tool started in background. Logs saved to output.log"
        sleep 2
        read -p "Press Enter to return to menu..."
    elif [ "$opt" == "3" ]; then
        echo ""
        echo "--- Live Logs (press Ctrl+C to return) ---"
        tail -f output.log
    elif [ "$opt" == "4" ]; then
        pkill -f sender.py
        echo "Tool stopped."
        sleep 1
    elif [ "$opt" == "5" ]; then
        termux-open-url https://wa.me/919999999999
    elif [ "$opt" == "6" ]; then
        echo "Exiting..."
        exit
    elif [ "$opt" == "7" ]; then
        echo ""
        echo "Checking your tokens..."
        python check_tokens.py
        echo ""
        read -p "Press Enter to return to menu..."
    elif [ "$opt" == "9" ]; then
        bash install.sh
        echo ""
        read -p "Setup complete. Press Enter to return to menu..."
    else
        echo "Invalid option"
        sleep 1
    fi
done
