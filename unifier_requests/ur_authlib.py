from unifier_requests.ur import cert_path
from unifier_requests.ur import proxies
import requests
from pathlib import Path
from base64 import b64encode
from datetime import datetime

'''
This library is for managing REST API tokens.
'''

username, password = '$$PIFTEST','test_password_abc'
def gen_token(env, username = username, password = password, session = None):
	'''generate a new token for a integration user'''
	assert env in ('stage','prod'), 'env must be \'stage\' or \'prod\'!'
	s = requests.Session() if session is None else session
	url = f'https://unifier.oraclecloud.com/hart/{env}/ws/rest/service/v1' if env=='stage' else 'https://unifier.oraclecloud.com/hart/ws/rest/service/v1'
	endpoint = '/login'
	__username, __password = username, password
	__basic_str = __username+':'+__password
	__basic_b64 = b64encode(__basic_str.encode()).decode('utf-8')
	headers = {'Authorization':'Basic '+__basic_b64}
	r = s.get( url + endpoint
			, verify = cert_path
			, proxies = proxies
			, headers = headers)
	if session is None:
		s.close()
	return r.json()

def is_token_valid(env, token, session = None):
	url = f'https://unifier.oraclecloud.com/hart/{env}/ws/rest/service/v1' if env=='stage' else 'https://unifier.oraclecloud.com/hart/ws/rest/service/v1'
	endpoint = '/admin/bps/'
	assert env in ('stage','prod'), 'env must be \'stage\' or \'prod\'!'
	s = requests.Session() if session is None else session
	auth_headers = {'Authorization': 'Bearer '+token}
	r = s.get(url+endpoint
		, verify = cert_path
		, proxies = proxies
		, headers = auth_headers)
	if session is None:
		s.close()
	if r.text == 'Unauthorized' and r.status_code == 401:
		return False
	return True

def evaluate_token_txt(env):
	pass
