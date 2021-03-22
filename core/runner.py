import os

#from core.process import processTemplate
from core.banner import showbanner
from core.fetch_templates import get_template_path, parse_template_file


class Runner:

    def __init__(self, url, template_subpath):
        self.url = url
        self.template_subpath = template_subpath

    def new(self):

        # same class object runner
        # check for headless options
        # run engine.new
        # reading nuclei ignore file
        pass

    def close(self):
        pass

    def runenum(self):

        showbanner()
        #site = "https://teenagerstartups.com"

        template_path = get_template_path()
        #template_subpath = 'exposed-panels/django-admin-panel.yaml'

        available_template = parse_template_file(
            template_path, self.template_subpath)  # return list of template object

        # print(available_template[0].ID)
        total = 0
        for template in available_template:
            print(template.ID)
            # print(total)
            # template.ID
            result = template.RequestsHTTP.get_result(self.url)
            if result:
                print(
                    f"Site: {self.url} vulnerable to template {template.ID} having {template.Severity} severity")
            total += 1
        print(total)
        '''
            update template

            check for inclusive template and exculded templates
            clustered repetetive module
            
            less priority
        '''

        # final_result = 0

        # for template in available_template:

        #     result = processTemplate(url, template)

        #     final_result += result

        #     # check len of template option if equal to 0 then append template Dir
        #     # if new templates available then add above
        #     # get included template(all or mention)
        #     # get excluded template(all - mention)
        #     # set default alltemplate as included
        #     # if exclude template len > 0 then remove from all

        #     # set workflowpath (template path)
        #     # filter templated based on severity
        #     # load template
        #     # set available workflow
        #     # load workflow

        # if final_result == 0:
        #     print('better luck next time')

        # pass
