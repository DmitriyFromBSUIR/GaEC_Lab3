

import os

pathSep = os.path.sep
scriptDir = os.path.dirname(os.path.realpath(__file__))

#
CITIES_FILEPATH = "./data/eil51.tsp"

#
OPTIMAL_TOUR_FILEPATH = "./data/eil51.opt.tour"

#
APP_RESOURCES_DIR = scriptDir + pathSep + "resources" + pathSep + "images" + pathSep

#
DIRECTORY_VIEWER_ROOT_PATH = scriptDir + pathSep + "data"

#
FILE_CONTENT_VIEWER_DEFAULT_FILEPATH = scriptDir + pathSep + "data" + pathSep + "eil51.opt.tour"

#
TEXT_EDITOR_RESOURCES_FILEPATH = scriptDir + pathSep + "resources" + pathSep + "icons" + pathSep

#
ALGORITHMS_DECL_LIST_SCRIPT_FILEPATH = scriptDir + pathSep + "GeneticAndEvoLib" + pathSep + "AlgorithmsDeclLists.py"