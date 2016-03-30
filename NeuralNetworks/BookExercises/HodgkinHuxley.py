import sys

# to make available all my other code
sys.path.append('C:\\Users\\Vic_\\Documents\\Coding\\_lib')

from visual import * # must import visual or vis first
from visual.graph import *	# import graphing features

from math import exp

class channel():
    Na = 1,
    K = 2,
    L = 3
    channels = [Na, K, L]

class coeficient():
    # Sodium (Na) activation
    m = 1
    # Sodium (Na) deactivation
    h = 2
    # Potasium (K) activation
    n = 3

Na = { 'E' : 115, 'g' : 120, }
K = { 'E' : -12, 'g' : 36, }
L = { 'E' : 10.6, 'g' : 0.3, }

def alpha(x, E):
    # x defines for which coeficient we will calculate
    # E is the current voltage or electric potential of the membrane
    result = {
        coeficient.m : ( 2.5 - 0.1 * E ) / ( exp( 2.5 - 0.1 * E ) - 1 ) if E != 25 else 1,
        coeficient.h : 0.07 * exp( -E / 20 ),
        coeficient.n : ( 0.1 - 0.01 * E ) / ( exp( 1 - 0.1 * E ) - 1 ) if E != 10 else 0.1,
    }[x]

    return result

def beta(x, E):
    # x defines for which coeficient we will calculate
    # E is the current voltage or electric potential of the membrane
    result = {
        coeficient.m : 4 * exp( -E / 18 ),
        # coeficient.m : 6.0e+4 * ( -4.9e-2 - E ) / ( 1 - exp( ( E + 4.9e-2 ) / 2.0e-2 ) ),
        coeficient.h : 1 / ( exp( 3 - 0.1 * E ) + 1 ),
        # coeficient.h : 4.0e+2 / ( 1 + ( exp( ( -3.6e-2 - E ) / 2.0e-3 ) ) ),
        coeficient.n : 0.125 * exp( -E / 80 ),
        # coeficient.n : 5.0e+3 * ( -2.8e-2 - E ) / ( 1 - exp( ( E + 2.8e-2 ) / 4.0e-4 ) )
    }[x]

    return result

def rest(x, E):
    a = alpha(x, -E)
    b = beta(x, -E)

    result =  a / ( a + b )

    return result

def x0(x, E):
    # This is the equilibrium function
    # x defines for which coeficient we will calculate
    # E is the current voltage or electric potential of the membrane
    a = alpha(x,E)
    b = beta(x,E)

    result =  a / ( a + b )

def Tx(x, E):
    # This is the time constant
    # x defines for which coeficient we will calculate
    # E is the current voltage or electric potential of the membrane
    a = alpha(x,E)
    b = beta(x,E)
    if a is None:
        result = None
    else:
        result = 1 / (a + b)
    return result

def partial_coeficient(x, E, val):
    # This will calculate the partial derivative of the coeficient
    # x defines for which coeficient we will calculate
    # E is the current voltage or electric potential of the membrane

    # t = Tx(x, E)
    # X0 = x0(x, E)
    # if t is not None and X0 is not None:
    #     result = -( 1 / t ) * ( val - X0 )
    # else:
    #     result = None

    result = alpha(x, E) * ( 1 - val ) - beta(x, E) * val

    return result

def current(x, E, m=0, h=0, n=0):
    result = {
        channel.Na : (E - Na['E']) * Na['g'] * (m ** 3) * h,
        channel.K : (E - K['E']) * K['g'] * (n ** 4),
        channel.L : (E - L['E']) * L['g'],
    }[x]

    return result

def model(E, m, h, n, Iext = 0, Cm = 1):
    currentSum = 0
    for c in channel.channels:
        currentSum += current(c, E, m, h, n)

    # These lines are equivalent to the loop above
    # Ina = current(channel.Na, E, m, h, n)
    # Ik = current(channel.K, E, m, h, n)
    # Il = current(channel.L, E, m, h, n)
    # currentSum = Ina + Ik + Il

    dE = (Iext - currentSum) / Cm

    dm = partial_coeficient( coeficient.m, E, m )
    dh = partial_coeficient( coeficient.h, E, h )
    dn = partial_coeficient( coeficient.n, E, n )

    return dE, dm, dh, dn

### EXAMPLES OF THE MODEL ###
def spikeA():
    gd = gdisplay( foreground=color.black,
                   background=color.white,
                   title='Example 1: Spike generation A',
                   xtitle='t[ms]',
                   ytitle='E(t)[mV]',
                #    xmax=100,
                #    xmin=-100,
                #    ymax=1,
                #    ymin=0,
                   width=1116,
                   height=512 )

    dEcurve = gcurve(color=color.blue)

    E = 0
    m = rest(coeficient.m, E)
    h = rest(coeficient.h, E)
    n = rest(coeficient.n, E)
    dt = 0.01
    time = arange(0,20,dt)

    I = 5000

    for t in time:
        dEcurve.plot(pos=(t, E))
        dE, dm, dh, dn = model(E, m, h, n, I)
        I = 0
        m += dm * dt
        h += dh * dt
        n += dn * dt
        E += dE * dt

def multiple_current():
    gd = gdisplay( foreground=color.black,
                   background=color.white,
                   title='Test 1 - Membrane Potential',
                   xtitle='t[ms]',
                   ytitle='E(t)[mV]',
                #    xmax=100,
                #    xmin=-100,
                #    ymax=1,
                #    ymin=0,
                   width=1116,
                   height=512 )

    dEcurve = gcurve(color=color.blue)
    dIcurve = gcurve(color=color.green)

    E = 0
    m = rest(coeficient.m, E)
    h = rest(coeficient.h, E)
    n = rest(coeficient.n, E)
    dt = 0.025
    time = arange(0,500,dt)
    I = 0

    i = 0
    for t in time:
        dEcurve.plot(pos=(t, E))
        dIcurve.plot(pos=(t, I))
        dE, dm, dh, dn = model(E, m, h, n, I)
        m += dm * dt
        h += dh * dt
        n += dn * dt
        E += dE * dt
        if i == 17000 or i == 11000 or i == 5000:
            I = 0
        elif i == 13000:
            I = 40
        elif i == 7000:
            I = 25
        elif i == 1000:
            I = 6.6
        i+=1
        
def displayx0():
    gd = gdisplay( foreground=color.black,
                   background=color.white,
                   title='Equilibrium function',
                   xtitle='E[mV]',
                   ytitle='x0(E)',
                   xmax=100,
                   xmin=-100,
                   ymax=1,
                   ymin=0,
                   width=1116,
                   height=512 )

    x0n = gcurve(color=color.red)
    x0m = gcurve(color=color.green)
    x0h = gcurve(color=color.blue)

    for E in range(-100, 101):
        y = x0(coeficient.n, E)
        if y is not None:
            x0n.plot( pos=( E, y ) )

        y = x0(coeficient.m, E)
        if y is not None:
            x0m.plot( pos=( E, y ) )

        y = x0(coeficient.h, E)
        if y is not None:
            x0h.plot( pos=( E, y ) )

    label(display=gd.display, pos=(-15, 0.2), text="n", color=color.red, box = False)
    label(display=gd.display, pos=(27, 0.4), text="m", color=color.green, box = False)
    label(display=gd.display, pos=(-13, 0.8), text="h", color=color.blue, box = False)

def displayT():
    gd = gdisplay( foreground=color.black,
                   background=color.white,
                   title='Time constant',
                   xtitle='E[mV]',
                   ytitle='T(E)[ms]',
                   xmax=100,
                   xmin=-100,
                   ymax=10,
                   ymin=0,
                   width=1116,
                   height=512 )

    Tn = gcurve(color=color.red)
    Tm = gcurve(color=color.green)
    Th = gcurve(color=color.blue)

    for E in range(-100, 101):
        y = T(coeficient.n, E)
        if y is not None:
            Tn.plot( pos=( E, y ) )

        y = T(coeficient.m, E)
        if y is not None:
            Tm.plot( pos=( E, y ) )

        y = T(coeficient.h, E)
        if y is not None:
            Th.plot( pos=( E, y ) )

    label(display=gd.display, pos=(-45, 5), text="n", color=color.red, box = False)
    label(display=gd.display, pos=(12, 0.8), text="m", color=color.green, box = False)
    label(display=gd.display, pos=(8, 8), text="h", color=color.blue, box = False)
