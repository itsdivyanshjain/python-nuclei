import os
import requests
import shutil
from zipfile import ZipFile
import yaml
#from core.http import Request
from core.templates import Templates


def update_templates():
    print('updating nuclei-templates feature currently not supported')


def download_templates():
    # fetch template in home dir and return Path
    # for debug only later change it
    link = 'https://codeload.github.com/projectdiscovery/nuclei-templates/zip/refs/heads/master'

    resp = requests.get(link)

    home = os.getenv("HOME")

    nuclei_template_path = os.path.join(home, 'nuclei-templates.zip')

    with open(nuclei_template_path, 'wb') as f:
        f.write(resp.content)

    with ZipFile(nuclei_template_path, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()
        zip.extractall(home)

        # extracting all the files
        print('Extracting all the files now...')
        # zip.extractall()
        print('Done!')

    extracted_template_path = os.path.join(home, 'nuclei-templates-master')
    main_path = os.path.join(home, 'nuclei-templates')

    print("downloaded nuclei-templates and extracted")
    if os.path.exists(extracted_template_path):
        shutil.move(extracted_template_path, main_path)
        return path


def get_template_path(explicit=False):

    if explicit:
        home = explicit_template_path
    else:
        home = os.getenv("HOME")
    nuclei = 'nuclei-templates'

    path = os.path.join(home, nuclei)
    if os.path.isdir(path):
        update_templates()
        return path
    else:
        return download_templates()


def list_template_file(path, subpath, files=[]):
    # path is template directory and subpath is module or selecting multiple folder and file
    basepath = os.path.join(path, subpath)
    if os.path.isdir(basepath):
        dirs = os.listdir(basepath)
        # print(dirs)
        for items in dirs:
            if os.path.isdir(os.path.join(basepath, items)):
                list_template_file(basepath, items, files)
            else:
                files += [basepath + '/' + items]
    return files


def parse_template_file(path, subpath):

    template_object_list = []

    template_list = []
    # if mention any directory
    if os.path.isdir(os.path.join(path, subpath)):
        template_list = list_template_file(path, subpath)
    # if mention only yaml file
    else:
        template_list = [os.path.join(path, subpath)]
    # print(template_list) #for debug

    if len(template_list) != 0:
        for template in template_list:
            with open(template, 'r') as file:
                data = file.read()
            yaml_data = yaml.safe_load(data)
            template_object = Templates()
            error = template_object.feed(yaml_data)
            if error:
                continue
            template_object_list.append(template_object)

    else:
        print('some template issue')

    return template_object_list


def get_parsed_templates():
    pass
# less priority but do checksum
