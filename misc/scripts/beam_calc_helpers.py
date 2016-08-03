import numpy as np


def IAngle(a, b, t):
    """
    Second moment of area for an angle-section beam
    a and b are the webbing lengths, i.e. the side lengths
    of the enclosing rectangle.  t is the thickness of the webs
    Returns I in m^4
    """
 
    # http://www.engineersedge.com/material_science/moment-inertia-gyration-7.htm
    d = b - t   
    y = b - (t*(2*d + a) + d**2)/(2*(d+a))
    I = 1/3 * (t*y**3 + a*(b-y)**3 - (a-t)*(b-y-t)**3)
    return I


def IRound(d):
    """
    Second moment of area for a round cross-section beam.
    d is the diameter.
    Returns I in m^4
    """
    # http://en.wikipedia.org/wiki/List_of_area_moments_of_inertia
    return np.pi / 4 * (d/2)**4


def WeightAngle(a, b, t, L, ro):
    """
    Mass of the angle section described in kg
    """
    A = a*t + (b-t)*t
    V = A*L
    return V*ro


def WeightRound(d, L, ro):
    """
    Mass of the described round section, in kg
    """
    A = np.pi * (d/2)**2
    V = A*L
    return V*ro


def YoungModulus(material):
    """
    Returns the Young Modulus of a material in N/m^2
    Materials:
        "mild" - Mild steel
        "al" - Aluminium
    """
    if material == "mild":
        return 200e9
    else:
        if material == "al":
            return 69e9
        else:
            raise ValueError("Invalid material `"+material+"'")


def Density(material):
    """
    Returns the density of a material in kg/m^3
    Materials:
        "mild" - Mild Steel
        "al" - Aluminium
    """
    if material == "mild":
        return 7850.0
    else:
        if material == "al":
            return 2700.0
        else:
            raise ValueError("Invalid material `"+material+"'")


def EulerBucklingForce(I, E, L):
    """
    Returns the Euler buckling force of a beam.
    I is the second moment of area
    E is the Young Modulus
    L is the uncorrected beam length
    It is assumed that the beam will be setup as a vertical cantilever.
    """
    # http://en.wikipedia.org/wiki/Buckling
    K = 2.0  # for a vertical cantilever
    F = np.pi**2 * E*I / (K*L)**2
    return F

def MaxColumn(I, E, d, ro):
    """
    Return the maximum height of a free-standing column made from
    this material.
    """
    # http://en.wikipedia.org/wiki/Buckling
    B = 1.86635
    g = 9.81
    h = (9 * B**2 * E*I / (4*ro*g*np.pi * (d/2)**2))**(1/3)
    return h


def BeamDeflection(I, E, L, q):
    """
    Returns the deflection of a horizontal cantilever of length L
    made from the material described by I and E, under a distributed uniform
    load q.
    """
    w = q * L**4 / (8*E*I)
    return w
