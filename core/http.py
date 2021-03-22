import sys
import requests
from core.matchers import Matchers
from core.utils import extract_headers


class HTTPRequests:

    def __init__(self, Url=None, Path=[], Raw=[], ID=None, Name=None, AttackType=None,
                 Method='Get', Body=None, Payload=None, Headers={}, RaceNumberRequests=None,
                 MaxRedirects=None, AllowRedirects=None, threads=None,
                 MatchersCondition='or', Matchers=[], Extractors=None):

        self.Url = Url
        self.Path = Path  # string or list
        self.Method = Method
        self.Allow_redirects = AllowRedirects
        self.MaxRedirects = MaxRedirects
        self.Headers = Headers  # dict
        self.Body = Body  # for post
        self.Raw = Raw  # default none or burp header
        self.MatchersCondition = MatchersCondition
        self.Matchers = Matchers
        self.Extractors = Extractors
        # self.ID = ID
        # self.Name = Name
        self.AttackType = AttackType
        self.Payload = Payload  # list
        self.RaceNumberRequests = RaceNumberRequests
        self.threads = threads

    def feed(self, yaml_data_requests, ID):
        # print(yaml_data_requests)
        self.Path = yaml_data_requests.get('path', [])
        self.Method = yaml_data_requests.get('method', 'Get')
        self.Allow_redirects = yaml_data_requests.get('allow-redirects', False)
        self.MaxRedirects = yaml_data_requests.get('max-redirects')
        self.Headers = yaml_data_requests.get('headers', {})
        self.Body = yaml_data_requests.get('body')
        self.Raw = yaml_data_requests.get('raw', [])
        # self.AttackType = yaml_data_requests.get('body')
        self.Payload = yaml_data_requests.get('payloads')  # list
        self.AttackType = yaml_data_requests.get('attack')

        self.MatchersCondition = yaml_data_requests.get(
            'matchers-condition', 'or')
        yaml_data_requests_matchers = yaml_data_requests.get('matchers', [])
        # print(yaml_data_requests_matchers)
        self.Matchers = []

        for itr in range(len(yaml_data_requests_matchers)):
            matcher = Matchers()
            matcher.feed(yaml_data_requests_matchers[itr])
            self.Matchers.append(matcher)

        self.Extractors = yaml_data_requests.get('extractors', None)

        # print("hello")
        # print(self.Matchers)

        if self.Payload != None:
            print(f"{ID}: payload feature currently not supported")
            return True
            # sys.exit(0)

        if self.AttackType != None:
            print(f"{ID}: Attacktype feature currently not supported")
            return True
            # sys.exit(0)

        if self.Extractors != None:
            print(f"{ID}: Extractors feature currently not supported")
            return True
            # sys.exit(0)

    def handle_raw(self, raw_data):

        self.Body = None
        self.Headers = {}

        # print(raw_data)
        if '{{BaseURL}}' in raw_data:
            raw_data = raw_data.replace('{{BaseURL}}', self.Url)
        if '{{Hostname}}' in raw_data:
            raw_data = raw_data.replace('{{Hostname}}', self.Url)

        if '\n\n' in raw_data:
            raw_data = raw_data.replace('\n\n', 'Below-is-response-body', 1)
            raw_data, self.Body = raw_data.split('Below-is-response-body')

        if '\n' in raw_data:
            raw_data = raw_data.replace('\n', 'Below-is-headers', 1)
            raw_data, self.Headers = raw_data.split('Below-is-headers')
            self.Headers = extract_headers((self.Headers))

        raw_data = raw_data.split(' ')
        self.Method = raw_data[0]
        self.Path = [self.Url + raw_data[1]]

        # if self.Method.upper() == 'POST':  # for debug
        #     print(self.Body)

    def prepare_and_send_request(self):
        session = requests.Session()
        for every_path in self.Path:
            if '{{BaseURL}}' in every_path:
                every_path = every_path.replace('{{BaseURL}}', self.Url)
                #print(every_path, url)
            # print(self.Headers)
            try:
                req = requests.Request(method=self.Method, url=every_path, headers=self.Headers,
                                       data=self.Body)

                send_request = session.prepare_request(req)

                resp = session.send(send_request)

            except UnicodeDecodeError:
                resp = None

            return resp
            # print(resp.text) #for debug
            # print("divyansh coded")
            # print(resp.request.headers)
            # print(resp.headers)

    def get_result(self, url):

        self.Url = url

        if len(self.Path) == 0 and self.Raw == None:
            print("Template requests is empty")
        if len(self.Raw):
            for raw in self.Raw:
                self.handle_raw(raw)
                resp = self.prepare_and_send_request()
        else:
            resp = self.prepare_and_send_request()

        if resp == None:
            print("some request Error")
            return False

        last_result = None
        for matcher in self.Matchers:
            # print(matcher.TypeList) #for debug
            result = matcher.get_match(resp)

            if last_result == None:
                last_result = result

            if self.MatchersCondition == 'or':
                last_result |= result

            else:
                last_result &= result

            # print(last_result)
            if (self.MatchersCondition == 'or' and last_result) or (self.MatchersCondition == 'and' and not last_result):
                return last_result

        return last_result

    def match_response(self):
        pass
