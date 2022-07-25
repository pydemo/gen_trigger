import os, sys, csv, time, logging, shutil
import datetime, decimal
import subprocess
from os.path import split, join, isdir, basename, isfile
from pprint import pprint as pp
from cli_layer.utils import timer, get_err, os_path
from ui_layer.utils import edit_file
from pathlib import Path
from cli_layer.common import PPL_DIR, IN_DIR, OUT_DIR, perr, FAILURE, LAYER_DIR, CFG_LAYER_DIR
from ui_layer.common import UI_TMPL_DIR
from cli_layer.fmt import  pfmt, psql, pfmtd, pfmtv

e=sys.exit

log = logging.getLogger()

PPL_TMPL = join(CFG_LAYER_DIR, 'pipeline','cli_template','new_pipeline.txt')
INC_TMPL = join(CFG_LAYER_DIR, 'pipeline','cli_template','new_includes.txt')

def create_ppl(fn, ppl_body):
    if isfile(fn):
        over = input('\nPipeline "%s" exists. Overwrite? y/n: ' % fn)
        if over.lower() !='y':
            return
    with open(fn, 'w') as fh: fh.write(ppl_body)

def create_ppl_includes(fn, ppl_body):
    if isfile(fn):
        over = input('\nPipeline "%s" exists. Overwrite? y/n: ' % fn)
        if over.lower() !='y':
            return
    with open(fn, 'w') as fh: fh.write(ppl_body)
    
def create_ppl_bat(fn, ppl_bat_body):
    if isfile(fn):
        over = input('\n"%s" file exists. Overwrite? y/n: ' % fn)
        if over.lower() !='y':
            return
    with open(fn, 'w') as fh: fh.write(ppl_bat_body)
    

def create_md(fn, ppl_body):
    if isfile(fn):
        over = input('\nMarkdown "%s" exists. Overwrite? y/n: ' % fn)
        if over.lower() !='y':
            return
    with open(fn, 'w') as fh: fh.write(ppl_body)
            
@timer (basename(__file__))
def utils_create_pipeline(**kwargs):
    
    usage(**kwargs)
    params = kwargs['params']
    pp(params)
    assert params, params
    cp = params.split()
    cp[1] = os_path(cp[1])
    nop = int(cp[0])
    args=cp[2:]
    assert nop==len(args), f'{nop}<>len({args})'
    new_ppl_nop = cp[0]
    if 1: #in
        pp(cp)
        #new_in_dir = join(LAYER_DIR,IN_DIR, os_path(cp[1]))
        new_in_dir = join(IN_DIR, cp[1])
        pp(new_in_dir)
        #e()
        if not isdir(new_in_dir):
            os.makedirs(new_in_dir)
    if 1: #out
        new_out_dir = join(LAYER_DIR, OUT_DIR, os_path(cp[1]))
        new_out_dir = join(OUT_DIR, cp[1])
        pp(new_out_dir)
        if not isdir(new_out_dir):
            os.makedirs(new_out_dir)
    #e()
    if 1: #process pipeline tmpl
        ppl = cp[1].split(os.sep)
        assert type(ppl) == list, f'Pipeline path must be  split by "{os.sep}"'
        
        new_ppl_dir = join(PPL_DIR, cp[1])
        new_ppl = cp[1].split(os.sep)[-1]
        new_ppl_name='%s.py' % new_ppl
        #pp(new_ppl_name)
        
        new_ppl_params=' '.join(cp[2:])
        if 0:
            assert not isdir(new_ppl_dir)
        if not isdir(new_ppl_dir):
            os.makedirs(new_ppl_dir)
        new_ppl_loc=join(new_ppl_dir,new_ppl_name)
        ppl_bat_fn= '%s.bat' % '.'.join([x for x in cp[1].split(os.sep)])
        ppl_sh_fn= '%s.sh' % '.'.join([x for x in cp[1].split(os.sep)])
        if 1: 
            print(PPL_TMPL)
            assert isfile(PPL_TMPL), PPL_TMPL
            with open(PPL_TMPL, 'r') as fh: tmpl=fh.read()
            new_ppl_param_list = '\n'.join(['        "%s" - param %d' % (p, pid) for pid ,p in enumerate(cp[2:])])
            fmdict=dict(new_ppl_nop=new_ppl_nop,new_ppl_name=new_ppl_name, new_ppl_dir=cp[1],new_ppl_param_list=new_ppl_param_list,\
                new_ppl_inc=cp[1].replace('/','.').replace('\\','.'), new_ppl_params=new_ppl_params, new_ppl_param_args=','.join(cp[2:]),\
                new_ppl_method_name='_'.join(cp[1].split(os.sep)), new_inc_1=ppl[0], cmd_file_name=ppl_bat_fn)
            pp(fmdict)
            new_ppl_body = tmpl.format(**fmdict)
            create_ppl(new_ppl_loc, new_ppl_body)
    if 1: #process pipeline includes tmpl
        ppl = cp[1].split(os.sep)
        assert type(ppl) == list, f'Pipeline path must be  split by "{os.sep}"'
        new_ppl_inc_dir = join('pipeline', cp[1], 'include')
        print(new_ppl_inc_dir)
        new_ppl_inc_name= f'utils.py'

        new_ppl_nop = cp[0]
        new_ppl_params=' '.join(cp[2:])

        if not isdir(new_ppl_inc_dir):
            os.makedirs(new_ppl_inc_dir)
        new_ppl_inc_loc=join(new_ppl_inc_dir,new_ppl_inc_name)
        
        if 1: 
            new_ppl_inc_loc=join(new_ppl_inc_dir,new_ppl_inc_name)
            assert isfile(INC_TMPL), INC_TMPL
            with open(INC_TMPL, 'r') as fh: tmpl=fh.read()
            new_ppl_param_list = '\n'.join(['        "%s" - param %d' % (p, pid) for pid ,p in enumerate(cp[2:])])
            fmdict=dict(new_ppl_nop=new_ppl_nop,new_ppl_name=new_ppl_inc_name, new_ppl_dir=cp[1],new_ppl_param_list=new_ppl_param_list, \
            new_ppl_params=new_ppl_params, new_ppl_param_args=','.join(cp[2:]), new_inc_1=ppl[0])
            new_ppl_body = tmpl.format(**fmdict)
            create_ppl_includes(new_ppl_inc_loc, new_ppl_body)

    if 1: #create default ui json
        ppl = cp[1].split(os.sep)
        assert type(ppl) == list, f'Pipeline path must be  split by "{os.sep}"'
        new_ppl_ui_dir = join('pipeline', *ppl,'ui')
        print(new_ppl_ui_dir)
        #e()
        #default_ui_loc = join(UI_TMPL_DIR, 'common', 'default.json')
        default_ui_loc = join(CFG_LAYER_DIR, 'pipeline','ui_template','default.json')

        new_ppl_nop = cp[0]
        new_ppl_params=' '.join(cp[2:])

        if not isdir(new_ppl_ui_dir):
            os.makedirs(new_ppl_ui_dir)
        assert isfile(default_ui_loc), default_ui_loc
        assert isdir(new_ppl_ui_dir), new_ppl_ui_dir
        shutil.copy(default_ui_loc,new_ppl_ui_dir)
            

            
    
    
    if 1: #create *.bat file
        bat_cmd='python cli.py  -nop {new_ppl_nop} -r DEV -p {new_ppl_dir} -pa {new_ppl_params}  %*'.format(**fmdict)
        pfmtd([{ppl_bat_fn : bat_cmd}], 'New nt pipeline "%s".' % join(cp[1],new_ppl_name))
        create_ppl_bat(ppl_bat_fn, bat_cmd+os.linesep)
        
    if 1: #create *.sh file
        new_ppl_dir_sh = cp[1].replace('\\','/')
        fmdict.update(dict(new_ppl_dir_sh=new_ppl_dir_sh))
        sh_cmd='python cli.py  -nop {new_ppl_nop} -r DEV -p {new_ppl_dir_sh} -pa {new_ppl_params}  %*'.format(**fmdict)
        pfmtd([{ppl_sh_fn : sh_cmd}], 'New posix pipeline "%s".' % join(cp[1],new_ppl_name))
        create_ppl_bat(ppl_sh_fn, sh_cmd+'\n')
        
    if 1: #create *.md file
        dir_1=cp[1].split(os.sep)[0]
        md_dir=join(PPL_DIR,'_docs', dir_1)
        if not isdir(md_dir): os.makedirs(md_dir)
        
        md_fn=join(md_dir, '%s.md' % cp[1].replace(os.sep,'.'))
        md_body="""
## nt
```%s```
## posix
```%s```
""" % (bat_cmd.strip('%*'), sh_cmd.strip('%*'))
        create_md(md_fn, md_body)
    if 1:
        edit_file(ppl_bat_fn)
        edit_file(md_fn)
        edit_file(new_ppl_loc)
        edit_file(new_ppl_inc_loc)
    
def check_pcount(params,pcount):
    
    if pcount == 1:
        assert params, 'Empty params.'
        assert type(params) in [str], params
        return
    
    assert len(params)==pcount, '%d - wrong parameter count (expecting %d)' % (len(params),pcount)

def usage(**kwargs):
    pfmtv(kwargs, 'Kwargs.')

    params = kwargs['params']
    pcount=1
    
    try:
        if kwargs['help']:
            assert False, 'Show usage.'    
        check_pcount(params,pcount)
        #e()
    except Exception as err:
        error=get_err()
        perr(error)
        pfmtd([dict(Usage=r"""
USAGE:

    python cli.py -nop 1 -r DEV -p utils\create_pipeline -pa " 2 import_csv\3rd_party\Microwell in_file out_file"
        
    Number of input paramenters [-nop]:
        "1" - count of pipeline params in "-pa" option.
        
    Runtime environment [-r]:
        "DEV" - runtime name (DEV/UAT/PROD)
        
    Pipeline name [-p]:
        "import_csv\create_pipeline" - pipeline used to bootstrap new pipeline.
    
    Pipeline parameters [-pa]:
        "pipeline_name" - new pipeline name
        "param_cnt"  - param count (to new pipeline) 
        "param_1 ... param_n"  - param list (to would be new pipeline)
""")])

        e(FAILURE)



    