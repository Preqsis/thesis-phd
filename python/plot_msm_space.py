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
    data = solve(0.146, t_end=400.)

    #  fig = plt.figure()
    #  ax = fig.add_subplot(projection='3d')
#
    fig, ax = plt.subplots(1, 2) 
    plt.subplots_adjust(
        left=0.08,
        bottom=0.16,
        right=.98,
        top=0.95,
        wspace=0.02
    )
    fig.set_size_inches(5.55, 3.)


    ax[0].plot(data[:,1], data[:,3], "black", marker="o", markersize=.05, linewidth=0.)
    ax[1].plot(data[:,2], data[:,3], "black", marker="o", markersize=.05, linewidth=0.)

    ax[0].set_xlabel(r"$z$")
    ax[0].set_ylabel(r"$m$")
    ax[1].set_xlabel(r"$\dot{z}$")

    ax[1].set_yticks(())
    ax[0].set_xlim((-3., 7.))
    ax[1].set_xlim((-11., 11.))

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
