#! /bin/zsh

echo "Enter file path:"
read -ep FILE # Enables autocompletion for file paths
sudo docker compose cp "$FILE" "web:/bus_booking/$FILE"
