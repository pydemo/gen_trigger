#generate.trigger.bat
import os, sys, csv, time, logging
import datetime as dt
from  datetime import datetime
import decimal
from os.path import split, join, isdir, basename, isfile
from pprint import pprint as pp
from cli_layer.utils import timer, get_err
from pathlib import Path
from cli_layer.common import *
from cli_layer.fmt import  pfmt, pfmtv, pfmtd, psql
#from include.utils import usage
from cli_layer.utils import load_pipeline_module
import cli_layer.config.app_config as app_config
apc = app_config.apc

utils        = load_pipeline_module(apc, join('include','utils'))

#import cli_layer.pipeline.generate.utils as ppl_utils
from cli_layer.pipeline.utils import get_params
import psycopg2

e=sys.exit

log = logging.getLogger()

import cli_layer.config.app_config as app_config
apc = app_config.apc

def get_connection():
        ENDPOINT = "database-1.cluster-ro-c4eshkxebh4n.us-east-1.rds.amazonaws.com"
        PORT = 5432
        USR = "postgres"
        REGION = "us-east-1"
        DBNAME = "postgres"
        PWD ='150Bay;ob'

        try:
            con = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PWD)


        except Exception as e:
            print("Database connection failed due to {}".format(e))
            raise
        return con

def exec_query(con,q):
        try:
            

            cur = con.cursor()
            cur.execute(q)
            query_results = cur.fetchall()
            print('Query results:', len(query_results))
            
        except Exception as e:
            print("Database query failed due to {}".format(e))
            raise
        return query_results
@timer (basename(__file__))
def generate_trigger(**kwargs):
    """	 
    Location	 : generate\trigger	
    Params : 
        "config" - param 0
        "env"    - param 1
    Num of params: 2
    Usage: python cli.py -nop 1 -r DEV -p generate\trigger -pa config.yaml DEV
    """
    cp, params=utils.usage(**kwargs)
    limit	= kwargs['lame_duck']
    config,env = params
    
    if 1:
        #delete_tr = 
        con=get_connection()
        #TODO
        schema_name = 'public'
        table_name  = f'test_delete'
        q=f'''SELECT column_name
      FROM information_schema.columns
     WHERE table_schema = '{schema_name}'
       AND table_name   = '{table_name}'
      order by ordinal_position;'''
        pp(q)
        table_name  = f'{schema_name}.{table_name}'
        data= exec_query(con,q)

        audit_table = f'{schema_name}.sdl_audit'
        if_list=[]
        for d in data:
            col_name, =d

            if_list.append(f'''
        --{col_name}
        if(OLD.{col_name} is not NULL) then 
            INSERT INTO {audit_table} SELECT event_id, '{table_name}', OLD.row_id, 'protocol_id', OLD.{col_name}, null, old.modified_by, now();
        end if;''')
        if_list = ''.join(if_list)
        print(if_list)
    if 1:
        
        tmpl_dir = join(apc.app_dir,'template')
        assert isdir(tmpl_dir),  tmpl_dir
        tmpl_fn = join(tmpl_dir,'delete_trigger.sql')
        assert isfile(tmpl_fn),  tmpl_fn
        with open(tmpl_fn, 'r') as fh:
            tmpl = fh.read()
        #pp(tmpl)
        
        trigger_name = f'{schema_name}.delete_trigger'
        func_name    = f'{schema_name}.delete_func'
        sequence_name= f'{schema_name}.trigger_seq'
        tt=eval(f"f'''{tmpl}'''")
        pp(tt)
        out_fn = 'create_delete_trigger.sql'
        
        with open(out_fn, 'w') as fh:
            fh.write(tt)

if __name__=="__main__":
    kwargs={} #TODO
    generate_trigger(**kwargs)

    