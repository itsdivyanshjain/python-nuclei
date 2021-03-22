import sys
from .http import HTTPRequests


class Templates():

    # similar to pkg/templates/templates.go
    def __init__(self, ID=None, Info=None, RequestsHTTP=None):  # , RequestsDNS,
        # RequestsFile, RequestsNetwork, Totalrequests):
        self.ID = ID  # basic string
        self.Info = Info  # list or can be #dict
        self.RequestsHTTP = RequestsHTTP  # dict
        #self.RequestsDNS = RequestsDNS
        #self.RequestsFile = RequestsFile
        #self.RequestsNetwork = RequestsNetwork
        #self.Totalrequests = Totalrequests
        #self.Matchers = Matchers

    def feed(self, yaml_data):
        # thinking to create new file then bind to this function
        # print(yaml_data) #for debug

        self.ID = yaml_data.get('id')
        # print(self.ID)
        self.Info = yaml_data.get('info')
        self.Severity = self.Info.get('severity', 'unknown')
        if yaml_data.get('headless'):
            print(f'{self.ID} headless feature is not supported.')
            return True
            # sys.exit(0)
        self.RequestsHTTP = HTTPRequests()
        return self.RequestsHTTP.feed(yaml_data.get('requests')[0], self.ID)
