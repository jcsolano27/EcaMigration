import os
import shutil
from zipfile import ZipFile
import re
import subprocess, sys

msapp_paths = ['', 'Components', 'Controls', 'References', 'Resources']

def get_zipfile():
    for file in os.listdir(f'Input/'):
        if file[-4:] == '.zip':
            return file


def unzip_app(file):

    path = file.split(".")[0]
    if path in os.listdir("Input"):
        shutil.rmtree(f'Input/{path}')
        print(f'Path: Input/{path} removed')

    with ZipFile(f'Input/{file}', 'r') as zObject:
        zObject.extractall(f"Input/{path}")
        print(f'Path: Input/{path} created')

def unzip_msapp(file):

    filename = (msapp_path.split("/")[-1:])[0][:-6]

    if 'msapp' in os.listdir("Input"):
        shutil.rmtree('Input/msapp')
        print(f'Path: Input/msapp removed')
    os.mkdir('Input/msapp')

    with ZipFile(file, 'r') as zObject:
        zObject.extractall(f'Input/msapp/{filename}')
        print(f'Path: Input/msapp created')

def extract_msapp(file):
    filename = (msapp_path.split("/")[-1:])[0]

    if 'msapp' in os.listdir("Input"):
        shutil.rmtree('Input/msapp')
        print(f'Path: Input/msapp removed')
    os.mkdir('Input/msapp')

    os.rename(file, f'Input/msapp/{filename}')
    print(f"File {file} moved into Input/msapp/{filename}")
    #os.system('extract.bat')

def compress_msapp(file):
    filename = (msapp_path.split("/")[-1:])[0]
    os.system('compress.bat')

    os.rename(f'Input/msapp/NewMSAPP/{filename}', file)
    print(f"FileInput/msapp/NewMSAPP/{filename} moved into {file}")

def getMsapp(project_name):
    app_folder = os.listdir(f'Input/{project_name}/Microsoft.PowerApps/apps/')[0]

    for file in os.listdir(f'Input/{project_name}/Microsoft.PowerApps/apps/{app_folder}'):
        if file[-6:] == '.msapp':
            return f'Input/{project_name}/Microsoft.PowerApps/apps/{app_folder}/{file}'

def zip_msapp(project_name, file_name):

    shutil.make_archive(f'Input/msapp/{file_name}', 'zip', f'Input/msapp/{file_name}')
    app_folder = os.listdir(f'Input/{project_name}/Microsoft.PowerApps/apps')[0]
    fullpath = f'Input/{project_name}/Microsoft.PowerApps/apps/{app_folder}/{file_name}.msapp'

    os.remove(fullpath)
    print(f"Removed: {fullpath}")

    os.rename(f'Input/msapp/{file_name}.zip', fullpath)
    print(f"Moved: Input/msapp/{file_name}.zip into {fullpath}")

def zip_app():
    shutil.make_archive(f'Output/ECAPortalProd', 'zip', f'Input/{path}')
    print(f'Zip file Output/{path} created.')

def replace_file(file_path, find, replace):

    with open(file_path, 'r') as file:
        data = file.read()
        data = data.replace(find, replace)

    with open(file_path, 'w') as file:
        file.write(data)
    print(f"Replaced {find} with {replace} on file {file_path}")

def msapp_replace(file_name, find, replace, exclude=[]):
    for mpath in msapp_paths:
        full_path = f'Input/msapp/{file_name}/{mpath}'
        for file in os.listdir(full_path):
            if file[-5:] == '.json' and file not in exclude:
                full_file_path = f'{full_path}/{file}'
                replace_file(full_file_path, find, replace)

def full_replace():
    with open('Values.csv', 'r') as v:
        for line in v.readlines()[1:]:
            parts = line.split(",")
            find = parts[1].strip()
            replace = parts[2].strip()
            # print(f'find: {find} - replace: {replace}')
            msapp_replace(msapp_file, find, replace)
            replace_file(f'Input/{path}/Microsoft.PowerApps/apps/{app_folder}/{app_folder}.json', find, replace)

def dynamic_replace():
    with open('DinamicSwitch.csv', 'r') as v:
        for line in v.readlines()[1:]:
            parts = line.split(",")
            find = parts[1].strip()
            replace = parts[2].strip()
            # print(f'find: {find} - replace: {replace}')
            msapp_replace(msapp_file, find, replace, exclude=['DataSources.json', 'Properties.json'])

def variable_replace():
    with open('mapping.csv', 'r') as v:
        for line in v.readlines()[1:]:
            parts = line.split(",")
            find = parts[1].strip()
            replace = parts[2].strip()
            # print(f'find: {find} - replace: {replace}')
            msapp_replace(msapp_file, find, replace, exclude=['DataSources.json', 'Properties.json'])


def replace_regex(source):
    controls = f"Input/msapp/{os.listdir('Input/msapp')[0]}/Controls"
    pattern = fr'"(?:[^"\\]|\\.)*{source}(?:[^"\\]|\\.)*"'
    if_statement = 'If(varEnv=\\"DEV\\",{0},{1})'

    for file in (os.listdir(controls))[0:2]:
        sfile = ""
        with open(f"{controls}\\{file}", 'r') as f:
            sfile = f.read()
            try:
                matches = re.findall(pattern, sfile)
                if (len(matches) > 0):
                    print(f"{file} - {sfile.split(':')[3]}")
                    for match in matches:
                        match = match[1:-1]
                        if match[:2] != "If" and match[:5] != "//Set" and match[:3] != "Set" :
                            # print(match)
                            prod = match.replace("-Dev", "-Prod")
                            transformed = if_statement.format(match, prod)
                            print(prod)
                            print(transformed)
                            sfile = sfile.replace(match, transformed)
            except:
                pass
        with open(f"{controls}/{file}", "w") as f:
            f.write(sfile)

def full_regex():
    with open('mapping.csv', 'r') as v:
        for line in v.readlines()[1:]:
            parts = line.split(",")
            find = parts[1].strip()
            replace = parts[2].strip()
            replace_regex(find)


app_zip = get_zipfile()  # ECAPortal_20230627195436.zip
path = app_zip.split(".")[0]  # ECAPortal_20230627195436
#unzip_app(app_zip)
#print(os.listdir(f'Input/{path}/'))
app_folder = os.listdir(f'Input/{path}/Microsoft.PowerApps/apps')[0]  # 4568856658079073990
#print(os.listdir(f'Input/{path}/Microsoft.PowerApps'))
#print(os.listdir(f'Input/{path}/Microsoft.PowerApps/apps'))

print(path)

msapp_path = getMsapp(path)
print(msapp_path)
msapp_file = (msapp_path.split("/")[-1:])[0][:-6]
#extract_msapp(msapp_path)
print(msapp_file)
variable_replace()

#full_replace()
#dynamic_replace()


#full_regex()

#compress_msapp(msapp_path)
#zip_app()
