from numpy import dot, exp, eye

from system.gpr.misc.functions import I_1, I_2, I_3


I = eye(3)


def U_1(I3, HYP):
    """ Returns the first component of the thermal energy density,
        given the third invariant of G
    """
    K0 = HYP.K0
    α = HYP.α
    return K0/(2*α**2) * (I3**(α/2) - 1)**2

def U_2(I3, S, HYP):
    """ Returns the second component of the thermal energy density,
        given the third invariant of G and entropy
    """
    cv = HYP.cv
    T0 = HYP.T0
    γ = HYP.γ
    return cv * T0 * I3**(γ/2) * (exp(S/cv) - 1)

def W(I1, I2, I3, HYP):
    """ Returns the internal energy due to shear deformations,
        given the invariants of G
    """
    B0 = HYP.B0
    β = HYP.β
    return B0/2 * I3**(β/2) * (I1**2 / 3 - I2)


def GdU_1dG(I3, HYP):
    """ Returns G * dU1/dG
    """
    K0 = HYP.K0
    α = HYP.α
    return K0/(2*α) * (I3**α - I3**(α/2)) * I

def GdU_2dG(I3, S, HYP):
    """ Returns G * dU2/dG
    """
    cv = HYP.cv
    T0 = HYP.T0
    γ = HYP.γ
    return cv * T0 * γ/2 * (exp(S/cv) - 1) * I3**(γ/2) * I

def GdWdG(G, I1, I2, I3, HYP):
    """ Returns G * dW/dG
    """
    B0 = HYP.B0
    β = HYP.β
    const = B0/2 * I3**(β/2)
    return const * ( (β/2)*(I1**2/3 - I2)*I - I1/3 * G + dot(G,G) )


def total_energy_hyp(A, S, v, HYP):
    """ Returns the total energy, given the distortion tensor and entropy
    """
    G = dot(A.T, A)
    I1 = I_1(G)
    I2 = I_2(G)
    I3 = I_3(G)
    return U_1(I3, HYP) + U_2(I3, S, HYP) + W(I1, I2, I3, HYP) + dot(v,v) / 2

def sigma_hyp(ρ, A, S, HYP):
    """ Returns the stress tensor
    """
    G = dot(A.T, A)
    I1 = I_1(G)
    I2 = I_2(G)
    I3 = I_3(G)
    GdedG = GdU_1dG(I3, HYP) + GdU_2dG(I3, S, HYP) + GdWdG(G, I1, I2, I3, HYP)
    return -2 * ρ * GdedG

def temperature_hyp(S, A, HYP):
    G = dot(A.T, A)
    I3 = I_3(G)
    T0 = HYP.T0
    γ = HYP.γ
    cv = HYP.cv
    return T0 * I3**(γ/2) * exp(S / cv)
