from pathlib import Path
from unifier_requests.ur_bp_attach import bp_attach
from unifier_requests.ur import temp_dir_path
from uuid import uuid4
from pprint import pprint

env = 'stage'
project_number = 'jttest1'
#record_nos = ['DWG-0024', 'DWG-0028', 'DWG-0031', 'DWG-0035', 'DWG-0040']
#record_nos = ['DWG-0010', 'DWG-0015', 'DWG-0017']
record_nos = ['DWG-0005', 'DWG-0013', 'DWG-0022', 'DWG-0026', 'DWG-0028']

bpid = 'uxdrw'

# create random text file

assert env=='stage', 'env must be stage!'
file_paths = []
for record_no in record_nos:
    file_name = uuid4().hex+' txt'
    file_path = temp_dir_path / file_name
    file_path.write_text(uuid4().hex)
    file_paths.append(file_path)
    r = bp_attach(env = env
        , bpid = bpid
        , project_number = project_number
        , record_no = record_no
        , file_path = file_path)
    pprint(r)

for file_path in file_paths:
    file_path.unlink()


