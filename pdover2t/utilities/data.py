import inspect
import json
import logging

import numpy as np

# https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python

logger = logging.getLogger(__name__)


def json2globals(json_fp, mapvars=None, _globals=None, clobber=False):
    """
    Convert JSON data into variables and import into global scope.
    """
    with open(json_fp, 'r') as _fh:
        data = json.load(_fh)    
    #_globals = globals()
    varnames = []
    if _globals is None:
        frame = inspect.stack()[1][0]  #  get calling frame
        _globals = frame.f_globals
    # vectorize the items listed in _vnmeta.vectorize
    # NOTE: each item must be an array/list
    # NOTE: item names as per json file (not mapvars)
    vectorize = data["_vnmeta"].get("vectorize", None) if "_vnmeta" in data else None
    if vectorize:
        for dpath in vectorize:
            _val = dotted_get(data, dpath)
            if _val and isinstance(_val, list):
                dotted_set(data, dpath, np.array(_val))
            else:
                logger.warning("json2globals: cannot vectorize: «%s» in «%s»" % (dpath, json_fp))
    for k,v in data.items():
        if not clobber and k in _globals: continue
        if k in ["_vnmeta"]: continue
        if mapvars and k in mapvars:
            key = mapvars[k]
        else:
            key = k
        _globals[key] = v
        varnames.append(key)
    logger.warning("json2globals: adding variables to global scope: %s from «%s»" % (str(varnames), json_fp))
    _meta = data["_vnmeta"].copy() if "_vnmeta" in data else {}
    _meta["_globals"] = varnames
    return _meta


def dotted_get(obj, dotted):
    keys = dotted.split(".")
    _o = obj
    for k in keys:
        _k = int(k) if k.isnumeric() else k
        #_o = _o[_k]
        try:
            _o = _o[_k]
        except Exception as err:
            logger.error("dotted_get: cannot find item: %s; %s" % (k, err))
            #raise KeyError(f"dotted_get: cannot find item: {k}; {err}")
            return None
    return _o


def dotted_set(obj, dotted, value):
    keys = dotted.split(".")
    _o = obj
    for k in keys[:-1]:
        _k = int(k) if k.isnumeric() else k
        _o = _o[_k]
    _k = int(keys[-1]) if keys[-1].isnumeric() else keys[-1]
    _o[_k] =  value
    return True


# def is_int(s):
#     try:
#         num = int(s)
#         return num
#     except ValueError:
#         return False
