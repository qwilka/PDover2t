"""

https://stackoverflow.com/questions/26180528/convert-a-namedtuple-into-a-dictionary/26180604#26180604
"""
#from collections import namedtuple
#import inspect
import logging
import sys

logger = logging.getLogger(__name__)

from ..config import use_numpy

if use_numpy:
    import numpy as np

# use_numpy = False
# if use_numpy:
#     import numpy as np
# # if "numpy" in sys.modules:
# #     import numpy as np

# #def makeReturnNamedTuple(typename, field_names, func_locals):
# def make_return_namedtuple(field_names, typename=None, prepend_name=False):

#     # https://github.com/python/cpython/blob/main/Lib/collections/__init__.py
#     if isinstance(field_names, str):
#         field_names = field_names.replace(',', ' ').split()
#     field_names = list(map(str, field_names))

#     # https://docs.python.org/3/library/inspect.html#inspect.currentframe
#     # https://stackoverflow.com/a/900404
#     if not typename:
#         typename = inspect.currentframe().f_back.f_code.co_name # .title().replace("_", "")
#         #print(f"{typename=}")
#     func_locals = dict(inspect.currentframe().f_back.f_locals)

#     field_dict = {}
#     # if prepend_name:
#     #     field_dict[typename] = ""
#     for _name in field_names:
#         if _name in func_locals:
#             field_dict[_name] = func_locals[_name]
#         else:
#             raise ValueError('make_return_namedtuple: ' + typename + ' Field missing: ' + _name)

#     # if prepend_name:
#     #     field_names.insert(0, typename)

#     retTuple = namedtuple(typename, field_names)
#     return retTuple(**field_dict)



def min_nums_vectors(nums_vectors):
    if all( list( map(lambda ii: isinstance(ii, (int, float)), nums_vectors) ) ):
        return min(nums_vectors)
    # if use_numpy:
    if "numpy" in sys.modules:
        import numpy as np
        # for itm in nums_vectors:
        #     if isinstance(itm, np.ndarray):
        mins = np.min( np.column_stack( np.broadcast_arrays(*nums_vectors) ), axis=1)
        return mins




if __name__=="__main__":
    larray = [3, 1, -5, 7]
    minval = min_nums_vectors(larray)
    print(f"{larray=} {minval=}")

    if use_numpy:
        import numpy as np
        larray = [3, np.array([4,-6.2,3.2, -100.1]), -5, np.array([4,-2,3.2,40.1]), 0.8]
        minval = min_nums_vectors(larray)
        print(f"{larray=} {minval=}")
