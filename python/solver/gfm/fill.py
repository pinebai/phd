from itertools import product

from numpy import array, logical_or, maximum, mean, ones, prod, zeros
from skfmm import distance

from ader.etc.boundaries import neighbor_cells

from gpr.multi import get_material_index
from gpr.multi.riemann import star_states
from solver.gfm.functions import finite_difference, normal, sign


def find_interface_cells(φ):
    """ Finds the cells lying on the interface of material i of m
        intMask = -1 on the inside and intMask = 1 on the outside
    """
    shape = φ.shape
    NDIM = φ.ndim
    intMask = zeros(shape)

    for indsL in product(*[range(s) for s in shape]):

        for d in range(NDIM):

            if indsL[d] < shape[d] - 1:

                indsR = indsL[:d] + (indsL[d] + 1,) + indsL[d + 1:]

                φL = φ[indsL]
                φR = φ[indsR]

                if φL * φR <= 0:
                    intMask[indsL] = sign(φL)
                    intMask[indsR] = sign(φR)

    return intMask


def boundary_inds(ind, φ, n, dX):
    """ Calculates indexes of the boundary states at position given by ind
    """
    xp = (array(ind) + 0.5) * dX

    d = 1.5

    xi = xp - φ[ind] * n               # interface position
    xL = xi - d * dX * n               # probe on left side
    xR = xi + d * dX * n               # probe on right side
    x_ = xi - dX * sign(φ[ind]) * n    # point on opposite side of interface

    # TODO: replace with interpolated values
    ii = array(xi / dX, dtype=int)
    iL = array(xL / dX, dtype=int)
    iR = array(xR / dX, dtype=int)
    i_ = array(x_ / dX, dtype=int)

    return ii, iL, iR, i_


def fill_boundary_cells(u, grid, intMask, mat, φ, Δφ, dX, MPs, dt):

    MPL = MPs[mat]

    for ind in product(*[range(s) for s in intMask.shape]):

        if intMask[ind] == -1:

            n = normal(Δφ[ind])
            ii, iL, iR, i_ = boundary_inds(ind, φ, n, dX)

            QL = u[tuple(iL)]
            QR = u[tuple(iR)]

            MPR = MPs[get_material_index(QR, len(MPs))]
            QL_, QR_ = star_states(QL, QR, MPL, MPR, dt, n)

            grid[tuple(ii)] = QL_
            grid[tuple(i_)] = QL_


def fill_from_neighbor(grid, Δφ, ind, dX, sgn):
    """ makes the value of cell ind equal to the value of its neighbor in the
        direction of the interface
        TODO: replace with interpolated values
    """
    n = normal(Δφ[ind])
    x = (array(ind) + 0.5) * dX
    xn = x + sgn * mean(dX) * n
    grid[ind] = grid[tuple(array(xn / dX, dtype=int))]


def fill_neighbor_cells(grid, intMask, Δφ, dX, N):

    shape = intMask.shape
    inds = [range(s) for s in shape]

    for N0 in range(1, N + 1):
        for ind in product(*inds):

            if intMask[ind] == 0:

                neighbors = neighbor_cells(intMask, ind)

                if N0 in neighbors:
                    intMask[ind] = N0 + 1
                    fill_from_neighbor(grid, Δφ, ind, dX, -1)


def renormalize_levelsets(u, nmat, dX, ncells):

    for i in range(nmat - 1):
        ind = i - (nmat - 1)
        φ = u.take(ind, axis=-1)
        u.reshape([ncells, -1])[:, ind] = distance(φ, dx=dX).ravel()


def material_indicator(u, mat, nmat, dX):

    φs = [-u.take(i - (nmat-1), axis=-1) for i in range(mat)] + \
            [u.take(i - (nmat-1), axis=-1) for i in range(mat, nmat-1)]

    if len(φs) > 1:
        φ = maximum(*φs)
        return distance(φ, dx=dX)
    else:
        return φs[0]


def fill_ghost_cells(u, nmat, N, dX, MPs, dt):

    ncells = prod(u.shape[:-1])
    renormalize_levelsets(u, nmat, dX, ncells)
    grids = [u.copy() for mat in range(nmat)]
    masks = [ones(u.shape[:-1], dtype=bool) for mat in range(nmat)]

    for mat in range(nmat):

        if MPs[mat].EOS > -1:  # not a vacuum

            φ = material_indicator(u, mat, nmat, dX)
            Δφ = finite_difference(φ, dX)
            intMask = find_interface_cells(φ)

            grid = grids[mat]
            fill_boundary_cells(u, grid, intMask, mat, φ, Δφ, dX, MPs, dt)
            fill_neighbor_cells(grid, intMask, Δφ, dX, N)

            masks[mat] *= logical_or((φ <= 0), (intMask == 1))

            grid.reshape([ncells, -1])[:, - (nmat - 1):] = u.reshape([ncells, -1])[:, - (nmat - 1):]

    return grids, masks
