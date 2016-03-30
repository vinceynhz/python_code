import os
import sys
import json
from datetime import datetime

import neurons
import neurons2
import neurons3
import neurons4
import neurons5

############################# TRAINING SETS #############################
### AND TRAINING SET
tset = [
    ([0,0], [0]),
    ([1,0], [0]),
    ([1,1], [1])
]
tvector = (0,1)
toutput = [0]

### OR TRAINING SET
# tset = [
#     ([0,0], [0]),
#     ([1,0], [1]),
#     ([1,1], [1])
# ]
# tvector = (0,1)
# toutput = [1]

### NAND TRAINING SET
# tset = [
#     ([1,1], [0]),
#     ([1,0], [1]),
#     ([0,0], [1])
# ]
# tvector = (0,1)
# toutput = [1]

### XOR TRAINING SET
# tset = [
#     ([0,0], [0]),
#     ([1,0], [1]),
#     ([1,1], [0])
# ]
# tvector = (0,1)
# toutput = [1]

## ENCODER 10-5-10
# tset = [
#     ( [1,0,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0] ),
#     ( [0,1,0,0,0,0,0,0,0,0], [0,1,0,0,0,0,0,0,0,0] ),
#     ( [0,0,1,0,0,0,0,0,0,0], [0,0,1,0,0,0,0,0,0,0] ),
#     ( [0,0,0,1,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,0] ),
#     ( [0,0,0,0,1,0,0,0,0,0], [0,0,0,0,1,0,0,0,0,0] ),
#     ( [0,0,0,0,0,1,0,0,0,0], [0,0,0,0,0,1,0,0,0,0] ),
#     ( [0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,1,0,0,0] ),
#     ( [0,0,0,0,0,0,0,1,0,0], [0,0,0,0,0,0,0,1,0,0] ),
#     ( [0,0,0,0,0,0,0,0,1,0], [0,0,0,0,0,0,0,0,1,0] ),
#     ( [0,0,0,0,0,0,0,0,0,1], [0,0,0,0,0,0,0,0,0,1] ),
# ]
# tvector = (0,1,0,0,0,1,0,0,0,1)
# toutput = [0,1,0,0,0,1,0,0,0,1]

def test(name, architecture, **kwargs):
    if 'max_epochs' in kwargs:
        max_epochs = kwargs['max_epochs']
    else:
        max_epochs = 300

    if 'trials' in kwargs:
        trials = kwargs['trials']
    else:
        # trials = 100 # AND and XOR
        trials = 25

    if 'learning_rate' in kwargs:
        learning_rate = kwargs['learning_rate']
    else:
        learning_rate = 0.1

    if 'learning_rate_max' in kwargs:
        learning_rate_max = kwargs['learning_rate_max']
    else:
        learning_rate_max = 1

    if 'learning_rate_step' in kwargs:
        learning_rate_step = kwargs['learning_rate_step']
    else:
        learning_rate_step = 0.1

    if 'weight_range_min' in kwargs:
        weight_range_min = kwargs['weight_range_min']
    else:
        weight_range_min = 0.5

    if 'weight_range_max' in kwargs:
        weight_range_max = kwargs['weight_range_max']
    else:
        weight_range_max = 2

    if 'weight_range_step' in kwargs:
        weight_range_step = kwargs['weight_range_step']
    else:
        weight_range_step = 0.5

    ntypes = {
        1 : neurons.network,
        2 : neurons2.network,
        3 : neurons3.network,
        4 : neurons4.network,
        5 : neurons5.network,
    }

    if 'network_type' in kwargs:
        network_type = kwargs['network_type']
        network = ntypes[ kwargs['network_type'] ]
    else:
        network_type = 1
        network = ntypes[1]

    if 'margin_type' in kwargs:
        margin_type = kwargs['margin_type']
    else:
        margin_type = 1

    if 'output' in kwargs:
        output = 'RES_' + kwargs['output'] + '.json'
    else:
        output = 'results.json'

    if 'comment' in kwargs:
        comment = kwargs['comment']
    else:
        comment = None

    if 'activation_function' in kwargs:
        activation_function = kwargs['activation_function']
    else:
        activation_function = 1

    print('##### START OF TESTING #####')
    print('---', datetime.now())
    print('--- Training {x} with architecture {y}'.format( x=name, y=architecture ) )
    print('--- Running {x} trials per [learning rate/weight range] combination'.format(x = trials))
    print('--- [learning rate] changing from {x} to {y}'.format(x=learning_rate, y=learning_rate_max))
    print('--- [weight_range] changing from {x} to {y}, step {z}'.format(x=weight_range_min, y=weight_range_max, z=weight_range_step))
    print('--- Max time per network: {x} epochs'.format(x=max_epochs))
    
    print('### TRAINING SET ### ')
    print(tset)
    print('### TRAINING TYPE ###')
    if network_type == 1:
        print('--- Standard Backpropagation')
    elif network_type == 2:
        print('--- Backpropagation by Schmidhuber')
    elif network_type == 3:
        import numpy as np
        print('--- Matrix approach for Backpropagation')
    elif network_type == 4:
        print('--- Fahlman\'s Quickprop')
    elif network_type == 5:
        print('--- Standard Backprop aplying margin function at each layer')
    
    print('### THRESHOLD TYPE ###')
    if margin_type == 1:
        print('--- Threshold evaluation at output')
    else:
        print('--- Margin evaluation at output [Fahlman 1988]')

    print('### ACTIVATION TYPE ###')
    if activation_function == 1:
        print('--- Standard sigmoid prime')
    else:
        print('--- Fahlman modification to sigmoid prime')

    print('### COMMENT ###')
    if comment is not None:
        print('---', comment)
    print()

    results = {}
    index = 1

    while learning_rate <= learning_rate_max:
    ### START OF WHILE FOR LEARNING RATE
        weight_range = weight_range_min
        while(weight_range <= weight_range_max):
        ### START OF WHILE FOR WEIGHT RANGE
            print(datetime.now().time(), 'lr:', learning_rate, 'wr:', weight_range, file=sys.stderr)
            print('---')
            print('>>> NEW SET: lr={x}, wr={y}'.format(x=learning_rate, y=weight_range), datetime.now().time() )
            print('---')

            results[index] = {}
            results[index]['lr'] = learning_rate
            results[index]['wr'] = weight_range
            results[index]['samples'] = {}

            for i in range(trials):
            ### START FOR
                restarts = 0

                while True:
                ### START WHILE
                    a = network(*architecture, 
                                learning_rate=learning_rate,
                                weight_range=weight_range,
                                margin_function=margin_type,
                                modified_sigmoid=activation_function)
                    error = False
                    try:
                        epochs, done = a.train(tset, False, max_epochs)
                    except Exception as e:
                        print('###',e)
                        done = False
                        error = True

                    if done:
                        if network_type == 3:
                            ex = bool( np.all( a.eval(*tvector) == toutput ) )
                        else:
                            ex = a.eval(*tvector) == toutput

                        results[index]['samples'][i] = {
                            'epochs' : epochs,
                            'extrapolation' : ex,
                            'restarts' : restarts
                            }

                        print('<<<', i, '= epochs:', epochs, 'extrapolation:', ex  )
                        break
                    else:
                        if restarts == 5:
                            print('<<<', i, 'max restarts reached' )
                            
                            results[index]['samples'][i] = {
                                'epochs' : -1,
                                'extrapolation' : False,
                                'restarts' : restarts
                            }
                            
                            break
                        else:
                            if error:
                                print('<<<', i, 'error occurred, restarting' )
                            else:
                                print('<<<', i, 'max epochs reached, restarting' )

                            print('restarting', file=sys.stderr)
                            restarts += 1
                ### END WHILE
            ### END FOR
            
            # results[index]['restarts'] = restarts


            weight_range = round(weight_range + weight_range_step, 1)
            index += 1

        learning_rate = round(learning_rate + learning_rate_step, 1)
        # index += 1

    print('---', datetime.now())
    print('##### END OF TESTING #####')
    with open( output, 'w' ) as saving:
        json.dump(results, saving)

def process(argv):
    name = None
    architecture = None
    kwargs = {}
    help = False
    for ind in range(1,len(argv)):
        if argv[ind] == '-h':
            help = True

        if argv[ind] == '-n':
            name = argv[ind+1]
        elif argv[ind] == '-a':
            architecture = [ int(x) for x in argv[ind+1].split('-') ]
        elif argv[ind] == '-e':
            kwargs['max_epochs'] = int( argv[ind+1] )
        elif argv[ind] == '-t':
            kwargs['trials'] = int( argv[ind+1] )
        elif argv[ind] == '-lr':
            kwargs['learning_rate'] = float( argv[ind+1] )
        elif argv[ind] == '-lrm':
            kwargs['learning_rate_max'] = float( argv[ind+1] )
        elif argv[ind] == '-lrs':
            kwargs['learning_rate_step'] = float( argv[ind+1] )
        elif argv[ind] == '-wr':
            kwargs['weight_range_min'] = float( argv[ind+1] )
        elif argv[ind] == '-wrm':
            kwargs['weight_range_max'] = float( argv[ind+1] )
        elif argv[ind] == '-wrs':
            kwargs['weight_range_step'] = float( argv[ind+1] )
        elif argv[ind] == '-nt':
            kwargs['network_type'] = int( argv[ind+1] )
        elif argv[ind] == '-mt':
            kwargs['margin_type'] = int( argv[ind+1] )
        elif argv[ind] == '-o':
            kwargs['output'] = argv[ind+1]
        elif argv[ind] == '-c':
            kwargs['comment'] = argv[ind+1]
        elif argv[ind] == '-af':
            kwargs['activation_function'] = int( argv[ind+1] )
        else:
            ind -= 1

        ind += 1

    if help:
        printhelp(argv)
    else:
        test(name, architecture, **kwargs)

def printhelp(argv):
    print('Usage: python {x} OPTIONS'.format(x=argv[0]))
    print('Options:')
    print('\t-n [name]                     name of the experiment, surrounded by quotes')
    print('\t-a [architecture]             architecture of the network, surrounded by quotes')
    print('\t-e [epochs]                   [300] max number of epochs per training')
    print('\t-t [trials]                   [25] number of trials per set')
    print('\t-lr [learning_rate]           [0.1] initial value for the learning_rate')
    print('\t-lrm [learning_rate_max]      [1] maximum value for the learning_rate')
    print('\t-lrs [learning_rate_step]     [0.1] step to increase the learning_rate')
    print('\t-wr [weight_range]            [0.5] initial value for the weight_range')
    print('\t-wrm [weight_range_max]       [2] maximum value for the weight_range')
    print('\t-wrs [weight_range_step]      [0.5] step to increase the weight_range')
    print('\t-nt [network_type]            [1] for standard backpropagation,')
    print('\t                               2  for Schmidhuber\'s')
    print('\t                               3  for matrix approach')
    print('\t                               4  for Quickprop')
    print('\t                               5  for std backprop applying threshold at every layer')
    print('\t-af [activation_function]     [1] is standard sigmoid, 2 is Fahlman sigmoid (adding 0.1)')
    print('\t-mt [margin_type]             [1] is threshold, 2 is margin')
    print('\t-o [output filename]          [results] suffix for the json file name to use')
    print('\t-c [comment]                  [None] add a comment for this experiment')
    print('\t-h                            show this help')

if __name__ == '__main__':
    if len(sys.argv) != 1:
        process( sys.argv )
    else:
        printhelp( sys.argv )

# BP001 # python experiment.py -n "AND GATE" -a "2-2-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP001" > TST_BP001.txt
# BP001_01 # python experiment.py -n "AND GATE" -a "2-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP001_01" -c "AND with a single unit" > TST_BP001_01.txt
# BP001_02 # python experiment.py -n "AND GATE" -a "2-3-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP001_02" -c "AND with a wider hidden layer" > TST_BP001_02.txt
# BP001_03 # python experiment.py -n "AND GATE" -a "2-2-1" -t 100 -lr 1.1 -lrm 10 -nt 1 -mt 1 -af 1 -o "BP001_03" -c "Extending learning rate range"> TST_BP001_03.txt

# BP002 # python experiment.py -n "OR GATE" -a "2-2-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP002" > TST_BP002.txt
# BP002_01 # python experiment.py -n "OR GATE" -a "2-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP002_01" -c "OR with a single unit"> TST_BP002_01.txt
# BP002_02 # python experiment.py -n "OR GATE" -a "2-3-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP002_02" -c "OR with a wider hidden layer"> TST_BP002_02.txt
# BP002_03 # python experiment.py -n "OR GATE" -a "2-2-1" -t 100 -lr 1.1 -lrm 10 -nt 1 -mt 1 -af 1 -o "BP002_03" -c "Extending learning rate range"> TST_BP002_03.txt

# BP003 # python experiment.py -n "XOR GATE" -a "2-2-1" -t 100 -nt 1 -mt 1 -af 1 -o "BP003" > TST_BP003.txt
# BP003_01 # python experiment.py -n "XOR GATE" -a "2-3-1" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP003_01" -c "XOR with a wider hidden layer" > TST_BP003_01.txt
# BP003_02 # python experiment.py -n "XOR GATE" -a "2-2-2-1" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP003_02" -c "XOR with an extra hidden layer"> TST_BP003_02.txt
# BP003_03 # python experiment.py -n "XOR GATE" -a "2-3-2-1" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP003_03" -c "XOR with an extra wider hidden layer"> TST_BP003_03.txt
# BP003_04 # python experiment.py -n "XOR GATE" -a "2-2-1" -t 100 -lr 1.1 -lrm 10 -nt 1 -mt 1 -af 1 -o "BP003_04" -c "Extending learning rate range"> TST_BP003_04.txt

# BP004 # python experiment.py -n "10-5-10 ENCODER" -a "10-5-10" -e 350 -t 100 -nt 1 -mt 1 -af 1 -o "BP004" > TST_BP004.txt
# BP004_01 # python experiment.py -n "10-6-10 ENCODER" -a "10-6-10" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP004_01" -c "Encoder with wider hidden layer"> TST_BP004_01.txt
# BP004_02 # python experiment.py -n "10-7-10 ENCODER" -a "10-7-10" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP004_02" -c "Encoder with wider hidden layer"> TST_BP004_02.txt
# BP004_03 # python experiment.py -n "10-5-5-10 ENCODER" -a "10-5-5-10" -e 1000 -t 100 -nt 1 -mt 1 -af 1 -o "BP004_03" -c "Encoder with extra hidden layer"> TST_BP004_03.txt
# BP004_04 # python experiment.py -n "10-5-10 ENCODER" -a "10-5-10" -e 350 -t 100 -lr 1.1 -lrm 10 -nt 1 -mt 1 -af 1 -o "BP004_04" -c "Extending learning rate range" > TST_BP004_04.txt

# BP005 # python experiment.py -n "AND GATE" -a "2-2-1" -t 100 -lr 0.5 -lrm 2 -wr 1 -nt 1 -mt 1 -af 2 -o "BP005" > TST_BP005.txt