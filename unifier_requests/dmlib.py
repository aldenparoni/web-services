import io
from unifier_requests.ur import gen_random_string
from unifier_requests.ur import throwaway_prefix
from unifier_requests.ur import urestv1
from unifier_requests.ur import urestv2
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur import timestamp_ymd
from unifier_requests.ur import log_pkl
from unifier_requests.ur import write_dicts_to_db
from unifier_requests.ur import write_dicts_to_csv
from unifier_requests.ur import prompt_random_string
from unifier_requests.ur import create_session_queue
from unifier_requests.ur import close_session_queue
from unifier_requests.ur import get_store_if_exists_default
from unifier_requests.ur import get_all_dict_fields
from unifier_requests.ur import download_default_path
from unifier_requests.ur import s_default_pkcols
from unifier_requests.udrlib import udr
from urllib.parse import urlencode
import requests
from requests_toolbelt import MultipartEncoder
import uuid
from uuid import uuid4
from pprint import pprint
from queue import Queue
from queue import PriorityQueue
import pathlib
import sqlite3
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import date
import time
import pickle
from collections import namedtuple
from collections import Counter
from itertools import filterfalse
from datetime import datetime
import re
import json
import sys
import shutil

DM_Report_Name = 'DM Report (Integration)'

ls_field = namedtuple('ls_field','name length r_name')
ls_fields = (
    ls_field(name='type', length=10, r_name = 'type')
    , ls_field(name = 'Node ID', length = 15, r_name = 'node_id')
    , ls_field(name = 'file_id', length = 15, r_name = 'file_id')
    , ls_field(name='Name',length=75, r_name='Name')
    , ls_field(name='Creation Date', length = 20 , r_name ='Creation Date')
    , ls_field(name = 'Size', length = 12, r_name = 'Size')
    )


ls_template = ''.join(['{'+field.name+':'+str(field.length)+'.'+str(field.length-2)+'}' for field in ls_fields])
ls_header = ls_template.format(**{_field.name:_field.name for _field in ls_fields})

def get_node_info(env, node_id, session = None):
    x = udr(env = env, project_number = None, session = session)
    query = {'label':'_doc_manager_nodes / ID', 'value1':str(node_id)}
    r = x.get_dicts(reportname = DM_Report_Name, query = query)
    if len(r) == 0:
        return {}
    return r[0]


def get_node_info_by_path(env, project_number_path, session = None):
    x = udr(env = env, project_number = None, session = session)
    query = {'label':'_doc_manager_nodes / PROJECT_NUMBER_PATH', 'value1':str(project_number_path)}
    r = x.get_dicts(reportname = DM_Report_Name, query = query)
    if len(r) == 0:
        return {}
    if len(r) > 1:
        raise Exception('There are more than one nodes with this path!')
    return r[0]

def check_path_exists(env, project_number_path, session = None):
    __result = get_node_info_by_path(env = env, project_number_path = project_number_path, session = session)
    if __result == {}:
        return False
    return True

def s_check_path_exists(env, sql_query, pool_size = 4, return_results = False, db_conn = None, tbl_name = None):
    '''
    sql_query required column: project_number_path
    '''
    __db_conn = sqlite3_dict_connect() if db_conn is None else db_conn
    cur = __db_conn.cursor()
    input_jobs = cur.execute(sql_query).fetchall()
    session_queue = create_session_queue(size = pool_size)
    all_dict_fields = get_all_dict_fields(input_dicts = input_jobs)
    assert 'project_number_path' in all_dict_fields, 'project_number_path column is missing!'
    __pkcols = [pkcol for pkcol in s_default_pkcols.split(';') if pkcol in all_dict_fields]
    def job_func(input_job):
        try:
            project_number_path = input_job['project_number_path']
            __session = session_queue.get()
            __check = check_path_exists(env = env, project_number_path = project_number_path, session = __session)
        except Exception as e:
            __session = requests.Session()
            __check = f'Exception encountered! {e}'
        finally:
            session_queue.put(__session)
            return_dict = {'project_number_path':project_number_path, 'check_result': __check}
            if len(__pkcols) > 0:
                for pk_col in __pkcols:
                    return_dict[pk_col] = input_job.get(pk_col, None)
            return return_dict
    with ThreadPoolExecutor(max_workers = pool_size) as ex:
        results = ex.map(job_func, input_jobs)
    results = list(results)
    close_session_queue(session_queue)
    if tbl_name is None:
        __tbl_name = throwaway_prefix+timestamp_ymd()+'_'+'s_check_path_exists_'+str(uuid.uuid4()).replace('-','').lower()
    else:
        __tbl_name = tbl_name
    write_dicts_to_db(input_dicts = results, tbl_name = __tbl_name, db_con = __db_conn)
    print('Wrote to table: ', __tbl_name)
    if db_conn is None:
        __db_conn.close()
    if return_results is True:
        return results


def run_dm_report(env, project_number, tbl_name = None, session = None, db_conn = None, query = None, if_exists = get_store_if_exists_default):
    x = udr(env = env, project_number = None, session = session)
    if query is not None:
        __query = query
    else:
        __query = {'label':'_doc_manager_nodes / PROJECT_NUMBER', 'value1':project_number}
    results = x.get_dicts(reportname = DM_Report_Name, query = __query)
    if tbl_name is None:
        tag = uuid4().hex
        ts = timestamp_ymd()
        tbl_name = throwaway_prefix +'_'+ 'DM_REPORT'+'_'+ts+tag
    _db_conn = sqlite3_dict_connect() if db_conn is None else db_conn
    write_dicts_to_db(input_dicts = results, tbl_name = tbl_name, db_con = _db_conn, if_exists = if_exists)
    if len(results) == 0:
        create_tbl_sql = f'''create table {tbl_name} (file_id integer, id integer, name text, node_path text, type text, parent_node_id integer, project_id integer, project_number text, project_number_path text);'''
        cur = _db_conn.cursor()
        cur.execute(create_tbl_sql)
        _db_conn.commit()
        cur.close()
    print('Wrote DM Report results to ', tbl_name)
    if db_conn is None:
        _db_conn.close()
    return tbl_name

def _s_check_project_numbers(dm_object, row):
    '''Compare project_number and raise Exception if there is a mismatch'''
    if 'project_number' not in row:
        raise Exception('"project_number" column is missing!')
    if dm_object.project_number is None:
        # inherit the project_number from the row
        return row['project_number']
    else: 
        if 'project_number' in row:
            if dm_object.project_number != row['project_number']:
                raise Exception('Mismatching project_number occured!')
        return dm_object.project_number

def folder_filter(input_dict):
    if input_dict.get('type','').lower()=='folder':
        return True
    return False

def ls_disp(list_of_dicts):
    '''Print out a list of dicts in a formatted manner'''
    assert isinstance(list_of_dicts, list), 'input must be a list of dicts!'
    print(ls_header)
    # print Folders first, then documents (alphabetical order)
    for d in sorted(list_of_dicts, key=lambda y: (0 if folder_filter(y) else 1,y.get('node_path',''))):
        __row = ls_template.format(**{_ls_field.name:truncate_str(d.get(_ls_field.r_name, ''), _ls_field.length-2)
                for _ls_field in ls_fields})
        print(__row)

def truncate_str(input_str, max_len):
    '''Truncate a string and end it with ellipses'''
    assert isinstance(max_len, int), 'max_len must be a integer!'
    assert max_len > 3, 'max_len must be greater than 3!'
    __input_str = str(input_str)
    return __input_str[:max_len-3]+'...' if len(__input_str)>max_len else __input_str

class FolderServices:
    '''Folder Services (see "Folder Services" under REST Web Services V1'''
    def __init__(self, env, project_number, pwd=None, session=None, log_enable=True):
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        if (pwd is not None) and (not pwd.startswith('/')):
            raise Exception('pwd must start with \'/\'!')
        self.project_number = project_number
        self.env = env
        self.session_v1 = urestv1(env=env, log_enable = log_enable)
        self.session_v2 = urestv2(env = env, log_enable = log_enable)
        self.session_queue = None
        self.session_object = session if session else requests.Session()
        self._pwd = '/' if pwd is None else pwd
        self._ls_cache = None
    
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.env}\', \'{self.project_number}\')\r\npwd: {self.pwd}'
    
    def _mkdir(self, Name, Path, verbose = True, **kwargs):
        # see "Create Folders by Path" under REST Web Services V1
        endpoint = '/dm/folder/create'
        body = urlencode({'projectnumber':self.project_number, 'data':[{'Path':Path, 'Name':Name, **kwargs}]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
            
    def mkdir(self, Name, Path=None, verbose = True, **kwargs):
        '''Make directory - point the Path variable to what is stored in self.pwd if there is no input Path'''
        __Path = self.pwd if Path is None else Path
        return self._mkdir(Name = Name, Path = __Path, verbose = verbose, **kwargs)
            
    def mkdir_id(self, Name, parent_folder_id, verbose = True, **kwargs):
        # see "Create Folders by Parent Folder ID under REST Web Services V1
        __parent_folder_id = str(parent_folder_id) if (not isinstance(parent_folder_id, str)) else parent_folder_id 
        endpoint = f'/dm/folder/create/{__parent_folder_id}'
        body = urlencode({'projectnumber':self.project_number, 'data':[{'Name':Name, **kwargs}]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
    
    def _update_dir_metadata(self, Path, verbose = True, **kwargs):
        # see "Update Folders Meta Data by Path"
        endpoint = f'/dm/folder/update'
        body = urlencode({'projectnumber':self.project_number, 'data':[{'Path':Path, **kwargs}]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
    
    def _update_dir_metadata_id(self, node_id, verbose = True, **kwargs):
        # see "Update Folder Meta Data by Folder ID"
        __node_id = str(node_id) if not isinstance(node_id, str) else node_id
        endpoint = f'/dm/folder/update/{__node_id}'
        body = urlencode({'projectnumber':self.project_number, 'data':[kwargs]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
    
    def _get_dir_metadata(self, parentpath, nodetype=None, verbose = True):
        # see "Get Folders or Documents Meta Data by Path
        endpoint = '/dm/node/properties'
        __body = {'parentpath':parentpath}
        if self.project_number is not None:
            __body['projectnumber'] = self.project_number
        if nodetype is not None:
            if nodetype.lower() not in ('document','folder'):
                raise Exception("nodetype not in ('Document','Folder')!")
            __body['nodetype'] = nodetype
        body = urlencode(__body)
        return self.session_v1.get(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
    
    def get_dir_metadata(self, parentpath, nodetype=None, verbose = True):
        return self._get_dir_metadata(parentpath = parentpath, nodetype = nodetype, verbose = verbose)
    
    def _get_dir_metadata_id(self, parent_folder_id, nodetype=None, verbose = True):
        __parent_folder_id = str(parent_folder_id) if not isinstance(parent_folder_id, str) else parent_folder_id
        endpoint = f'/dm/node/properties/{__parent_folder_id}'
        __body = {'projectnumber':self.project_number}
        if nodetype is not None:
            if nodetype.lower() not in ('document', 'folder'):
                raise Exception("nodetype not in ('document', 'folder')!")
            __body = {'nodetype':nodetype}
        body = urlencode(__body)
        return self.session_v1.get(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
    @property
    def pwd(self):
        return self._pwd
    @property
    def ls(self):
        __r = self._get_dir_metadata(self.pwd)
        __rd = __r['data']
        self._ls_cache = __r
        print('Current Directory:', self.pwd, end='\n\n')
        ls_disp(__rd)
    @property
    def ls2(self):
        return self._get_dir_metadata(self.pwd)
        
    def cd(self, input_dir):
        assert isinstance(input_dir, str) or isinstance(input_dir, int), 'input_dir must be a str or int!'
        if isinstance(input_dir, str):
            if input_dir.startswith('/'):
                __path = input_dir
            else:
                __path = '/'+input_dir if self.pwd=='/' else self.pwd+'/'+input_dir
            __r = self._get_dir_metadata(__path)
            if __r['status']==200:
                self._pwd = __path
                self._ls_cache=__r
                print('Current Directory: ', self.pwd, end='\n\n')
                ls_disp(__r['data'])
    @property
    def up(self):
        __path = self.pwd.rsplit('/',1)[0]
        if __path=='':
            __path='/'
        self.cd(__path)
                
    def run_dm_report(self, tbl_name = None, db_conn = None, query = None, if_exists =get_store_if_exists_default):
        return run_dm_report(env = self.env
                    , project_number = self.project_number
                    , session = self.session_object
                    , tbl_name = tbl_name
                    , db_conn = db_conn
                    , query = query
                    , if_exists = if_exists)
            
    def walk(self, top, tbl_name = None, db_conn = None, if_exists =get_store_if_exists_default):
        __top = top
        assert isinstance(__top, str), 'top must be a str!'
        assert __top.startswith('/'), "unifier_top must start with '/' (ex: '/04 Plans', '/09 Correspondence', or '/' for the root Project Documents folder)"
        print('Checking that unifier_top exists...')
        if __top.endswith('/') and (len(__top)>1):
            check_project_number_path = self.project_number+'_'+__top[:-1]
        else:
            check_project_number_path = self.project_number+'_'+__top   
        __unifier_top_exists = check_path_exists(env = self.env
                    , project_number_path = check_project_number_path
                    , session = self.session_object)
        if __unifier_top_exists is False:
            raise Exception('unifier_top does not exist!')
        __db_con = sqlite3_dict_connect() if db_conn is None else db_conn
        ts = timestamp_ymd()
        random_tag = uuid4().hex
        if tbl_name is None:
            tbl_name = throwaway_prefix+'_'+'DM_WALK_'+self.env+'_'+ts+random_tag
        __project_number_path_contains = self.project_number+'_'+top
        __query = {'label':'_doc_manager_nodes / PROJECT_NUMBER_PATH_CONTAINS','value1': str(__project_number_path_contains)}
        self.run_dm_report(tbl_name = tbl_name, db_conn = __db_con, if_exists = if_exists, query = __query)
        cur = __db_con.cursor()
        if not __top.endswith('/'):
            sql = f'''delete from {tbl_name} where node_path not like '{__top.replace("'","''")}/%';'''
        else:
            sql = f'''delete from {tbl_name} where node_path not like '{__top.replace("'","''")}%';'''
        cur.execute(sql)
        __db_con.commit()
        cur.execute(f'''delete from {tbl_name} where project_number <> '{self.project_number}';''')
        __db_con.commit()
        if db_conn is None:
            __db_con.close()
        print(f'Walk results written to: {tbl_name}')
        return tbl_name
                
    def walk_compare(self
            , top
            , unifier_top
            , pool_size = 4
            , return_results= False
            , omit_subset = None
            , db_conn = None
            , folders_only = False
            , glob = '*'):
        assert isinstance(top, pathlib.Path) or isinstance(top, str), 'top must be a str or Path object!'
        if isinstance(top, str):
            if top=='.' or top==pathlib.Path('.'):
                __top = pathlib.Path().cwd()
            else:
                __top = pathlib.Path(top)
        else:
            __top = top
        assert __top.is_dir(), f'Input (local) top is not a valid dir! {str(__top)}'  
        if omit_subset is not None:
            assert isinstance(omit_subset, str) or isinstance(omit_subset, list), 'omit_subset must be a list or str!'
            if isinstance(omit_subset, list):
                if all(isinstance(j, pathlib.Path) for j in omit_subset):
                    __omit_subset = omit_subset
                else:
                    __omit_subset = [pathlib.Path(j) for j in omit_subset]
            else:
                __omit_subset = [pathlib.Path(omit_subset)]
        print(f'{__name__}:: Fetching unifier DM contents...')
        t1 = time.time()
        __db_conn = sqlite3_dict_connect() if db_conn is None else db_conn
        walk_tbl_name = self.walk(top = unifier_top, db_conn = __db_conn)
        cur = __db_conn.cursor()
        cur.execute(f'''select id, parent_node_id, node_path, project_number from {walk_tbl_name} where lower(type) = 'folder';''')
        unifier_folder_paths = {d['node_path']: {**d, **{'in_unifier':True}} for d in cur}
        cur.execute(f'''select id, parent_node_id, node_path, project_number from {walk_tbl_name} where lower(type) = 'document';''')
        unifier_document_paths = {d['node_path']: {**d, **{'in_unifier':True}} for d in cur}
        unifier_top_path = pathlib.PurePosixPath(unifier_top)
        local_walk_results = [] 
        print('Fetching local contents...')
        __empty_result = {'id':None, 'parent_node_id':None, 'node_path':None, 'project_number': None, 'in_unifier':False}
        for iter_path in __top.rglob(glob):
            str_iter_path = str(iter_path)
            if omit_subset is not None:
                if any(str_iter_path.startswith(str(omit_path)) for omit_path in __omit_subset):
                    continue
            relative_segment = iter_path.relative_to(__top)
            __unifier_node_path = pathlib.PurePosixPath(unifier_top_path.joinpath(relative_segment))
            unifier_node_path = str(__unifier_node_path)
            path_type = 'Folder' if iter_path.is_dir() else 'Document'
            if path_type =='Folder':
                unifier_entry = unifier_folder_paths.get(unifier_node_path, __empty_result)
            else:
                if folders_only is True:
                    continue
                unifier_entry = unifier_document_paths.get(unifier_node_path, __empty_result)
            d = {'unifier_node_path': unifier_node_path
                , 'local_node_path': str_iter_path
                , 'local_node_path_object': iter_path
                , 'unifier_node_path_object': __unifier_node_path
                , 'type': path_type
                , 'name': iter_path.name
                , 'unifier_parent_path': str(__unifier_node_path.parent)
                , 'in_unifier': unifier_entry['in_unifier']
                , 'id': unifier_entry['id']
                , 'parent_node_id': unifier_entry['parent_node_id']
                , 'project_number': unifier_entry['project_number']
                }
            local_walk_results.append(d)
        t2 = time.time()
        print(f'Completed in {str(t2-t1)}s')
        ts = timestamp_ymd()
        tag = uuid4().hex
        log_name = f'dm_walk_compare_{self.env}_'+ts+tag
        log_tbl_name = throwaway_prefix+log_name
        tbl_fields = 'unifier_node_path;local_node_path;type;name;unifier_parent_path;in_unifier;id;parent_node_id;project_number'
        pkl_path = log_pkl(input_object = local_walk_results, name = log_name, timestamp = False, random_tag = False)
        write_dicts_to_db(input_dicts = local_walk_results, tbl_name = log_tbl_name, tbl_fields=tbl_fields, db_con = __db_conn)
        if db_conn is None:
            __db_conn.close()
        csv_path = write_dicts_to_csv(input_dicts = local_walk_results, name = log_name , tbl_fields = tbl_fields)
        print(f'{__name__}:: Wrote walk_compare results to (pkl): ', str(pkl_path))
        print(f'{__name__}:: Wrote walk_compare results to (csv): ', str(csv_path))
        print(f'{__name__}:: Wrote walk_compare results to (tbl): ', log_tbl_name)
            
        if return_results is True:
            return local_walk_results
    def walk_recursive(self
            , top
            , pool_size = 4
            , tbl_name = None
            , db_conn = None
            , if_exists = get_store_if_exists_default):
        assert isinstance(top, (int, str)), 'top must be a str or int!'
        __db_conn = sqlite3_dict_connect() if db_conn is None else db_conn
        dm_queue = Queue()
        for _ in range(pool_size):
            dm_queue.put(DM(env = self.env, project_number = self.project_number))
        job_queue = Queue()
        job_queue.put(top)
        def remove_special_chars_in_keys(input_dict):
            return {
                'id': input_dict['node_id']
                , 'file_id': input_dict.get('file_id', None)
                , 'Owner': input_dict['Owner']
                , 'project_number': self.project_number
                , 'projectnumber':input_dict['projectnumber']
                , 'node_path':input_dict['node_path']
                , 'Description': input_dict['Description']
                , 'type': input_dict['type'].lower()
                , 'name': input_dict['Name']
                , 'parent_node_id': input_dict['parent_node_id']
                , 'creation_date':input_dict['Creation Date']
                , 'project_id':input_dict['project_id']
                , 'project_number_path':f'{self.project_number}_'+input_dict['node_path']
                , 'uuu_content_status':input_dict['uuu_content_status']
                , 'pct_complete': input_dict['% Complete']
                , 'location': input_dict['Location']
                }
        tbl_fields = 'id;file_id;projectnumber;node_path;Description;type;name;parent_node_id;creation_date;project_id;project_number;project_number_path;location;Owner'
        total_results = dict()
        def job_func(parent_path):
            try:
                x = dm_queue.get()
                if isinstance(parent_path, str):
                    r = x._get_dir_metadata(parentpath = parent_path)
                else:
                    r = x._get_dir_metadata_id(parent_folder_id = parent_path)
                assert r['status']==200, f"Error: {r['status']}, {str(r['message'])}"
                rd = r.get('data',[])
                #pprint(rd)
                if len(rd) > 0:
                    total_results[parent_path] = []
                    for d in rd:
                        if isinstance(d, dict):
                            d = remove_special_chars_in_keys(d)
                            total_results[parent_path].append(d)
                            if d['type']=='folder':
                                job_queue.put(d['id'])
                                #print('added to job queue: ', d['node_path'])
            except Exception as e:
                print(f'Exception encountered: {e}; parent_path: {parent_path}')
                x = DM(env = self.env, project_number = self.project_number)
                total_results[parent_path].append({'id': None
                , 'file_id':None
                , 'Owner': None
                , 'project_number': self.project_number
                , 'projectnumber':self.project_number
                , 'node_path':None
                , 'Description': f'Error encountered! {e} parent_path: {parent_path}'
                , 'type': ''
                , 'name': None
                , 'parent_node_id': None
                , 'creation_date':None
                , 'project_id':None
                , 'project_number_path':None
                , 'uuu_content_status':None
                , 'pct_complete': None
                , 'location': None
                })
            finally:
                dm_queue.put(x)
                #print('Unfinished tasks: ', job_queue.unfinished_tasks)
                job_queue.task_done()
                print(f'finished evaluating: {parent_path} job_queue size: {job_queue.unfinished_tasks}')
                #print('Unfinished tasks after decrement: ', job_queue.unfinished_tasks)
        t1 = time.time()
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            while True:
                if job_queue.unfinished_tasks == 0:
                    #print('unfinished_tasks == 0 - exiting...')
                    break
                if job_queue.empty():
                    #print('job_queue is empty. unfinished_tasks: ', job_queue.unfinished_tasks)
                    continue
                parent_path = job_queue.get()
                ex.submit(job_func, parent_path)
        RESULTS = []
        for parent_path in total_results:
            for d in total_results[parent_path]:
                RESULTS.append(d)
        t2 = time.time()
        print(f'Finished in: {t2-t1}s')
        ts = timestamp_ymd()
        if tbl_name is None:
            tbl_name = throwaway_prefix+f'DM_WALKRECURSIVE_{self.env}_{ts}_{uuid4().hex}'
        write_dicts_to_db(input_dicts = RESULTS
            , tbl_name = tbl_name
            , tbl_fields = tbl_fields
            , db_con = __db_conn)
        print('Wrote to: ', tbl_name)
        while True:
            # close all DM objects in dm_queue
            if dm_queue.empty():
                break
            x = dm_queue.get()
            x.session_object.close()
        if db_conn is None:
            __db_conn.close()

class DocumentServices(FolderServices):
    '''Document Services methods (See "Document Services" under REST Web Services V1)'''
    def __init__(self, env, project_number, pwd=None, session=None, log_enable=True):
        super().__init__(env = env, project_number = project_number, pwd=pwd, session=session, log_enable = log_enable)
                
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.env}\', \'{self.project_number}\')\r\npwd: {self.pwd}'
    def _update_doc_metadata(self, Path, verbose = True, **kwargs):
        endpoint = f'/dm/document/update'
        body = urlencode({'projectnumber':self.project_number, 'data':[{'Path':Path, **kwargs}]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
                    
    def _update_doc_metadata_id(self, document_id, verbose = True, **kwargs):
        endpoint = f'/dm/document/update/{document_id}'
        body = urlencode({'projectnumber':self.project_number, 'data':[kwargs]})
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
                    
    def _search(self, Path, match='AND', query=None, nodetype=None, verbose = True):
        endpoint = f'/dm/search'
        if match not in ('AND','OR'):
            raise Exception ('match param must be one of \'AND\' or \'OR\'!')
        if self.project_number is not None:
            __body['project_number'] = self.project_number
        __body['match'] = match
        __body['parentpath'] = Path
        if query is not None:
            if not isinstance(query, list):
                raise Exception('query must be a list of search terms!')
            __body['query'] = [query]
        else:
            __body['query'] = []
        if nodetype is not None:
            if nodetype.lower() not in ('document','folder'):
                raise Exception("nodetype not in ('document', 'folder')!")
            __body['nodetype'] = nodetype
        body = urlencode(__body)
        return self.session_v1.post(endpoint = endpoint, params = __body, session = self.session_object, verbose = verbose)
                    
    def _rename_node(self, node_id, new_node_name, forceful = 'yes', verbose = True):
        if forceful not in ('yes','no'):
            raise Exception('forceful param must be \'yes\' or \'no\'!')
        __node_id = str(node_id) if not isinstance(node_id, str) else node_id
        endpoint = f'/dm/node/rename/{__node_id}'
        __body = {'projectnumber':self.project_number, 'data':[{'new_node_name':new_node_name, 'forceful':forceful}]}
        body = urlencode(__body)
        return self.session_v1.post(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
            
    def upload(self
            , file_path
            , Path
            , docTitle = None
            , Name=None
            , verbose = True
            , demo = False
            , dorevise = 'no'
            , timeout = None
            , **kwargs):
        assert isinstance(file_path, pathlib.Path) or isinstance(file_path, str), 'file_path must be a str or Path object!'
        assert dorevise in ('yes','no'), 'dorevise must be \'yes\' or \'no\'!'
        if self.env == 'prod' and demo == 'demo':
            raise Exception('demo mode is disabled when env == \'prod\'!')
        if timeout is not None:
            assert isinstance(timeout, float) or isinstance(timeout, int), 'timeout param must be a int or float!'
        endpoint = f'/dm/document/create'
        __file_path = pathlib.Path(file_path) if isinstance(file_path, str) else file_path
        __Name = __file_path.name if Name is None else Name
        __Path = Path
        __data_fields = {'Path':__Path, 'Name':__Name}
        if docTitle is not None:
            __data_fields['docTitle'] = docTitle
        __data_fields = {**__data_fields, **kwargs}
        if __file_path.is_dir():
            raise Exception('Input file is a directory! It needs to be a file.')    
        data_field = json.dumps([__data_fields])
        fields = {'projectnumber':self.project_number, 'dorevise': dorevise, 'data': data_field}
        if demo == 'demo':
            __m = MultipartEncoder(fields = fields) 
            r = self.session_v1.post(endpoint = endpoint, data = __m, headers = {'Content-Type':__m.content_type})
        else:
            if not __file_path.exists():
                return {'data':[], 'message':[{'message':f'{str(__file_path)} does not exist!'}], 'status':9999}
            if __file_path.stat().st_size == 0:
                return {'data':[], 'message':[{'message':f'{__file_path.name} has size 0 bytes!'}], 'status':9999}
            with open(__file_path, 'rb') as ff:
                fields['0'] = (__file_path.name, ff, 'application/octet-stream')
                __m = MultipartEncoder(fields = fields) 
                r = self.session_v1.post(endpoint = endpoint, data = __m, headers = {'Content-Type':__m.content_type}, timeout = timeout)
        return r
                
    def upload_id(self
            , file_path
            , parent_folder_id
            , Name=None
            , verbose = True
            , demo = False
            , dorevise = 'no'
            , timeout = None
            ,**kwargs):
        '''upload file to folder identified by parent_folder_id'''
        assert isinstance(file_path, pathlib.Path) or isinstance(file_path, str), 'file_path must be a str or Path object!'
        assert dorevise in ('yes','no'), 'dorevise must be \'yes\' or \'no\'!'
        assert isinstance(parent_folder_id, str) or isinstance(parent_folder_id, int), 'parent_folder_id must be a str or int!'
        assert 'Path' not in kwargs, 'Path cannot be a parameter when uploading using id!'
        if self.env == 'prod' and demo == 'demo':
            raise Exception('demo mode is disabled when env == \'prod\'!')
        if timeout is not None:
            assert isinstance(timeout, float) or isinstance(timeout, int), 'timeout param must be a int or float!'
        __parent_folder_id = str(parent_folder_id) if isinstance(parent_folder_id, int) else parent_folder_id
        endpoint = f'/dm/document/create/{__parent_folder_id}'
        __file_path = pathlib.Path(file_path) if isinstance(file_path, str) else file_path
        __Name = __file_path.name if Name is None else Name
        data_field = json.dumps([{'Name':__Name, **kwargs}])
        fields = {'projectnumber':self.project_number, 'dorevise':dorevise, 'data': data_field}
        if demo == 'demo':
            __m = MultipartEncoder(fields = fields) 
            r = self.session_v1.post(endpoint = endpoint, data = __m, headers = {'Content-Type':__m.content_type})
        else:
            if not __file_path.exists():
                return {'data':[], 'message':[{'message':f'{str(__file_path)} does not exist!'}], 'status':9999}
            if __file_path.stat().st_size == 0:
                return {'data':[], 'message':[{'message':f'{__file_path.name} has size 0 bytes!'}], 'status':9999}
            with open(__file_path, 'rb') as ff:
                fields['0'] = (__file_path.name, ff, 'application/octet-stream')
                __m = MultipartEncoder(fields = fields) 
                r = self.session_v1.post(endpoint = endpoint, data = __m, headers = {'Content-Type':__m.content_type}, timeout = timeout)
        return r
            
    def upload_tree(self
            , top
            , unifier_top
            , pool_size = 4
            , return_results = False
            , prompt = False
            , overwrite=False
            , db_conn = None
            , demo = False
            , omit_subset = None
            , folders_only = False
            , glob = '*'
            , timeout = None):
        #__unifier_top = self.pwd if unifier_top is None else unifier_top
        #__top = pathlib.Path().cwd() if (top is None) or (top=='.') or top==pathlib.Path('.') else top 
        assert unifier_top.startswith('/'), "unifier_top must start with '/' (ex: '/04 Plans' or '/' for the root)"
        assert isinstance(pool_size, int), 'pool_size must be a int!'
        if self.env == 'prod' and demo == 'demo':
            raise Exception('demo mode is disabled when env == \'prod\'!')
        assert folders_only in (True, False), 'folders_only param must be True or False!'
        __unifier_top = unifier_top
        __top = top
        __db_conn = sqlite3_dict_connect() if db_conn is None else db_conn  
        print('Upload Directory tree')
        print(f'Local top directory: {str(__top)}')
        print(f'Unifier env: {str(self.env)}')
        print(f'Unifier shell: {str(self.project_number)}')
        print(f'Unifier top directory: {__unifier_top}')
        print('pool_size: ', pool_size)
        print('folders_only: ', str(folders_only))
        print('glob: ', glob)
        print('timeout: ', str(timeout))
        if prompt is True:
            prompt_random_string()
        walk_compare_results = self.walk_compare(top = __top
                , unifier_top = __unifier_top
                , return_results = True
                , db_conn = __db_conn
                , omit_subset = omit_subset
                , folders_only = folders_only
                , glob = glob
                )
        if overwrite is False:
            job_list = sorted((d for d in walk_compare_results if d['in_unifier'] is False), key = lambda x: x['unifier_node_path'])
        else:
            job_list = sorted((d for d in walk_compare_results), key = lambda x: x['unifier_node_path'])
            
        folder_uploads = (d for d in job_list if d['type']=='Folder')
        document_uploads = (d for d in job_list if d['type'] == 'Document')
                
        print('upload_tree: Creating folders...')
        t1 = time.time()
        progress_output_template = "Type: {node_type}\tUnifier path: {unifier_path}\tResponse msg: {response_msg}"  
        dm_queue = Queue()
        folder_jobs_queue = PriorityQueue()
        for _ in range(pool_size + 2):
            __dm_inst = self.__class__(env = self.env, project_number = self.project_number, session = requests.Session()) 
            dm_queue.put(__dm_inst)
        for d in folder_uploads:
            # the shortest paths have highest priority due to being dependencies (the lowest level folders need to be created first)
            priority = len(d['local_node_path_object'].parent.parts)
            # priority2 is a random string to serve as a tiebreaker for folders at the same level
            priority2 = str(uuid.uuid4())
            folder_jobs_queue.put((priority, priority2, d))
        def folder_create_job_func(input_tuple):
            try:
                priority, priority2, d = input_tuple
                __response_msg = ''
                __dm_inst = dm_queue.get(timeout = 3)
                print('Evaluating: ', d['unifier_node_path'])
                r = __dm_inst._mkdir(Name = d['name'], Path = d['unifier_parent_path'], verbose = False)
                d['response_message'], d['response_status'] = str(r['message']), r['status']
                d['node_id'] = r['data'][0].get('node_id', None) if len(r['data']) > 0 else None
                __response_msg = r['message'][0].get('message','')
            except Exception as e:
                __dm_inst = self.__class__(env = self.env, project_number = self.project_number, session = requests.Session()) 
                d['response_message'], d['response_status'] = f'Exception encountered! {e}', 9999
            finally:
                d['project_number'] = str(self.project_number)
                print(progress_output_template.format(node_type=d['type']
                                            , unifier_path=d['unifier_node_path']
                                            , local_path=d['local_node_path']
                                            , response_msg=d['response_message']))
                # If for some reason the folder still does not exist after sending the _mkdir command, put the job back into the queue
                # Response 200 on a _mkdir command indicates successful folder creation
                if d['response_status'] != 200:
                    if __response_msg == 'Parent path or node id is invalid or does not exists.':
                        folder_jobs_queue.put((priority, priority2, d))
                    elif __response_msg == 'Folder with given name already exists':
                        'do nothing'
                    else:
                        try:
                            __folder_exists_check = False
                            __folder_exists_check = __dm_inst.check_path_exists(Path = d['unifier_node_path'])
                        except Exception as e:
                            __folder_exists_check = False
                        finally:
                            if __folder_exists_check is False:
                                folder_jobs_queue.put((priority, priority2, d)) 
                dm_queue.put(__dm_inst)
                folder_jobs_queue.task_done()
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            while True:
                if not folder_jobs_queue.empty():
                    input_tuple = folder_jobs_queue.get()
                    ex.submit(folder_create_job_func, input_tuple)
                if folder_jobs_queue.unfinished_tasks == 0:
                    break
        if folders_only is False:
            def job_func(d):
                try:
                    __dm_inst = dm_queue.get()
                    __dorevise = 'yes' if overwrite is True else 'no'
                    r = __dm_inst.upload(file_path = d['local_node_path_object']
                        , Path = d['unifier_parent_path']
                        , verbose = False
                        , demo = demo
                        , dorevise = __dorevise
                        , timeout = timeout
                        )
                    d['response_message'], d['response_status'] = str(r['message']), r['status']
                    if len(r['data']) > 0:
                        d['node_id'] = r['data'][0].get('node_id', None)
                        d['parentId'] = r['data'][0].get('parentId', None)
                        d['from_object_id'] = r['data'][0].get('from_object_id', None)
                    else:
                        d['node_id'], d['parentId'], d['from_object_id'] = None, None, None
                except Exception as e:
                    __dm_inst = self.__class__(env = self.env, project_number = self.project_number, session = requests.Session()) 
                    d['response_message'], d['response_status'] = f'Exception encountered! {e}', 9999
                finally:
                    d['project_number'] = str(self.project_number)
                    dm_queue.put(__dm_inst)
                    print(progress_output_template.format(node_type=d['type']
                                                    , unifier_path=d['unifier_node_path']
                                                    , local_path=d['local_node_path']
                                                    , response_msg=d['response_message']))
            with ThreadPoolExecutor(max_workers = pool_size) as ex:
                ex.map(job_func, document_uploads)
        t2 = time.time()
        print(f'upload_tree: Completed in {str(t2-t1)}s')
        response_counts = dict(Counter(str(d.get('response_status',''))+'\t'+str(d.get('response_message','')) for d in job_list))
        print('Counts of response messages:')
        pprint(response_counts)
        ts = timestamp_ymd()
        tag = uuid4().hex
        log_name = f'dm_upload_tree_{self.env}_'+ts+tag
        log_tbl_name = throwaway_prefix+log_name
        tbl_fields = 'project_number;unifier_node_path;local_node_path;type;name;unifier_parent_path;response_message;response_status;node_id;parentId;file_id;from_object_id'
        pkl_path = log_pkl(input_object = job_list, name = log_name, timestamp = False, random_tag = False)
        # tbl_fields param is required in this case due to non-text fields in the response dictionaries
        csv_path = write_dicts_to_csv(input_dicts = job_list, name = log_name, tbl_fields = tbl_fields)
        write_dicts_to_db(input_dicts = job_list, tbl_name = log_tbl_name, db_con = __db_conn, tbl_fields = tbl_fields)
        print(f'{__name__}:: Wrote upload_tree results to (pkl): ', str(pkl_path))
        print(f'{__name__}:: Wrote upload_tree results to (csv): ', str(csv_path))
        print(f'{__name__}:: Wrote upload_tree results to (tbl): ', log_tbl_name)
        while True:
            if not dm_queue.empty():
                __dm_inst = dm_queue.get()
                __dm_inst.session_object.close()
                del __dm_inst
            else:
                break
        if db_conn is None:
            __db_conn.close()
        if return_results is True:
            return job_list
        return None

def log_results(list_of_results, log_name, tbl_fields = None, db_conn = None, **kwargs):
    pkl_path = log_pkl(input_object = list_of_results, name = log_name, timestamp = False, random_tag = False)
    csv_path = write_dicts_to_csv(input_dicts = list_of_results, name = log_name, tbl_fields = tbl_fields)
    print('Wrote to: '+str(pkl_path))
    print('Wrote to: '+str(csv_path))


class DM(DocumentServices):
    def __init__(self, env, project_number, pwd=None, session=None, log_enable=True):
        super().__init__(env = env, project_number = project_number, pwd = pwd, session = session, log_enable = log_enable)
            
    def get_path_info(self, Path):
        __project_number_path = self.project_number+'_'+Path
        return get_node_info_by_path(env = self.env, project_number_path = __project_number_path, session = self.session_object)
            
    def check_path_exists(self, Path):
        __project_number_path = self.project_number+'_'+Path
        return check_path_exists(env = self.env, project_number_path = __project_number_path, session = self.session_object)
    
    def s_upload(self, sql_query, pool_size = 4, db_conn = None, return_results = False):
        '''
        Input sql is expecting the following columns:
            Path        - unifier path of where to upload the file to 
            file_path   - local file path of file to upload
            Name        - file name
            Optional columns:
            dorevise    - 'yes' to overwrite existing, default is 'no'
            **additional columns are metadata
        '''
        ts = timestamp_ymd()
        tag = uuid4().hex
        log_name = f'dm_s_upload_{self.env}_'+ts+'_'+tag
        con = sqlite3_dict_connect() if db_conn is None else db_conn
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        session_queue = create_session_queue(size = pool_size)
        def _single_iteration(row):
            try:
                __file_path = row.pop('file_path',None)
                __project_number = ''
                __project_number = _s_check_project_numbers(dm_object = self, row = row)
                row.pop('project_number',None)
                __Path = row.pop('Path',None)
                if pathlib.Path(__file_path).is_dir():
                    raise Exception('Input path is a directory!')
                __session = session_queue.get()
                if __file_path is None:
                    raise Exception('file_path is missing!')
                if __Path is None:
                    raise Exception('Path is missing!')
                __inst = DM(env = self.env, project_number = __project_number, session = __session)
                r = __inst.upload(file_path = __file_path, Path = __Path, **row)
                __rd = r.get('data', [])[0]
                __rm = r.get('message', [])[0]
                return_dict = {**{'file_path':__file_path
                    , 'project_number':__project_number
                    , 'r_message': str(__rm)
                    , 'status':r['status']}
                    , **__rd}
                del __inst
            except Exception as e:
                __session = requests.Session()
                return_dict = {'file_path':str(__file_path)
                    , 'project_number':__project_number
                    , 'r_message': 'Exception encountered! '+str(e)
                    , 'status':9999}
            finally:
                session_queue.put(__session)
                print(str(return_dict['status'])+'\t'+str(return_dict['file_path']))
                return return_dict
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            __results = ex.map(_single_iteration, rows)
        __list_results = list(__results)
        log_results(list_of_results = __list_results, log_name = log_name, db_conn = con)
        close_session_queue(session_queue)
        if db_conn is None:
            con.close()
        if return_results is True:
            return __list_results
                
    def s_mkdir(self, sql_query, db_conn = None, return_results = False, pool_size = 1):
        '''
        Input sql query expects the following columns:
            project_number
            Path    - unifier parent path of the folder to create
            Name    - name of the folder to create
        '''
        ts = timestamp_ymd()
        log_name = f'dm_s_mkdir{self.env}_'+ts+gen_random_string(8)
        con = sqlite3_dict_connect() if db_conn is None else db_conn
        cur = con.cursor()
        def get_dict_path(d):
            return d.get('Path', None)
        rows = cur.execute(sql_query).fetchall()
        rows = sorted(rows, key = get_dict_path)
        session_queue = create_session_queue(size = pool_size+1)
        def _single_iteration(row):
            #print('abc')
            try:
                __Path = row.pop('Path', None)
                __Name = row.pop('Name', None)
                __project_number = ''
                __project_number = _s_check_project_numbers(dm_object = self, row = row)
                row.pop('project_number', None)
                __session = session_queue.get()
                if __Path is None:
                    raise Exception('Path is missing!')
                if __Name is None:
                    raise Exception('Name is missing!')
                __inst = DM(env = self.env, project_number = __project_number, session = __session)
                r = __inst._mkdir(Name = __Name, Path = __Path, **row)
                __rd = r.get('data', [])[0]
                __rm = r.get('message', [])[0]
                return_dict = {**{'Name':__Name
                    , 'Path':__Path
                    , 'project_number':__project_number
                    , 'r_message': str(__rm)
                    , 'status':r['status']}
                    , **__rd}
                del __inst
            except Exception as e:
                __session = requests.Session()
                return_dict = {'Name':__Name
                    , 'Path':__Path
                    , 'project_number':__project_number
                    , 'r_message': 'Exception encountered! '+str(e)
                    , 'status':9999}
            finally:
                session_queue.put(__session)
                print(str(return_dict['status'])+'\t'+str(return_dict['Path'])+'\t'+str(return_dict['Name']))
                return return_dict
        __list_results = []
        if pool_size > 1:
            with ThreadPoolExecutor(max_workers = pool_size) as ex:
                results = ex.map(_single_iteration, rows)
            __list_results = list(results)
        else:
            for row in rows:
                __r = _single_iteration(row = row)
                __list_results.append(__r)
        log_results(list_of_results = __list_results, log_name = log_name, db_conn = con)
        close_session_queue(session_queue)
        if db_conn is None:
            con.close()
        if return_results is True:
            return __list_results
            
    def s_update_by_id(self, sql_query, pool_size = 4, db_conn = None, return_results = False):
        '''Update metadata using id column'''
        ts = timestamp_ymd()
        log_name = f'dm_s_update_{self.env}_'+ts+gen_random_string(8)
        con = sqlite3_dict_connect() if db_conn is None else db_conn
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        session_queue = create_session_queue(size = pool_size)
        def _single_iteration(row):
            try:
                __project_number = ''
                __project_number = _s_check_project_numbers(dm_object = self, row = row)
                row.pop('project_number', None)
                __node_id = row.pop('id', None)
                __session = session_queue.get()
                if __node_id is None:
                    raise Exception('id is missing!')
                __inst = DM(env = self.env, project_number = __project_number, session = __session)
                r = __inst.update_node_metadata_id(node_id = __node_id, val = row)
                __rd = r.get('data', [])[0]
                __rm = r.get('message', [])[0]
                if __rm['message']=='OK':
                    r['status'] = 200
                return_dict = {**{'id':str(__node_id)
                    , 'project_number':__project_number
                    , 'r_message': str(__rm)
                    , 'status':r['status']}
                    , **__rd}
                del __inst
            except Exception as e:
                __session = requests.Session()
                return_dict = {'id': str(__node_id)
                    , 'project_number':__project_number
                    , 'r_message': 'Exception encountered! '+str(e)
                    , 'status':9999}
            finally:
                session_queue.put(__session)
                return return_dict
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            __results = ex.map(_single_iteration, rows)
        _list_results = list(__results)
        log_results(list_of_results = _list_results, log_name = log_name, db_conn = con)
        close_session_queue(session_queue)
        if db_conn is None:
            con.close()
        if return_results is True:
            return _list_results
        
    def s_update_by_path(self, sql_query, pool_size = 4, db_conn = None, return_results = False):
        '''Update metadata using id column'''
        ts = timestamp_ymd()
        log_name = f'dm_s_update_{self.env}_'+ts+gen_random_string(8)
        con = sqlite3_dict_connect() if db_conn is None else db_conn
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        session_queue = create_session_queue(size = pool_size)
        def _single_iteration(row):
            try:
                __project_number = ''
                __project_number = _s_check_project_numbers(dm_object = self, row = row)
                row.pop('project_number', None)
                __project_number_path = row.pop('project_number_path', None)
                if __project_number_path is None:
                    raise Exception('project_number_path is missing!')
                __session = session_queue.get()
                __inst = DM(env = self.env, project_number = __project_number, session = __session)
                r = __inst.update_node_metadata_path(project_number_path = __project_number_path, val = row)
                __rd = r.get('data', [])[0]
                __rm = r.get('message', [])[0]
                if __rm['message']=='OK':
                    r['status'] = 200
                return_dict = {**{'project_number_path':str(__project_number_path)
                    , 'project_number':__project_number
                    , 'r_message': str(__rm)
                    , 'status':r['status']}
                    , **__rd}
                del __inst
            except Exception as e:
                __session = requests.Session()
                return_dict = {'project_number_path':str(__project_number_path)
                    , 'project_number':__project_number
                    , 'r_message': 'Exception encountered! '+str(e)
                    , 'status':9999}
            finally:
                session_queue.put(__session)
                return return_dict
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            __results = ex.map(_single_iteration, rows)
        _list_results = list(__results)
        log_results(list_of_results = _list_results, log_name = log_name, db_conn = con)
        close_session_queue(session_queue)
        if db_conn is None:
            con.close()
        if return_results is True:
            return _list_results
            
    def __getitem__(self, key):
        d = get_node_info(env = self.env, node_id = key, session = self.session_object)
        if d == {}:
            return {}
        parent_node_id = d['parent_node_id']
        r1 = self._get_dir_metadata_id(parent_node_id, verbose = False)
        r1d = r1['data']
        for d in r1['data']:
            if d['node_id'] == key:
                pprint(d)
                return d
        return {}
            
    def update_node_metadata_id(self, node_id, val):
        assert isinstance(val, dict), 'val must be a dict!'
        d = get_node_info(env = self.env, node_id = node_id, session = self.session_object)
        if d == {}:
            raise Exception('node_id not found!')
        elif d['type'].lower() == 'document':
            return self._update_doc_metadata_id(document_id = node_id, verbose = True, **val)
        else:
            return self._update_dir_metadata_id(node_id = node_id, verbose = True, **val)
                
    def update_node_metadata_path(self, project_number_path, val):
        assert isinstance(val, dict), 'val must be a dict!'
        d = get_node_info_by_path(env = self.env, project_number_path = project_number_path,  session = self.session_object)
        if d == {}:
            raise Exception('project_number_path not found!')
        elif d['type'].lower() == 'document':
            node_id = d['id']
            return self._update_doc_metadata_id(document_id = node_id, verbose = True, **val)
        else:
            node_id = d['id']
            return self._update_dir_metadata_id(node_id = node_id, verbose = True, **val)
                
    def __setitem__(self, key, val):
        self.update_node_metadata_id(node_id = key, val = val)
            
    def __get_doc(self
            , endpoint
            , dest_filename
            , dest_folder = download_default_path
            , params = None
            , verbose = True
            , stream = True
            , write_content = True
            , session = None):
        assert isinstance(dest_folder, str) or isinstance(dest_folder, pathlib.Path), 'dest_folder must be a str or Path object!'
        assert isinstance(dest_filename, str), 'dest_filename must be a str!'
        __session = self.session_object if session is None else session
        __dest_folder = dest_folder if isinstance(dest_folder, pathlib.Path) else pathlib.Path(dest_folder)
        if not __dest_folder.exists():
            __dest_folder.mkdir(parents=True)
        # stream = True is required when using shutil.copyfileobj
        r = self.session_v1.get(endpoint = endpoint, params = params, session = __session, verbose = verbose, response_json = False, stream = True)
        r.raise_for_status()
        if write_content is False:
            # write_content = False for debugging purposes
            # it returns the raw response object for analysis, instead of writing it to file
            return r
        if r.headers.get('Content-Type','')=='text/plain':
            r_json = r.json()
            if ('status' in r_json) and ('message' in r_json):
                print(str(r_json['status'])+' '+str(r_json['message']))
            return r_json
        else:
            filename = dest_filename
            dest_path = pathlib.Path(__dest_folder)/filename
            if write_content is True:
                if r.status_code==200:
                    with open(dest_path, 'wb') as ff:
                        # stream = True is required when using shutil.copyfileobj
                        shutil.copyfileobj(r.raw, ff) 
                    __msg_str = str(dest_path)
                    if verbose is True:
                        print('200 '+__msg_str)
                    return {'data':[], 'message':[__msg_str], 'status':200}
        __msg_str = r.status_code
        if verbose is True:
            print('9999 '+__msg_str)
        return {'data':[r], 'message': [__msg_str], 'status':9999}
            
    def get_doc_by_file_id(self
            , file_id
            , dest_filename
            , dest_folder = download_default_path
            , verbose = True
            , stream = True
            , write_content = True
            , session = None):
        endpoint = f'/dm/file/download/{file_id}'
        return self.__get_doc(endpoint = endpoint
                        , dest_folder = dest_folder
                        , dest_filename = dest_filename
                        , verbose = verbose
                        , stream = stream
                        , write_content = write_content
                        , session = session)
            
    def get_doc_by_path(self
            , parentpath
            , dest_filename
            , dest_folder = download_default_path
            , verbose = True
            , stream = True
            , write_content = True
            , session = None):
        projectnumber = '' if self.project_number is None else self.project_number
        body = urlencode({'projectnumber':projectnumber, 'parentpath':parentpath, 'iszip':'yes'})
        endpoint = '/dm/document'
        return self.__get_doc(endpoint = endpoint
                        , dest_folder = dest_folder
                        , dest_filename = dest_filename
                        , params = body
                        , session = session
                        , stream = stream
                        , write_content = write_content
                        , verbose = verbose)
            
    def get_doc_by_parent_folder_id(self
            , parent_folder_id
            , dest_filename
            , dest_folder = download_default_path
            , verbose = True
            , stream = True
            , write_content = True
            , session = None):
        body = urlencode({'iszip':'yes'})
        endpoint = f'/dm/document/{parent_folder_id}'
        return self.__get_doc(endpoint = endpoint
                        , dest_folder = dest_folder
                        , dest_filename = dest_filename
                        , params = body
                        , session = session
                        , stream = stream
                        , write_content = write_content
                        , verbose = verbose)
            
    def get_doc_by_file_id_tiff(self
            , file_id
            , dest_filename
            , dest_folder = download_default_path
            , verbose = True
            , stream = True
            , write_content = True
            , session = None):
        endpoint = f'/dm/file/view/{file_id}'
        return self.__get_doc(endpoint = endpoint
                        , dest_folder = dest_folder
                        , dest_filename = dest_filename
                        , session = session
                        , stream = stream
                        , write_content = write_content
                        , verbose = verbose)

class DMAuth:
    def __init__(self, env, project_number, session = None, log_enable = True):
        assert env in ('stage','prod'), 'env must be in "stage" or "prod"!'
        assert log_enable in (True, False), 'log_enable must be True or False!'
        self.project_number = project_number
        self.env = env
        self.session_v1 = urestv1(env = env, log_enable = log_enable)
        self.session_v2 = urestv2(env = env, log_enable = log_enable)
        self.session_queue = None
        self.session_object = session if session else requests.Session()
    def get_path_permissions(self, node_path, verbose = True):
        endpoint = f"/dm/permission/{self.project_number}/node/{node_path}"
        return self.session_v1.get(endpoint = endpoint, verbose = verbose)
            
    def get_path_user_permissions(self, node_path, username, verbose = True):
        usertype = 'U'
        endpoint = f"/dm/permission/{self.project_number}/node/{node_path}/user/{username}?usertype={usertype}"
        return self.session_v1.get(endpoint = endpoint, session = self.session_object, verbose = verbose)
    def get_path_group_permissions(self, node_path, group_name, verbose = True):
        usertype = 'PG'
        endpoint = f"/dm/permission/{self.project_number}/node/{node_path}/user/{group_name}?usertype={usertype}"
        return self.session_v1.get(endpoint = endpoint, session = self.session_object, verbose = verbose)
        
    def add_path_permissions(self, node_path, body, verbose = True):
        endpoint = f"/dm/permission/{self.project_number}/node/{node_path}"
        body = json.dumps(body)
        return self.session_v1.post(endpoint = endpoint, data = body, headers={'Content-Type':'application/json'}, session = self.session_object, verbose = verbose)
        
    def remove_all_path_permissions(self, node_path, verbose = True):
        endpoint = f"/dm/permission/{self.project_number}/node/{node_path}/remove"
        return self.session_v1.put(endpoint = endpoint, session = self.session_object, verbose = verbose)
            
    def gen_ro_group_dict(self, groupname):
        return gen_ro_group_dict(groupname = groupname)
             
    def gen_ro_user_dict(self, username, full_name):
        return gen_ro_user_dict(username = username, full_name = full_name)
    def __repr__(self):
        return self.__class__.__name__+f"('{self.env}','{self.project_number}')"
            
    def __getitem__(self, node_path):
        r = self.get_path_permissions(node_path = node_path)
        pprint(r)
        return r
    def __setitem__(self, key, value):
        self.update_path_permissions(node_path = key, body = value)
            

def gen_ro_group_dict(groupname):
    print('generating read only template for group: ', groupname)
    __d = {
'Inheritance': False
, 'ApplyToAllSubFolders': True
, 'UserPermission': [{'Type': 'PG'
, 'GroupName': groupname
, 'FullName': groupname
, 'DocumentPermission': {
'View': 1
, 'Move': 0
, 'Copy': 1
, 'Delete': 0
, 'Download': 1
, 'ModifyProperties': 0
, 'ModifyPermissions': 0
, 'AddComments': 0
, 'Revise': 0}
, 'FolderPermission': {'View': 1
, 'Move':0
, 'Copy': 1
, 'Delete': 0
, 'ModifyProperties': 0
, 'ModifyPermissions': 0
, 'CreateSubFolders': 0
, 'AddDocuments': 0}}]}
    pprint(__d)
    return __d

def gen_ro_user_dict(username, full_name ):
    print('generating read only template for user: ', username)
    __d = {
'Inheritance': False
, 'ApplyToAllSubFolders': True
, 'UserPermission': [{'Type': 'U'
, 'LoginName': username
, 'FullName': full_name
, 'DocumentPermission': {
'View': 1
, 'Move': 0
, 'Copy': 1
, 'Delete': 0
, 'Download': 1
, 'ModifyProperties': 0
, 'ModifyPermissions': 0
, 'AddComments': 0
, 'Revise': 0}
, 'FolderPermission': {'View': 1
, 'Move':0
, 'Copy': 1
, 'Delete': 0
, 'ModifyProperties': 0
, 'ModifyPermissions': 0
, 'CreateSubFolders': 0
, 'AddDocuments': 0}}]}
    pprint(__d)
    return __d
