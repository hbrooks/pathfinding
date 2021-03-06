"""
Words go here.

Usage:
    wrapper.py N MAPS ALGS [-g] [--cycles=<10>]

Options:
    --version     Show version.
    -g --gif      Creates a .gif of the solution.
    --cycles=<N>  How many times would you like to run the provided process.

"""
import copy
import numpy as np
from docopt import docopt
from create_map import make_map
from execute import apply_solver

createMapArguments = {
        '--help': False,
        '--save': False,
        '--version': False,
        '--display': False,
        'GROUPS': None,
        'N': -1,
        'OFFSET_STD_DEV': None,
        'TECHNIQUE': '',
        'X_PEAKS': None,
        'Y_PEAKS': None,
        'ball': False,
        'donut': False,
        'fixed_number_of_groups': False,
        'random_uniform': False,
        'sinusoidal': False
}
executeArguments = {
    '--force': False,
    '--gif': False,
    '--help': False,
    '--save': False,
    '--verbose': False,
    '--version': False,
    'MAP_ID': None,
    'SOLVER': None,
    'brute': False,
    'nearest_neighbor': False,
    'random_neighbor': False
}


def main(cliArguments):

    solutions = {}

    cliArguments['MAPS'] = cliArguments['MAPS'].split(',')
    cliArguments['ALGS'] = cliArguments['ALGS'].split(',')

    

    for cycleIndex in np.arange(0, int(cliArguments['--cycles'])):

        for mapName in cliArguments['MAPS']:

            createMapTempArgs = copy.deepcopy(createMapArguments)
            if mapName not in createMapTempArgs.keys():
                print 'Invalid map name:',mapName
                continue
        
            createMapTempArgs[mapName] = True
            createMapTempArgs['N'] = int(cliArguments['N'])
            createMapTempArgs['TECHNIQUE'] = mapName
            createMapTempArgs['--save'] = True
            statusCode, node_metadata, node_locations = make_map(createMapTempArgs)
            solutions[node_metadata['map_id']] = {
                'metadata': createMapTempArgs['TECHNIQUE']
            }

            for algName in cliArguments['ALGS']:

                executeTempArgs = copy.deepcopy(executeArguments)
                if algName not in executeTempArgs.keys():
                    print 'Invalid alg name:',algName
                    continue
            
                executeTempArgs[algName] = True
                executeTempArgs['SOLVER'] = algName
                executeTempArgs['MAP_ID'] = node_metadata['map_id']
                executeTempArgs['--save'] = True
                executeTempArgs['--force'] = True
                if cliArguments['--gif'] is True:
                    executeTempArgs['--gif'] = True
                statusCode, solution = apply_solver(executeTempArgs)
                solutions[node_metadata['map_id']][solution['sol_id']] = solution

    # Print all the soltions after everything is finished running.
    for mapKey in solutions.keys():
        for solKey in solutions[mapKey].keys():
            if solKey != 'metadata':
                print '{} ({}) {} ({}): {}'.format(mapKey, solutions[mapKey]['metadata'], solKey, solutions[mapKey][solKey]['SOLVER'], solutions[mapKey][solKey]['cost_of_path'])


if __name__ == '__main__':
    cliArguments = docopt(__doc__, version='Wrapper 1.0')
    if cliArguments['--cycles'] == None:
            cliArguments['--cycles'] = 1
    main(cliArguments)