from unifier_requests.ur import urestv1
from unifier_requests.ur import sqlite3_dict_connect
from unifier_requests.ur import gen_random_string
from unifier_requests.ur import timestamp_ymd
from unifier_requests.ur import throwaway_prefix
from unifier_requests.ur import write_dicts_to_db
from unifier_requests.ur import get_store_if_exists_default
import requests
from urllib.parse import urlencode
from pprint import pprint


class CBS:
    def __init__(self, env, project_number, session = None, log_enable = True):
        self.session_v1 = urestv1(env = env, log_enable = log_enable)
        self.session_object = session if session else requests.Session()
        self.project_number = project_number
        self.env = env
         
    def get_cbs_codes(self, data = None, verbose = True):
        # post
        # Example data:
        # {
        #"options":
        #{
        #"cost_type":"Capital",
        #"summary_detail":"true",
        #"status":"active"
        #"hierarchy":true
        #}
        #}
        if data is None:
            data = {'options':{'hierarchy':True}}
        project_number = self.project_number
        endpoint = f'/cost/cbs/list/{project_number}'
        params = urlencode({'project_num':project_number})
        return self.session_v1.post(endpoint = endpoint
                                    , data = data
                                    , params = params
                                    , session = self.session_object
                                    , verbose = verbose)
             
    def create_cbs_codes(self, data, verbose = True):
        # post
        ### example input data:
        ##{"data": [
        ##{"code": "CostB~~Cost1",
        ##"description": "Creating Cost Code using REST webservice",
        ##"item": " Cost Item",
        ##"uResProgressAmount": 10,
        ##"status": "Active",
        ##"cost_type": "Food"},
        ##{"code": "Cost1",
        ##"description": "Creating Cost Code using REST webservice",
        ##"item": "Cost1 Item",
        ##"uResProgressAmount": 10,
        ##"status": "Active",
        ##"cost_type": "Capital"
        ##}]}
        project_number = self.project_number
        endpoint = f'/cost/cbs/{project_number}'
        params = urlencode({'project_number':project_number})
        assert isinstance(data, (list,dict, str)), 'data must be list, dict, or str!'
        if isinstance(data, list):
            _data = {'data': data}
        elif isinstance(data, dict):
            # post data should have single key 'data'
            if len(data.keys()) > 1:
                _data = {'data':[data]}
        else:
            _data = data
        return self.session_v1.post(endpoint = endpoint
                                    , data = _data
                                    , params = params
                                    , session = self.session_object
                                    , verbose = verbose)
             
    def update_cbs_codes(self, data, key = None, verbose = True):
        # put
        project_number = self.project_number
        endpoint = f'/cost/cbs/{project_number}'
        _params = {'project_number':project_number}
        if key is not None:
            _params['options'] = {'key':key}
        params = urlencode(_params)
        ###Notes:
        ###    The complete path from parent to child CBS code (separated by delimiter '~~') should be given in code field of input request if code is chosen as value for key.
        ###    The "orderid" and "parentid" cannot be updated. All other cost attributes can be updated.
        ###    The value in the CBS code field can be updated when the value of key in options parameter is"'bitemid."
        ###    Partial Update is not allowed.
        ### example input data
        ###{"data": [{
        ###"bitemid": "26",
        ###"code": "CostX"
        ###"description": "Updating Cost Code using REST webservice",
        ###"status": "InActive"}]}
        assert isinstance(data, (list,dict, str)), 'data must be list, dict, or str!'
        if isinstance(data, list):
            _data = {'data': data}
        elif isinstance(data, dict):
            # put data should have single key 'data'
            if len(data.keys()) > 1:
                _data = {'data':[data]}
        else:
            _data = data
        return self.session_v1.put(endpoint = endpoint
                                    , data = data
                                    , params = params
                                    , session = self.session_object
                                    , verbose = verbose)
             
    def get_column_data(self, columnname, verbose = True):
        # get
        project_number = self.project_number
        params = urlencode({'columnname': columnname})
        endpoint = f'/cost/columndata/{project_number}'
        return self.session_v1.get(endpoint = endpoint
                                    , params = params
                                    , session = self.session_object
                                    , verbose = verbose)
            
    def update_column_data(self, columnname, data, verbose = True):
        # put
        project_number = self.project_number
        endpoint = f'/cost/columndata/{project_number}'
        params = urlencode({'columnname':columnname})
        assert isinstance(data, (list,dict, str)), 'data must be list, dict, or str!'
        if isinstance(data, list):
            _data = {'data': data}
        elif isinstance(data, dict):
            # put data should have single key 'data'
            if len(data.keys()) > 1:
                _data = {'data':[data]}
        else:
            _data = data
        return self.session_v1.put(endpoint = endpoint
                                    , data = data
                                    , params = params
                                    , session = self.session_object
                                    , verbose = verbose)
    def __repr__(self):
        return self.__class__.__name__+f'(\'{self.env}\', \'{self.project_number}\')'


