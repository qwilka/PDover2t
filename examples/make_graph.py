

# from ast import literal_eval as make_tuple
# https://stackoverflow.com/questions/9763116/parse-a-tuple-from-a-string
# https://stackoverflow.com/questions/36330860/pythoncially-check-if-a-variable-name-is-valid/36331242

import importlib
import inspect
import keyword

import pdover2t
from pflacs import Loadcase

mod = importlib.import_module("pdover2t.dnvgl_st_f101.press_contain")

def valid_identifier(name):
    avoidlist = ["int", "float", "str", "list", "tuple", "dict", "set"]
    if (str.isidentifier(name) and 
        not keyword.iskeyword(name) and
        name not in avoidlist):
        return True
    else:
        return False


CHECK_MOD = False

if CHECK_MOD:
    for itm in dir(mod):
        print(itm, end="")
        obj = getattr(mod, itm)
        print(" callable", callable(obj), end="")
        print(" isfunction", inspect.isfunction(obj))
        if callable(obj):
            #print(itm)
            try:
                _sig = inspect.signature(obj)
            except (ValueError, TypeError) as err:
                print("inspect.signature: cannot find sig:", itm)
                continue
            #print(list(_sig.parameters.items()))
            print(obj.__annotations__)
            if obj.__name__ == (lambda: None).__name__:   # '<lambda>'
                print("is lambda:", itm)

# from mod import press_contain_unity
# print(press_contain_unity)

# for ii in pkgutil.iter_modules([pathlib.Path(pdover2t.__file__).parent]):
#     print(ii)
# smod = importlib.import_module("."+"dnvgl_st_f101", package='pdover2t')

from pdover2t.dnvgl_st_f101 import press_contain_unity
mod = importlib.import_module(press_contain_unity.__module__)
print(dir(mod))
sig = inspect.signature(press_contain_unity)
#print(sig.parameters)
for _k, _p in sig.parameters.items():
    print(_k, _p.name, _p.annotation)
    if _p.annotation:
        print("_p.annotation is true", _p.annotation, _p.annotation==inspect.Parameter.empty)
print("return annotation:", sig.return_annotation)

parameters = {
    "alpha_U": 1.0,
    "D": 0.6176,
    "g": 9.81,
    "gamma_inc": 1.1,
    "h_ref": 30.,
    "material": "CMn",
    "p_d": 240e5, 
    "rho_cont": 275.,
    "rho_water": 1027.,
    "rho_t": 1027.,
    "SC": "medium",
    "SMYS": 450.e6,
    "SMTS": 535.e6,
    "t": 0.0212,
    "t_corr": 0.0005,
    "t_fab": 0.001,
    "T": 60,
}
basecase = Loadcase("Base case", parameters=parameters,
                data={"desc": "This is the base-case loadcase."})

import networkx as nx
G = nx.DiGraph()

G.add_node(press_contain_unity)
