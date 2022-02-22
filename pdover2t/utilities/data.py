import inspect
import json



def json2globals(json_fp, _globals=None):
    """
    Convert JSON data into variables and import into global scope.
    """
    with open(json_fp, 'r') as _fh:
        data = json.load(_fh)    
    #_globals = globals()
    if _globals is None:
        frame = inspect.stack()[1][0]  #  get calling frame
        _globals = frame.f_globals
    for k,v in data.items():
        if k not in _globals:
            _globals[k] = v


