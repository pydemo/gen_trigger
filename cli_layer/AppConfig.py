import os, re, sys, copy, string, logging 
from os.path import isfile, isdir, join, basename
import json
from datetime import datetime 
from copy import deepcopy
from pprint import pprint as pp
from cli_layer.Config import *
import shutil
import logging

log=logging.getLogger()

e=sys.exit


class AppConfig(Config): 
    def __init__(self, **kwargs):
        Config.__init__(self,**kwargs)
        if 1:
            cfg_root =TMP_DIR
            cfgfn = 'GH_cli.json'
            cfg_loc = join(cfg_root, cfgfn)

        self.apc_path=cfg_loc
        if not isfile(cfg_loc):
            self.initCfgFile(path=cfg_loc)
        self.kwargs=kwargs
        self.cli_layout=kwargs.get('cli_layout')
        self.app_dir = join(self.pipeline_dir, self.cli_layout)
    def getConn(self):
        env=self.env
        cfg=self.cfg
        assert env in cfg.env
        ckey = cfg.env[env][self.conn_name]
        conn = cfg.stores[ckey]
        assert 'conn_string' in conn
        assert conn.conn_string
        assert 'env_refs' in conn
        assert conn.env_refs
        for k in list(conn.env_refs.keys()):
            v=conn.env_refs[k]
            if type(v) == list: # it's env var
                var=v[0]
                conn.env_refs[k] = os.environ[var]
        
        conn.conn_string=conn.conn_string.format(**conn.env_refs)

        return conn
    def setConnName(self, cname):  
        self.conn_name=cname
 
