import logging
import requests
from copy import copy
import io
import os
import csv
from datetime import datetime
import json
from json.decoder import JSONDecodeError
import random
import string
import time
import pickle
import pandas as pd
import zipfile
from copy import copy
from urllib.parse import urlencode
import base64
import uuid
from uuid import uuid4
from pathlib import Path
from pprint import pprint
from pprint import pformat
import shutil
import urllib3
import http
import http.client
from datetime import datetime
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from functools import partial
from collections import OrderedDict
from collections import Counter
import sys
import configparser
# from unifier_requests import credentials

file_extensions = ['csv', 'doc', 'docx', 'dwg', 'jpg', 'msg', 'pdf', 'png', 'ppt', 'rtf', 'txt', 'xer', 'xls', 'xlsx', 'zip']

unifier_requests_path = Path(__file__).parent.absolute()
throwaway_prefix = 'AA00TEMP_'
hm_db_path = Path().home()/'unifier_requests_db.db'
log_dir_path = Path().home()/'ureqlogs'
temp_dir_path = Path().home()/'unifier-requests-TEMP'
download_default_path = Path().home()/'ureq_downloads'
cert_path = unifier_requests_path / 'certificate.pem'
ur_config_path = Path().home() / 'UR_USER_PREFERENCES.txt'
s_default_pkcols = 'project_number;record_no;master_key;parent_key;cms_master_key;r_record_no;rowid;id;row_id' 

restv1_stage_url = 'https://unifier.oraclecloud.com/hart/stage/ws/rest/service/v1' 
restv2_stage_url = 'https://unifier.oraclecloud.com/hart/stage/ws/rest/service/v2' 
restv1_prod_url = 'https://unifier.oraclecloud.com/hart/ws/rest/service/v1'
restv2_prod_url =  'https://unifier.oraclecloud.com/hart/ws/rest/service/v2'

# load preferences
ur_config_default_values_dict = {}
if ur_config_path.exists():
    ur_config_parser = configparser.ConfigParser()
    ur_config_parser.read(ur_config_path)
    if 'ur_default_values' in ur_config_parser:
        ur_config_default_values_dict = dict(ur_config_parser['ur_default_values'])

get_store_if_exists_default = ur_config_default_values_dict.get('get_store_if_exists_default','fail')

if not cert_path.exists():
    cert_path = None
    requests.packages.urllib3.disable_warnings()

if not download_default_path.exists():
    download_default_path.mkdir()

if not temp_dir_path.exists():
    temp_dir_path.mkdir()

if not log_dir_path.exists():
    log_dir_path.mkdir()

if not hm_db_path.exists():
    con = sqlite3.connect(hm_db_path)
    con.close()


def gen_proxy_dict(cch_username=None, cch_password=None):
    # txt file (ansi encoded) with first row as: username,password
    cch_auth_csv = Path().home()/'cch_credentials.txt'
    if not os.path.exists(cch_auth_csv):
        return None
    with open(cch_auth_csv, 'r') as f:
        cch_auth_pair = list(csv.reader(f))[0]
        cch_username = cch_auth_pair[0]
        cch_password = cch_auth_pair[1]
    return {'http':f'http://{cch_username}:{cch_password}@cchproxy:8080', 'https':f'https://{cch_username}:{cch_password}@cchproxy:8080'}

proxies = gen_proxy_dict()

# read txt file (ansi encoded) containing Unifier WS auth token
rest_stage_token_txt_path = Path().home()/'token_stage.txt'
rest_prod_token_txt_path = Path().home()/'token_prod.txt'

if rest_stage_token_txt_path.exists():
    with open(rest_stage_token_txt_path) as f:
        rest_stage_token = f.read().strip()
else:
    rest_stage_token = ''

if rest_prod_token_txt_path.exists():
    with open(rest_prod_token_txt_path) as f:
        rest_prod_token = f.read().strip()
else:
    rest_prod_token = ''

class urestv1:
    def __init__(self, env, token=None, log_directory=None, log_enable=True):
        self.proxies = proxies
        self.url = restv1_stage_url if env == 'stage' else restv1_prod_url
        self.delay_time = 0
        self.logs_enabled = log_enable
        self.env = env
        user_home_folder = os.path.expanduser('~')
        
        if env not in ('stage', 'prod'):
            raise Exception('Env must be in \'stage\' or \'prod\'!')
            
        if not token:
            if env == 'stage':
                self.token = rest_stage_token
            elif env=='prod':
                self.token = rest_prod_token
        else:
            self.token = token
        self.auth_token_dict = {'Authorization':f'Bearer {self.token}'} 
        
        if self.logs_enabled:
            if not log_directory:
                log_directory = os.path.join(user_home_folder, 'ureqlogs')
                if not os.path.exists(log_directory):
                    os.mkdir(log_directory)
            
            logfile_name = datetime.now().strftime('%Y%m%d%H%M%S%p').lower()
            logfile_path = os.path.join(log_directory, logfile_name+'.log')
            logging.basicConfig(format=f'%(levelname)s %(asctime)s {self.env}: %(message)s', datefmt='%m/%d/%Y %H:%M:%S %p', handlers=[logging.FileHandler(logfile_path,'w+','utf-8')], level=logging.DEBUG)
            logging.info(f'Logging initialized from {self.__class__.__name__}, environment:{env}')
    
    def _transaction_function(self, endpoint, op, data=None, params=None, session=None, verbose=True,encode_data=True, log_response = True, response_json = True, **kwargs):
        assert response_json in (True, False), 'response_json must be True or False!'
        if encode_data:
            # convert data to json
            __data = json.dumps(data) if isinstance(data, (list,dict)) else data
        else:
            __data = data
        __params = json.dumps(params) if isinstance(params, dict) else params
        time.sleep(self.delay_time)
        session_object = session if session else requests
        # add additional headers if the user provided any in kwargs
        # otherwise the auth token is the only headers to send
        headers = {**self.auth_token_dict, **kwargs.pop('headers', {})}
        if op not in ('get','post','put'):
            raise Exception('op must be in (\'get\',\'post\',\'put\')!')
        if op=='get':
            #self.url = 'http://httpbin.org/'; endpoint='get'; verify = None; headers['Authorization'] = 'aaa';
            r = session_object.get(self.url+endpoint
                            , data=__data
                            , params = __params
                            , headers=headers
                            , verify=cert_path
                            , proxies=self.proxies
                            , **kwargs)
        if op=='post':
            #self.url = 'http://httpbin.org/'; endpoint='post'; verify = None; headers['Authorization'] = 'aaa';
            r = session_object.post(self.url+endpoint
                            , data=__data
                            , params = __params
                            , headers=headers
                            , verify=cert_path
                            , proxies=self.proxies
                            , **kwargs)
        if op=='put':
            #self.url = 'http://httpbin.org/'; endpoint='put'; verify = None; headers['Authorization'] = 'aaa';
            r = session_object.put(self.url+endpoint
                            , data=__data
                            , params=__params
                            , headers=headers
                            , verify=cert_path
                            , proxies=self.proxies
                            , **kwargs)
        if response_json is False:
            return r
        if r.status_code == 401 and (r.text == 'Unauthorized'):
            print('Unauthorized error occured! Check if token is valid.')
            raise Exception('Unauthorized error occured! Check if token is valid.')
        r_json = r.json()
        if verbose:
            # if verbose flag is enabled, print the status code and status msg to console
            print(f"{r_json.get('status','')}", end=' ')
            if ('message' in r_json) and (len(r_json.get('message',()) )==1):
                if '_record_status' in r_json['message'][0]:
                    print(r_json['message'][0]['_record_status'], end='')
                else:
                    print(r_json['message'], end='')
            print('')
        if self.logs_enabled and log_response:
            # if response status is 200, set the log level to "Info"
            logging_function = logging.info if r_json.get('status','')==200 else logging.error
            logging_function(r.text)
        # if sending test requests to httpbin, print the response objects
        if self.url == 'http://httpbin.org/':
            print(r.text)
        return r_json
    def get(self, endpoint, data=None, session=None, verbose=True, params=None, log_response = True, **kwargs):
        return self._transaction_function(endpoint=endpoint, op='get', data=data, params=params, session=session, verbose=verbose, log_response = log_response, **kwargs)
    def post(self, endpoint, data=None, session=None, verbose=True, params=None, log_response = True, **kwargs):
        return self._transaction_function(endpoint=endpoint, op='post', data=data, params = params, session=session, verbose=verbose, log_response = log_response, **kwargs)
    def put(self, endpoint, data=None, session=None, verbose=True, params = None, log_response = True, **kwargs):
        return self._transaction_function(endpoint=endpoint, op='put', data=data, params = params, session=session, verbose=verbose, log_response = log_response, **kwargs)

class urestv2(urestv1):
    def __init__(self,env, token=None, log_directory=None, log_enable=True):
        super().__init__(env = env, token = token, log_directory = log_directory, log_enable = log_enable)
        self.url = restv2_stage_url if env == 'stage' else restv2_prod_url

########################### DataFrame functions
def handle_NaN_strings(x):
    # make sure NaN strings get converted to None
    if x=='NaN': 
        return None
    return x

def perform_df_checks(df):
    if isinstance(df, pd.DataFrame):
        # Convert replace missing values with None
        df2 = df.where(pd.notnull(df),None)
        # Convert NaN strings to None
        df3 = df2.applymap(handle_NaN_strings)
        # Convert DataFrame entries to list<dict>
        return df3.to_dict('records')
    return df

def convert_df_dict_to_list(data):
    # If data is a DataFrame, return records as list of dicts
    # If data is a single dict, return a list of single dict
    # the result should always be list<dict>
    assert isinstance(data, (pd.DataFrame, dict, list)), 'input must be DataFrame, dict, or list<dict>!'
    if isinstance(data, pd.DataFrame):
        # Handle NaN strings and convert to list<dict>
        return perform_df_checks(data)
    elif isinstance(data, dict):
        return [data]
    else:
        if len(data)>0:
            assert all(isinstance(d, dict) for d in data), 'input must be DataFrame, dict, or list<dict>!'
        return data



def nest_line_items(data, line_items, li_cond_func = None):
    assert isinstance(line_items, (pd.DataFrame, list)), 'line_items must be DataFrame, list<DataFrame> or list<dict>!'
    if isinstance(line_items, list):
        if len(line_items)==0:
            line_items_type = 'empty_list'
        elif all(isinstance(line_item, pd.DataFrame) for line_item in line_items):
            line_items_type = 'list<DataFrame>'
        elif all(isinstance(line_item, dict) for line_item in line_items):
            line_items_type = 'list<dict>'
        else:
            raise Exception('line_items must be DataFrame, list<DataFrame> or list<dict>!')
        
    if li_cond_func is None:
        # if no child record condition is specified, use matching record_no columns by default
        def record_no_check(x, y):
            if ('record_no' in x) and ('record_no' in y):
                return x['record_no']==y['record_no']
            return False
            
        li_cond_func = record_no_check
        
    if isinstance(line_items, pd.DataFrame) or line_items_type == 'list<dict>':
        return _nest_line_items(left_tbl = data, right_tbl = line_items, cond_function = li_cond_func)
    elif line_items_type == 'list<DataFrame>':
        # if line_items is list<DataFrame>, nest each DataFrame
        for line_item_df in line_items:
            data = _nest_line_items(left_tbl = data, right_tbl = line_item_df, cond_function = li_cond_func)  
    return data

def _nest_line_items(left_tbl, right_tbl, cond_function):
    '''Nest child items into parent items when a condition is met
    Inputs: 
        left_tbl: DataFrame/dict/list<dict>
        right_tbl: DataFrame/dict/list<dict>
        cond_function: function of two args
            The first arg pertains to a dict in left_tbl
            the second arg pertains to a dict in right_tbl
            cond_function gives True if the second arg should be a child of the first arg
    '''
    left_tbl_list = convert_df_dict_to_list(left_tbl)
    right_tbl_list = convert_df_dict_to_list(right_tbl)
    for itm in left_tbl_list:
        child_records = [child for child in right_tbl_list if cond_function(itm, child)]
        if len(child_records) > 0:
            _itm_bp_lineitems = itm.get('_bp_lineitems', [])
            _itm_bp_lineitems.extend(child_records)
            itm['_bp_lineitems'] = _itm_bp_lineitems
    return left_tbl_list

#################### end DataFrame functions


def create_session_queue(size):
    queue = Queue()
    for _ in range(size):
        queue.put(requests.Session())
    return queue

def close_session_queue(queue):
    while True:
        if queue.empty():
            break
        s = queue.get()
        s.close()

class bpclass:
    def __init__(self, env, project_number, session=None, log_enable=True):
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.project_number = project_number
        self.env = env
        self.session_v1 = urestv1(env=env, log_enable=log_enable)
        self.session_v2 = urestv2(env=env, log_enable=log_enable)
        self.session_queue = None
        self.bpname = 'bpname'
        self.session_object = session if session else requests.Session()
    
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.env}\',\'{self.project_number}\')'
    
    def get(self, record_fields = None, filter_condition = None, lineitem = 'yes', lineitem_fields=None, filter_criteria=None, verbose=True):
        if lineitem not in ('yes','no'):
            raise Exception('lineitem must be \'yes\' or \'no\'!')
        endpoint = f'/bp/records/{self.project_number}' if self.project_number else f'/bp/records/'
        post_body = {'bpname':self.bpname, 'lineitem':lineitem}
        post_body['general_comments']='yes'
        if record_fields:
            post_body['record_fields']=record_fields
        if filter_condition:
            post_body['filter_condition']=filter_condition
        if lineitem_fields and (lineitem=='yes'):
            post_body['lineitem_fields']=lineitem_fields
        if filter_criteria:
            post_body['filter_criteria']=filter_criteria
        return self.session_v1.post(endpoint=endpoint, data=post_body, session=self.session_object, verbose=verbose)
    
    def create(self, data, workflow_name=None, action_name=None, line_items=None, li_cond_func=None, verbose=True, LineItemIdentifier=None):
        return self.createv1(data = data
            , workflow_name = workflow_name
            , action_name = action_name
            , line_items = line_items
            , li_cond_func = li_cond_func
            , verbose = verbose
            , LineItemIdentifier = LineItemIdentifier)
        
    def update(self, data, WFCurrentStepName = None, WFActionName = None, line_items=None, li_cond_func=None, verbose=True, LineItemIdentifier = None):
        return self.updatev1(data = data
            , WFCurrentStepName = WFCurrentStepName
            , WFActionName = WFActionName
            , line_items=line_items
            , li_cond_func=li_cond_func
            , verbose=verbose
            , LineItemIdentifier = LineItemIdentifier)
            
    def createv1(self, data, workflow_name=None, action_name=None, line_items=None, li_cond_func = None, verbose=True, LineItemIdentifier=None):
        endpoint = f'/bp/record/{self.project_number}' if self.project_number else '/bp/record/'
        if (workflow_name is None) != (action_name is None):
            raise Exception('workflow_name and action_name are both required together!')
        # convert input data to list<dict>
        _data = convert_df_dict_to_list(data)
        # if there are line items, nest line items
        if not (line_items is None):
            _data = nest_line_items(data = _data, line_items = line_items, li_cond_func = li_cond_func)
        # create post body and send
        post_body = {'options':{'bpname':self.bpname},'data':_data}
        if LineItemIdentifier is not None:
            post_body['options']['LineItemIdentifier'] = LineItemIdentifier
        if workflow_name or action_name:
            workflow_details = {'workflow_name':workflow_name
                                    , 'user_name':'System Integration'
                                    ,'action_name':action_name}
            post_body['options']['workflow_details']=workflow_details
        return self.session_v1.post(endpoint=endpoint, data=post_body, session=self.session_object, verbose=verbose)
        
    def updatev1(self, data, WFCurrentStepName = None, WFActionName = None, line_items=None, li_cond_func=None, verbose=True, LineItemIdentifier = None):
        endpoint = f'/bp/record/{self.project_number}' if self.project_number else '/bp/record/'
        if (WFCurrentStepName is None) != (WFActionName is None):
            raise Exception('WFCurrentStepName and WFActionName are both required together!')
        # convert input data to list<dict>
        _data = convert_df_dict_to_list(data)
        # if there are line items, nest line items
        if not (line_items is None):
            _data = nest_line_items(data = _data, line_items = line_items, li_cond_func = li_cond_func)
        # create put body and send
        put_body = {'options':{'bpname':self.bpname}, 'data':_data}
        if LineItemIdentifier is not None:
            put_body['options']['LineItemIdentifier'] = LineItemIdentifier
        if WFCurrentStepName or WFActionName:
            put_body['options']['workflow_details'] = {'WFCurrentStepName':WFCurrentStepName, 'WFActionName':WFActionName}
        #print(put_body)
        return self.session_v1.put(endpoint=endpoint, data=put_body, session=self.session_object, verbose=verbose)
            
    def createv2(self, data, workflow_name=None, action_name=None, line_items=None, li_cond_func=None, verbose=True, LineItemIdentifier = None):
        endpoint = '/bp/record'
        if (workflow_name is None) != (action_name is None):
            raise Exception('workflow_name and action_name are both required together!')
         # convert input data to list<dict>
        _data = convert_df_dict_to_list(data)
         # if there are line items, nest line items
        if not (line_items is None):
            _data = nest_line_items(data = _data, line_items = line_items, li_cond_func = li_cond_func)
         # create post body and send
        post_body = {'options':{'bpname':self.bpname},'data':_data}
        if self.project_number:
            post_body['options']['project_number'] = self.project_number
        if LineItemIdentifier is not None:
            post_body['options']['LineItemIdentifier'] = LineItemIdentifier
        if workflow_name or action_name:
            workflow_details = {'workflow_name':workflow_name
                                    , 'user_name':'System Integration'
                                    ,'action_name':action_name}
            post_body['options']['workflow_details']=workflow_details
        return self.session_v2.post(endpoint=endpoint, data=post_body, session=self.session_object, verbose=verbose)
        
    def updatev2(self, data, WFCurrentStepName = None, WFActionName = None, line_items=None, li_cond_func=None, verbose=True, LineItemIdentifier = None):
        endpoint = '/bp/record/'
        if (WFCurrentStepName is None) != (WFActionName is None):
            raise Exception('WFCurrentStepName and WFActionName are required together!')
         # convert input data to list<dict>
        _data = convert_df_dict_to_list(data)
         # if there are line items, nest line items
        if not (line_items is None):
            _data = nest_line_items(data = _data, line_items = line_items, li_cond_func = li_cond_func)
         # create put body and send
        put_body = {'options':{'bpname':self.bpname}, 'data':_data}
        if (WFCurrentStepName is None) != (WFActionName is None):
            raise Exception('WFCurrentStepName and WFActionName are required!')
        if self.project_number:
            put_body['options']['project_number'] = self.project_number
        if LineItemIdentifier is not None:
            put_body['options']['LineItemIdentifier'] = LineItemIdentifier
        if WFCurrentStepName or WFActionName:
            put_body['options']['workflow_details'] = {'WFCurrentStepName':WFCurrentStepName, 'WFActionName':WFActionName}
        return self.session_v2.put(endpoint=endpoint, data=put_body, session=self.session_object, verbose=verbose)
        
    def add_attachment_single_record(self, data, input_attachments, verbose=True, version = 'v1', timeout = 20):
        assert version in ('v1','v2'), 'version must be \'v1\' or \'v2\'!'
        assert isinstance(data, (list, pd.DataFrame, dict)), 'data must be list<dict>, DataFrame, or dict!'
        # convert data to list<dict>
        _data = convert_df_dict_to_list(data)
        assert len(_data)==1, 'expecting exactly one data record!'
        assert 'record_no' in _data[0], 'record_no column is required but missing!'
        assert _data[0]['record_no'] is not None, 'record_no is blank!'
        assert len(_data[0]['record_no'])>0, 'record_no is blank!'
        # _data will be a list with a single dict, with record_no as a required field
        # example: [{'record_no': record_no, ...(optional fields to update)... }]
                
        # input_attachments should be dict of the form:
         # {'file_path': required str or Path object
            #, 'title': optional str
            #, 'issue_date': optional str
            #, 'revision_no': optional str
            #}
        assert isinstance(input_attachments, dict), 'input_attachments must be a dict!'
        assert 'file_path' in input_attachments, 'file_path column is required!'
        _attachment = copy(input_attachments)
        # upload might fail if file_path column is in the _attachment dict; pop the entry
        file_path_str = _attachment.pop('file_path')
        file_path = Path(file_path_str)
            
            
        # give error msg if a input file is a folder or does not exist
        if (file_path.is_file() is False):
            _data[0]['_record_status'] = f'Input file does not exist!: {str(file_path)}'
            return {'data':[],'message':_data,'status':9999}
            
        _attachment['file_name']= file_path.name
        for file_ext in file_extensions:
            # check for invalid file ext (ex: rename abc pdf to abc pdf.pdf)
            # example: if the input file has filename 'abc pdf', it will fail to upload.
            # create a temp copy with the name 'abc pdf.pdf' and upload the temp copy
            if _attachment['file_name'].lower().endswith(' '+file_ext):
                _attachment['file_name'] += '.'+file_ext
                file_path = create_temp_copy(original_file_path = file_path, new_file_name = _attachment['file_name'])
              
        # create the put body
        # attachment_zip has the form required by web services:
        #        {'zipped_file_name': name of zip file
        #           , 'zipped_file_size': size of zip file
        #           , 'zipped_file_content': zip file as b64 encoded string
        #            }
        attachment_zip = makeZipArchive(file_path)
        _data[0]['_attachment'] = [_attachment]
        put_body = {'options':{'bpname':self.bpname, 'project_number':self.project_number}
                , 'data':_data
                , '_attachment': attachment_zip}
        if version == 'v1':
            endpoint = '/bp/record/file/' if self.project_number is None else f'/bp/record/file/{self.project_number}'
            r = self.session_v1.put(endpoint=endpoint, data=put_body, session=self.session_object, verbose=verbose, timeout = timeout)
        else:
            endpoint = '/bp/record/file'
            r = self.session_v2.put(endpoint=endpoint, data=put_body, session=self.session_object, verbose=verbose, timeout = timeout)
                
        ### Remove temp files
        if file_path.parent == temp_dir_path:
            file_path.unlink()
        return r
                
    def add_attachment_single_record_v1(self, data, input_attachments, verbose=True, timeout = 20):
        return self.add_attachment_single_record(data = data
                                            , input_attachments = input_attachments
                                            , verbose = verbose
                                            , version = 'v1'
                                            , timeout = timeout)
        
    def get_record(self, record_no, record_fields = None,lineitem='yes', verbose=True):
        if lineitem not in ('yes','no'):
            raise Exception('lineitem must be \'yes\' or \'no\'!')
        if len(record_no)<1:
            raise Exception('record_no is blank!')
        endpoint = f'/bp/record/{self.project_number}' if self.project_number else f'/bp/record/'
        return self.get(record_fields=record_fields, filter_condition=f'record_no={record_no}',lineitem=lineitem, verbose=verbose)
    def get_record2(self, record_no, verbose=True):
        '''Get BP Record implementation'''
        assert len(record_no)>0, 'record_no is blank!'
        endpoint = f'/bp/record/{self.project_number}'
        __params = {'bpname':self.bpname
            , 'record_no':record_no
            , 'lineitem':'yes'
            , 'general_comments':'yes'}
        __params_json = json.dumps(__params)
        __params = urlencode({'input':__params_json})
        r = self.session_v1.get(endpoint = endpoint
                            , params = __params
                            , verbose = verbose
                            , log_response = False)
        if len(r.get('data',[]))<1:
            return {'project_number':self.project_number
                , 'record_no':record_no
                , 'status':999
                , 'message':'no data found!'}
        return r
                
    def get_full_record(self, record_no, verbose = True, download_path = download_default_path, append_tag = False, return_response = False):
        # get record data and attachments
        assert isinstance(download_path, (Path, str)), 'download_path must be a str or Path object!'
        assert append_tag in (True, False), 'append_tag must be True or False!'
        assert len(record_no)>0, 'record_no is blank!'
        __download_path = Path(download_path) if isinstance(download_path, str) else download_path
        endpoint = f'/bp/record/file/{self.project_number}'
        __params = {'bpname':self.bpname
            , 'record_no':record_no
            , 'lineitem':'yes'
            , 'lineitem_file':'yes'
            , 'general_comments':'yes'
            , 'attach_all_publications':'yes'}
        __params_json = json.dumps(__params)
        __params = urlencode({'input':__params_json})
        r = self.session_v1.get(endpoint = endpoint, params = __params, verbose = verbose, log_response = False)
        if len(r.get('data',[]))<1:
            return {'project_number':self.project_number
                , 'record_no':record_no
                , 'status':999
                , 'message':'no data found!'}
        __record_data = r['data'][0].pop('record_data')
        __file_name = r['data'][0] 
        __project_number = 'CompanyWorkspace' if self.project_number is None else self.project_number
        __download_directory_name = __project_number+'_'+record_no
        __download_path = __download_path/__download_directory_name
        __tag = '' if append_tag is False else '_'+timestamp_ymd()+'_'+uuid.uuid4().hex
        __record_data_filename = __project_number+'_'+record_no+'_'+'record_data'+__tag+'.txt'
        __record_info_path = __download_path/__record_data_filename
        if not __download_path.exists():
            __download_path.mkdir(parents=True)
        with open(__record_info_path, 'w') as record_info_stream:
            record_info_stream.write(pformat(__record_data))
            print('Wrote record data to: ', str(__record_info_path))
        if 'file_handler' in r['data'][0]:
            __attachment_zip_filename = r['data'][0]['file_name']
            __attachment_zip_path = __download_path/__attachment_zip_filename
            with open(__attachment_zip_path, 'wb') as ff:
                ff.write(base64.b64decode(r['data'][0]['file_handler']))
                print('Wrote attachments data to: ', str(__attachment_zip_path))
            with zipfile.ZipFile(__attachment_zip_path, 'r') as zf:
                zf.extractall(path = __download_path)
        return {'project_number':self.project_number
            , 'record_no':record_no
            , 'status':200
            , 'message':'success. saved to: '+str(__download_path)}
        
    def get_store(self, record_fields = None,*, table_name = None, filter_condition=None, lineitem='no', lineitem_fields=None, filter_criteria=None, db_conn=None, if_exists = get_store_if_exists_default):
        if table_name is None:
            ts = timestamp_ymd()
            _table_name = throwaway_prefix+ts+self.__class__.__name__+'_'+uuid4().hex
        else:
            _table_name = table_name
        _db_conn = get_temp_con(db_conn)
        if (record_fields is not None) and 'record_no' not in record_fields.split(';'):
            # always fetch record_no
            __record_fields = 'record_no;'+record_fields
        else:
            __record_fields = record_fields
        rd = self.get(record_fields=__record_fields, filter_condition=filter_condition, lineitem='no', lineitem_fields=None, filter_criteria=filter_criteria)['data']
        for d in rd:
            d['project_number'] = self.project_number if self.project_number is not None else ''
        if len(rd)==0:
            _table_name = None
            print('No records detected!')
        else:
            write_dicts_to_db(input_dicts = rd, tbl_name = _table_name, db_con = _db_conn, if_exists = if_exists)
            print('Wrote to table: ', _table_name)
        close_temp_con(db_conn, _db_conn)
        return _table_name
            
            
    def get_store_csv(self, record_fields = None,*,filedir = None, csv_name = None, filter_condition=None, lineitem='no', lineitem_fields=None, filter_criteria=None):
        ts = timestamp_ymd()
        csv_name = throwaway_prefix+ts+self.__class__.__name__+'_'+uuid4().hex
        _filedir = get_temp_filedir(filedir)
        if (record_fields is not None) and 'record_no' not in record_fields.split(';'):
            # always fetch record_no
            __record_fields = 'record_no;'+record_fields
        else:
            __record_fields = record_fields
        rd = self.get(record_fields=__record_fields, filter_condition=filter_condition, lineitem='no', lineitem_fields=None, filter_criteria=filter_criteria)['data']
        for d in rd:
            d['project_number'] = self.project_number if self.project_number is not None else ''
        return_dict = {'csv_name':csv_name, 'file_path': None, 'file_dir': filedir}
        if len(rd)==0:
            print('No records detected! No csv created.')
        else:
            file_path = write_dicts_to_csv(input_dicts = rd, name = csv_name, filedir = _filedir)
            return_dict['file_path'] = file_path
            print('Wrote to csv: ', str(file_path))
        return return_dict
            
    def get_dt(self, filter_condition = None, lineitem_fields = None, filter_criteria = None):
        '''
            get lineitems
        '''
        rd_list = self.get(record_fields='record_no;_bp_lineitems', filter_condition = filter_condition, filter_criteria = filter_criteria, lineitem='yes', lineitem_fields = lineitem_fields)['data']
        dt_records = dict()
        tab_names = dict()
        for d1 in rd_list:
            for d2 in d1.get('_bp_lineitems',{}):
                if d2:
                    d2['record_no'] = d1['record_no']
                    d2['project_number'] = self.project_number if self.project_number is not None else ''
                    tab_name = remove_nonalnum(d2['uuu_tab_id']).lower()
                    if (len(tab_name) > 0) and (tab_name[0].isdigit()):
                        # prevent table names from starting with a number 
                        # table names starting with a number is inconvenient for sql tables
                        tab_name = 'n'+tab_name
                    tab_id = d2['tab_id']
                    dt_records[tab_id] = dt_records.get(tab_id, []) + [d2]
                    if tab_id not in tab_names:
                        tab_names[tab_id] = tab_name
        return dt_records, tab_names
                
    def get_store_dt(self,*,table_name = None, filter_condition=None, lineitem_fields=None, filter_criteria=None, db_conn=None, if_exists = get_store_if_exists_default):
        '''
            get line items and write to database table
        '''
        tabs, tab_names = self.get_dt(filter_condition = filter_condition, lineitem_fields = lineitem_fields, filter_criteria = filter_criteria)
        ts = timestamp_ymd()
        tbl_names = []
        _db_conn = get_temp_con(db_conn)
        for tab_id in tabs:
            __tab_name = tab_names[tab_id]
            if table_name is None:
                __tbl_name = throwaway_prefix+ts+self.__class__.__name__+self.env+__tab_name+'_'+uuid4().hex
            else:
                __tbl_name = table_name+'_'+__tab_name
            write_dicts_to_db(input_dicts = tabs[tab_id], tbl_name = __tbl_name, db_con = _db_conn, if_exists = if_exists)
            print(f'Wrote tab: {__tab_name} to table: {__tbl_name}')
            tbl_names.append(__tbl_name)
        close_temp_con(db_conn, _db_conn)
        if len(tbl_names) <1:
            print('No line items to evaluate.')
        return tbl_names
                
                
    def get_store_dt_csv(self,*, filedir = None, filter_condition=None, lineitem_fields=None, filter_criteria=None):
        '''
            get line items and write to csv
        '''
        ts = timestamp_ymd()
        _filedir = get_temp_filedir(filedir)
        tabs, tab_names = self.get_dt(filter_condition = filter_condition, lineitem_fields = lineitem_fields, filter_criteria = filter_criteria)
        return_dicts = []
        for tab_id in tabs:
            __tab_name = tab_names[tab_id]
            csv_name = throwaway_prefix+ts+self.__class__.__name__+self.env+__tab_name+'_'+uuid4().hex
            file_path = write_dicts_to_csv(input_dicts = tabs[tab_id], name = csv_name, filedir = _filedir)
            d = {'file_path':file_path, 'filedir':_filedir, 'csv_name':csv_name, 'tab_name':__tab_name}
            return_dicts.append(d)
            print(f'Wrote tab: {__tab_name} to: {str(file_path)}')
        if len(tabs) <1:
            print('No line items to evaluate.')
        return return_dicts
                
    def _eval_single_row(self, row, op, version=1, **kwargs):
        # single iter for s_create, s_update, and s_create_update functions
        if (version not in (1,2)) or (op not in ('create','update')):
            raise Exception('Invalid input argument!')
        assert isinstance(row, dict), 'input row needs to be a dict!'
        PKCols = s_default_pkcols if 'PKCols' not in kwargs else kwargs['PKCols']   
        try:
            if ('project_number' not in row):
                raise Exception('"project_number" column is missing!')
            else:
                if (self.project_number != row['project_number']) and (self.project_number is not None):
                    raise Exception(f"Cancelled due to differing project_number. row: {row['project_number']} bp: {self.project_number}")
            for __param in kwargs:
                if __param in row:
                    if (kwargs[__param] != row[__param]):
                        raise Exception(f"Cancelled due to disagreeing row & arg param {__param}.\r\n\trow: {row[__param]}\r\n\t arg: {kwargs[__param]}")
            _workflow_name = kwargs.pop('workflow_name', None) or row.pop('workflow_name', None)
            _action_name = kwargs.pop('action_name', None) or row.pop('action_name', None)
            _WFCurrentStepName = kwargs.pop('WFCurrentStepName', None) or row.pop('WFCurrentStepName', None)
            _WFActionName = kwargs.pop('WFActionName', None) or row.pop('WFActionName', None)
            _LineItemIdentifier = kwargs.pop('LineItemIdentifier', None) or row.pop('LineItemIdentifier', None)
            
            s = self.session_queue.get()    
            _bp_inst = self.__class__(env = self.env, project_number = row['project_number'], session = s)
            if op == 'create':
                __func = _bp_inst.createv1 if version==1 else _bp_inst.createv2
                r = __func(data=row, workflow_name = _workflow_name, action_name = _action_name, verbose=True, LineItemIdentifier = _LineItemIdentifier)
            else:
                __func = _bp_inst.updatev1 if version==1 else _bp_inst.updatev2
                assert row.get('record_no', None) is not None, 'record_no is required!'
                assert len(row['record_no'])>0, 'record_no is required!'
                r = __func(data=row, WFCurrentStepName = _WFCurrentStepName, WFActionName = _WFActionName, verbose=True, LineItemIdentifier = _LineItemIdentifier)
            self.session_queue.put(_bp_inst.session_object)
            del _bp_inst
            r['project_number'] = row['project_number']
            if isinstance(r['message'][0], dict):
                r['_record_status'] = r['message'][0].get('_record_status', 'None')
                r_record_no = r['message'][0].get('record_no', 'None')
                if r_record_no is not None:
                    r['r_record_no'] = r_record_no
            else:
                r['_record_status'] = r['message']
            return {**r, **{col: row[col] for col in row if col.lower() in PKCols.lower().split(';')}, 'PKCols':PKCols}
        except Exception as e:
            self.session_queue.put(requests.Session())
            print('Exception encountered: ', e)
            return_dict = {'project_number': row.get('project_number', '')
                , "data": []
                , "message":[{"_record_status":f'Exception encountered! {str(e)}'}]
                , '_record_status':f'Exception encountered! {str(e)}'
                , 'status':9999
                }
            return {**return_dict, **{col: row[col] for col in row if col.lower() in PKCols.lower().split(';')}, 'PKCols':PKCols}
            
                
    def _eval_single_row_dt(self, row, LineItemIdentifier = None):
        op = 'update'
        LineItemIdentifierDict = {}
        _LineItemIdentifier = None
        PKCols = s_default_pkcols
        try:
            assert isinstance(row, dict), 'expecting row to be dict'
            assert row.get('record_no',None) is not None, 'record_no is required!'
            assert len(row['record_no'])>0, 'record_no is required!'
            assert row.get('uuu_tab_id',None) is not None, 'uuu_tab_id is required!'
            assert len(row['uuu_tab_id'])>0, 'uuu_tab_id is required!'
            if (self.project_number != row['project_number']) and (self.project_number is not None):
                raise Exception(f"Cancelled due to differing project_number. row: {row['project_number']} bp: {self.project_number}")
            if 'LineItemIdentifier' in row:
                # if a row has LineItemIdentifier column in it, it should match the value passed in kwarg
                _LineItemIdentifier = row.pop('LineItemIdentifier', None)
                if (LineItemIdentifier is not None) and (LineItemIdentifier != _LineItemIdentifier):
                    raise Exception('Cancelled due to disagreeing LineItemIdentifier param!')
            else:
                _LineItemIdentifier = LineItemIdentifier
                    
            if _LineItemIdentifier is not None:
                # LineItemIdentifierDict is used for logging purposes
                LineItemIdentifierDict = {'LineItemIdentifier__'+_LineItemIdentifier:row.get(_LineItemIdentifier,'')} 
                    
            s = self.session_queue.get()
            _bp_inst = self.__class__(env = self.env, project_number = row['project_number'], session = s)
            __data = {'record_no':row['record_no'],'_bp_lineitems':[row]} 
            r = _bp_inst.updatev1(data=__data, verbose=True, LineItemIdentifier = _LineItemIdentifier)
            self.session_queue.put(_bp_inst.session_object)
            del _bp_inst
            r['project_number'] = row['project_number']
            if isinstance(r['message'][0], dict):
                r['_record_status'] = r['message'][0].get('_record_status', None)
                r_record_no = r['message'][0].get('record_no', None)
                if r_record_no is not None:
                    r['r_record_no'] = r_record_no
            else:
                r['_record_status'] = r['message']
        except Exception as e:
            self.session_queue.put(requests.Session())
            print('Exception encountered: ', e)
            r = {'project_number': row.get('project_number', '')
                , "data": []
                , "message":[{"_record_status":f'Exception encountered! {str(e)}'}]
                , '_record_status':f'Exception encountered! {str(e)}'
                , 'status':9999
                }
        finally:
            return {
                **{col: row[col] for col in row if col.lower() in PKCols.lower().split(';')}
                , **LineItemIdentifierDict
                , **r
                , 'PKCols':PKCols+';'+';'.join(LineItemIdentifierDict.keys())
                }
                    
    def _fmt_s_function_results(self, results_list):
        ''' this function specifies the columns of the log csv file 
        input: list of dictionaries for response objects
        output: pandas DataFrame in the format specified
        '''
        df_results_list = []
        for r in results_list:
            df_results_list.append(
            { 'project_number': r.get('project_number', 'None')
            , 'record_no': r.get('record_no','None')
            , **{col:r.get(col, 'None') for col in r if col.lower() in r['PKCols'].lower().split(';')}
            , '_record_status': r.get('_record_status', 'None')
            , 'status': r.get('status', 'None')
            })
        return pd.DataFrame(df_results_list)
                
    def _bp_iter_function(self, rows, func, pool_size = 4, return_results = False):
        '''
        Apply a function over rows
        '''
        t1 = time.time()
        self.session_queue = create_session_queue(size = pool_size + 2)
        with ThreadPoolExecutor(pool_size) as ex:
            results = ex.map(func, rows)
        t2 = time.time()
        print(f'Completed in {str(t2-t1)}s')
        results_list = list(results)
        _df = self._fmt_s_function_results(results_list)
        close_session_queue(self.session_queue)
        if hasattr(func, '__name__'):
            __name = self.env+'_'+self.__class__.__name__+'_'+func.__name__
        else:
            __name = self.env+'_'+self.__class__.__name__
        pprint(Counter([d['status'] for d in results_list]))
        results_csv = df_save_csv(_df, name=__name, timestamp=True)
        log_pkl(input_object = results_list, name = __name)
        if return_results is True:
            return results_list
        return None
            
    def _s_function(self, sql_query, func, pool_size = 4, db_conn = None, return_results = False):
        '''SQL Query functions:
        First query the database, then apply the function (func) over the result set
        '''
        _db_conn = get_temp_con(db_conn)
        cur = _db_conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        close_temp_con(db_conn, _db_conn)
        return self._bp_iter_function(rows, func, pool_size, return_results = return_results)
                
    def _create_update(self, rows, version, pool_size = 4, **kwargs):
        '''
        if record_no does not exist, create a new record
        if the record_no does exist, update the existing record

        1) create the dict: {project_number: [list of record_no belonging to project_number]}
        2) a) if record_no of a row does not exist, create a new record
           b) if the record_no does exist, update the existing record
        3) save a csv of the results
        '''
        assert isinstance(rows, list), 'rows must be list instance!'
        if any(d.get('record_no', None) is None for d in rows):
            raise Exception('detected row null record_no!')
        assert all('project_number' in d for d in rows), '\'project_number\' column is missing!'
        project_numbers = (d['project_number'] for d in rows)
        distinct_project_numbers = set(project_numbers)
        t1 = time.time()
        self.session_queue = create_session_queue(size = pool_size)
                
        def _fetch_record_numbers(project_number = None):
            # get existing record numbers from each project
            s = self.session_queue.get()
            if project_number is None:
                project_number = self.project_number
            x = self.__class__(env = self.env, project_number = project_number, session = s)
            r = x.get(record_fields='record_no')
            record_numbers = [d.get('record_no',None) for d in r['data']]
            self.session_queue.put(s)   
            return (project_number, record_numbers)
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            _existing_record_numbers = ex.map(_fetch_record_numbers, distinct_project_numbers)
        existing_record_numbers = dict(_existing_record_numbers)
        # existing_record_numbers is a dictionary:
            # keys are project_number 
            # values are list of record_no belonging to the project_number
                
        def _create_update_single_row(row):
            # if record_no does not exist, create a new record
            # if the record_no does exist, update the existing record
            __project_number = row['project_number']
            if row['record_no'] in existing_record_numbers.get(__project_number, []):
                __op = 'update'
            else:
                __op = 'create'
            return self._eval_single_row(row, op = __op, version = version, **kwargs)
                
        with ThreadPoolExecutor(max_workers = pool_size) as ex:
            results = ex.map(_create_update_single_row, rows)
                
        t2 = time.time()
        print(f'Completed in {str(t2-t1)}s')
        results_list = list(results)
        # close open sessions    
        close_session_queue(self.session_queue)
            
        # save results as a csv in the the log folder
        _df = self._fmt_s_function_results(results_list)
        __name = self.env+'_'+self.__class__.__name__+'_createupdate'
        results_csv = df_save_csv(_df, name=__name, timestamp=True)
        log_pkl(input_object = results_list, name = __name)
            
         # print the counts of status codes
        pprint(Counter([d['status'] for d in results_list]))
        return results_list
             
    def s_create_update(self, sql_query, pool_size = 4, db_conn = None, version = 1, return_results = False, **kwargs):
        # read the results of a sql query, and send the rows to _create_update
        # If the results are needed, set return_results = True
        con = sqlite3_dict_connect() if db_conn is None else db_conn
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        results_list = self._create_update(rows = rows, pool_size = pool_size, version = version, **kwargs)
        if db_conn is None:
            con.close()
        if return_results is True:
            return results_list
            
    def s_create_updatev2(self, sql_query, pool_size = 4, db_conn = None, return_results = False, **kwargs):
        if return_results is True: 
            return self.s_create_update(sql_query = sql_query, pool_size = pool_size, db_conn = db_conn, version=2, return_results = True, **kwargs)
        self.s_create_update(sql_query = sql_query, pool_size = pool_size, db_conn = db_conn, version=2, return_results = False, **kwargs)
            
    def s_create(self, sql_query, pool_size=4, db_conn=None, return_results = False, **kwargs):
        '''SQL create
        Send the create command over a sql result set
        Returns a iterator of dicts
        '''
        _func = partial(self._eval_single_row, version=1, op='create', **kwargs)
        _func.__name__ = 'create'
        return self._s_function(sql_query=sql_query, pool_size = pool_size, db_conn = db_conn, func = _func, return_results = return_results)
                
    def s_createv2(self, sql_query, pool_size=4, db_conn=None, return_results = False, **kwargs):
        '''SQL create
        Send the create command over a sql result set
        Returns a iterator of dicts
        '''
        _func = partial(self._eval_single_row, version=2, op='create', **kwargs)
        _func.__name__ = 'create'
        return self._s_function(sql_query=sql_query, pool_size = pool_size, db_conn = db_conn, func = _func, return_results = return_results)
    
    def s_update(self, sql_query, pool_size=4, db_conn = None, return_results = False, **kwargs):
        '''SQL update
        Send the update command over a sql result set
        Returns a iterator of dicts
        '''
        _func = partial(self._eval_single_row, version=1, op='update', **kwargs)
        _func.__name__ = 'update'
        return self._s_function(sql_query=sql_query, pool_size = pool_size, db_conn = db_conn, func = _func, return_results = return_results)
         
    def s_updatev2(self, sql_query, pool_size=4, db_conn = None, return_results = False, **kwargs):
        '''SQL update
        Send the update command over a sql result set
        Returns a iterator of dicts
        '''
        _func = partial(self._eval_single_row, version=2, op='update', **kwargs)
        _func.__name__ = 'update'
        return self._s_function(sql_query=sql_query, pool_size = pool_size, db_conn = db_conn, func = _func, return_results = return_results)
         
    def _csv_function(self, csv_path, func, pool_size, return_results = False):
        assert isinstance(csv_path, (str, Path)), 'csv_path must be str or Path!'
        _path = csv_path if isinstance(csv_path, Path) else Path(csv_path)
        with open(_path, 'r') as ff:
            rows = list(csv.DictReader(ff))
        return self._bp_iter_function(rows, func, pool_size, return_results = return_results)
            
    def csv_update(self, csv_path, pool_size = 4, version = 1, return_results = False, **kwargs):
        _func = partial(self._eval_single_row, version=1, op='update', **kwargs)
        _func.__name__ = 'update'
        return self._csv_function(csv_path = csv_path
                                    , func = _func
                                    , pool_size = pool_size
                                    , return_results = return_results)
            
    def csv_create(self, csv_path, pool_size = 4, version = 1, return_results = False, **kwargs):
        _func = partial(self._eval_single_row, version=1, op='create', **kwargs)
        _func.__name__ = 'create'
        return self._csv_function(csv_path = csv_path
                                    , func = _func
                                    , pool_size = pool_size
                                    , return_results = return_results)
            
    def s_dt(self, sql_query, pool_size = 4, db_conn = None, version = 1, return_results = False, LineItemIdentifier = None):
        con = get_temp_con(db_conn)
        cur = con.cursor()
        rows = cur.execute(sql_query).fetchall()
        close_temp_con(con, db_conn)
        for rn, d in enumerate(rows, 1):
            assert 'project_number' in d.keys(), f'project_number is required! error at row number: {rn}'
            assert 'record_no' in d.keys(), f'record_no is required! error at row number: {rn}'
            assert len(d['record_no'])>0, f'record_no is blank! error at row number: {rn}'
            assert 'uuu_tab_id' in d.keys(), f'uuu_tab_id is required! error at row number: {rn}'
            assert len(d['uuu_tab_id'])>0, f'uuu_tab_id is required! error at row number: {rn}'
        _func = partial(self._eval_single_row_dt, LineItemIdentifier = LineItemIdentifier)
        _func.__name__ = 'dt'
        return self._bp_iter_function(rows, func = _func, pool_size = pool_size, return_results = return_results)
    def csv_dt(self, csv_path, pool_size = 4, return_results = False, LineItemIdentifier = None):
        _func = partial(self._eval_single_row_dt, LineItemIdentifier = LineItemIdentifier)
        _func.__name__ = 'dt'
        return self._csv_function(csv_path = csv_path
                                    , func = _func
                                    , pool_size = pool_size
                                    , return_results = return_results)
            
    def __getitem__(self, key):
        if not isinstance(key, str):
            raise Exception('Key must be a string!')
        r = self.get_record(record_fields = None, lineitem='yes', record_no=key)
        pprint(r)
        return r
                
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise Exception('Key must be a string!')
        endpoint = '/bp/record' if self.project_number is None else f'/bp/record/{self.project_number}'
        data = copy(value)
        data['record_no'] = key
        _ping = self.get_record(record_fields='record_no',record_no=key, verbose=False)
        body = {}
        body['options'] = {'bpname':self.bpname}
        if len(_ping['data'])==0:
            print('Record does not exist!')
        else:
            # update existing record
            workflow_details = {'WFActionName':data.pop('WFActionName', None)
                , 'WFCurrentStepName':data.pop('WFCurrentStepName', None)}
            body['options']['workflow_details'] = workflow_details
            body['options']['LineItemIdentifier'] = data.pop('LineItemIdentifier', None)
            body['data'] = [data]
            return self.session_v1.put(endpoint = endpoint, data=body, session=self.session_object)

def gen_random_string(k=4):
    #'''Return a length k string composed of random lowercase letters'''
    _random_list = random.choices(string.ascii_lowercase, k=k)
    return ''.join(_random_list)


def timestamp_ymd():
    '''Return timestamp in YYYYmmdd format'''
    return datetime.now().strftime('%Y%m%d')

def df_save_csv(df, name, filedir = log_dir_path, timestamp = True, random_tag = True):
    '''Save a DataFrame as a csv
    Required Inputs: df (DataFrame), name (string), directory (string or Path - default to log directory)
    Append timestamp and a random tag (optional) to name, and use the result as the filename for csv output of df
    Ex: df = pd.DataFrame(results); df_save_csv(df,'action_items_results')
    '''
    if not isinstance(df, pd.DataFrame):
        raise TypeError('Expecting DataFrame input!')
    if not (isinstance(filedir, str) or isinstance(filedir, Path)):
        raise TypeError('Expecting Path or str input for filedir!')
    elif isinstance(filedir, str):
        _filedir = Path(filedir)
    else:
        _filedir = filedir
    if not _filedir.exists():
        _filedir.mkdir()
    ts = timestamp_ymd() if timestamp else ''
    random_tag = gen_random_string() if random_tag else ''
    filename = name+ts+random_tag+'.csv'
    filepath = _filedir/filename
    df.to_csv(filepath, index=False)
    print('Results saved to: ', str(filepath))
    return filename


####### sqlite3 objects
def sqlite3_connect(db_path = hm_db_path):
    #''' Returns default sqlite3 connection - rows are tuples'''
    assert isinstance(db_path, (Path, str)), 'db_path must be a string or a path!'
    if isinstance(db_path, str):
        _conn = sqlite3.connect(Path(db_path))
    else:
        _conn = sqlite3.connect(db_path)
    return _conn

def sqlite3_tuple_connect(db_path = hm_db_path):
    #''' Returns default sqlite3 connection - rows are tuples'''
    return sqlite3_connect(db_path = db_path)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def sqlite3_dict_connect(db_path = hm_db_path):
    #''' Returns a sqlite3 connection with row_factory changed to dict_factory - rows are dicts'''
    _conn = sqlite3_connect(db_path = db_path)
    _conn.row_factory = dict_factory
    return _conn


def get_temp_con(con):
    if con is None:
        return sqlite3_dict_connect()
    return con


def close_temp_con(con, _con):
    if con is None:
        _con.close()





############ end of sqlite3 objects


def prompt_random_string():
    __aaa = gen_random_string()
    print('\n')
    __bbb = input(f'To continue, input "{__aaa}": ')
    if __bbb != __aaa:
        raise Exception('Discontinued!')
        sys.exit(0)

def log_pkl(input_object, name, filedir = log_dir_path, timestamp = True, random_tag = True):
    '''
    Purpose: save a python object as a pkl for future use
    
    input_object: python object to save
    name: name of object (this will be part of the file name)
    filedir: directory to save pkl (default is the log dir)
    timestamp: append timestamp in filename
    random_tag: append random tag in filename
    '''
    assert isinstance(filedir, Path) or isinstance(filedir, str), 'filedir must be a Path or str!'
    ts = timestamp_ymd() if timestamp is True else ''
    _filedir = Path(filedir) if isinstance(filedir, str) else filedir
    if not _filedir.exists():
        _filedir.mkdir()
    random_tag = gen_random_string(7) if random_tag is True else ''
    pkl_filename = name+ts+random_tag+'.pkl'
    pkl_path = log_dir_path/pkl_filename
    with open(pkl_path, 'wb') as ff:
        pickle.dump(input_object, ff)
    return pkl_path

def get_all_dict_fields(input_dicts):
    '''return a list of all dictionary keys.
    return a empty list if the input iterable has 0 records.
    '''
    if len(input_dicts) == 0:
        return []
    # the reason for using _key_list instead of a set is because set is unordered
    _key_list = []
    for d in input_dicts:
        for key in d.keys():
            if key not in _key_list:
                _key_list.append(key)
    for key in _key_list:
        for character in key:
            if character.lower() not in string.ascii_lowercase+'_'+string.digits:
                print('Warning: column name with special characters detected!\t'+key)
    return _key_list

def write_dicts_to_db(input_dicts, tbl_name, tbl_fields=None, db_con = None, if_exists = 'fail'):
    if len(input_dicts)==0:
        print('No input dicts detected. No changes were made.')
        return None
    assert if_exists in ('fail','replace'), 'if_exists must be \'fail\' or \'replace\'!'
    if tbl_fields is None:
        assert isinstance(input_dicts, list), 'input_dicts must be a list of dicts when tbl_fields is unspecified!'
        __tbl_fields = get_all_dict_fields(input_dicts = input_dicts)
    else:
        assert isinstance(tbl_fields, (str, tuple, list)), 'tbl_fields must be tuple, list, or ; delimited str!'
        if isinstance(tbl_fields, str):
            __tbl_fields = tbl_fields.split(';')
        else:
            __tbl_fields = tbl_fields
    if db_con is None:
        __con = sqlite3_dict_connect()
    else:
        __con = db_con
    if if_exists == 'replace':
        cur = __con.cursor()
        drop_tbl_sql = f'drop table if exists "{tbl_name}";'
        cur.execute(drop_tbl_sql)
        __con.commit()
        cur.close()
    cur = __con.cursor()
    create_tbl_statement = f'create table "{tbl_name}" ('+','.join((f'"{x}"' for x in __tbl_fields))+');'
    insert_tbl_statement = f'insert into "{tbl_name}" values ('+','.join(('?' for x in __tbl_fields))+');'
    cur.execute(create_tbl_statement)
    def results_tuples():
        for d in input_dicts:
            #print(d)
            yield tuple(d.get(x, None) for x in __tbl_fields)
    __results_tuples = results_tuples()
    cur.executemany(insert_tbl_statement, __results_tuples)
    __con.commit()
    if db_con is None:
        __con.close()

def write_dicts_to_csv(input_dicts, name, filedir = log_dir_path, tbl_fields=None):
    ''' Write a csv from a iterable of dicts
        - If tbl fields is not specified, the input must be a list or tuple of dicts
    '''
    assert isinstance(filedir, str) or isinstance(filedir, Path), 'filedir must be a str or a Path!'
    assert isinstance(name, str), 'name must be a str!'
    __name = name if name.endswith('.csv') else name+'.csv'
    filepath = filedir/__name if isinstance(filedir, Path) else Path(filedir)/__name
    if tbl_fields is None:
        assert isinstance(input_dicts, (list, tuple)), 'input_dicts must be a list or tuple!'
        __tbl_fields = get_all_dict_fields(input_dicts)
    else:
        __tbl_fields = tbl_fields.split(';')
    with open(filepath, 'w', newline='', encoding='utf-8') as ff:
        dw = csv.DictWriter(ff, fieldnames = __tbl_fields, quoting=csv.QUOTE_NONNUMERIC)
        dw.writeheader()
        for d in input_dicts:
            dw.writerow({field:d.get(field, None) for field in __tbl_fields})
    return filepath

def remove_nonalnum(input_str):
    return ''.join(x for x in input_str if x.lower() in string.ascii_lowercase+string.digits+'_')


def create_temp_copy(original_file_path, new_file_name = None):
    '''
    Purpose: create copy of original_file_path in the temp_dir_path folder
    '''
    assert isinstance(original_file_path, (str, Path)), 'input must be Path or str!'
    assert (new_file_name is None) or isinstance(new_file_name, str), 'new_file_name must be a str!'
    # cast original_file_path as Path object
    if isinstance(original_file_path, str):
        __original_file_path = Path(original_file_path)
    else:
        __original_file_path = original_file_path
    if new_file_name is None:
        new_file_name = __original_file_path.name
    temp_file_path = temp_dir_path/new_file_name
    shutil.copy2(original_file_path, temp_file_path)
    return temp_file_path

def makeZipArchive(input_absolute_paths):
    # given input path as Path object or str, return 
    assert isinstance(input_absolute_paths, (str, Path)), 'expecting str or Path!'
        
    # convert to Path object if input is a str
    __path = Path(input_absolute_paths) if isinstance(input_absolute_paths, str) else input_absolute_paths
        
    # zip the input file and write the zip file in memory
    mem_zip = io.BytesIO()
    mem_zip.name = str(uuid.uuid4()).replace('-','').lower()+'.zip'
    arcname = __path.name
    with zipfile.ZipFile(mem_zip, mode = 'w', compression = zipfile.ZIP_DEFLATED) as zf:
        zf.write(__path, arcname = arcname)
        
    # read the zip file and encode into base64 str
    # return the result as dict in web services format
    # the base64 encoded str starts from index 2, ends 1 char before the end
    mem_zip.seek(0)
    filestringb64 = str(base64.b64encode(mem_zip.read()))[2:-1]
    zipped_file_size = mem_zip.tell()
    mem_zip.close()
    attachment = {'zipped_file_name':mem_zip.name
                , 'zipped_file_size':str(zipped_file_size)
                ,'zipped_file_content':filestringb64}
    return attachment


def get_temp_filedir(filedir, temp_dir = download_default_path):
    '''
    Check if the input filedir is None.
    If the input is None, return temp dir
    otherwise return the input filedir
    '''
    assert isinstance(temp_dir, (str, Path)), 'temp_dir must be str or Path!'
    if filedir is not None:
        assert isinstance(filedir, (str, Path)), 'filedir must be str or Path!'
        # return as a Path object
        if isinstance(filedir, str):
            return Path(filedir)
        return filedir
    return temp_dir


