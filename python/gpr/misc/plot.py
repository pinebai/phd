import matplotlib.pyplot as plt
import matplotlib.animation as animation

from numpy import arange, flipud, linspace, mgrid, zeros
from matplotlib.pyplot import colorbar, figure, get_cmap, imshow, plot, scatter
from matplotlib.pyplot import streamplot, ticklabel_format, xlabel, ylabel, xlim

from gpr.misc.structures import Cvec_to_Pclass
from multi.gfm import get_material_index
from solvers.basis import NODES, PSI

from options import nx, ny, ndim


def plot1d(y, style, x, lab, col, ylab, xlab='x', sci=1):

    if x is None:
        x = arange(len(y)) + 0.5

    if style == '-':
        plot(x, y, label=lab, color=col, linewidth=1)

    elif style == '.':
        scatter(x, y, label=lab, color=col)

    elif style == 'x':
        scatter(x, y, marker='x', s=10, label=lab, color=col, linewidth=1)

    xlim(x[0], x[-1])

    if sci:
        ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    xlabel(xlab)
    ylabel(ylab)
    plt.show()


def plot2d(x, style, y=None):
    if style == 'colormap':
        im = imshow(y, get_cmap('viridis'))
        colorbar(im)
    elif style == 'streams':
        Y, X = mgrid[0:nx, 0:ny]
        streamplot(X, Y, flipud(y), flipud(x))


def plot_density(u, style='-', x=None, lab=None, col=None, sci=0):
    figure(0, figsize=(10, 10))
    if ndim == 1:
        y = u[:, 0, 0, 0]
        plot1d(y, style, x, lab, col, 'Density', sci=sci)
    elif ndim == 2:
        y = u[:, :, 0, 0]
        plot2d(y, 'colormap')


def plot_energy(u, style='-', x=None, lab=None, col=None, sci=0):
    figure(1, figsize=(10, 10))
    if ndim == 1:
        y = u[:, 0, 0, 1] / u[:, 0, 0, 0]
        plot1d(y, style, x, lab, col, 'Total Energy', sci=sci)
    elif ndim == 2:
        y = u[:, 0, :, 1] / u[:, 0, :, 0]
        plot2d(y, 'colormap')


def plot_velocity(u, i=0, style='-', x=None, lab=None, col=None, sci=0,
                  offset=0, dims=None):
    figure(2 + i, figsize=(10, 10))
    if dims == None:
        dims = ndim
    if dims == 1:
        y = u[:, 0, 0, 2 + i] / u[:, 0, 0, 0] + offset
        plot1d(y, style, x, lab, col, 'Velocity Component %d' % (i + 1),
               sci=sci)
    elif dims == 2:
        x = u[:, :, 0, 2] / u[:, :, 0, 0] + offset
        y = u[:, :, 0, 3] / u[:, :, 0, 0] + offset
        plot2d(x, 'streams', y)


def plot_distortion(u, i, j, style='-', x=None, lab=None, col=None, sci=0):
    figure(5 + i * 3 + j, figsize=(10, 10))
    y = u[:, 0, 0, 5 + 3 * j + i]
    plot1d(y, style, x, lab, col, 'Distortion Component %d,%d' % (i + 1, j + 1),
           sci=sci)


def plot_thermal_impulse(u, i, style='-', x=None, lab=None, col=None, sci=0):
    figure(14 + i, figsize=(10, 10))
    y = u[:, 0, 0, 14 + i] / u[:, 0, 0, 0]
    plot1d(y, style, x, lab, col, 'Thermal Impulse Component %d' % (i + 1),
           sci=sci)


def plot_concentration(u, style='-', x=None, lab=None, col=None, sci=0):
    figure(18, figsize=(10, 10))
    y = u[:, 0, 0, 17] / u[:, 0, 0, 0]

    plot1d(y, style, x, lab, col, 'Concentration', sci=sci)


def plot_pressure(u, MPs, style='-', x=None, lab=None, col=None, sci=0):
    figure(19, figsize=(10, 10))
    n = len(u)
    y = zeros(n)

    for i in range(n):
        Q = u[i, 0, 0]
        j = get_material_index(Q, MPs)
        y[i] = Cvec_to_Pclass(Q, MPs[j]).p()

    plot1d(y, style, x, lab, col, 'Pressure', sci=sci)


def plot_temperature(u, MPs, style='-', x=None, lab=None, col=None, sci=0):
    figure(20, figsize=(10, 10))
    n = len(u)
    y = zeros(n)

    for i in range(n):
        Q = u[i, 0, 0]
        j = get_material_index(Q, MPs)
        y[i] = Cvec_to_Pclass(Q, MPs[j]).T()

    plot1d(y, style, x, lab, col, 'Temperature', sci=sci)


def plot_sigma(u, i, j, MPs, style='-', x=None, lab=None, col=None, sci=0):
    figure(21 + i * 3 + j, figsize=(10, 10))
    n = len(u)
    y = zeros(n)

    for k in range(n):
        Q = u[k, 0, 0]
        j = get_material_index(Q, MPs)
        y[k] = Cvec_to_Pclass(Q, MPs[j]).σ()[i, j]

    plot1d(y, style, x, lab, col,
           'Viscous Stress Component %d,%d' % (i + 1, j + 1), sci=sci)


def plot_heat_flux(u, i, MPs, style='-', x=None, lab=None, col=None, sci=0):
    figure(30 + i, figsize=(10, 10))
    n = len(u)
    y = zeros(n)

    for k in range(n):
        Q = u[k, 0, 0]
        j = get_material_index(Q, MPs)
        y[k] = Cvec_to_Pclass(Q, MPs[j]).q()[i]

    plot1d(y, style, x, lab, col, 'Heat Flux Component %d' % (i + 1), sci=sci)


def plot_variable(u, var, style='-', x=None, lab=None, col=None, sci=0):
    figure(34, figsize=(10, 10))
    y = u[:, 0, 0, var]
    plot1d(y, style, x, lab, col, 'Variable %d' % var, sci=sci)


def plot_primitives(u, MPs, style='-', x=None):
    plot_density(u, style=style, x=x)
    plot_velocity(u, 0, style=style, x=x)
    plot_pressure(u, MPs, style=style, x=x)


def plot_interfaces(u, figNum=None, loc=None, col=None):
    # use axvline
    return "Not implemented"


def colors(n):
    cmap = get_cmap('viridis')
    return [cmap.colors[i] for i in linspace(0, 255, n, dtype=int)]


def plot_weno(wh, var, MPs=None):
    n, _, _, N, nV = wh.shape
    x = zeros(N * n)
    u = zeros([N * n, 1, 1, nV])
    for i in range(n):
        ind = N * i
        for j in range(N):
            x[ind + j] = i + NODES[j]
            u[ind + j] = wh[i, 0, 0, j]

    if var == 'density':
        plot_density(u, x=x)
    if var == 'energy':
        plot_energy(u, x=x)
    if var == 'velocity':
        plot_velocity(u, x=x)
    if var == 'pressure':
        plot_pressure(u, MPs, x=x)


def plot_dg(qh, var, t, MPs=None):
    n, _, _, N, _, nV = qh.shape
    wh = zeros([n, 1, 1, N, nV])
    for i in range(n):
        for j in range(N):
            for k in range(N):
                wh[i, 0, 0, j] += PSI[k](t) * qh[i, 0, 0, k, j]

    plot_weno(wh, var, MPs)


def plot_res_ref(res, ref, x=None, reflab='Reference', reslab='Results'):
    cm = colors(3)
    if x is not None:
        plot(x, res, col=cm[1], label=reslab, marker='x', linestyle='none',
             markersize=5)
        plot(x, ref, col=cm[0], label=reflab, linewidth=1)
    else:
        plot(res, col=cm[1], label=reslab, marker='x', linestyle='none',
             markersize=5)
        plot(ref, col=cm[0], label=reflab, linewidth=1)


def anim(data, var):
    fig = figure()

    im = imshow(data[0][:, :, 0, var])

    def animate(i):
        im.set_array(data[i][:, :, 0, var])
        return im,

    return animation.FuncAnimation(fig, animate, interval=200, repeat=True)