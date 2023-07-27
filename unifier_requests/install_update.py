from pathlib import Path
from unifier_requests.udrlib import udr
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur import hm_db_path
from unifier_requests.ur import unifier_requests_path
from unifier_requests.ur import log_dir_path
from unifier_requests.ur import temp_dir_path
import csv

env = 'stage'
hm = Path().home()
logs_dir = log_dir_path
temp_dir = temp_dir_path
bplib_py_path = unifier_requests_path / 'bplib.py'
bplist_csv_path = unifier_requests_path / 'bplist.csv'

def print_if_verbose(input_str, verbose):
    if verbose is True:
        print(input_str)


def get_local_bplist():
    '''
    Return list of dicts of bplist.csv
    '''
    if bplist_csv_path.exists() is False:
        return []
    dr = csv.DictReader(bplist_csv_path.open())
    local_bplist_dicts = list(dr)
    return local_bplist_dicts

def get_cloud_bplist(env = env, verbose = True):
    print_if_verbose('Reading cloud udr "BP List (Integration)" for list of business processes...', verbose)
    x = udr(env,project_number=None)
    report_rows = x.get_dicts(reportname = 'BP List (Integration)', verbose = verbose)
    return report_rows

def compare_bplists(a, b):
    a_bpid = {d['BPID'] for d in a}
    b_bpid = {d['BPID'] for d in b}
    return a_bpid == b_bpid


def update_bplib_py(report_rows, verbose = True):
    bplib_str = '''
from unifier_requests.ur import bpclass
from unifier_requests.install_update import install_update
install_update(verbose = False)

'''
    template = '''
class {BPID}(bpclass):
    def __init__(self, env, project_number, *args, **kwargs):
        super().__init__(env, project_number, *args, **kwargs)
        self.bpname = '{BP_NAME}'
'''
    for report_row in report_rows:
        kwargs = {'BPID':report_row['BPID'], 'BP_NAME':report_row['BP_NAME'].replace("'","\\'")}
        bplib_str = bplib_str + template.format(**kwargs)
        
    print_if_verbose(f'Updating bplib.py: {str(bplib_py_path)}', verbose)
    with open(bplib_py_path,'w') as ff:
        ff.write(bplib_str)
        
    print_if_verbose(f'Updating bplist.csv: {str(bplist_csv_path)}', verbose)
    with open(bplist_csv_path, 'w', newline='') as ff:
        writer = csv.DictWriter(ff, fieldnames=report_rows[0].keys(), quoting = csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(report_rows)
        


def install_update(verbose = True):
    '''
    This script does the following:
        Creates necessary directories (ureqlogs, unifier-requests-TEMP, etc...)
            home/ureqlogs
            home/unifier-requests-TEMP
        Creates necessary files if they don't exist:
            home/unifier_requests_db.db
        Updates bplist.csv to the BPs in the cloud (the list is in the stage env)
        Updates bplib.py to the BPs in the cloud (the list is in the stage env)
    '''
    directories = (logs_dir, temp_dir)
    for directory in directories:
        if not directory.exists():
            directory.mkdir()
            print_if_verbose(f'Created directory: {str(directory)}', verbose)
        else:
            print_if_verbose(f'Directory exists: {str(directory)}', verbose)
    report_rows = get_cloud_bplist(env, verbose)
    local_bplist = get_local_bplist()
    bplists_are_same = compare_bplists(local_bplist, report_rows)
    if bplists_are_same is False:
        print_if_verbose('BP List sync required.', verbose)
        update_bplib_py(report_rows, verbose)
        
    # If home/unifier_requests_db.db does not exist, create it.
    if hm_db_path.exists() is False:
        con = sqlite3_dict_connect()
        con.close()
    print_if_verbose('Exiting...', verbose)

if __name__=='__main__':
    install_update()

