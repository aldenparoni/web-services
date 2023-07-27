from pathlib import Path
from unifier_requests import bplib
from unifier_requests.ur import temp_dir_path
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur_bp_attach import s_attach
from unifier_requests.ur_bp_attach import attach_from_csv
from uuid import uuid4
from pprint import pprint
import csv

env = 'stage'
project_number = 'jctest21'
bpid = 'uxfr2'

assert env=='stage', 'env must be stage!'
print('ur_bp_attach.attach_from_csv test')
print('env: ', env)
print('project_number: ', project_number)
print('bpid: ', bpid)



# create random text files
n_files = 5
file_paths = []
print('Creating random files...')

# create temp text files and temp csv
temp_csv_name = uuid4().hex+'.csv'
temp_csv_path = temp_dir_path / temp_csv_name
file_paths.append(temp_csv_path)

with open(temp_csv_path,'w', encoding = 'utf-8') as ff:
    fieldnames = ['bpid','project_number','record_no','file_path','title','issue_date','revision_no']
    dw = csv.DictWriter(ff, fieldnames = fieldnames)
    dw.writeheader()
    for _ in range(n_files):
        file_name = uuid4().hex+' txt'
        fp = temp_dir_path / file_name
        fp.write_text(uuid4().hex)
        file_paths.append(fp)
        record_no = 'FR-0001' if (_%2==0) else 'FR-0002'
        row_dict = {'bpid':bpid
            , 'project_number': project_number
            , 'record_no': record_no
            , 'file_path': str(fp)
            , 'title': uuid4().hex
            , 'issue_date': '11/29/2021 10:00:00'
            , 'revision_no': 'A'}
        dw.writerow(row_dict)


results = attach_from_csv(env = env, csv_path = temp_csv_path, return_results = True)
pprint(results)

# delete temp files
for file_path in file_paths:
    file_path.unlink()


