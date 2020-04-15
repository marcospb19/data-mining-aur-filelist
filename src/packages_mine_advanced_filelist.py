import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor


regex = re.compile(r'ls-blob[^>]+?>(.+?)</a>' , flags = re.DOTALL | re.MULTILINE)


def get_file_list_from_package(url):
	text = requests.get(url).text
	file_list = regex.findall(text)
	name = url[url.find('=') + 1:]

	return {
		'name': name,
		'filelist': file_list
	}


package_list = []
with open('aur_packages.json' , 'r') as json_file:
	package_list = [package['name'] for package in json.load(json_file)]


urls = (f'https://aur.archlinux.org/cgit/aur.git/tree/?h={package}'
        for package in package_list)


pool = ThreadPoolExecutor(max_workers = 25)
json_text = []



files = 0
i = 0
for package_dict in pool.map(get_file_list_from_package , urls):
	json_text.append(package_dict)

	files += len(package_dict['filelist'])
	i += 1

	if i % 50 == 0:
		print(f'{files} files! {i}/{len(package_list)} done.')

print(f'{files} files, {i}/{len(package_list)} done.')


with open('aur_package_filelist.json' , 'w') as output_json_file:
	json.dump(json_text , output_json_file , indent = '\t')

