import datetime as dt
import multiprocessing as mp
import os

import pandas as pd
from tqdm import tqdm
from yt_dlp import YoutubeDL
import time
import subprocess

# code from https://github.com/keunwoochoi/audioset-downloader/blob/master/audioset_dl/__init__.py
def _download_video_shell(x):
    (
        ytid,
        start,
        end,
        out_dir,
    ) = x

    start_dt, end_dt = dt.timedelta(milliseconds=start), dt.timedelta(milliseconds=end)
    ydl_opts = {
        "outtmpl": f"{out_dir}/[{ytid}]-[{start // 1000}-{end // 1000}].%(ext)s",
        "format": "(bestvideo[height<=640]/bestvideo[ext=webm]/best)+(bestaudio[ext=webm]/best[height<=640])",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # one of avi, flv, mkv, mp4, ogg, webm
            }
        ],
        "quiet": True,
        "no-mtime": True,
    }
    yturl = f"https://youtube.com/watch?v={ytid}"
    section_opt = f"*{start_dt}-{end_dt}"
    cmd = (
        f'yt-dlp -f "{ydl_opts["format"]}" {yturl} '
        f"--download-sections {section_opt} "
        f"--quiet "
        f'--output "{ydl_opts["outtmpl"]}"'
    )
    try:
        # time.sleep(0.1)
        subprocess.run(cmd, shell=True, timeout=100)
    except subprocess.CalledProcessError as e:
        print(e)
    except KeyboardInterrupt:
        raise


def _download_audio(x):
    (
        ytid,
        start,
        end,
        out_dir,
    ) = x
    start_dt, end_dt = dt.timedelta(milliseconds=start), dt.timedelta(milliseconds=end)
    ydl_opts = {
        # "outtmpl": f"{out_dir}/%(id)s.%(ext)s",
        "outtmpl": f"{out_dir}/[%(id)s]-[{start//1000}-{end//1000}].%(ext)s",
        "format": "bestaudio[ext=webm]/bestaudio/best",
        "external_downloader": "ffmpeg",
        # "external_downloader_args": [
        #     "-loglevel",
        #     "panic",
        #     "-http_proxy",
        #     "socks5://127.0.0.1:1080"
        # ],
        "external_downloader_args": [
            "-ss",
            str(start_dt),
            "-to",
            str(end_dt),
            "-loglevel",
            "panic",
            "-http_proxy",
            "socks5://127.0.0.1:1080"
        ],
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet": True,
        "no-mtime": True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={ytid}"])
    except KeyboardInterrupt:
        raise
    except Exception:
        pass


def download_ps(ytid, st_list, ed_list, save_path, target, num_processes=None, desc=None):
    with mp.Pool(processes=num_processes) as pool, tqdm(total=len(ytid), desc=desc) as pbar:
        if target == "audio":
            for _ in tqdm(
                pool.imap(
                    _download_audio,
                    zip(ytid, st_list, ed_list, [save_path] * len(ytid)),
                ),
                total=len(ytid),
            ):
                pbar.update()
        elif target == "video":
            for _ in tqdm(
                pool.imap(
                    _download_video_shell,
                    zip(ytid, st_list, ed_list, [save_path] * len(ytid)),
                )
            ):
                pbar.update()
        else:
            raise NotImplementedError(f"target {target} is not implemented yet.")

def dl_audioset(save_path, args):
    target = args.target
    os.makedirs(args.save_path, exist_ok=True)
    meta = pd.read_csv(f"metadata/musiccaps-public.csv")
    yids = meta["ytid"]

    # If you wanna n-iter download
    # _yids = meta["ytid"]
    # print(set([i.split(".")[-1] for i in os.listdir(args.save_path)]))
    # already_down_ids = [i.split("[")[1].split("]")[0] for i in os.listdir(args.save_path)]
    # yids = list(set(_yids).difference(already_down_ids))
    # print(len(yids), len(already_down_ids))

    start_time = (meta.start_s * 1000).astype(int)
    end_time = (meta.end_s * 1000).astype(int)
    download_ps(yids, start_time, end_time, args.save_path, target, num_processes=mp.cpu_count()-10)