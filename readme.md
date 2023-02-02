## Music Caps Donwloader

Unofficial download repository for [MusicCaps](https://www.kaggle.com/datasets/googleai/musiccaps)

`The MusicCaps dataset contains 5,521 music examples, each of which is labeled with an English aspect list and a free text caption written by musicians.`

### Current Status
- 5501 (/5,521) music is crawling!

### ydl_opts
```
ydl_opts = {
        "outtmpl": f"{out_dir}/%(id)s.%(ext)s",
        "format": "bestaudio[ext=webm]/bestaudio/best",
        "external_downloader": "ffmpeg",
        "external_downloader_args": [
            "-loglevel",
            "panic",
            "-http_proxy",
            "socks5://127.0.0.1:1080"
        ],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "quiet": True,
        "no-mtime": True,
    }
```

### issue

```
# invalid start time
WARNING: [youtube] Invalid start time (53886.0 < 0) for chapter "26-08-09 Melding : 13-119 A1 AMSTERDAM BOLSTOEN -- RIT:175"
WARNING: [youtube] Invalid start time (380.0 < 0) for chapter "Genre:"
WARNING: [youtube] Invalid start time (380.0 < 0) for chapter "Duur"                                        
...

# issue: Private video & unavailable & terminated
ERROR: [youtube] 0J_2K1Gvruk: Private video. Sign in if you've been granted access to this video
ERROR: [youtube] 63rqIYPHvlc: Private video. Sign in if you've been granted access to this video
ERROR: [youtube] Ah_aYOGnQ_I: Private video. Sign in if you've been granted access to this video
...
ERROR: [youtube] Akg1n9IWSrw: Video unavailable. This video is no longer available because the YouTube account associated with this video has been terminated.
ERROR: [youtube] B7iRvj8y9aU: Video unavailable. This video is no longer available because the YouTube account associated with this video has been terminated.
ERROR: [youtube] NIcsJ8sEd0M: Video unavailable. This video is no longer available because the YouTube account associated with this video has been terminated.
...

# issue: country(KR)
ERROR: [youtube] KMQmM12G9Z4: Video unavailable. This video contains content from WMG, who has blocked it in your country on copyright grounds
```

### Reference
- https://www.kaggle.com/datasets/googleai/musiccaps
- https://github.com/SangwonSUH/audioset-downloader
- https://github.com/keunwoochoi/audioset-downloader
