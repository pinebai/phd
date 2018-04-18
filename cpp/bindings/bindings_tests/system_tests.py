import GPRpy

from numpy import dot, zeros
from numpy.random import rand

from bindings_tests.test_functions import check, generate_vector

from system import flux, source, nonconservative_matrix, system_matrix

from options import NV


### EQUATIONS ###


def flux_test(d, MP):
    Q = generate_vector(MP)
    F_cp = zeros(NV)
    GPRpy.system.flux(F_cp, Q, d, MP)
    F_py = flux(Q, d, MP)
    print("F     ", check(F_cp, F_py))
    return F_cp, F_py


def source_test(d, MP):
    Q = generate_vector(MP)
    S_cp = zeros(NV)
    GPRpy.system.source(S_cp, Q, MP)
    S_py = source(Q, MP)
    print("S     ", check(S_cp, S_py))
    return S_cp, S_py


def nonconservative_product_test(d, MP):
    Q = generate_vector(MP)
    x = rand(NV)
    Bx_cp = zeros(NV)
    Bx_py = zeros(NV)
    GPRpy.system.Bdot(Bx_cp, Q, x, d, MP)
    B_py = nonconservative_matrix(Q, d, MP)
    Bx_py = dot(B_py, x)
    print("Bdot  ", check(Bx_cp, Bx_py))
    return Bx_cp, Bx_py


def system_test(d, MP):
    Q = generate_vector(MP)
    M_cp = GPRpy.system.system_matrix(Q, d, MP)
    M_py = system_matrix(Q, d, MP)
    print("M     ", check(M_cp, M_py))
    return M_cp, M_py