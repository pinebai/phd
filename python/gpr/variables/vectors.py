from numpy import zeros

from gpr.variables.eos import total_energy
from gpr.variables.state import pressure, temperature


class primitive():
    """ Returns the primitive varialbes, given a vector of conserved variables
    """
    def __init__(self, Q, PAR, SYS):
        self.ρ = Q[0]
        self.E = Q[1] / self.ρ
        self.v = Q[2:5] / self.ρ
        self.A = Q[5:14].reshape([3,3])
        self.J = Q[14:17] / self.ρ
        self.λ = Q[17] / self.ρ

        self.p = pressure(self.E, self.v, self.A, self.ρ, self.J, self.λ, PAR, SYS)
        self.T = temperature(self.ρ, self.p, PAR.γ, PAR.pINF, PAR.cv)

def conserved(ρ, p, v, A, J, λ, PAR, SYS):
    """ Returns the vector of conserved variables, given the primitive variables
    """
    Q = zeros(18)
    Q[0] = ρ
    Q[1] = ρ * total_energy(ρ, p, v, A, J, λ, PAR, SYS)
    Q[2:5] = ρ * v
    Q[5:14] = A.ravel()
    Q[14:17] = ρ * J
    Q[17] = ρ * λ
    return Q

def primitive_vector(P):
    ret = zeros(18)
    ret[0] = P.ρ
    ret[1] = P.p
    ret[2:11] = P.A.ravel()
    ret[11:14] = P.v
    ret[14:17] = P.J
    return ret

def Pvec_reordered_to_Cvec(P, PAR, SYS):
    """ Returns the vector of conserved variables, given the vector of (reordered) primitive
        variables
    """
    Q = zeros(18)
    ρ = P[0]
    p = P[1]
    A = P[2:11].reshape([3,3])
    v = P[11:14]
    J = P[14:17]
    λ = 0
    Q[0] = ρ
    Q[1] = ρ * total_energy(ρ, p, v, A, J, λ, PAR, SYS)
    Q[2:5] = ρ * v
    Q[5:14] = P[2:11]
    Q[14:17] = ρ * J
    return Q

def Pvec_to_Cvec(P, PAR, SYS):
    """ Returns the vector of conserved variables, given the vector of (reordered) primitive
        variables
    """
    Q = P.copy()
    ρ = P[0]
    A = P[5:14].reshape([3,3])
    Q[1] = ρ * total_energy(ρ, P[1], P[2:5], A, P[14:17], P[17], PAR, SYS)
    Q[2:5] *= ρ
    Q[14:18] *= ρ
    return Q

def Cvec_to_Pvec(Q, PAR, SYS):
    """ Returns the vector of primitive variables in standard ordering, given the vector of
        conserved variables.
    """
    ρ = Q[0]
    E = Q[1] / Q[0]
    v = Q[2:5] / ρ
    A = Q[5:14].reshape([3,3])
    J = Q[14:17] / ρ
    λ = Q[17] / ρ
    p = pressure(E, v, A, ρ, J, λ, PAR, SYS)

    ret = zeros(18)
    ret[0] = ρ
    ret[1] = p
    ret[2:5] = v
    ret[5:14] = Q[5:14]
    ret[14:17] = J
    ret[17] = λ
    return ret