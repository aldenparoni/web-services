from unifier_requests.ur import urestv1
from unifier_requests.ur import gen_random_string
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur import throwaway_prefix
from unifier_requests.ur import write_dicts_to_db
from unifier_requests.ur import write_dicts_to_csv
from unifier_requests.ur import timestamp_ymd
from unifier_requests.ur import log_dir_path
from unifier_requests.ur import get_store_if_exists_default
from pathlib import Path
from collections import OrderedDict
import pandas as pd
import requests

def decode_binary(x):
    return x.decode('ascii', 'ignore')

type_map = {
'java.lang.Boolean': str
, 'java.lang.Byte': str
, 'java.lang.Character': str
, 'java.lang.Double': float
, 'java.lang.Integer': int
, 'java.lang.Long': float
, 'java.lang.String': str
, 'java.sql.Timestamp':str
}

def type_translate(java_type, input_element):
    f = type_map.get(java_type, str)
    if java_type not in type_map:
        print('Unseen type encountered:\t'+java_type+'\tConverted to string.')
    if (f is int) or (f is float):
        input_element = input_element.replace(',','')
    if (f is int) and (input_element.endswith('.00')):
        input_element = input_element.replace('.00','')
    return f(input_element)

def tuple_first_elem(input_tuple):
    ''' 
    Return the column number. This method is used for sorting.
    The report rows follow the format:
        'report_row': [{'c1': 'Action Items', 'c2': 'uai'},
                      {'c1': 'Activity Calendar', 'c2': 'uxac'},
                      {'c1': 'All Projects', 'c2': 'us_xap'},
                      {'c1': 'All Properties', 'c2': 'us_apr'}]
    The key is in the column number
    '''
    return int(input_tuple[0].replace('c',''))

def cast_numbers_to_str(input_dict):
    '''
    Cast input_dict items that are numbers to strings.
    Input dicts used in the query param must have string items. Otherwise, the query will be unrecognized.
    Note that this mutates the input_dict
    '''
    if isinstance(input_dict, dict):
        for key, val in input_dict.items():
            if isinstance(val, int) or isinstance(val, float) or isinstance(val, bool):
                input_dict[key] = str(val)


class udr:
    def __init__(self, env, project_number, reportname=None,query=None,session=None, **kwargs):
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.env = env
        self.project_number = project_number
        self.restv1 = urestv1(env=env, log_enable=True)
        self.session_object = session if session is not None else requests.Session()
                
    def get(self, reportname, *, query=None, verbose = True):
        '''
        _query: expecting a list of dicts
        [{'label':'Requests for Bid / Title','value1':'Standard'},
        {'label':'Requests for Bid / Due Date','value1':'34','value2':'43'}]
        '''
        endpoint = f'/data/udr/get/{self.project_number}' if self.project_number else f'/data/udr/get/'
        _reportname = reportname
        _query = query.copy() if query is not None else None
        if isinstance(_query, list):
            for d in _query:
                cast_numbers_to_str(input_dict = d)
        if isinstance(_query, dict):
            cast_numbers_to_str(input_dict = _query)
            _query = [_query]
        if _query is not None and (not isinstance(_query, list)):
            raise Exception('query needs to be a list of dicts!')
        post_body = {'reportname':_reportname,'query':_query}
        return self.restv1.post(endpoint = endpoint, data=post_body, session=self.session_object, verbose = verbose)
    
    def get_dicts(self, reportname = None, query = None, verbose = True):
        '''
        Returns a list of dicts.
        Example headers dict
        {'c1':{ 'name': 'REPORT_COL_NAME'
            , 'type':'java.lang.String'}
        , 'c2':{'name':'REPORT_COL_NAME2'
            , 'type':'java.lang.Integer}}
        '''
        r = self.get(reportname = reportname, query = query, verbose = verbose)
        if r['status']==709:
            raise Exception(f"{str(r['message'])}")
        headers_dict = r['data'][0]['report_header']
        report_rows = r['data'][0]['report_row']
        return [{headers_dict[key]['name']: type_translate(java_type=headers_dict[key]['type'], input_element = val) 
            for key,val in sorted(d.items(), key = tuple_first_elem)} for d in report_rows]
            
    def get_df(self, reportname = None, query = None, verbose = True):
        r = self.get_dicts(reportname = reportname, query = query, verbose = verbose)
        return pd.DataFrame(r)
            
    def get_store(self, reportname, *, table_name = None, query = None, db_conn=None, if_exists = get_store_if_exists_default, verbose = True):
        _db_conn = sqlite3_dict_connect() if db_conn is None else db_conn
        ts = timestamp_ymd()
        _table_name =throwaway_prefix+ts+'_udr_'+self.env+'_'+gen_random_string(8).lower() if table_name is None else table_name
        results_list = self.get_dicts(reportname = reportname, query = query, verbose = verbose)
        write_dicts_to_db(input_dicts = results_list, tbl_name = _table_name, db_con = _db_conn, if_exists = if_exists)
        print('Wrote to table: ', _table_name)
        if db_conn is None:
            _db_conn.close()
        return _table_name
        
    def get_store_csv(self, reportname, *, csv_name = None, query = None, filedir = log_dir_path, verbose = True):
        assert isinstance(filedir, str) or isinstance(filedir, Path), 'filedir must be a string or a Path object!'
        __filedir = Path(filedir) if isinstance(filedir, str) else filedir
        ts = timestamp_ymd()
        _csv_name = 'udr_'+self.env+'_'+reportname+'_'+ts+gen_random_string(7).lower() if csv_name is None else csv_name
        results_list = self.get_dicts(reportname = reportname, query = query, verbose = verbose)
        __filepath = write_dicts_to_csv(input_dicts = results_list, name = _csv_name, filedir = __filedir)
        print('Wrote results to: ', __filepath)
        return __filepath
        
    def __getitem__(self, key):
        #return udr(self.env, self.project_number, reportname=key)
        return self.get_dicts(reportname=key)
        
    def __repr__(self):
        return f'udr(\'{self.env}\',\'{self.project_number}\')'
# udr('stage','jctest21', udr_name, query)
