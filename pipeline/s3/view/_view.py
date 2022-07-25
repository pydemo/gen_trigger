#s3.view.bat
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
from pipeline.s3.view.include.utils import usage
#import cli_layer.pipeline.s3.utils as ppl_utils
from cli_layer.pipeline.utils import get_params

e=sys.exit

log = logging.getLogger()


import cli_layer.config.app_config as app_config
apc = app_config.apc

@timer (basename(__file__))
def s3_view(**kwargs):
	"""	 
	Location	 : s3\view	
	Params : 
		        "bucket" - param 0
        "key" - param 1
	Num of params: 2
	Usage: python cli.py -nop 1 -r DEV -p s3\view -pa bucket key
	"""
	cp, params=usage(**kwargs)
	limit	= kwargs['lame_duck']
	bucket,key = params
	#TODO
	

if __name__=="__main__":
	kwargs={} #TODO
	s3_view(**kwargs)

	