from itertools import product

from numpy import dot, tensordot, zeros

from solvers.basis import DERVALS
from solvers.split.analytical import ode_stepper_analytical
from solvers.split.numerical import ode_stepper_numerical
from system import Bdot, flux, system
from options import NV, N, NDIM, NUM_ODE


def ode_launcher(u, dt, MP, USE_JAC=False):
    if NUM_ODE:
        ode_stepper_numerical(u, dt, MP, USE_JAC=USE_JAC)
    else:
        ode_stepper_analytical(u, dt, MP)


def derivative(X, dX, dim):
    """ Returns the derivative of polynomial coefficients X with respect to
        dimension dim. X can be of shape (N,...) or (N,N,...)
    """
    if dim == 0:
        return tensordot(DERVALS, X, (1, 0)) / dX[0]
    elif dim == 1:
        return tensordot(DERVALS, X, (1, 1)).swapaxes(0, 1) / dX[1]


def weno_midstepper(wh, dt, dX, MP):
    """ Steps the WENO reconstruction forwards by dt/2, under the homogeneous system
    """
    USE_JACOBIAN = 0

    nx, ny, nz = wh.shape[:3]

    F = zeros([N] * NDIM + [NV])
    G = zeros([N] * NDIM + [NV])
    Bdwdx = zeros(NV)
    Bdwdy = zeros(NV)

    for i, j, k in product(range(nx), range(ny), range(nz)):

        w = wh[i, j, k]
        dwdx = derivative(w, dX, 0)

        if NDIM == 1:

            if USE_JACOBIAN:
                for a in range(N):
                    Mx = system(w[a], 0, MP)
                    w[a] -= dt / 2 * dot(Mx, dwdx[a])
            else:
                for a in range(N):
                    F[a] = flux(w[a], 0, MP)
                dFdx = derivative(F, dX, 0)
                for a in range(N):
                    Bdot(Bdwdx, dwdx[a], w[a], 0, MP)
                    w[a] -= dt / 2 * (dFdx[a] + Bdwdx)

        elif NDIM == 2:

            dwdy = derivative(w, dX, 1)

            if USE_JACOBIAN:
                for a, b in product(range(N), range(N)):
                    Mx = system(w[a, b], 0, MP)
                    My = system(w[a, b], 1, MP)
                    w[a, b] -= dt / 2 * \
                        (dot(Mx, dwdx[a, b]) + dot(My, dwdy[a, b]))
            else:
                for a, b in product(range(N), range(N)):
                    F[a, b] = flux(w[a, b], 0, MP)
                    G[a, b] = flux(w[a, b], 1, MP)
                dFdx = derivative(F, dX, 0)
                dGdy = derivative(G, dX, 1)
                for a, b in product(range(N), range(N)):
                    Bdot(Bdwdx, dwdx[a, b], w[a, b], 0, MP)
                    Bdot(Bdwdy, dwdy[a, b], w[a, b], 1, MP)
                    w[a, b] -= dt / 2 * \
                        (dFdx[a, b] + dGdy[a, b] + Bdwdx + Bdwdy)