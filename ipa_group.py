from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

import requests
import json

IPA_PROT = "https"
IPA_HOST = "127.0.0.1"
IPA_USER = "admin"
IPA_PASS = "password"
IPA_PORT = "443"


class IPAClient:
    def __init__(self, host, port, username, password, protocol):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.protocol = protocol
        self.headers = {'referer': self.get_base_url(),
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'}
        self.cookies = None

    def get_base_url(self):
        return '{prot}://{host}/ipa'.format(prot=self.protocol, host=self.host)

    def get_json_url(self):
        return '{base_url}/session/json'.format(base_url=self.get_base_url())

    def login(self):
        s = requests.session()
        url = '{base_url}/session/login_password'.format(base_url=self.get_base_url())
        data = dict(user=self.username, password=self.password)
        headers = {'referer': self.get_base_url(),
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        try:
            s = requests.post(url=url, data=data, headers=headers, verify=False)
            s.raise_for_status()
        except Exception as e:
            self._fail('login', e)
        self.cookies = s.cookies

    def _fail(self, msg, e):
        if 'message' in e:
            err_string = e.get('message')
        else:
            err_string = e
        raise AnsibleError('{}: {}'.format(msg, err_string))

    def _post_json(self, method, name, item=None):
        if item is None:
            item = {}

        url = '{base_url}/session/json'.format(base_url=self.get_base_url())
        data = {'method': method, 'params': [[name], item]}
        try:
            r = requests.post(url=url, data=json.dumps(data), headers=self.headers, cookies=self.cookies, verify=False)
            r.raise_for_status()
        except Exception as e:
            self._fail('post {}'.format(method), e)

        resp = json.loads(r.content)
        err = resp.get('error')
        if err is not None:
            self._fail('repsonse {}'.format(method), err)

        if 'result' in resp:
            result = resp.get('result')
            if 'result' in result:
                result = result.get('result')
                if isinstance(result, list):
                    if len(result) > 0:
                        return result[0]
            return result
        return None

    def group_find(self, name):
        return self._post_json(method='group_find', name=None, item={'all': True, 'cn': name})


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwaargs):
        ipa_prot = kwaargs.get('ipa_prot', IPA_PROT)
        ipa_host = kwaargs.get('ipa_host', IPA_HOST)
        ipa_port = kwaargs.get('ipa_port', IPA_PORT)
        ipa_user = kwaargs.get('ipa_user', IPA_USER)
        ipa_pass = kwaargs.get('ipa_pass', IPA_PASS)

        client = IPAClient(host=ipa_host,
                           port=ipa_port,
                           username=ipa_user,
                           password=ipa_pass,
                           protocol=ipa_prot)

        client.login()
        return [client.group_find(name=terms[0])]
