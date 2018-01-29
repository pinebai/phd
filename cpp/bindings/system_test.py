import GPRpy

from numpy import zeros
from numpy.random import rand

from test_functions import diff, generate_vector

from system import flux_ref, source_ref, block_ref, Bdot

from options import nV


### EQUATIONS ###


def flux_test(d, MP):
    Q = generate_vector(MP)
    F_cp = zeros(nV)
    F_py = zeros(nV)
    GPRpy.system.flux(F_cp, Q, d, MP)
    flux_ref(F_py, Q, d, MP)
    print("F    diff =", diff(F_cp, F_py))
    return F_cp, F_py


def source_test(d, MP):
    Q = generate_vector(MP)
    S_cp = zeros(nV)
    S_py = zeros(nV)
    GPRpy.system.source(S_cp, Q, MP)
    source_ref(S_py, Q, MP)
    print("S    diff =", diff(S_cp, S_py))
    return S_cp, S_py


def block_test(d, MP):
    Q = generate_vector(MP)
    B_cp = zeros([nV, nV])
    B_py = zeros([nV, nV])
    GPRpy.system.block(B_cp, Q, d)
    block_ref(B_py, Q, d, MP)
    print("B    diff =", diff(B_cp, B_py))
    return B_cp, B_py


def Bdot_test(d, MP):
    Q = generate_vector(MP)
    x = rand(nV)
    Bx_cp = zeros(nV)
    Bx_py = zeros(nV)
    GPRpy.system.Bdot(Bx_cp, Q, x, d, MP)
    Bdot(Bx_py, x, Q, d, MP)
    print("Bdot diff =", diff(Bx_cp, Bx_py))
    return Bx_cp, Bx_py