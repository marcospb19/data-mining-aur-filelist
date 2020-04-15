from concurrent.futures import ThreadPoolExecutor
import requests
import re


# Wrap this function to use in ThreadPoolExecutor.map()
def get_page_text(url):
	return requests.get(url).text


# List urls format
# https://aur.archlinux.org/packages/?O=0&PP=250
# https://aur.archlinux.org/packages/?O=250&PP=250
# https://aur.archlinux.org/packages/?O=500&PP=250
# ...


blank_page_text = get_page_text('https://aur.archlinux.org/packages/?O=9999999')
quantity_of_packages = int(re.findall(r'(\d+) packages found' , blank_page_text)[0])


pool = ThreadPoolExecutor(max_workers=50)
urls = (f"https://aur.archlinux.org/packages/?PP=250&O={i}" for i in range(0 , quantity_of_packages + 252 , 250))

i = 0
for result in pool.map(get_page_text , urls):
	arquivo = open(f'files/{i}' , 'w')
	arquivo.write(result)
	arquivo.close()
	print(i)
	i += 250
