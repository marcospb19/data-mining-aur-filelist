import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor
from itertools import chain , count
flatten = chain.from_iterable


github_page = 'https://github.com/marcospb19/data-mining-aur-filelist'


def get_page_content(url: str):
	return requests.get(url).text


# This regex pattern will be used in the function below
regexes = [re.compile(rf'<{tag}[^>]*?>.+?</{tag}>' , flags = re.MULTILINE | re.DOTALL)
           for tag in ['tbody' , 'tr' , 'td']]
#
def separate_package_page_information(page: str):

	try:
		page  = regexes[0].findall(page)[0]
		lista = regexes[1].findall(page)

		for i , _ in enumerate(lista):
			lista[i] = regexes[2].findall(lista[i])

	# This never occured
	except IndexError:
		print("A error on the data was found and ignored.")

	return lista


#
regex = re.compile(r'<([^>]+?)( [^>]+?)?>([^\s<].*)</\1>')
#
def f(package_list: list):
	dictionary_keys = ['name' , 'version' , 'votes' , 'popularity',
	                   'description' , 'maintainer' , 'outdated']
	flagged_as_outdated = []

	for i , _ in enumerate(package_list):

		flagged_as_outdated.append(package_list[i][1].find('<td class=\"flagged\"') != -1)

		# Error handling
		if len(package_list[i]) != 6:
			if package_list[i][0].find('package') == -1:
				print("Unexpected error, exiting")
				exit(1)

			pkgname = regex.findall(package_list[i][0])[0][2]
			if len(package_list[i]) == 5 and package_list[i][-1].count('\t') > 5:
				# AUR shows None for missing descriptions, but this may be more convenient
				print(f'Missing description field on the package \"{pkgname}\", using empty string')
				package_list[i].insert(-1 , '')
				package_list[i][-1] = package_list[i][-1].split("\">")[-1].split('</')[0]

			else:
				print(f"Unexpected missing information on the possible package \"{pkgname}\"?")
				print(f"If possible, leave a issue at {github_page}")
				exit(0)


		for j in range(len(package_list[i])):
			if len(package_list[i][j]):
				package_list[i][j] = regex.findall(package_list[i][j])[0][2]

		package_list[i] = {key: package_list[i][j]
				           for j , key in enumerate(dictionary_keys[:-1])}

		package_list[i]['outdated'] = flagged_as_outdated[i]


	return package_list


blank_page_text = get_page_content('https://aur.archlinux.org/packages/?O=999999')
quantity_of_packages = int(re.findall(r'(\d+) packages found', blank_page_text)[0])


# Generator for the URLs
urls = (f'https://aur.archlinux.org/packages/?PP=250&O={i}'
        for i in range(0 , quantity_of_packages + 255 , 250))


pool = ThreadPoolExecutor(max_workers = 25)
packages_info = []


skip_one_print = True
for page in pool.map(get_page_content , urls):
	package_information = separate_package_page_information(page)
	packages_info.extend(f(package_information))

	if not skip_one_print:
		print(len(packages_info))
	skip_one_print = not skip_one_print


with open('aur_packages.json' , 'w') as output_json:
	json.dump(packages_info , output_json , indent = '\t')


counter = 0
for pkg in packages_info:
	if not pkg['description']:
		counter += 1
print(f'{counter} packages have empty description')
