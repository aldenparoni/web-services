from unifier_requests.bplib import uxcor

env = 'prod'
shells = [
    'DB200', 'DB320', 'DB450', 'DBB171', 'DBB271', 'DBB371', 'DBB385', 'DBB505', 'DBB511', 'DBB511.1',
    'DBB511.2', 'DBB525', 'DBB602', 'DBB701', 'DBB701.1', 'DBB921', 'DBOM920', 'UTIL', 'FD140', 'FD240',
    'FD340', 'FD430', 'FD530', 'FD550', 'FD700', 'FD701', 'MI900', 'MI930', 'MM940', 'MM595', 'MM596',
    'MM900', 'MM901', 'MM902', 'MM905', 'MM910', 'MM913', 'MM915', 'MM920', 'MM921', 'MM922', 'MM925',
    'MM930', 'MM935', 'MM936', 'MM937', 'MM940', 'MM941', 'MM945', 'MM950', 'MM951', 'MM953', 'MM960',
    'MM962', 'MM964', 'MM970', 'MM975', 'MM981', 'MM982', 'MM983', 'MM985', 'MM986', 'MM990', 'MM991'
]
folder = r'C:\Users\alden.paroni\uxcor-void-unvoid'
file_void = '-void.csv'
file_unvoid = '-unvoid.csv'

for i in shells:
    x = uxcor(env = env, project_number = i)
    full_void = f'{folder}\\{i}{file_void}'
    full_unvoid = f'{folder}\\{i}{file_unvoid}'
    print(full_void)
    print(full_unvoid)
    