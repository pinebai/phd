# Some scripts to test the Python bindings for the C++ GPR implementation
# Make sure Git/GPR-cpp and Git/GPR/python are in PYTHONPATH
import GPRpy

from models.gpr.tests.one import fluids
from models.gpr.tests.two import validation

from bindings_tests.system_tests import flux_test, source_test
from bindings_tests.system_tests import nonconservative_product_test, system_test

from bindings_tests.solver_tests import lgmres_test, newton_krylov_test
from bindings_tests.solver_tests import weno_test, rhs_test, obj_test, dg_test
from bindings_tests.solver_tests import midstepper_test, ode_test

from bindings_tests.fv_tests import TAT_test, Bint_test, D_RUS_test, D_ROE_test, D_OSH_test
from bindings_tests.fv_tests import FVc_test, FVi_test, FV_test

from solvers.weno.weno import weno_launcher

from options import NDIM, SPLIT, N, NV, CPP_LVL


assert(GPRpy.N() == N)
assert(GPRpy.NV() == NV)
assert(CPP_LVL > 0)


if NDIM == 1:
    u, MPs, _, dX = fluids.heat_conduction_IC()
else:
    u, MPs, _, dX = validation.hagen_poiseuille_IC()

MP = MPs[0]
d = 0
dt = 0.0001
dx = dX[0]


F_cp, F_py = flux_test(d, MP)
S_cp, S_py = source_test(d, MP)
Bx_cp, Bx_py = nonconservative_product_test(d, MP)
M_cp, M_py = system_test(d, MP)

lgmres_cp, lgmres_py = lgmres_test()
nk_cp, nk_py = newton_krylov_test(u, dt, dX, MP)

wh_cp, wh_py = weno_test()

TAT_cp, TAT_py = TAT_test(d, MP)
Bint_cp, Bint_py = Bint_test(d, MP)
D_RUS_cp, D_RUS_py = D_RUS_test(d, MP)
D_ROE_cp, D_ROE_py = D_ROE_test(d, MP)
D_OSH_cp, D_OSH_py = D_OSH_test(d, MP)

if SPLIT:
    mid_cp, mid_py = midstepper_test(u, dX, dt, MP)
    ode_cp, ode_py = ode_test(dt, MP)
    qh_py = weno_launcher(u)
else:
    rhs_cp, rhs_py = rhs_test(u, dX, dt, MP)
    obj_cp, obj_py = obj_test(u, dX, dt, MP)
    qh_cp, qh_py = dg_test(u, dX, dt, MP)

FVc_cp, FVc_py = FVc_test(qh_py, dX, dt, MP)
FVi_cp, FVi_py = FVi_test(qh_py, dX, dt, MP)
FV_cp, FV_py = FV_test(qh_py, dX, dt, MP)
