import argparse
from utils import dl_audioset

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_path", default="../metadata/wav", type=str)
    parser.add_argument("--target", default="audio", choices=['audio', 'video'], type=str)
    args = parser.parse_args()
    dl_audioset(args.save_path, args=args)