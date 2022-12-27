import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser, Action
from h5py import File
from pathlib import Path

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 10})

class parse_csvarg(Action):
    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, [v for v in values.split(",")])

def plot(plot_file: str, data_file: str, dkeys: list) -> None:
    data = {}
    with File(data_file, "r") as f: 
        for dkey in dkeys:
            data[dkey] = f[dkey][()]

    fig, axes = plt.subplots(len(dkeys), 1) 
    fig.set_size_inches(5.5, len(dkeys) * 2.)
    
    for i, dkey in enumerate(dkeys):
        ax, d = axes[i], data[dkey]

        ax.set_ylabel(r"$L_{\mathrm{bol}}\ \mathrm{[erg \cdot s^{-1}]}$")
        if i < len(dkeys)-1:
            ax.axes.xaxis.set_ticklabels([])
        else:
            ax.set_xlabel(r"$t\ \mathrm{[s]}$")
        #  ax.xaxis.set_tick_params(width=1, length=7, direction="in")
        #  ax.yaxis.set_tick_params(width=1, length=7, direction="in", which="both")

        ax.plot(d[:,0], d[:,4], color="black", linewidth=1.) 
    fig.savefig(plot_file, bbox_inches="tight", format=Path(plot_file).suffix[1:])

def main() -> None:
    parser = ArgumentParser()

    parser.add_argument("--data_file", type=str)
    parser.add_argument("--plot_file", type=str)
    parser.add_argument("--dkeys", action=parse_csvarg, default=[], help="")

    args = parser.parse_args()

    plot(args.plot_file, args.data_file, args.dkeys)

if __name__ == '__main__':
    main()
