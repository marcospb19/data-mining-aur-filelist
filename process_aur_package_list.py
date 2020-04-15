import glob # To list files
import re   # To filter packages from the files


file_name_list = glob.glob('files/*')


# Let's use a set to remove duplicated entries
set_of_packages = set()


regex = re.compile(r'<td><a href="/packages/([^/]+)/">\1</a></td>')


for file_name in file_name_list:
	with open(file_name , 'r') as input_file:

		for package in regex.findall(input_file.read()):
			set_of_packages.add(package)


with open('package_list.txt' , 'w') as package_list_output:
	for package in sorted(set_of_packages):
		package_list_output.write(package + '\n')
