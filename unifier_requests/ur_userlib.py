from unifier_requests.ur import urestv1
from unifier_requests.ur import write_dicts_to_db
from unifier_requests.udrlib import udr
from pprint import pprint
from pprint import pformat
from concurrent.futures import ThreadPoolExecutor
from unifier_requests.shelllib import Shell
import requests

shell_groups_report = 'Shell Groups Report (Integration)'


class Groups:
    def __init__(self, env, project_number, session=None, log_enable=True): 
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.env = env
        self.session_object = session if session else requests.Session()
        self.project_number = project_number
        self.log_enable = log_enable
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.env}\',\'{self.project_number}\')'
    def __getitem__(self, group_name):
        return Group(self.env, self.project_number, group_name, self.session_object, self.log_enable)
    def __setitem__(*args):
        pass
            
    def add_partner_company(self, partner_shortname):
        __x = Shell(env = self.env, session = self.session_object)
        return __x.add_partner_company(project_number = self.project_number, partner_shortname = partner_shortname)
        
    def remove_partner_company(self, partner_shortname):
        __x = Shell(env = self.env, session = self.session_object)
        return __x.remove_partner_company(project_number = self.project_number, partner_shortname = partner_shortname)

class Group:
    endpoint = '/admin/user/shell/membership'
    def __init__(self, env, project_number, group_name, session=None, log_enable=True): 
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.env = env
        self.session_v1 = urestv1(env=env, log_enable=log_enable)
        self.session_object = session if session else requests.Session()
        self.project_number = project_number
        self.group_name = group_name
    def _add_sub_users(self, user, op):
        if op not in ('group_add','group_remove'):
            raise Exception("op not in ('group_add','group_remove')!")
        if isinstance(user, str):
            _users = [user]
        elif isinstance(user, list) or isinstance(user, tuple):
            _users = user
        else:
            raise TypeError('Expecting str, list, or tuple input!')
        put_body = {'shellnumber': self.project_number, 'users': [{'username': _user, op: self.group_name} for _user in _users]}
        return self.session_v1.put(endpoint = Group.endpoint, data = put_body, session = self.session_object)
    def __iadd__(self, user):
        self._add_sub_users(user = user, op = 'group_add')
        return
    
    def __isub__(self, user):
        self._add_sub_users(user = user, op = 'group_remove')
        return
                    
    def get(self, verbose = True):
        project_number_groupname = self.project_number+'_'+self.group_name
        __results = get_group_users(env = self.env, project_number_groupname = project_number_groupname, session = self.session_object)
        if verbose is True:
            pprint(__results)
        return __results
    def __repr__(self):
        __users = self.get(verbose = False)
        __users_str = '\r\n\t'
        for user in __users:
            __users_str = __users_str+'\r\n\t'+str(user)
        __return_str = f'env: {self.env}'+'\n'+f'project_number: {self.project_number}'+'\n'+f'group_name: {self.group_name}'+'\n'+f'users: {__users_str}'
        return __return_str
class Users:
    def __init__(self, env, project_number, session=None, log_enable=True):
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.env = env
        self.session_object = session if session else requests.Session()
        self.project_number = project_number
        self.log_enable = log_enable
    def _set_active_inactive(self, users, op):
        if op not in ('activate','deactivate'):
            raise Exception('op must be in (\'activate\',\'deactivate\')!')
        if isinstance(users, str):
            __users = users.split()
        else:
            __users = users
        if op == 'activate':
            return self[__users].activate()
        return self[__users].deactivate()
    def deactivate_users(self, users):
        '''Deactivate or activate a iterable of users
        examples:
        x = Users('stage','jctest21')
        x.deactivate_users(('user1','user2','user3')) # deactivates users given as a input tuple
        x.deactivate_users(['user1','user2','user3']) # deactivates users given as a input list
        x.deactivate_users('user1') # single user in a str
        x.deactivate_users('user1 user2 user3') # multiple users in a single str, separated by spaces
        '''
        return self._set_active_inactive(users=users, op='deactivate')
    def activate_users(self, users):
        return self._set_active_inactive(users=users, op='activate')
    def __getitem__(self, user):
        return User(env = self.env, project_number = self.project_number, user = user, session = self.session_object, log_enable = self.log_enable)
    def __setitem__(*args):
        pass    
    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.env}\',\'{self.project_number}\')'
            
    def add_partner_company(self, partner_shortname):
        __x = Shell(env = self.env, session = self.session_object)
        return __x.add_partner_company(project_number = self.project_number, partner_shortname = partner_shortname)
        
    def remove_partner_company(self, partner_shortname):
        __x = Shell(env = self.env, session = self.session_object)
        return __x.remove_partner_company(project_number = self.project_number, partner_shortname = partner_shortname)


class User:
    endpoint = '/admin/user/shell/membership'
    def __init__(self, env, project_number, user, session=None, log_enable=True): 
        if env not in ('stage','prod'):
            raise Exception('env must be in \'stage\' or \'prod\'!')
        self.env = env
        self.session_v1 = urestv1(env = env, log_enable = log_enable)
        self.session_object = session if session else requests.Session()
        self.project_number = project_number
        self.user = user
    def _add_sub_groups(self, group_name, op):
        '''add or subtract user from groups'''
        if op not in ('group_add', 'group_remove'):
            raise Exception("op not in ('group_add', 'group_remove')!")
        if isinstance(group_name, str):
            _group_names = [group_name]
        elif isinstance(group_name, list) or isinstance(group_name,tuple):
            _group_names = group_name
        else:
            raise TypeError('Expecting str, list, or tuple input of groups!')
        put_body = {'shellnumber': self.project_number, 'users': [{'username': self.user, op: _group_name} for _group_name in _group_names]}
        self.session_v1.put(endpoint = User.endpoint, data = put_body, session = self.session_object)
    def __iadd__(self, group_name):
        if isinstance(group_name,str):
            _group_name = (group_name,)
        else:
            _group_name = group_name
        self._add_sub_groups(group_name = _group_name, op='group_add')
        return
    def __isub__(self, group_name):
        if isinstance(group_name,str):
            _group_name = (group_name,)
        else: 
            _group_name = group_name
        self._add_sub_groups(group_name = _group_name, op='group_remove')
        return
    def _set_status(self, status):
        if status not in ('Active','Inactive'):
            raise Exception('status must be in (\'Active\',\'Inactive\')!')
        if isinstance(self.user, str):
            _user_names = [self.user]
        else:
            _user_names = self.user
        put_body = {'shellnumber': self.project_number, 'users': [{'username': _user_name, 'status': status} for _user_name in _user_names]}
        return self.session_v1.put(endpoint = User.endpoint, data = put_body, session = self.session_object)
    def activate(self):
        return self._set_status(status='Active')
    def deactivate(self):
        return self._set_status(status='Inactive')
    def get(self, verbose = True):
        project_number_username = self.project_number+'_'+self.user
        user_info_dict, user_groups = get_user_groups(env = self.env, project_number_username = project_number_username, session = self.session_object)
        if verbose is True:
            pprint(user_info_dict)
            group_str = '\r\n\t'+'\r\n\t'.join(user_groups)
            print(group_str)
        return user_groups
    def __repr__(self):
        project_number_username = self.project_number+'_'+self.user
        user_info_dict, groups = get_user_groups(env = self.env, project_number_username = project_number_username, session = self.session_object)
        group_str = '\r\n\t'+'\r\n\t'.join(groups)
        user_info_str = pformat(user_info_dict)
        return_str = f'''
env: {self.env}
project_number: {self.project_number}
user: {self.user}
{user_info_str}
groups: {group_str}
'''
        return return_str

def get_user_groups(env, project_number_username, session = None):
    __udr = udr(env = env, project_number = None, session = session)
    query = {'label':'_shell_groups / PROJECT_NUMBER_USERNAME', 'value1':project_number_username}
    __results = __udr.get_dicts(reportname = shell_groups_report, query = query)
    user_info_keys = ('fullname','shortname','companyname','email')
    user_info_dict = dict.fromkeys(user_info_keys, '')
    if len(__results)>0:
        info = __results[0]
        for key in user_info_keys:
            user_info_dict[key] = info[key]
    user_groups = [d['groupname'] for d in __results]
    return user_info_dict, user_groups


def get_group_users(env, project_number_groupname, session = None):
    __udr = udr(env = env, project_number = None, session = session)
    query = {'label':'_shell_groups / PROJECT_NUMBER_GROUPNAME', 'value1': project_number_groupname}
    __results = __udr.get_dicts(reportname = shell_groups_report, query = query)
    return [{'fullname':d['fullname'], 'username':d['username'], 'email':d['email']} for d in __results]


