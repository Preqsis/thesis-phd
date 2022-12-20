import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 11})

def plot(plot_file: str, data) -> None:
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.subplots_adjust(
        left=0.05,
        bottom=0.08,
        right=0.98,
        top=0.97,
        wspace=0.09,
        hspace=0.09
    )
    fig.set_size_inches(11.7, 6.7)
    
    
    ax.plot(data[:,0], data[:,1], "black", linewidth=0., marker="o", markersize=.5)
    
    ax.set_xlabel(r"$v_0$")
    ax.set_ylabel(r"$T_{n}$", rotation=0)

    ax.set_xlim((0.13, 0.18))

    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--data_file", type=str)
    parser.add_argument("--plot_file", type=str)
    args = parser.parse_args()

    data = np.load(args.data_file)
    
    plot(args.plot_file, data)

if __name__ == '__main__':
    main()
