from flask import request
import datetime
from common.logger import service_logger
from common.dbc import select_cur
from common.dbc import get_db_connect
logger = service_logger('dummy-manager')

def healthcheck():
    try:
        # request data
        logger.info("Running - request/data")
        request_headers = request.headers
        print(request_headers)
        target_host = request_headers.get('Host')
        user_agent = request_headers.get('User-Agent')
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _data_request = {
            'service_path': 'service_path_tbd',
            'current_time': current_time,
            'user_agent': user_agent,
            'target_host': target_host
        }
        # version data
        logger.info("Running - version/data")
        with open('versionFile', 'r') as f:
            _line = f.readline()
            _v = _line.strip()
            v=_v.split('::')
            f.close()
            _data_version = {
                'rc': 200,
                'service_name': v[0],
                'service_version': v[1],
                'service_version_sha': v[2]
            }
        # jdbc data
        logger.info("Running - jdbc/data")
        sql_string = 'select version()'
        try:
            db_connect = get_db_connect()
            jdbc_result = select_cur(sql_string, db_connect)
            _data_jdbc = {
                'jdbc_rc': 200,
                'jdbc_result': jdbc_result
            }
        except Exception as e:
            _data_jdbc = {
                'jdbc_rc': 500,
                'jdbc_result': str(e)
            }
        # merge data
        logger.info("Running - total/data")
        _data = {**_data_request, **_data_version, **_data_jdbc}
        logger.info(_data)
        return _data
    except Exception as e:
        return {
            'rc': 500,
            'error': str(e)
            }