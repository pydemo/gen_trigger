import sys

from cli_layer.fmt import  pfmtd, pfmtv
from cli_layer.pipeline.utils import get_params, check_pcount
from cli_layer.utils import  get_err
from cli_layer.common import  perr, FAILURE

e=sys.exit
def usage(**kwargs):
    pfmtv(kwargs, 'Kwargs.')

    cp, params=get_params(**kwargs)
    pfmtd([cp], 'Params.')
    pcount=2
    try:
        if kwargs['help']:
            assert False, 'Show usage.'    
        check_pcount(params,pcount)
        
        #assert pcount==2+1 #remove
        
        filter,limit = params
        

    except Exception as err:
        error=get_err()
        perr(error)
        pfmtd([dict(Usage=r"""
USAGE:

    python cli.py -nop 1 -r DEV -p aws\list_pipelines -pa filter limit
        
    Number of input paramenters [-nop]:
        "2" - count of pipeline params in "-pa" option.
        
    Runtime environment [-r]:
        "DEV" - runtime name (DEV/UAT/PROD)
        
    Pipeline name [-p]:
        "aws\list_pipelines" - pipeline description.
    
    Pipeline parameters [-pa]:
        "filter" - param 0
        "limit" - param 1
""")])

        e(FAILURE)
    loc=locals()
    out=dict()
    for par in 'filter,limit'.split(','): out[par]=loc[par] 
    pfmtv(out,'',['Parameter', 'Value'])
    
    return (cp, params)