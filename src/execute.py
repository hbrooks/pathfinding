"""
Write me

Usage:
    execute.py brute MAP_ID [--save] [--verbose] [--force]
    execute.py nearest_neighbor MAP_ID [--save] [--verbose]
    execute.py random_neighbor MAP_ID [--save] [--verbose]
    execute.py -h
    execute.py --help
    execute.py --version

Options:
  -h --help     Show this screen.
  -s --save     Include if you would like to save script output.
  -f --force    Ignore all warnings about lengthy runtimes. 
  -v --verbose  Print the entire solution data.
  --version     Show version.
"""
import numpy as np
import json
from functions import complex as cmplx
import create_map
from docopt import docopt
import sys
import ast # used to open node_metadata files


def load_map(map_id):
    """
    This function attempts to load a node_locations from /data/hist/<map_ID>/<map_ID>_locations.txt
    """
    map_load_path, meta_load_path = cmplx.get_filepath_to_map_data(map_id)

    print '- loading map from '+map_load_path
    try:
        node_locations = np.loadtxt(map_load_path)
    except Exception as e:
        print 'ERROR: opening map locaiton data.'
        print 'exact python error:',str(e)
        sys.exit(1)
        
    print '- loading meta from '+meta_load_path
    try:
        with open(meta_load_path, 'r') as in_file:
            meta_data_string = in_file.read()
            node_metadata = ast.literal_eval(meta_data_string)
    except Exception as e:
        print 'ERROR: opening map meta data.'
        print 'exact python error:', str(e)
        sys.exit(1)
    return node_locations, node_metadata


def save_solution(solution):
    """
    Saves script output.
    """
    file_path_prefix = cmplx.get_filepath_to_solution_data(solution['map_id'], solution['sol_id'])
    print 'Attempting to save solution @ '+file_path_prefix
    try:
        for key in solution.keys():
            if type(solution[key]) == type(np.zeros([10,10])):
                solution[key] = solution[key].tolist()
        with open(file_path_prefix, 'w') as outfile:
            json.dump(solution,outfile)
        print 'INFO: solution saved as json file'
    except Exception as e:
        print 'ERROR: unable to save solution as json'
        print '- exact Python error:',str(e)


def apply_solver(args):
    
    node_locations, node_metadata = load_map(args['MAP_ID'])

    try:
        temp_resource = __import__('solvers.'+args['SOLVER'],
                                   globals(), locals(), ['solvers'], -1)
    except ImportError:
        print 'Unable to import solver for algorithm named '+args['SOLVER']
        sys.exit(1)

    solution = temp_resource.solve(args, node_locations, node_metadata)

    solution['sol_id'] = cmplx.generate_ID('SID', 5)
    solution['map_id'] = node_metadata['map_id']

    if args['--save']:
        save_solution(solution)
    else:
        print 'INFO: Not saving results.'

    return 0


if __name__ == "__main__":
    cli_arguments = docopt(__doc__, version='Execute 1.0')
    cli_arguments['SOLVER'] = sys.argv[1]
    print cli_arguments
    apply_solver(cli_arguments)