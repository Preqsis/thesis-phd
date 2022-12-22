
import cairo
import IPython
import PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from io import BytesIO, StringIO
from h5py import File
from argparse import Action, ArgumentParser

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Computer Modern"],
    "font.size": 10})

R_SUN = 6.957e10

def render_disc(data, idim, jdim, w=1920, h=1080, cmap=None, r_in=0.1, r_out=0.45, 
        val_index=5, bg_rgb=(0, 0, 0), 
        return_surface=False, skip_empty=False, log_norm=False,
        scf=1.0, limits=(1e-9, 10.)
        ):
    colormap = plt.cm.get_cmap("inferno" if cmap is None else cmap)

    if log_norm:
        low = limits[0]
        high = limits[1]
    else:
        low = 0.
        high = np.max(data[:,:,val_index])

    print(low, high)

    dr = (r_out - r_in) / idim

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surface)
    c.scale(h, h)

    c.set_source_rgb(*bg_rgb)
    c.paint()
    c.save()
    c.restore()

    c.set_line_width(1.02 * dr)
    
    dphi = 2. * np.pi / jdim

    r = r_out
    for i in range(idim):
        for j in range(jdim):
            val, azm = data[i][j][val_index] * scf, data[i][j][8] % (2. * np.pi)

            if val == 0. and skip_empty:
                continue
            
            if log_norm:
                rgba = colormap(np.clip(np.log10(val), low, high) / (high - low))
            else:
                rgba = colormap(np.clip(val, low, high) / (high - low))

            c.arc(0.495, 0.5, r, azm, azm+dphi*1.02)
            c.set_source_rgb(rgba[0], rgba[1], rgba[2])  # Solid color
            c.stroke()

        r -= dr

    c.set_line_width(dr * 0.15)
    c.arc(0.495, 0.5, r_out + 0.6 * dr, 0., 2. * np.pi)
    c.set_source_rgb(0, 0, 0)
    c.stroke()

    c.arc(0.495, 0.5, r_in + 0.4 * dr, 0., 2. * np.pi)
    c.set_source_rgb(0, 0, 0)
    c.stroke()

    if return_surface:
        return surface

    buff = BytesIO()
    surface.write_to_png(buff)
    imdata = buff.getvalue()
    buff.close()

    surface.finish()

    return imdata

def plot(data: np.ndarray, plot_file: str, attrs: any) -> None:
    idim, jdim, kdim = data.shape
    r0, r1 = 0.1, 0.48
    surfaces = {}
    cmaps = ("viridis", "inferno")
    width, height = 1500, 1500
    limits = (0., 0.12)
    log_limits = (1., 5.5)

    r_in = attrs["r_in"] * R_SUN
    r_out = attrs["r_out"] * R_SUN
    qs = attrs["qs"]

    S = np.zeros_like(data[:,:,5])
    idx = np.arange(0, idim, 1)
    r   = r_in + (idim - idx - 1) * (r_out - r_in) / (idim - 1) 
    for i in idx:
        S[i,:] = r[i] * 2. * np.pi * (r[0] - r[1]) / jdim
    data[:,:,5] = data[:,:,5] * qs / S

    #density distribution
    surfaces["density"] = render_disc(
            data,
            idim, jdim,
            r_in=r0, r_out=r1,
            w=width, h=height,
            return_surface=True,
            bg_rgb=(1,1,1),
            val_index=5,
            skip_empty=True,
            cmap=cmaps[0],
            limits=limits
            )

    # temprature distribution
    surfaces["temperature"] = render_disc(
            data,
            idim, jdim,
            r_in=r0, r_out=r1,
            w=width, h=height,
            return_surface=True,
            bg_rgb=(1,1,1),
            val_index=10,
            cmap=cmaps[1],
            skip_empty=True,
            log_norm=True,
            limits=log_limits
            )

    fig, ax = plt.subplots(1, 2)
    plt.subplots_adjust(
            left=0.03,
            bottom=0.0,
            right=0.97,
            top=1.18,
            wspace=0.0,
            hspace=0.0
            )
    fig.set_size_inches(7, 4.)

    buff = BytesIO()
    surfaces["density"].write_to_png(buff)
    ms = np.array(PIL.Image.open(buff))

    buff = BytesIO()
    surfaces["temperature"].write_to_png(buff)
    ts = np.array(PIL.Image.open(buff))

    ms_img = ax[0].imshow(ms)
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    ax[0].axis("off")

    ts_img = ax[1].imshow(ts)
    ax[1].set_xticks([])
    ax[1].set_yticks([])
    ax[1].axis("off")

    dens_map = plt.cm.ScalarMappable(cmap=cmaps[0], norm=mpl.colors.Normalize(vmin=limits[0], vmax=limits[1]))
    dens_map.set_array(np.clip(data[:,:,5], limits[0], limits[1]))
    axins_0 = inset_axes(ax[0], width="80%", height="5%", loc='lower center', borderpad=-1.7)
    cb1 = fig.colorbar(dens_map, cax=axins_0, orientation="horizontal")
    cb1.set_label(label="$\Sigma\ \mathrm{[g \cdot cm^{-2}]}$")

    temp_map = plt.cm.ScalarMappable(
        cmap=cmaps[1], 
        norm=mpl.colors.LogNorm(
            vmin=np.power(10., log_limits[0]), vmax=np.power(10., log_limits[1])
        )
    )
    temp_map.set_array(
        np.clip(data[:,:,10], np.power(10., log_limits[0]), np.power(10., log_limits[1]) )
    )
    axins_1 = inset_axes(ax[1], width="80%", height="5%", loc='lower center', borderpad=-1.7)
    cb2 = fig.colorbar(temp_map, cax=axins_1, orientation="horizontal")
    cb2.set_label(label="$T\ \mathrm{[K]}$")

    fig.savefig(plot_file, dpi=600, format="pdf")
    plt.close(fig)

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--data_file", type=str)
    parser.add_argument("--plot_file", type=str)
    parser.add_argument("--dkey", type=str)
    #  parser.add_argument("--r_in", type=float)
    #  parser.add_argument("--r_out", type=float)
    #  parser.add_argument("--qs", type=float)
    args = parser.parse_args()

    with File(args.data_file) as f:
        frame = f[args.dkey]
        plot(frame[()], args.plot_file, frame.attrs)

if __name__ == "__main__":
    main()
