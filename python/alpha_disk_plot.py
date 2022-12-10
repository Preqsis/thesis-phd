import numpy as np
import matplotlib.pyplot as plt

from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 11})

def _alpha_H(a, Q, R_10, m_1, R_m) -> float:
    M_16 = Q * 1e-16
    f = (1. - (R_m / R_10)**(0.5))**(0.25)
    H = 1.7e8 * a**(-0.1) * M_16**(3./20.) * m_1**(-3./8.) * R_10**(9./8.) * f**(3./5.)
    return H
alpha_H = np.vectorize(_alpha_H)

def _alpha_T(a, Q, R_10, m_1, R_m) -> float:
    M_16 = Q * 1e-16
    f = (1. - (R_m / R_10)**(0.5))**(0.25)
    T = 1.4e4 * a**(-0.7) * M_16**(3./10.) * m_1**(1./4.) * R_10**(-3./4.) * f**(6./5.)
    return T
alpha_T = np.vectorize(_alpha_T)

def plot(plot_file) -> None:
    M_sun = 1.9891e33
    G = 6.67259e-12
    r_in = 5e8
    r_out = 50 * r_in
    r = np.linspace(r_in, 40 * r_in, 500)
    R_10 = r * 1e-10
    alphas = [.1, .5, .95]
    labels = [r"$\alpha = 0.1$", r"$\alpha = 0.5$", r"$\alpha = 0.95$"]

    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(
            left=0.07,
            bottom=0.16,
            right=0.98,
            top=0.9,
            wspace=0.26,
            hspace=0.0
            )
    fig.set_size_inches(5.55, 2.8)

    for i, a in enumerate(alphas):
        ax[0].plot(R_10, alpha_T(a, 1e14, R_10, 0.8, R_10[0]) / 1e4, label = labels[i], linewidth=1.)
        ax[1].plot(R_10, alpha_H(a, 1e14, R_10, 0.8, R_10[0]) / 1e8, linewidth = 1.)
        
    ax[0].set_xlabel(r"$R_{10}\ [10^{10} \mathrm{cm}]$")
    ax[1].set_xlabel(r"$R_{10}\ [10^{10} \mathrm{cm}]$")

    ax[0].set_ylabel(r"$T_\mathrm{c}\ [10^4 \mathrm{K}]$")
    ax[1].set_ylabel(r"$H\ [10^8 \mathrm{cm}]$")

    lines, labels = ax[0].get_legend_handles_labels()
    leg = fig.legend(lines, labels, ncol=3, loc="upper left", frameon=False, bbox_to_anchor=(0.18,1.05))
    
    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    args = parser.parse_args()
    plot(args.plot_file)

if __name__ == '__main__':
    main()
