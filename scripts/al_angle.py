#!/usr/bin/python3

from beam_calc_helpers import *
import numpy as np
from numpy import sqrt


def print_deets(a,b,t,L):
    I = IAngle(a, b, t)
    ro = Density("al")
    E = YoungModulus("al")
    A = t * (a + (b-t))
    print("Euler Buckling Force: {0:.2f}N".format(EulerBucklingForce(I,E,5)))
    print("Max column without load: {0:.2f}m".format(MaxColumn(I, E,
                                                        0.0127*sqrt(2), ro)))
    roLED = (ro*t*(a+b-t) + 0.057) / (t*(a+b-t))
    print("Max column with LEDs: {0:.2f}m".format(MaxColumn(I, E,
                                                        0.0127*sqrt(2), roLED)))
    print("Self-weight deflection as horizontal cantilever: {0:.2f}m".format(
                                        BeamDeflection(I, E, L, A*ro*9.81)))
    print("Self-weight deflection as horizontal cantilever with LEDs: {0:.2f}m".format(
                                        BeamDeflection(I, E, L, A*roLED*9.81)))
# http://www.knmi.nl/samenw/hydra/faq/press.html
    print("Deflection under ~30mph wind load: {0:.2f}m".format(
                                        BeamDeflection(I, E, L, a*119)))
    print("Deflection under ~40mph wind load: {0:.2f}m".format(
                                        BeamDeflection(I, E, L, a*268)))
    print("Weight each and for 50: {0:.2f}kg {1:.2f}kg".format(
                                                     WeightAngle(a,b,t,L,ro),
                                                     WeightAngle(a,b,t,L,ro)*50))
    print("")


print("One-piece Al section, .5\" .5\" 1/16\" 5m")
print("Cost each, in quantity, 1.80GBP")
print_deets(0.0127, 0.0127, 0.0015875, 5)

print("One-piece Al section, .75\" .75\" 1/16\" 5m")
print("Cost each, in quantity, 2.91GBP")
print_deets(0.01905, 0.01905, 0.0015875, 5)

print("One-piece Al section, 1\" 1\" 1/16\" 5m")
print("Cost each, in quantity, 4.27GBP")
print_deets(0.0254, 0.0254, 0.0015875, 5)

print("One-piece Al section, .5\" .5\" 1/8\" 5m")
print("Cost each, in quantity, 3.73GBP")
print_deets(0.0127, 0.0127, 0.003175, 5)

