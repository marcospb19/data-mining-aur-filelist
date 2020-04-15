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
def f(package_list: list):

	regex = re.compile(r'<([^>]+?)( [^>]+?)?>([^\s<].*)</\1>')
	dictionary_keys = ['name' , 'version' , 'votes' , 'popularity' , 'description' , 'maintainer']
	should_pop = set()


	for i , _ in enumerate(package_list):

		if len(package_list[i]) == 6:
			for j in range(len(package_list[i])):
				package_list[i][j] = regex.findall(package_list[i][j])[0][2]

		# Error handling
		else:
			if package_list[i][0].find('package') == -1:
				print("Missing field information on unknown package, ignoring.")

			else:
				missing_name = regex.findall(package_list[i][0])[0][2]
				print(f"Missing field information on the package \"{missing_name}\", ignoring.")

			should_pop.add(i)
			continue


		package_list[i] = {key: package_list[i][j]
				           for j , key in enumerate(dictionary_keys)}


	for element in reversed(sorted(should_pop)):
		package_list.pop(element)

	return package_list



blank_page_text = get_page_content('https://aur.archlinux.org/packages/?O=999999')
quantity_of_packages = int(re.findall(r'(\d+) packages found', blank_page_text)[0])


# Generator for the URLs
urls = (f'https://aur.archlinux.org/packages/?PP=250&O={i}'
        for i in range(0 , quantity_of_packages + 255 , 250))


pool = ThreadPoolExecutor(max_workers = 25)
packages_info = []


total_size = 0
for page in pool.map(get_page_content , urls):
	package_information = separate_package_page_information(page)

	packages_info.extend(f(package_information))

	total_size += len(package_information)
	print(total_size)


with open('aur_packages.json' , 'w') as output_json:
	json.dump(packages_info , output_json , indent = '\t')
