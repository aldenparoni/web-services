from unifier_requests.bplib import uxrf

env = 'prod'
shells = [
    'DB120', 'DB200', 'DB320', 'DB450', 'DBB171', 'DBB271', 'DBB371', 'DBB385',
    'DBB505', 'DBB511', 'DBB511.1', 'DBB511.2', 'DBB525', 'DBB602', 'DBB701',
    'DBB701.1', 'DBOM920', 'DBOM9201', 'FD140', 'FD240', 'FD340',
    'FD430', 'FD440', 'FD530', 'FD550', 'MI930', 'MI940', 'MM905'
]
folder = r'C:\Users\alden.paroni\uxrf-void-unvoid'
file_void = '-uxrf-void.csv'
file_unvoid = '-uxrf-unvoid.csv'

for i in shells:
    x = uxrf(env = env, project_number = i)
    full_void = f'{folder}\\{i}{file_void}'
    full_unvoid = f'{folder}\\{i}{file_unvoid}'
    x.csv_update(full_void)
    x.csv_update(full_unvoid)
    