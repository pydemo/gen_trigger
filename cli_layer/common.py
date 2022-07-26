import os, json, codecs
from os.path import join, isdir, isfile

CONFIG_DIR  = 'config'

_MAPPING_DIR= 'mapping'
LAYER_DIR   = 'cli_layer'
CFG_LAYER_DIR   = 'config_layer'
MOCK_DIR    = 'mock_data'
STACK_DIR   = 'stack' 
TMPL_DIR    = 'template'
PLAN_DIR    = 'plan'
QUERY_DIR   = 'query'
TEST_EVENT_DIR = 'test_event'
IN_DIR      = 'in'
OUT_DIR     = 'out'
INCLUDE_DIR = 'include'
CODE_DIR    = 'code_staging'
PIPELINE_DIR='pipeline'
SUCCESS = 0
FAILURE = 1
NODATA  = 3

FUNC_DIR = 'lambda_function'

assert 'ZZZ_STACK_NAME__' in os.environ
sn= os.environ['ZZZ_STACK_NAME__']
assert len(sn.split('.'))==2
prj, stack_name = sn.strip().split('.')


if os.name == 'nt':
    SLITE_LOC   = join (LAYER_DIR,'sqlite', 'nt', 'sqlite3.exe')
else:
    SLITE_LOC   = join (LAYER_DIR,'sqlite', 'posix', 'sqlite3')

is_nt=False
if os.name == "nt":
    is_nt=True
    TMP_DIR=join('C:\\','tmp','gh_cli')
    OPT_DIR= ''
    PPL_DIR = join(LAYER_DIR, 'pipeline')
    PPL_DIR = 'pipeline'
    DOWN_DIR=join(TMP_DIR,'downloads')
    IMPLOG_DIR=join(TMP_DIR,'import_log')
else:
    TMP_DIR=join('/tmp','gh_cli')
    #OPT_DIR= join('/opt', 'python')
    OPT_DIR= ''
    PPL_DIR = 'pipeline'
    DOWN_DIR=join(TMP_DIR,'downloads')
    IMPLOG_DIR=join(TMP_DIR,'import_log')
    
if not isdir(TMP_DIR): os.makedirs(TMP_DIR)


def load_config(config_path,  verify_version=True):
    from collections import OrderedDict
    with codecs.open(config_path, encoding="utf-8") as stream:
        data=stream.read()
        config = json.loads(data, object_pairs_hook=OrderedDict)

    return config
join (LAYER_DIR,CONFIG_DIR,'subconfig') 
def perr(err):
    print('#'*80)
    print('#'*80)
    print('ERROR:', err)
    print('#'*80)
    print('#'*80)
    
class dict2(dict):                                                              

    def __init__(self, **kwargs):                                               
        super(dict2, self).__init__(kwargs)                                     

    def __setattr__(self, key, value):                                          
        self[key] = value                                                       

    def __dir__(self):                                                          
        return self.keys()                                                      

    def __getattr__(self, key):                                                 
        try:                                                                    
            return self[key]                                                    
        except KeyError:                                                        
            raise AttributeError(key)                                           

    def __setstate__(self, state):                                              
        pass 

