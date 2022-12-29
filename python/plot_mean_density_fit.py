import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser, Action
from pathlib import Path
from h5py import File
from scipy.optimize import curve_fit

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

class parse_csvarg(Action):
    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, [v for v in values.split(",")])

def area_density(r, a):
    Q = 1e14
    m_1 = 0.63
    M_16 = Q * 1e-16
    R_10 = r * 1e-10
    f = (1. - (r[-1] / r)**(0.5))**(0.25)
    return 5.2 * a**(-4./5.) * M_16**(7./10.) * m_1**(1./4.) * R_10**(-3./4.) * f**(14./5.)

def plot(plot_file: str, data_files: list, ids: list) -> None:
    fig, axes = plt.subplots(len(data_files), 1) 
    plt.subplots_adjust(
        left=0.08,
        bottom=0.1,
        right=0.95,
        top=0.97,
        wspace=0.15,
        hspace=0.2
    )
    fig.set_size_inches(5.5, 8.5)

    for di, data_file in enumerate(data_files):
        attrs, ax = {}, axes[di]
        with File(data_file, "r") as f:
            data = None
            for key, value in f.attrs.items():
                attrs[key] = value
            
            for i in range(2000, 2200, 1):
                try:
                    data += f[f"d{i}"][()]
                    n += 1
                except:
                    data = f[f"d{i}"][()]
                    n = 1
        data /= n

        r_in, r_out = attrs["r_in"]*R_sun, attrs["r_out"]*R_sun
        idim, jdim = attrs["idim"], attrs["jdim"]
        qs = attrs["qs"] * 10
        S = np.zeros_like(data[:,:,5])
        idx = np.arange(0, idim, 1)
        r = r_in + (idim - idx - 1) * (r_out - r_in) / (idim - 1) 
        for i in idx:
            S[i,:] = r[i] * 2. * np.pi * (r[0] - r[1]) / jdim

        m = data[:,:,5]
        density = m * qs / S
        mean_density = density.mean(axis=1)

        init_vals = [0.5]
        best_vals, covar = curve_fit(area_density, r[1:-2], mean_density[1:-2], p0=init_vals, bounds=((0., 2.)))

        alpha = best_vals[0]
        error = np.sqrt(np.diag(covar))[0]
        print("alpha:", alpha, ", error:", error)

        rcon = np.linspace(r[1], r[-3], 500)
        ax.plot(r[1:-2] / 1e10, mean_density[1:-2], color="black", linewidth=0., marker="o", markersize=2.)
        ax.plot(rcon / 1e10, area_density(rcon, alpha), linewidth=1., linestyle="dotted")
        ax.set_title(r"${0}:\ \alpha = ({1:.3f} \pm {2:.3f})$".format(ids[di], alpha, error))

        if di < len(data_files)-1:
            ax.axes.xaxis.set_ticklabels([])
        else:
            ax.set_xlabel(r"$R_{10}\ [10^{10} \mathrm{cm}]$");
        ax.set_ylabel(r"$\bar{\Sigma}\ [\mathrm{g} \cdot \mathrm{cm}^{-2}]$")
        ax.xaxis.set_tick_params(direction="in")
        ax.yaxis.set_tick_params(direction="in", which="both")
        
    fig.savefig(plot_file, bbox_inches="tight", format=Path(plot_file).suffix[1:])

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    parser.add_argument("--data_files", action=parse_csvarg, default=[], help="")
    parser.add_argument("--ids", action=parse_csvarg, default=[], help="")
    args = parser.parse_args()
    plot(args.plot_file, args.data_files, args.ids)

if __name__ == '__main__':
    main()
