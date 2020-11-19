import functools
import inspect
import logging

logger = logging.getLogger(__name__)



def func_call_exception_trap(func):
    @functools.wraps(func)
    def trap_exception(*args, **kwargs):
        caller = inspect.stack()[1][3]  # gives incorrect module path in turn_on_logging
        # callerObj = inspect.stack()[1][3]
        # print("callerObj=", callerObj, type(callerObj))
        try:
            retObj = func(*args, **kwargs)
        except Exception as err:
            argstr = ""
            for arg in args:
                argstr += f"{arg},"
            for k,v in kwargs.items():
                argstr += f"{k}={v},"
            if argstr.endswith(","): argstr = argstr[:-1]
            logger.error("%s: Exception «%s»; Cannot call function «%s» with arguments (%s)" % (caller, err, func.__name__, argstr))
            retObj = None # float("inf")
            #raise ValueError(f"{caller}: cannot call function «{func.__name__}» with arguments ({argstr})")
        return retObj
    return trap_exception    

