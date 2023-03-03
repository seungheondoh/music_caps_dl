import json

def _json_dump(path, item):
    with open(path, mode="w") as io:
        json.dump(item, io, indent=4)
