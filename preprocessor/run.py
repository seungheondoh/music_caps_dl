import os
import ast
import pandas as pd
import numpy as np
import multiprocessing
from constants import DATASET, MUSIC_SAMPLE_RATE, DATA_LENGTH
from audio_utils import load_audio, STR_CH_FIRST
from io_utils import _json_dump
    
def audio_resampler(_id, audio_path, save_path):
    src, _ = load_audio(
        path= os.path.join(audio_path, _id + ".wav"),
        ch_format= STR_CH_FIRST,
        sample_rate= MUSIC_SAMPLE_RATE,
        downmix_to_mono= True)
    save_name = os.path.join(save_path, _id + ".npy")
    if not os.path.exists(os.path.dirname(save_name)):
        os.makedirs(os.path.dirname(save_name))
    np.save(save_name, src.astype(np.float32))
    
def mc_preprocessor(root_path):
    """
    music caps preprocessor:
        params: root_path (str): proj dir
        return: annotation (json): kv style annotation dictionary
    """
    df = pd.read_csv(os.path.join(root_path, "metadata/musiccaps-public.csv"))
    df['aspect_list'] = df['aspect_list'].apply(ast.literal_eval)
    annotation = {}
    for idx in range(len(df)):
        instance = df.iloc[idx]
        item_dict = instance.to_dict()
        _id = f"[{instance.ytid}]-[{int(instance.start_s)}-{int(instance.end_s)}]"
        outtmpl = f"{root_path}/metadata/wav/{_id}.wav"
        if os.path.exists(outtmpl):
            annotation[_id] = item_dict
    df_filtered = pd.DataFrame(annotation).T
    total_track = list(df_filtered.index)
    trva_track = list(df_filtered[df_filtered['is_audioset_eval'] == True].index)
    test_track = list(df_filtered[df_filtered['is_audioset_eval'] == False].index)
    valid_idx = int(0.9 * len(trva_track))
    train_track = trva_track[:valid_idx]
    valid_track = trva_track[valid_idx:]
    track_split = {
        "train_track": train_track,
        "valid_track": valid_track,
        "test_track": test_track
    }
    print(len(train_track), len(valid_track), len(test_track), len(annotation), len(total_track), len(df))
    _json_dump(os.path.join(root_path, "metadata", "track_split.json"), track_split)
    _json_dump(os.path.join(root_path, "metadata", "annotation.json"), annotation)
    return total_track


def main():
    audio_path= "../metadata/wav"
    save_path= "../metadata/npy"
    total_track = mc_preprocessor(root_path = "../")

    # audio resampling
    pool = multiprocessing.Pool(20)
    pool.starmap(audio_resampler, zip(total_track, [audio_path] * len(total_track), [save_path] * len(total_track)))
    
if __name__ == '__main__':
    main()