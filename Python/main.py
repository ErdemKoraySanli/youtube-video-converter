from pytube import YouTube
from flask import Flask, render_template, url_for,request
from flask_cors import CORS
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/youtube/mp4')
@limiter.limit("5/minute")
def youtubemp4():
   url = request.args.get('url')
   if url:
        yt = YouTube(url)
        video = {
            "info":{
                "title":yt.title,
                "channel": yt.author,
                "thumbnail":yt.thumbnail_url,
                "description": yt.description,
                "lenght": time.strftime("%H:%M:%S", time.gmtime(yt.length)),
                "views": yt.views,
                "publish_date":yt.publish_date
            },
            "sources": []
        }
        videos = yt.streams.filter(progressive=True,mime_type="video/mp4")
        for item in videos:
            video['sources'].append({
                "url":item.url,
                "filesize":item.filesize,
                "resolution":item.resolution
            })
        return video
   else :  
        return("Video Bulunamadı")  

if __name__ == "__main__":
    app.run(debug=True)
