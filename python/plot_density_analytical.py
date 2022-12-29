import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pathlib import Path

M_sun = 1.9891e33
R_sun = 6.957e+10
G = 6.67259e-12

r_in = 0.01 * R_sun
r_out = 1.16 * R_sun

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 10})

def area_density(r, a):
    Q = 1e14
    m_1 = 0.63
    M_16 = Q * 1e-16
    R_10 = r * 1e-10
    f = (1. - (r[-1] / r)**(0.5))**(0.25)
    return 5.2 * a**(-4./5.) * M_16**(7./10.) * m_1**(1./4.) * R_10**(-3./4.) * f**(14./5.)

def plot(plot_file: str) -> None:
    alphas = [.1, .5, .95]
    labels = [r"$\alpha = 0.1$", r"$\alpha = 0.5$", r"$\alpha = 0.95$"]

    fig, ax = plt.subplots(1, 1) 
    fig.set_size_inches(5.5, 5.9)

    r = np.linspace(r_out, r_in, 500)

    for i, a in enumerate(alphas):
        ax.plot(r / 1e10, area_density(r, a), linewidth=1., label = labels[i]) 

    ax.set_xlabel(r"$R_{10}\ [10^{10} \mathrm{cm}]$")
    ax.set_ylabel(r"$\Sigma\ [\mathrm{g} \cdot \mathrm{cm}^{-2}]$")
    ax.xaxis.set_tick_params(direction="in")
    ax.yaxis.set_tick_params(direction="in", which="both")
    
    lines, labels = ax.get_legend_handles_labels()
    leg = fig.legend(lines, labels, ncol=3, loc="upper left", frameon=False, bbox_to_anchor=(0.18,0.95))

    fig.savefig(plot_file, bbox_inches="tight", format=Path(plot_file).suffix[1:])

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    args = parser.parse_args()
    plot(args.plot_file)

if __name__ == '__main__':
    main()
