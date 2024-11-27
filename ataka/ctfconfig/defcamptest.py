import requests
from ataka.common.flag_status import FlagStatus


FLAG_SUBMIT_HOST = 'http://10.10.4.74:5000/submit'
CYBEREDU_SESSION = 'some_secret'

# URL to ataka-api-1 service, 0.0.0.0:8000->8000/tcp
ATAKA_HOST = '10.10.4.74:8000'

# NOP team
RUNLOCAL_TARGETS = [
    '10.11.19.2',
    '10.11.19.3',
    '10.11.19.4',
]

# our IP
STATIC_EXCLUSIONS = {
    '10.11.14.2',
    '10.11.14.3',
    '10.11.14.4',
}

ROUND_TIME = 120

FLAG_REGEX = r'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9\.eyJjb250ZXN0X2lkIjo[a-zA-Z0-9-_]+?\.[a-zA-Z0-9-_]+', 0
FLAG_BATCHSIZE = 200
FLAG_RATELIMIT = 1

START_TIME = 1732581990


def get_targets():
    services = ['test_service']
    
    targets = {
        'test_service': [
            {
                "ip": '127.0.0.1',
                "extra": '["5000"]',   
            }
        ]
    }
    
    return targets


def submit_flags(flags):
    flag_cache = {}
    for f in flags:
        flag_cache[f] = FlagStatus.OK

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Cookie': 'cyberedu_session=' + CYBEREDU_SESSION + ';'
    }
    
    payload = {'flags': flags}

    res = requests.post(FLAG_SUBMIT_HOST, headers=headers, json=payload)
    if not res.ok:
        print('Flag submission failed, status=' + f'{res.status_code}' + 'body=' + res.text)
        return []

    # {"flag": "msg"}
    ans = res.json()
    if not ans:
        print('Flag submission empty body?? Return code: ' + f'{res.status_code}')
        return []

    for flag, msg in ans.items():
        if 'Game is not running / Contest is over' in msg:
            flag_cache[flag] = FlagStatus.CONTEST_OVER
        elif 'Submission not approved' in msg:
            flag_cache[flag] = FlagStatus.SUBMISSION_NOT_APPROVED
        elif 'Membership not approved' in msg:
            flag_cache[flag] = FlagStatus.MEMBERSHIP_NOT_APPROVED
        elif 'Break time' in msg:
            flag_cache[flag] = FlagStatus.BREAK_TIME
        elif 'Invalid flag format' in msg:
            flag_cache[flag] = FlagStatus.INVALID_FORMAT
        elif 'Flag not found for this contest.' in msg:
            flag_cache[flag] = FlagStatus.FLAG_NOT_FOUND
        elif 'You cannot submit your own flag.' in msg:
            flag_cache[flag] = FlagStatus.OWN_FLAG
        elif 'Flag is from the future.' in msg:
            flag_cache[flag] = FlagStatus.FLAG_FROM_FUTURE
        elif 'Flag is too old' in msg:
            flag_cache[flag] = FlagStatus.FLAG_TOO_OLD
        elif 'Flag already submitted.' in msg:
            flag_cache[flag] = FlagStatus.FLAG_ALREADY_SUBMITTED
        elif 'You are not allowed to submit flags from NOP teams' in msg:
            flag_cache[flag] = FlagStatus.NOP_TEAM
        elif 'Generic error' in msg:
            flag_cache[flag] = FlagStatus.GENERIC_ERROR
        else:
            flag_cache[flag] = FlagStatus.GENERIC_ERROR
            print('Unknown error: ' + msg)

    return [v for _, v in flag_cache.items()]
