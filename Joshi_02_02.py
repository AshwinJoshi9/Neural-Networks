# Joshi, Ashwin
# 1001-554-272
# 2018-09-23
# Assignment-02-02

import numpy as np
# This module calculates the activation function
def calculate_activation_function(weight,bias,input_array,type='Symmetrical Hardlimit'):
    out = np.dot(weight, input_array)
    net_value = out + bias
    if type == "Linear":
        #activation = net_value
        if net_value >= 1:
            activation = 1
        else:
            activation = -1
    elif type == "Hyperbolic Tangent":
        activation = np.tanh(net_value)
    elif type == "Symmetrical Hardlimit":
        if net_value >= 0:
            activation = 1
        else:
            activation = -1
    return activation, net_value