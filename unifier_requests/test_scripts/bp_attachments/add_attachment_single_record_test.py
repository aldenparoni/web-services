from pathlib import Path
from unifier_requests import bplib
from unifier_requests.ur import temp_dir_path
from uuid import uuid4
from pprint import pprint

env = 'stage'
project_number = 'jctest21'
record_no = 'FR-0002'
bpid = 'uxfr2'
version = 'v1'

# create random text file
file_name = uuid4().hex+' txt'
file_path = temp_dir_path / file_name
file_path.write_text(uuid4().hex)

assert env=='stage', 'env must be stage!'
_bp = getattr(bplib, bpid)
x = _bp(env = env, project_number = project_number)

data = {'record_no': record_no}
input_attachments = {'file_path': file_path}


r = x.add_attachment_single_record(data = data
    , input_attachments = input_attachments
    , version = version)


print('env: ', env)
print('project_number: ', project_number)
print('bpid: ', bpid)
print('record_no: ', record_no)
print('file_path: ', str(file_path))
print('version: ', version)

pprint(r)
file_path.unlink()




