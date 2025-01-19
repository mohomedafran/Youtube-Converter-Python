import os
import shutil
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from yt_dlp import YoutubeDL

app = Flask(__name__)

# Directory to store the converted files temporarily
DOWNLOAD_DIR = 'downloads'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def convert():
    if request.method == 'POST':
        video_url = request.form['video_link']
        try:
            video_info = YoutubeDL().extract_info(url=video_url, download=False)
            title = video_info['title']
        except Exception as e:
            return f"Error occurred: {e}"

        # Sanitize the title to create a valid file name
        sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"{sanitized_title}.mp3"

        # Define download options for yt_dlp
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename
        }
        try:
            with YoutubeDL(options) as ytaudio:
                ytaudio.download([video_info['webpage_url']])
        except Exception as e:
            return f"Download failed: {e}"

        # Ensure the downloads directory exists
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        # Move the file to the downloads directory
        dest = os.path.join(DOWNLOAD_DIR, filename)
        try:
            shutil.move(filename, dest)
        except Exception as e:
            return f"File move failed: {e}"

        # Redirect to the download route
        return redirect(url_for('download', filename=filename))

@app.route('/download/<filename>')
def download(filename):
    # Serve the file for download
    try:
        return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)
    except Exception as e:
        return f"File not found: {e}"

if __name__ == '__main__':
    app.run(debug=True)
