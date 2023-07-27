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

class Shell:
	def __init__(self, env, session = None, log_enable = True):
		self.session_v1 = urestv1(env = env, log_enable = log_enable)
		self.session_object = session if session else requests.Session()
		self.cache = None
	def _get_shell(self, shell_type = None, verbose = True):
		endpoint = '/admin/shell'
		if shell_type is not None:
			# body = urlencode({'filter':kwargs})
			body = {'filter':{'shell_type':shell_type}}
			params = urlencode({'options':body})
		else:
			params = None
		# pprint(body)
		return self.session_v1.get(endpoint = endpoint, params = params, session = self.session_object, verbose = verbose)
				
	def _get_project_shell_list(self, options = None, status = None, shell_type = None, filter_condition = None, verbose = True):
		endpoint = f'/admin/projectshell'
		d = {}
		if options is not None:
			d['options'] = options
		if status is not None:
			assert status in ('Active','Inactive','On-Hold','View-Only'), "status must be in ('Active','Inactive','On-Hold','View-Only')!"
			d['status'] = status
		if shell_type is not None:
			d['type'] = shell_type
		if filter_condition is not None:
			d['filter_condition'] = filter_condition
		if len(d) > 0:
			body = urlencode(d)
		else:
			body = None
		return self.session_v1.get(endpoint = endpoint, params = body, session = self.session_object, verbose = verbose)
				
	def _get_bps(self, project_number, verbose = True):
		endpoint = '/admin/bps' if project_number is None else f'/admin/bps/{project_number}'
		return self.session_v1.get(endpoint = endpoint, session = self.session_object, verbose = verbose)
			
	def _update_shell(self, options, data, verbose = True):
		endpoint = '/admin/shell'
		if not isinstance(data, list):
			_data = [data]
		else:
			_data = data
		__data = {'options':options, 'data':_data}
		return self.session_v1.put(endpoint = endpoint, data = __data, session = self.session_object, verbose = verbose)
			
	def update_cpp(self, cppnumbersysshellnum,  **kwargs):
		options = {'shelltype':'CPPs'}
		data = [{'cppnumbersysshellnum':cppnumbersysshellnum, **kwargs}]
		return self._update_shell(options = options, data = data)
			
	def update_cpp_name(self, cppnumbersysshellnum, cppnamesysshellname):
		return self.update_cpp(cppnumbersysshellnum, cppnamesysshellname = cppnamesysshellname)
		
	def __getitem__(self, project_number):
		r = self._get_project_shell_list(verbose = False)
		r2 = self._get_shell(verbose = False)
		__r = [d for d in r['data'] if d.get('projectnumber','') == project_number]
		__r2 = [d for d in r2['data'] if d.get('cppnumbersysshellnum','') == project_number]
		if len(__r) > 0:
			pprint(__r)
			pprint(__r2)
		else:
			print('project_number not found!')
				
	def get_store(self,table_name = None, if_exists = get_store_if_exists_default):
		r = self._get_shell()
		data = r['data']
		if table_name is None:
			ts = timestamp_ymd()
			tbl_name =throwaway_prefix+ts+'shell'+gen_random_string(k=7)
		else:
			tbl_name = table_name
		write_dicts_to_db(input_dicts = data, tbl_name = tbl_name, if_exists = if_exists)
		print('Wrote to: '+tbl_name)
		
	def s_update_cpp(self, sql, db_con = None, return_responses = False):
		if db_con is None:
			con = sqlite3_dict_connect()
		else:
			con = db_con
		cur = con.cursor()
		cur.execute(sql)
		responses = []
		for query_result in cur:
			r = self.update_cpp(**query_result)
			responses.append(r)
		if db_con is None:
			con.close()
		if return_responses is True:
			return responses
	def add_partner_company(self, project_number, partner_shortname, verbose = True):
		endpoint = '/admin/company/shell/member/add'
		__data = {'shortname':partner_shortname, 'shellnumber': project_number}
		return self.session_v1.put(endpoint = endpoint, data = __data, session = self.session_object, verbose = verbose)
	def remove_partner_company(self, project_number, partner_shortname, verbose = True):
		endpoint = '/admin/company/shell/member/remove'
		__data = {'shortname':partner_shortname, 'shellnumber': project_number}
		return self.session_v1.put(endpoint = endpoint, data = __data, session = self.session_object, verbose = verbose)
