THIS README IS A UNFINISHED and weird **DRAFT**
I'm going to sleep now, it'll be finished later


# Arch User Repository filelist

In a salty discussion about what kind of files the users are pushing into AUR, I created this
project to analyse the file extensions on the whole repository.

This code may be reusable if you're interesting of getting informations from AUR, for this reason,
the code here has been splitten into several files, depending on your case of use, you can keep
a file or two and rewrite just a small part to get your custom results. Let's then go to the explanation
on each file.


Sequence:
`mine_aur_package_list.py` -> files/*
files/* -> `process_aur_package_list.py` -> package_list.json
package_list.txt -> 
`



`mine_aur_package_list.py` will mine ~23MB+ of files containing the list of the packages
from [This listing section](https://aur.archlinux.org/packages/?O=0&PP=250)

then `process_aur_package_list.py` processes these files and creates `package_list.txt`

