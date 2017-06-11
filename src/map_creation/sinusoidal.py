# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------- #
import numpy as np

# -------------------------------------------------------------------------------------- #
def create_map(configParams):

    map = np.zeros([configParams['number_of_cities'],2])

    xFunctionInput = np.linspace(0,
                                 np.pi*configParams['number_of_x_humps'], 
                                 configParams['number_of_cities'])
    map[:,0] = np.random.choice(xFunctionInput,
                                size=configParams['number_of_cities'],
                                p=np.sin(xFunctionInput)**2/np.sum(np.sin(xFunctionInput)**2))

    yFunctionInput = np.linspace(0,
                                 np.pi*configParams['number_of_y_humps'],
                                 configParams['number_of_cities'])
    map[:,1] = np.random.choice(yFunctionInput,
                                size=configParams['number_of_cities'],
                                p=np.sin(yFunctionInput)**2/np.sum(np.sin(yFunctionInput)**2))
    
    # normalize
    map[:,0] = map[:,0]/np.max(map[:,0])
    map[:,1] = map[:,1]/np.max(map[:,1])

    return map



# -------------------------------------------------------------------------------------- #