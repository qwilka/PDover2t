import json



def json2globals(json_fp, _globals):
    with open(json_fp, 'r') as _fh:
        data = json.load(_fh)    
    #_globals = globals()
    for k,v in data.items():
        if k not in _globals:
            _globals[k] = v


