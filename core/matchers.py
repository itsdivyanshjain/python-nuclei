import re


class Matchers:
    def __init__(self, Type=None, TypeList=[], Condition='or', Part=None):
        self.Type = Type
        self.TypeList = TypeList

        self.Condition = Condition
        self.Part = Part

    def feed(self, yaml_data_requests_matchers):
        # print(yaml_data_requests_matchers) #for debug
        self.Type = yaml_data_requests_matchers.get('type', 'word')
        if self.Type == 'word':
            self.TypeList = yaml_data_requests_matchers.get('words')
        elif self.Type == 'status':
            self.TypeList = yaml_data_requests_matchers.get('status')
        elif self.Type == 'regex':
            self.TypeList = yaml_data_requests_matchers.get('regex')
        elif self.Type == 'dsl':
            self.TypeList = yaml_data_requests_matchers.get('dsl')
        elif self.Type == 'binary':
            self.TypeList = yaml_data_requests_matchers.get('binary')
        elif self.Type == 'size':
            self.TypeList = yaml_data_requests_matchers.get('size')
        else:
            print(f"{self.Type} type is not supported")
        self.Condition = yaml_data_requests_matchers.get('condition', 'or')
        self.Part = yaml_data_requests_matchers.get('part', 'all')

        # print(self.TypeList)

    def get_match(self, response):
        # print(self.TypeList) #for debug
        last_match = None
        #match = False
        if len(self.TypeList) == 0:
            return False

        for element in self.TypeList:
            if self.Type == 'status':
                if response.status_code == int(element):
                    match = True
                else:
                    match = False
            elif self.Type == 'regex':
                try:
                    if self.Part == 'all':
                        match_item = re.findall(
                            element, str(response.text)) + re.findall(element, str(response.headers))
                        if len(match_item) == 0:
                            match = False
                        else:
                            match = True
                    elif self.Part == 'headers':
                        match_item = re.findall(element, str(response.headers))
                        if len(match_item) == 0:
                            match = False
                        else:
                            match = True
                    elif self.Part == 'body':
                        # print(str(element))
                        match_item = re.findall(element, str(response.text))
                        if len(match_item) == 0:
                            match = False
                        else:
                            match = True
                    else:
                        match = False
                except re.error:
                    print("some regex error")
            elif self.Type == 'word':
                if self.Part == 'all':
                    if element in str(response.headers) and element in str(response.text):
                        match = True
                    else:
                        match = False
                elif self.Part == 'header':
                    if element in str(response.headers):
                        match = True
                    else:
                        match = False
                elif self.Part == 'body':
                    if element in str(response.text):
                        match = True
                    else:
                        match = False

            elif self.Type == 'dsl' or self.Type == 'binary' or self.Type == 'size':
                match = False
                print(f"{self.Type} type feature currently not available")
            if last_match == None:
                last_match = match

            if self.Condition == 'or':
                last_match |= match

            else:
                # print("not here")
                last_match &= match

            # print(last_match, match)

            if (self.Condition == 'or' and last_match) or (self.Condition == 'and' and not last_match):
                return last_match

        return last_match
