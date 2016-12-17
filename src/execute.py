# -------------------------------------------------------------------------------------- #
# This script performs a TSP solution on a map.  If you provide it with the map_ID of an
# existing map, it will attempt to find the shortest path of that map.  If not, it will
# create a map using the configuration parameters in a config file.
#
# This script is most simply called by:
#    $ python execute.py
# The above command line command will draw parameters from the configuration file at
# tsp/config/execute/paramteres.config.  Additionally, the configuration parameters can
# be passed directly into the command line command via something like:
#    $ python execute.py {"alg": "brute"}
# The above technique might be useful for creating a wrapper script to solve many maps
# with many algorithums.
# -------------------------------------------------------------------------------------- #
import numpy as np
import json
from functions import complex as cmplx
import create_map
import sys


# -------------------------------------------------------------------------------------- #
def load_map(map_ID):
    # This function attempts to load a cityMap from 
    # "tsp/data/hist/<map_ID>/<map_ID>_locations.txt".
    #
    #     INPUTS:
    #        - map_ID: string representing the map indetifier to load
    #     OUTPUTS:
    #        - cityMap: [nCities,2] sized where 1st column is X coordindate
    #                   and 2nd column is Y cordinate for each city
    #        - mapMeta: dictionary containing metadata about cityMap
    #
    print ' INFO: Attempting to load map.'
    print '\t- map_ID:', map_ID
    mapLoadPath, metaLoadPath = cmplx.get_filepath_to_map_data(map_ID)
    print '\t- loading map from '+mapLoadPath
    cityMap = np.loadtxt(mapLoadPath)
    print '\t- loading meta from '+metaLoadPath
    with open(metaLoadPath, 'r') as infile:
        meta_data_string = infile.read()
    mapMeta = json.loads(meta_data_string)
    return cityMap, mapMeta


def print_detail_solution(solution):
    # Simply prints a more detailed view of the solution. CURRENTLY ONLY WORKS FOR ALG=brute
    # 
    print '\t\t index, path, distance:'
    for i in range(0, len(solution['distances'])):
        lineToPrint = '\t\t\t'+str(i)+', '+str(solution['paths'][i,:])+', '+str(solution['distances'][i])
        if i in solution['shortest_path_index']:
            lineToPrint = lineToPrint + ' *'
        print lineToPrint


def print_quick_solution(solution):
    # Simply prints the fastest routes. CURRENTLY ONLY WORKS FOR ALG=brute.
    #
    for entry in solution['shortest_path_index']:
        print '\t\t', solution['paths'][entry]


# -------------------------------------------------------------------------------------- #
def main():
    print '\nBegining script...'

    if len(sys.argv) == 1:
        # command looks like: $ python execute.py
        configParams = cmplx.get_config_params('execute')

    else:
        if sys.argv[1] == 'config':
            # command looks like: $ python execute.py config
            configParams = cmplx.get_config_params('execute')
        else:
            # command looks like: $ python execute.py {"alg":"brute"}
            try:
                configParams = json.loads(sys.argv[1])
            except:
                print ' ERROR: Unable to load configuration parameters as JSON.'

    # see if we need to create a map or can retrieve one by its map_ID
    if 'map_ID' in configParams and configParams['map_ID'] != '':
        cityMap, mapMeta = load_map(configParams['map_ID'])
    else:
        print ' INFO: Creating map...'
        create_map_configParams = cmplx.get_config_params('map_creation')
        cityMap, mapMeta = create_map.process_to_create_map(create_map_configParams)
    
    # import solver
    temp_resource = __import__('algs.'+configParams['alg'],
                               globals(), locals(), ['algs'], -1)
    
    # solve
    solution = temp_resource.solve(configParams, cityMap, mapMeta)

    # create solution ID and add to solution dictionary
    solution['sol_ID'] = cmplx.generate_ID('SID', 5)
    solution['map_ID'] = mapMeta['map_ID']

    # print solution
    if solution is not None:
        print ' INFO: solve() complete.'
        print '\t- detailed solution:'
        print_detail_solution(solution)
        #print '\t- quick solution:'
        #print_quick_solution(solution)
    else:
        print ' INFO: solution is None. Something went wrong... did you check the alg file?'
    
    # save solution if applicable
    if 'save_method' in configParams and configParams['save_method'] != '':
        saveMethods = configParams['save_method'].split(',')
        for entry in saveMethods:
            cmplx.save_solution(str(entry), solution)

    print '\n'


# -------------------------------------------------------------------------------------- #	
if __name__ == "__main__":
    main()
