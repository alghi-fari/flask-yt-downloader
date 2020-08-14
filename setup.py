# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, send_from_directory
from werkzeug.exceptions import HTTPException
from markupsafe import escape
from pytube import YouTube
import youtube_dl

app = Flask(__name__,static_folder='files')

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/proccess', methods=['POST'])

def proccess():
    data = request.form['urlyoutube']
    option = request.form['opt']
    if option == 'mp4':
     print(data)
     data = data
     yt = YouTube(data)
     judul = yt.title
     title = "{} - Ghifari Downloader".format(judul).replace(" ","")
     yt.register_on_progress_callback(progress_function)
     yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download(output_path='files', filename=title)
     return render_template('done.html', title=title,path=title)
    else:
     ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
     ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])

def progress_function(stream, chunk, bytes_remaining):
    percent = round((1-bytes_remaining/stream.filesize)*100)
    if( percent%30 == 0):
        print(percent, 'done')

@app.route('/files/<path:filename>')
def download(filename):
    return send_from_directory(directory='files', filename=filename)

@app.errorhandler(Exception)
def handle_exception(e):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
