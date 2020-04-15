import requests
import re
import json
from concurrent.futures import ThreadPoolExecutor
from itertools import chain , count
flatten = chain.from_iterable



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

	except IndexError:
		print("A error on the data was found and ignored.")

	return lista



#
def f(packages_list: list):

	regex = re.compile(r'<([^>]+?)( [^>]+?)?>([^\s<].*)</\1>')
	dictionary_keys = ['name' , 'version' , 'votes' , 'popularity' , 'description' , 'maintainer']

	for i , _ in enumerate(packages_list):

		if len(packages_list[i]) == 6:
			for j in range(len(packages_list[i])):
				packages_list[i][j] = regex.findall(packages_list[i][j])[0][2]

		# Error handling
		else:
			if packages_list[i][0].find('package') == -1:
				print("Missing field information on unknown package, ignoring.")

			else:
				missing_name = regex.findall(packages_list[i][0])[0][2]
				print(f"Missing field information on the package \"{missing_name}\", ignoring.")

			packages_list.pop(i)
			continue


		packages_list[i] = {key: packages_list[i][j]
				           for j , key in enumerate(dictionary_keys)}

	return packages_list



blank_page_text = get_page_content('https://aur.archlinux.org/packages/?O=999999')
quantity_of_packages = int(re.findall(r'(\d+) packages found', blank_page_text)[0])


# Generator for the URLs
urls = (f'https://aur.archlinux.org/packages/?PP=250&O={i}'
        for i in range(0 , quantity_of_packages + 255 , 250))


pool = ThreadPoolExecutor(max_workers = 30)
packages_list = []


total_size = 0
for page in pool.map(get_page_content , urls):
	package_information = separate_package_page_information(page)

	len_before = len(package_information)
	packages_list.extend(package_information)

	if len(package_information) > len_before:
		packages[len_before:-1] = f(package_information[len_before:-1])

	total_size += len(package_information)
	print(total_size)


# Organized info into list of sets
packages_info = f(packages_list)


with open('aur_packages.json' , 'w') as output_json:
	output_json.write(json.dumps(packages_info , indent = '\t'))
