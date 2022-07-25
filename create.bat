:set ZZZ_STACK_NAME__=Pipline.AU
:set ZZZ_RUNTIME_ENV__=DEV
:create.bat 2 new_pipeline param1 param2
python cli.py -nop 1 -r DEV -p utils/create_pipeline -pa "%*" 