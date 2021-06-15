import os

path = "rename"
print(os.listdir(path))

for filename in os.listdir(path):
    shortname, ext = os.path.splitext(filename)
    f_moreno, f_fileNumber, f_imgNumber = shortname.split('_')
    i = int(f_fileNumber)

    if f_fileNumber.startswith("00"):
        newName = f_moreno + '_' + '00' + str(i - 1) + '_' + f_imgNumber + ext

    elif f_fileNumber.startswith("0"):
        newName = f_moreno + '_' + '0' + str(i - 1) + '_' + f_imgNumber + ext

    else:
        newName = f_moreno + '_' + str(i - 1) + '_' + f_imgNumber + ext

    print(newName)
