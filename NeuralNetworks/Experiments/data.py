import sys
import json

from math import sqrt

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

headers = 'ID|WEIGHT_RANGE|AVERAGE|LEARNING_RATE|RESTARTS|SD|MIN|MAX|EXTRAPOLATION|TRIALS|NC_TRIALS'
record = '{key}|{wr}|{avg}|{lr}|{rests}|{sd}|{min}|{max}|{extras}|{trials}|{nc_trials}'

def analyze(data, csv, time, extrapolation, stddev, useid):
    # Here I get the list of all the keys
    a = list(data.keys())
    a = [int(x) for x in a]
    a.sort()
    a = [str(x) for x in a]

    if csv or useid is not None:
        print(headers)

    avgt = { 'min' : None, 'id' : None }
    extr = { 'max' : None, 'id' : None }
    sdev = { 'min' : None, 'id' : None }
    
    for key in a:

        epochs = []
        extras = 0
        restarts = 0

        mins = None
        maxs = None
        
        # Get the number of trials for this configuration 
        trials = len(data[key]['samples'])
        not_convergent_trials = 0

        # For each trial
        for subkey in data[key]['samples']:
            # Get the number of epochs
            e = data[key]['samples'][subkey]['epochs']
            r = data[key]['samples'][subkey]['restarts']

            # If we have 5 restarts and epochs is -1, the trial is not valid:
            if r == 5 and e == -1:
                not_convergent_trials += 1
                continue

            # check for minimum and maximum values
            if mins is None or e < mins:
                mins = e
            if maxs is None or e > maxs:
                maxs = e

            # add for averaging
            epochs.append(e)
            restarts += r

            # if there is extrapolation, we count it
            if data[key]['samples'][subkey]['extrapolation']:
                extras += 1
        
        # At the end of the trials for this configuration
        avg = sum(epochs) / ( trials - not_convergent_trials )

        # Calculate variance
        var = [ x - avg for x in epochs ]
        var = [ x ** 2 for x in var ]
        var = sum(var) / ( trials - not_convergent_trials - 1 )

        sd = round( sqrt(var), 3 )

        if csv or ( useid is not None and key == useid ):
            print(
                record.format(
                              key = key,
                              trials = trials,
                              nc_trials = not_convergent_trials,
                              lr = data[key]['lr'],
                              wr = data[key]['wr'],
                              rests = restarts,
                              avg = avg,
                              sd = sd,
                              min = mins,
                              max = maxs,
                              extras = extras
                             )
            )

        avgt = assignif(time, avgt, True, avg, key)
        extr = assignif(extrapolation, extr, False, extras, key)
        sdev = assignif(stddev, sdev, True, sd, key)

    if time:
        print('Best time:', avgt, file=sys.stderr)

    if extrapolation:
        print('Best extrapolation:', extr, file=sys.stderr)

    if stddev:
        print('Best standard deviation:', sdev, file=sys.stderr)

def assignif(flag, dic, minimum, value, key):
    k = 'min' if minimum else 'max'

    if flag and (
          dic[k] is None or 
          dic[k] == 0 or 
          ( 
            ( minimum and value < dic[k] ) or
            ( not minimum and value > dic[k] )
          )
        ):
       dic[k] = value
       dic['id'] = key

    return dic

def process(argv):
    filename = None
    csv = False
    time = False
    extrapolation = False
    stddev = False
    useid = None
    help = False

    for ind in range(1,len(argv)):
        if argv[ind] == '-f' or argv[ind] == '--file':
            filename = argv[ind+1]
            ind += 1
        
        elif argv[ind] == '-c' or argv[ind] == '--csv':
            csv = True
        
        elif argv[ind] == '-b' or argv[ind] == '--best':
            if "t" in argv[ind+1] or "T" in argv[ind+1]:
                time = True
            
            if "e" in argv[ind+1] or "E" in argv[ind+1]:
                extrapolation = True
            
            if "s" in argv[ind+1] or "S" in argv[ind+1]:
                stddev = True

            ind += 1

        elif argv[ind] == '-i' or argv[ind] == '--id':
            useid = argv[ind+1]
            ind += 1

        elif argv[ind] == '-h' or argv[ind] == '--help':
            help = True

    if help or filename is None:
        printhelp(argv)
        return

    data = None
    with open(filename, 'r') as parsing:
        data = json.load(parsing)

    analyze(data, csv, time, extrapolation, stddev, useid)

def printhelp(argv):
    print('Usage: python {x} OPTIONS'.format(x=argv[0]))
    print('Options:')
    print('\t-f, --file [filename]    JSON file name to analyze - MUST')
    print('\t-c, --csv                print to std output the csv information of the json file')
    print('\t-i, --id [id]            get the csv record for a specific ID within the json file')
    print('\t                         id and csv are mutually exclusive, if both are passed, csv will be used')
    print('\t-b, --best [t|e|s]       get back the best result over a property, possible properties are:')
    print('\t                          > [t]ime : smallest average')
    print('\t                          > [e]xt  : highest extrapolation ')
    print('\t                          > [s]d   : smallest standard deviation ')
    print('\t                         multiple values can be used')
    print('\t-h, --help               show this help')

if __name__ == '__main__':
    if len(sys.argv) != 1:
        process( sys.argv )
