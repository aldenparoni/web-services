from unifier_requests.bplib import uxcor

env = 'prod'
shells = ['ART', 'DB120']
folder = r'C:\Users\alden.paroni\uxcor-void-unvoid'
file_void = '-void.csv'
file_unvoid = '-unvoid.csv'

for i in shells:
    x = uxcor(env = env, project_number = i)
    full_void = f'{folder}\\{i}{file_void}'
    full_unvoid = f'{folder}\\{i}{file_unvoid}'
    x.csv_update(full_void)
    x.csv_update(full_unvoid)
    