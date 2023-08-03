from unifier_requests.bplib import uxncr

env = 'prod'
shells = [
    'DB120', 'DB200', 'DB320', 'DB450', 'DBB171', 'DBB271', 'DBB371', 'DBB385',
    'DBB505', 'DBB511', 'DBB511.1', 'DBB511.2', 'DBB602', 'DBOM920', 'FD140',
    'FD240', 'FD340', 'FD430', 'FD440', 'FD530', 'MM905', 'MM910'
]
folder = r'C:\Users\alden.paroni\uxncr-void-unvoid'
file_void = '-uxncr-void.csv'
file_unvoid = '-uxncr-unvoid.csv'

for i in shells:
    x = uxncr(env = env, project_number = i)
    full_void = f'{folder}\\{i}{file_void}'
    full_unvoid = f'{folder}\\{i}{file_unvoid}'
    x.csv_update(full_void)
    x.csv_update(full_unvoid)
    