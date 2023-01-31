# -*- coding: UTF-8 -*-
import os
import sys
import shutil
import stat
import json
import urllib.request
import tarfile
import zipfile

script_dir = os.path.split(os.path.realpath(__file__))[0]
operator = None
res_name = None
res_version = None
list_type = 'all'
resource_json = []
relative_cache_dir = '.cache'
absolute_cache_dir = f'{script_dir}{os.sep}{relative_cache_dir}'
library = 'arsiachou'


def usage():
    print('python build.py [operator] [parameters...]\n')
    print('Usage:')
    print('    build <name> <version>    Build docker image.')
    print('    list <type>               List supported resources.')
    print('    help                      Print help message.')
    sys.exit(0)


def init_args():
    global operator, res_name, res_version, list_type
    arguments = sys.argv[1:]
    length = len(arguments)

    if 0 == length or 'help' == arguments[0]:
        usage()
    elif 'build' == arguments[0]:
        operator = 'build'
        if 3 != length:
            print("error: 'build' need arguments 'name' and 'version'.\n")
            usage()
        res_name = arguments[1]
        res_version = arguments[2]
    elif 'list' == arguments[0]:
        operator = 'list'
        if 2 == length:
            list_type = arguments[1]
            if 'all' != list_type and 'jdk' != list_type and 'jre' != list_type:
                print("error: Only support all/jdk/jre")
                sys.exit(0)
        elif 2 < length:
            print('error: Only one parameter is required.\n')
            sys.exit(0)
    else:
        print("error: Operation", arguments[0], "not support.")
        sys.exit(0)


def init_resource():
    global resource_json
    with open(f'{script_dir}{os.sep}resource.json', 'r', encoding='utf-8') as f:
        resource_json = json.load(f)


def decompress(file_path: str, extract_path: str):
    if file_path.endswith('.tar.gz') or file_path.endswith('.tar.xz'):
        tar = tarfile.open(file_path)
        tar.extractall(extract_path)
    elif file_path.endswith('.zip'):
        fz = zipfile.ZipFile(file_path, 'r')
        for file in fz.namelist():
            fz.extract(file, extract_path)


def rm(file_path):
    while 1:
        if not os.path.exists(file_path):
            break

        try:
            shutil.rmtree(file_path)
        except PermissionError as e:
            err_file_path = str(e).split("\'", 2)[1]
            if os.path.exists(err_file_path):
                os.chmod(err_file_path, stat.S_IWUSR)


def operation_list(ltype):
    res_list = [i for i in resource_json if 'all' == ltype or i['type'] == ltype]
    for item in res_list:
        print(item['name'], item['version'])


def operation_build(name, version):
    target = None
    for item in resource_json:
        if item['name'] == name and item['version'] == version:
            target = item

    if target is None:
        print(f"error: {name}:{version} not exist.")
        sys.exit(1)

    # check cache dir
    if not os.path.exists(absolute_cache_dir):
        os.makedirs(absolute_cache_dir)

    # download file
    filename = target['filename']
    file_location = f'{absolute_cache_dir}{os.sep}{filename}'
    if not os.path.exists(file_location):
        url = target['url']
        if url is None or url == '':
            print('error: Download URL not set.')
            sys.exit(1)

        print(f'Downloading from {url}')

        def download_callback(a, b, c):
            per = 100.0 * a * b / c
            if per > 100:
                per = 100
            print(f'\r{filename} %.2f%%' % per, end='')

        urllib.request.urlretrieve(url, file_location, download_callback)

    # decompress
    extract_root = target['extractRoot']
    if extract_root is None or extract_root == '':
        extract_target = f'{absolute_cache_dir}{os.sep}{name}_{version}'
        docker_package = f'{relative_cache_dir}/{name}_{version}'
    else:
        extract_target = absolute_cache_dir
        extract_dir = f'{extract_target}{os.sep}{extract_root}'
        docker_package = f'{relative_cache_dir}/{extract_root}'
        if os.path.exists(extract_dir):
            print('Remove', extract_dir)
            rm(extract_dir)

    print(f'\rExtract to {extract_target}')
    decompress(file_location, extract_target)

    # build
    build_cmd = "docker build -q " \
                f"-t {library}/{name}:{version}-alpine " \
                f"--build-arg Package={docker_package} " \
                f"--build-arg FolderName={name} {script_dir}"

    print(f'Building {name}:{version}...')
    os.system(build_cmd)


if __name__ == "__main__":
    init_args()
    init_resource()

    if 'list' == operator:
        operation_list(list_type)
    elif 'build' == operator:
        operation_build(res_name, res_version)
