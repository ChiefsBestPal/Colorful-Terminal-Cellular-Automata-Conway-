

BENCHMARK = """
FUNCTION = f=lambda n,a=0,b=1:b/2/n*(b-a)or f(n,b,a+b)

nested_loop_arr_range(test_array2d) x 100:      0.13983829999999997
nested_loop_arr_item(test_array2d) x 100:       0.12455870000000008
single_loop_arr_range(test_array1d) x 100:      0.11735289999999998
single_loop_arr_item(test_array1d) x 100:       0.12294280000000002
NUMPYnested_loop_arr_range(numpy_array2d) x 100:        2.0448250999999997
NUMPYnested_loop_arr_item(numpy_array2d) x 100: 1.7995422999999997
NUMPYsingle_loop_arr_range(numpy_array1d) x 100:        1.7209325
NUMPYsingle_loop_arr_item(numpy_array1d) x 100: 1.8732628
nested_NDITER(numpy_array2d) x 100:     1.6403906999999993
linear_NDITER(numpy_array1d) x 100:     1.5220448000000015
nested_NDENUMERATE(numpy_array2d) x 100:        1.8771842000000003
linear_NDENUMERATE(numpy_array1d) x 100:        1.948681800000001
single_loop_gen(test_array1d) x 100:    3.419999999998424e-05
nested_loop_gen(test_array2d) x 100:    3.460000000110597e-05
NUMPYsingle_loop_gen(numpy_array1d) x 100:      3.459999999932961e-05
NUMPYnested_loop_gen(numpy_array2d) x 100:      3.489999999928273e-05
NUMPY_yield_linear(numpy_array1d) x 100:        3.379999999886252e-05
NUMPY_yield_nested(numpy_array2d) x 100:        3.410000000059199e-05

"""
import numpy as np
#import cpython
import timeit

from numpy.core.fromnumeric import size

test_array2d = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

test_array1d = [el for row in test_array2d for el in row]

numpy_array1d = np.array(test_array1d, dtype=bool)
numpy_array2d = np.array(test_array2d, dtype=bool)


#FUNCTION = lambda el: el^1
FUNCTION = lambda n,a=0,b=1:b/2/(n+4234)*(b-a)or FUNCTION((n+3242),b,a+b)


def generate_IX_only_array(array1d=test_array1d,N=50,N2=2500):
    for ix,cell in enumerate(array1d):
        if bool(cell):
            yield ix


def generate_COORDS_only_array(array1d=test_array1d,N=50,N2=2500):
    for ix,cell in enumerate(array1d):
        if bool(cell):
            yield divmod(ix,N)

test1 = generate_IX_only_array()
test2 = generate_COORDS_only_array()



def nested_loop_arr_range(array_space,N=50,N2=2500):
    for i in range(N):
        for j in range(N):
            array_space[i][j] = FUNCTION(array_space[i][j])
    return array_space


def nested_loop_arr_item(array_space,N=50,N2=2500):
    for i,row in enumerate(array_space):
        for j,el in enumerate(row):
            array_space[i][j] = FUNCTION(el)
            
    return array_space

def single_loop_arr_range(array_space,N=50,N2=2500):
    for i in range(N2):
        array_space[i] = FUNCTION(array_space[i])
    return array_space


def single_loop_arr_item(array_space,N=50,N2=2500):
    for i,el in enumerate(array_space):
        array_space[i] = FUNCTION(el)
    return array_space

NUMPYnested_loop_arr_range = nested_loop_arr_range
NUMPYnested_loop_arr_item = nested_loop_arr_item
NUMPYsingle_loop_arr_range = single_loop_arr_range
NUMPYsingle_loop_arr_item = single_loop_arr_item
def nested_NDITER(array_space,N=50,N2=2500):
    ix2d = int()
    for el in np.nditer(array_space):
        array_space[divmod(ix2d,N)] = FUNCTION(el)
        ix2d += 1
    return array_space

def linear_NDITER(array_space,N=50,N2=2500):
    ix1d = int()
    for el in np.nditer(array_space):
        array_space[ix1d] = FUNCTION(el)
        ix1d += 1
    return array_space


def nested_NDENUMERATE(array_space,N=50,N2=2500):
    for ix2d,el in np.ndenumerate(array_space):
        array_space[ix2d] = FUNCTION(el)    
    return array_space

def linear_NDENUMERATE(array_space,N=50,N2=2500):
    for ix1d,el in np.ndenumerate(array_space):
        array_space[ix1d] = FUNCTION(el)    
    return array_space


def single_loop_gen(array_space,N=50,N2=2500):
    gen = iter(array_space)
    while N2 >= 0:
        N2 -= 1
        yield FUNCTION(next(gen))

def nested_loop_gen(array_space,N=50,N2=2500):
    gen = iter(array_space)
    for arr in gen:
        inner_gen = iter(arr)
        for el in inner_gen:
            yield FUNCTION(el)

NUMPYsingle_loop_gen = single_loop_gen
NUMPYnested_loop_gen = nested_loop_gen

def NUMPY_yield_linear(array_space,N=50,N2=2500):
    for el in array_space:
        yield FUNCTION(el)


def NUMPY_yield_nested(array_space,N=50,N2=2500):
    for ndLayer in array_space:
        for el in ndLayer:
            yield FUNCTION(el)

# a = np.array([[1, 2], [3, 4]])
# for index, x in np.nditer(np.ndenumerate(a)): #!GREAT FOR 2D ARRAYS
#     print(index, x)


#*looping and accessing lists
print("nested_loop_arr_range(test_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :nested_loop_arr_range(test_array2d),number=100))

print("nested_loop_arr_item(test_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :nested_loop_arr_item(test_array2d),number=100))

print("single_loop_arr_range(test_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :single_loop_arr_range(test_array1d),number=100))

print("single_loop_arr_item(test_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :single_loop_arr_item(test_array1d),number=100))


#*looping and accessing np.arrays
print("NUMPYnested_loop_arr_range(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYnested_loop_arr_range(numpy_array2d),number=100))

print("NUMPYnested_loop_arr_item(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYnested_loop_arr_item(numpy_array2d),number=100))

print("NUMPYsingle_loop_arr_range(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYsingle_loop_arr_range(numpy_array1d),number=100))

print("NUMPYsingle_loop_arr_item(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYsingle_loop_arr_item(numpy_array1d),number=100))

print("nested_NDITER(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :nested_NDITER(numpy_array2d),number=100))

print("linear_NDITER(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :linear_NDITER(numpy_array1d),number=100))

print("nested_NDENUMERATE(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :nested_NDENUMERATE(numpy_array2d),number=100))

print("linear_NDENUMERATE(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :linear_NDENUMERATE(numpy_array1d),number=100))


#*iterating generators and yielding
print("single_loop_gen(test_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :single_loop_gen(test_array1d),number=100))

print("nested_loop_gen(test_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :nested_loop_gen(test_array2d),number=100))

print("NUMPYsingle_loop_gen(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYsingle_loop_gen(numpy_array1d),number=100))

print("NUMPYnested_loop_gen(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPYnested_loop_gen(numpy_array2d),number=100))

print("NUMPY_yield_linear(numpy_array1d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPY_yield_linear(numpy_array1d),number=100))

print("NUMPY_yield_nested(numpy_array2d) x 100",end=":\t")
print(timeit.timeit(stmt=lambda :NUMPY_yield_nested(numpy_array2d),number=100))


print()#code partially generated from using __name__ of callables


"""
FUNCTION = f=lambda n,a=0,b=1:b/2/n*(b-a)or f(n,b,a+b)

nested_loop_arr_range(test_array2d) x 100:      0.13983829999999997
nested_loop_arr_item(test_array2d) x 100:       0.12455870000000008
single_loop_arr_range(test_array1d) x 100:      0.11735289999999998
single_loop_arr_item(test_array1d) x 100:       0.12294280000000002
NUMPYnested_loop_arr_range(numpy_array2d) x 100:        2.0448250999999997
NUMPYnested_loop_arr_item(numpy_array2d) x 100: 1.7995422999999997
NUMPYsingle_loop_arr_range(numpy_array1d) x 100:        1.7209325
NUMPYsingle_loop_arr_item(numpy_array1d) x 100: 1.8732628
nested_NDITER(numpy_array2d) x 100:     1.6403906999999993
linear_NDITER(numpy_array1d) x 100:     1.5220448000000015
nested_NDENUMERATE(numpy_array2d) x 100:        1.8771842000000003
linear_NDENUMERATE(numpy_array1d) x 100:        1.948681800000001
single_loop_gen(test_array1d) x 100:    3.419999999998424e-05
nested_loop_gen(test_array2d) x 100:    3.460000000110597e-05
NUMPYsingle_loop_gen(numpy_array1d) x 100:      3.459999999932961e-05
NUMPYnested_loop_gen(numpy_array2d) x 100:      3.489999999928273e-05
NUMPY_yield_linear(numpy_array1d) x 100:        3.379999999886252e-05
NUMPY_yield_nested(numpy_array2d) x 100:        3.410000000059199e-05

"""