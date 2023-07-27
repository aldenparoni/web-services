from pathlib import Path
from unifier_requests import bplib
from unifier_requests.ur import temp_dir_path
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur_bp_attach import s_attach
from uuid import uuid4
from pprint import pprint

env = 'stage'
project_number = 'jctest21'
bpid = 'uxfr2'
db_conn = ':memory:'
pool_size = 3

assert env=='stage', 'env must be stage!'
print('ur_bp_attach.s_attach test')
print('env: ', env)
print('project_number: ', project_number)
print('bpid: ', bpid)
print('db_conn: ', db_conn)
print('pool_size: ', pool_size)


con = sqlite3_dict_connect(db_conn)


# create random text files
n_files = 5
file_paths = []
fp_sql_statements = []
print('Creating random files...')
for _ in range(n_files):
    file_name = uuid4().hex+' txt'
    fp = temp_dir_path / file_name
    fp.write_text(uuid4().hex)
    record_no = 'FR-0001' if (_%2==0) else 'FR-0002'
    fp_sql = f'''select '{bpid}' bpid
    , '{project_number}' project_number
    , '{record_no}' record_no
    , '{str(fp)}' file_path
    , '{uuid4().hex}' title
    , '11/29/2021' issue_date
    , 'A' revision_no'''
    fp_sql_statements.append(fp_sql)
    file_paths.append(fp)

# create temp table
print('Creating temp table...')
tbl_name = 'temp_'+uuid4().hex 
create_tbl_sql = f'''create table {tbl_name} as\n'''

fp_sql = '\nunion\n'.join(fp_sql_statements)
create_tbl_sql = create_tbl_sql+fp_sql+';'
print('create_tbl_sql: ')
print(create_tbl_sql)
cur = con.cursor()
cur.execute(create_tbl_sql)
con.commit()

sql = f'select * from {tbl_name};'
results = s_attach(env = env, sql_query = sql, pool_size = pool_size, db_conn = con, return_results = True)
pprint(results)

# delete temp files
for file_path in file_paths:
    file_path.unlink()
con.close()


