import json
import re


with open('aur_package_filelist.json' , 'r') as input_file:
	json_loaded = json.load(input_file)

filelist = set()
[filelist.update(pkg_list['filelist']) for pkg_list in json_loaded]


regex = re.compile(r'\.[^\.]+$')
file_extensions_list = {regex.findall(file)[0] if len(regex.findall(file)) else '.' for file in filelist}


[print(i) for i in sorted(file_extensions_list)]
