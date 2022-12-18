import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from argparse import ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 11})

def odes(y, s):
    return np.array([np.sin(y[2]), (-1.)*np.cos(y[2]), (np.cos(y[2]) / y[0]) - y[1]])

def create_faucet(raidus: float):
    return np.array(
        (
            (0., 0.),
            (0., .5),
            (.3, .5),
            (.3, 0.)
        )
    )

def corect_for_faucet(data, faucet_radius):
    m = data[:,0] <= faucet_radius
    data = data[m]
    dz = .5 - data[-1,1]
    data[:,1] += dz
    return data

def solve(p):
    y0 = np.array((1e-20, p, np.radians(90.)))
    s = np.linspace(0., 8., 2000)
    data, info = sp.integrate.odeint(odes, y0, s, full_output=True)
    return data

def plot_eq(plot_file: str, faucet_radius: float = None) -> None:
    data = [ 
        {"p": .5},
        {"p": 1.},
        {"p": 1.5},
        {"p": 2.},
        {"p": 2.5},
        {"p": 3.},
        {"p": 3.5},
        {"p": 4.},
        {"p": 4.5}
    ]

    for d in data:
        d["data"] = solve(d["p"])    
        d["data"] = corect_for_faucet(d["data"], faucet_radius)

    fig, ax = plt.subplots(3, 3)
    plt.subplots_adjust(
        left=0.08,
        bottom=0.1,
        right=0.95,
        top=0.97,
        wspace=0.09,
        hspace=0.09
    )
    fig.set_size_inches(5.55, 5.55)

    for k, d in enumerate(data):
        j = k % 3
        i = int(k / 3)
        a = ax[i, j]
        dat = d["data"]

        if faucet_radius is not None:
            faucet = create_faucet(0.9)
            a.plot(faucet[:,0]+faucet_radius, faucet[:,1], "black", linewidth=1)
            a.plot(faucet[:,0]-faucet_radius-.3, faucet[:,1], "black", linewidth=1)

        a.plot(dat[:,0], dat[:,1], "blue", linewidth=1)
        a.plot((-1.)*dat[:,0], dat[:,1], "blue", linewidth=1)
        a.set_xlim((-2.5, 2.5))
        a.set_ylim((0., 5.))
        a.invert_yaxis()
        if i != 2:
            a.set_xticks([])
        else:
            a.set_xlabel("$r$")
        if j != 0:
            a.set_yticks([])
        else:
            a.set_ylabel("$z$")

        a.text(-2.3, 4.7, r"$P_{\mathrm{b}}=" + str(d["p"]) + r"$")
    
    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def plot_pv(plot_file: str, faucet_radius: float = None) -> None:
    pb = np.arange(1e-20, 6, 0.01)
    pv = np.empty((pb.shape[0], 2))
    for i, p in enumerate(pb):
        data = solve(p)
        if faucet_radius:
            data = corect_for_faucet(data, faucet_radius)
        else:
            data = data[data[:,1]>0.]

        h = np.abs(data[:-1,1] - data[1:,1])
        v = np.sum(h * data[:-1,0]**2. * np.pi)
        pv[i,0] = p
        pv[i,1] = v

    pv_max = pv[pv[:,1] == pv[:,1].max()]
    print(pv_max)
    
    fig, ax = plt.subplots(1, 1)
    plt.subplots_adjust(
        left=0.07,
        bottom=0.15,
        right=0.98,
        top=0.97,
        wspace=0.09,
        hspace=0.09
    )
    fig.set_size_inches(5.55, 3.)

    ax.plot(pv[:,0], pv[:,1], "black", marker="o", markersize=0.8, linewidth=0.)
    ax.set_xlabel(r"$P_{\mathrm{b}}$")
    ax.set_ylabel(r"$V_{\mathrm{d}}$")
    
    ax.xaxis.set_tick_params(direction="in")
    ax.yaxis.set_tick_params(direction="in", which="both")

    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--plot_file", type=str)
    parser.add_argument("--faucet_radius", type=float)
    parser.add_argument("--eq", action="store_true")
    parser.add_argument("--pv", action="store_true")
    args = parser.parse_args()

    if args.eq:
        plot_eq(args.plot_file, args.faucet_radius)

    if args.pv:
        plot_pv(args.plot_file, args.faucet_radius)

if __name__ == '__main__':
    main()
