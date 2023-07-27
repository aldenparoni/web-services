from pathlib import Path
from unifier_requests.ur_bp_attach import bp_attach
from unifier_requests.ur import temp_dir_path
from uuid import uuid4
from pprint import pprint

env = 'stage'
project_number = 'jttest1'
record_no = 'DWG-0042'
bpid = 'uxdrw'

# create random text file
file_name = uuid4().hex+' txt'
file_path = temp_dir_path / file_name
file_path.write_text(uuid4().hex)

assert env=='stage', 'env must be stage!'
r = bp_attach(env = env
    , bpid = bpid
    , project_number = project_number
    , record_no = record_no
    , file_path = file_path)

print('env: ', env)
print('project_number: ', project_number)
print('bpid: ', bpid)
print('record_no: ', record_no)
print('file_path: ', str(file_path))

pprint(r)
file_path.unlink()
