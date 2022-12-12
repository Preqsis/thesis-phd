import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 11})

def f_r(i, r_in, r_out):
    return r_in + (i.shape[0] - i - 1) * (r_out - r_in) / (i.shape[0] - 1)

def f_gravity(i, r_in, r_out):
    r = f_r(i, r_in, r_out)
    return (r[0]/r)**2.

def f_omega(i, r_in, r_out):
    r = f_r(i, r_in, r_out)
    return (r[0]/r)**(3./2.)

def plot(plot_file: str, idim: int) -> None:
    M_sun = 1.9891e33
    G = 6.67259e-12
    r_in = 5e8
    r_out = 50 * r_in
    i = np.arange(0, idim, 1)

    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(
            left=0.1,
            bottom=0.16,
            right=0.98,
            top=0.95,
            wspace=0.26,
            hspace=0.0
            )
    fig.set_size_inches(5.55, 2.8)

    ax[0].plot(i, f_gravity(i, r_in, r_out), "red", linewidth=1.)
    ax[1].plot(i, f_omega(i, r_in, r_out), "blue", linewidth=1.)

    ax[0].set_yscale("log")
    ax[1].set_yscale("log")

    ax[0].invert_xaxis()
    ax[1].invert_xaxis()

    ax[0].xaxis.set_tick_params(direction="in")
    ax[0].yaxis.set_tick_params(direction="in", which="both")
    ax[1].xaxis.set_tick_params(direction="in")
    ax[1].yaxis.set_tick_params(direction="in", which="both")

    ax[0].set_ylim((0.5, 4000.))
    ax[1].set_ylim((0.5, 4000.))

    ax[0].set_ylabel(r"$f_{\mathrm{g}}[\mathrm{arbitrary\ units}]$")
    ax[1].set_ylabel(r"$f_{\omega}[\mathrm{arbitrary\ units}]$")

    ax[0].set_xlabel(r"layer index $i$")
    ax[1].set_xlabel(r"layer index $i$")

    ax[0].set_xticks(i[::4])
    ax[1].set_xticks(i[::4])
    
    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    parser.add_argument("--idim", type=int)
    args = parser.parse_args()
    plot(args.plot_file, args.idim)

if __name__ == '__main__':
    main()
