# Filelist data mining from the Arch User Repository

Project initally  intent of analysing the file types in AUR, I took the chance and made this project where
I gather information about AUR packages and store it on a .json, for whatever purpouse you want to.



Sequence:
`mine_aur_package_list.py` -> files/*
files/* -> `process_aur_package_list.py` -> package_list.json
package_list.txt -> 
`



`mine_aur_package_list.py` will mine ~23MB+ of files containing the list of the packages
from [This listing section](https://aur.archlinux.org/packages/?O=0&PP=250)

then `process_aur_package_list.py` processes these files and creates `package_list.txt`

