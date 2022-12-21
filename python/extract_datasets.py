import json
import numpy as np
from argparse import ArgumentParser, Action
from h5py import File
from pathlib import Path

def extract(fpath: str, frame: str):
    with File(fpath, "r") as f:
        attrs = {}
        for key, value in f.attrs.items():
            attrs[key] = value
        return f[frame][()], attrs

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--conf", type=str)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()

    with open(args.conf, "r") as f:
        conf = json.load(f)

    with File(args.output, "w") as f:
        for e in conf["extract"]:
            print(e)
            data, attrs = extract(e["fpath"], e["frame"])
            dset = f.create_dataset(e["frame_out"], data=data)

            for key, value in attrs.items():
                dset.attrs[key] = value

if __name__ == "__main__":
    main()
