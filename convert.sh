clear
echo -e "\e[32mDownloading Requiremwnts...\e[97m"
echo ""
pip install yt_dlp flask
termux-setup-storage
echo -e "\e[32mRequirements Downloaded Successfully\e[97m"
echo""
python main.py
