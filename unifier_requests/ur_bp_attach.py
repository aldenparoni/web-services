from unifier_requests import bplib
from unifier_requests.ur import file_extensions
from unifier_requests.ur import write_dicts_to_csv
from unifier_requests.ur import log_dir_path
from unifier_requests.ur import gen_random_string
from unifier_requests.ur import get_all_dict_fields
from unifier_requests.ur import timestamp_ymd
from unifier_requests.ur import create_session_queue
from unifier_requests.ur import close_session_queue
from unifier_requests.ur import s_default_pkcols
from unifier_requests.ur import sqlite3_dict_connect
import uuid
from datetime import datetime
from requests import Session
from csv import DictWriter
from csv import DictReader
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

def bp_attach(env, bpid, project_number, record_no, file_path, title = None, issue_date = None, revision_no = None, timeout = 20, session = None):
    _bp = getattr(bplib, bpid)
    try:
        assert record_no is not None, 'record_no is blank!'
        assert len(record_no)>0, 'record_no is blank!'
        assert file_path is not None, 'file_path is blank!'
        assert bpid is not None, 'bpid is blank!'
        x = _bp(env = env, project_number = project_number, session = session)
        data = {'record_no':record_no}
        attachment_dict = {'file_path':file_path, 'title':title, 'issue_date':issue_date, 'revision_no': revision_no}
        return x.add_attachment_single_record_v1(data = data, input_attachments = attachment_dict, timeout = timeout)
    except Exception as e:
        session = Session()
        return {'data':[]
            ,'message':[{'_record_status':'Exception encountered! '+str(e), 'issue_date':issue_date, '_attachment':[], 'title':title}]
            ,'status':99999}


def attach_from_csv(env, csv_path, timeout = 20, return_results = False):
    responses = []
    session = Session()
    with open(csv_path, 'r') as ff:
        dr = DictReader(ff)
        for row in dr:
            bpid = row['bpid']
            project_number = row['project_number']
            record_no = row['record_no']
            file_path = row['file_path']
            title = row.get('title','')
            issue_date = row.get('issue_date','')
            r = bp_attach(env = env
                    , bpid = bpid
                    , project_number = project_number
                    , record_no = record_no
                    , file_path = file_path
                    , title = title
                    , issue_date = issue_date
                    , timeout = timeout
                    , session = session
                    )
            rr = dict()
            rm = r['message'][0]
            rr['bpid'] = bpid
            rr['project_number'] = project_number
            rr['record_no'] = record_no
            rr['file_path'] = file_path
            rr['title'] = title
            rr['issue_date'] = issue_date
            rr['_record_status'] = rm['_record_status']
            rr['status'] = r['status']
            responses.append(rr)    
    session.close()
    ts = timestamp_ymd()
    random_tag = gen_random_string()
    csv_name = 'bpattachfromcsv_'+env+'_'+ts+random_tag+'.csv'
    logfile_path = write_dicts_to_csv(input_dicts = responses, name = csv_name)
    print('Wrote results to: ')
    print(str(logfile_path))
    if return_results is True:
        return responses


def s_attach(env, sql_query, pool_size = 4, db_conn = None, return_results = False, timeout = 20, **kwargs):
    '''
    SQL query columns:
    required columns: bpid
                    , project_number
                    , record_no
                    , file_path
    optional columns: title
                    , issue_date
                    , revision_no
    '''
    session_queue = create_session_queue(size = pool_size) 
    if db_conn is None:
        __con = sqlite3_dict_connect()
    else:
        __con = db_conn
    cur = __con.cursor()
    sql_results = cur.execute(sql_query).fetchall()
    if db_conn is None:
        __con.close()
    N_RESULTS = len(sql_results)
    N_RESULTS_STR = str(N_RESULTS)
    required_cols = ['bpid', 'project_number', 'record_no', 'file_path']
    all_dict_fields = get_all_dict_fields(input_dicts = sql_results)
    for col in required_cols:
        assert col in all_dict_fields, f'required column is missing: {col}'
    # collect return parameter names, and store into return_dict_cols
    return_dict_cols = required_cols
    s_default_pkcols_list = s_default_pkcols.lower().split(';')
    for col in all_dict_fields:
        if (col not in required_cols) and (col.lower() in s_default_pkcols_list):
            return_dict_cols.append(col)
    def _s_attach_single_iter(input_tuple):
        '''
        input_tuple is the tuple: (idx, result_row)
        '''
        idx, row = input_tuple
        return_dict = dict.fromkeys(return_dict_cols)
        bpid, record_no, project_number, file_path = row['bpid'], row['record_no'], row['project_number'], row['file_path']
        title, issue_date, revision_no = row.get('title', None), row.get('issue_date', None), row.get('revision_no', None)
        for col in return_dict_cols:
            return_dict[col] = row[col]
        session = session_queue.get()
        try:
            r = bp_attach(env = env
                        , bpid = bpid
                        , project_number = project_number
                        , record_no = record_no
                        , file_path = file_path
                        , title = title
                        , issue_date = issue_date
                        , revision_no = revision_no
                        , session = session
                        , timeout = timeout)
            return_dict['_record_status'] = r['message'][0]['_record_status']
            return_dict['status'] = r['status']
            pct = round(idx/N_RESULTS, 2)
            print(f'Finished evaluating: {str(idx)} of {N_RESULTS_STR} ({str(pct)} pct)  {project_number}  {record_no}  {str(file_path)}')
        except Exception as e:
            return_dict['_record_status'] = f'Exception encountered!!! {str(e)}'
            return_dict['status'] = 9999
            session = Session()
        finally:
            session_queue.put(session)
            return return_dict
    with ThreadPoolExecutor(max_workers = pool_size) as ex:
        RESULTS = ex.map(_s_attach_single_iter, enumerate(sql_results, 1))
    RESULTS = list(RESULTS)
    ts = timestamp_ymd()
    logfile_name = f's_attach_{env}_{ts}_'+str(uuid.uuid4()).replace('-','').lower()+'.csv'
    __logfile_path = write_dicts_to_csv(input_dicts = RESULTS, name = logfile_name)
    print('Wrote results to: ')
    print(str(__logfile_path))
    close_session_queue(queue = session_queue)
    if return_results is True:
        return RESULTS


