import numpy as np
import matplotlib.pyplot as plt
from msmm import solve
from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 11})

def plot(plot_file: str) -> None:
    data = solve(0.146, t_end=500.)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    #  fig, ax = plt.subplots(1, 2, projection='3d')
    plt.subplots_adjust(
        left=0.0,
        bottom=0.1,
        right=0.9,
        top=0.97,
        wspace=0.09,
        hspace=0.09
    )
    fig.set_size_inches(5.55, 5.55)

    ax.plot(data[:,1], data[:,2], data[:,3], "navy", marker="o", markersize=.1, linewidth=0.)

    ax.set_xlabel(r"$z$")
    ax.set_ylabel(r"$\dot{z}$")
    ax.set_zlabel(r"$m$")

    ax.view_init(20, -45)

    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)
    #  plt.show()
    

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    args = parser.parse_args()

    plot(args.plot_file)

if __name__ == '__main__':
    main()
