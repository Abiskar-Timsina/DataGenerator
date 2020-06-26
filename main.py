from tkinter import *
from tkinter import filedialog
import os
import cv2
import pickle
import numpy as np
import datetime
from tqdm import tqdm

# initializing variables
DATA = []

# in-code documentation


def decor():
    os.system('cls')
    print('\t\t\t\tData Generator - Coded by: Abiskar Timsina\n')
    print('Description: Use this script to generate image array from images stored in directories.The images and labels are saved in a single array and pickled.')
    print('\tThe images are read and converted to array using opencv. The one-hot-encodings are based on the no of sub directories; if there are 6 sub-directories ')
    print(
        '\tfor 6 different objects; they are saved as [1,0,0,0,0,0] for all images in the first directory and subsequently [0,1,0,0,0,0] ... [0,0,0,0,0,1] for')
    print('\timages in other directories.\n\n')
    print('Pickling Format: [Image_array,one-hot-encoding]\n')
    print('Usuage: in python;')
    print('\tdata = pickle.load(\'<file>.data\')')
    print('\t<shuffle the data>')
    print('\tfor x,y in data:')
    print('\t\tX.append(x)  # will contain image array')
    print('\t\tY.append(y)  # contains one hot encoding\n\n')
    print('Directory Selection:Select the parent folder that has multiple classes as its sub-directory')
    print('Viz.')
    print('Data(directory)')
    print('|_ 0 -> (images belonging to that class)')
    print('|_ 1 -> (images belonging to that class)')
    print('|_ 2 -> (images belonging to that class)')
    print('|_ 3 -> (images belonging to that class)')
    print('|_ 4 -> (images belonging to that class)')
    print('. ')
    print('.')
    print('.')
    print('Select the parent directory(in this case the data directory).\n\n')
    print('Default Values:')
    print('\tConvert to Grayscale: False')
    print('\tDefault Dimenstion: 250x250')
    print('\nVersion:0.1')
    print('\t-Only Supports one hot encoding.')
    print("__________________________________________________________________________________________")
    print('Do not exit the program untill you get the " [COMPLETED] "\n\n\n\n')
    input('Press any key to continue ...\n\n')

#reshaping/converting to grayscale
def data_manip(image_array, convert, IMAGE_SIZE):
    if convert:
        try:
            image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))
        except Exception as e:
            pass
    else:
        try:
            image = cv2.resize(image_array, (IMAGE_SIZE, IMAGE_SIZE))
        except Exception as e:
            pass

    return image

#opening the files inside the sub directorires
def file(NAME, convert=False, image_size=250):

    root = Tk()
    DIRECTORY = filedialog.askdirectory()
    root.destroy()
    SUB_DIRECTORIES = os.listdir(DIRECTORY)
    SUB_DIRECTORIES = tqdm(
        SUB_DIRECTORIES, desc='Converting', unit='directory')
    NUMBER_CLASSES = len(SUB_DIRECTORIES)
    os.system('cls')
    for encoding, each_directory in enumerate(SUB_DIRECTORIES):
        directory_path = str(DIRECTORY) + '/' + str(each_directory)
        items = os.listdir(directory_path)
        LABEL = np.zeros((1, NUMBER_CLASSES))
        for item in items:
            path = str(directory_path) + '/' + str(item)
            raw_image = cv2.imread(path)

            if (raw_image is not None):
                processed_image = data_manip(raw_image, convert, image_size)
                LABEL[0][encoding] = 1
                DATA.append([processed_image, LABEL[0]])
                LABEL = np.zeros((1, NUMBER_CLASSES))
            else:
                pass

        os.system('cls')

        os.chdir(DIRECTORY)

    length_set = len(DATA)
    print(f'\n\nLength of the Set: {length_set}')
    print('[NOTE] It is likely that not all pictures could be added to the data set. Use \'jpeg\' format.')
    input('Press any key to save...')
    write(length_set, image_size, convert, DIRECTORY, DATA, NAME)

#outputting the file and saved datas
def write(length, image_size, convert, directory, DATA, name='data'):
    os.chdir(directory)

    os.mkdir('GeneratedData')
    os.chdir('./GeneratedData')

    NAME = str(name) + '.data'

    with open(NAME, 'wb') as file:
        pickle.dump(DATA, file)

    with open('config.txt', 'w') as f:
        f.write('Configuration:\n')
        f.write(f'Converted to Grayscale: {convert}\n')
        f.write(f'Image Size: {image_size}x{image_size}\n')
        f.write(f'Length of the Set: {length}\n')
        f.write(f'\tCreated on: {datetime.datetime.today()}\n')

    saved_at = str(directory) + '/GeneratedData'
    print(f'File saved at: {saved_at}')
    print(f'[COMPLETED]Congif file saved.(contails all the settings and dimension of the pickled format)')
    input('[COMPLETED] Press any key to exit...')

#menu
def main():
    name = str(input('Save as filename: '))
    while True:
        yes_no = str(input('Convert to Grayscale? [y/n]: '))
        yes_no.lower()

        if (yes_no == 'y'):
            convert_inp = True
            break

        elif (yes_no == 'n'):
            convert_inp = False
            break

        else:
            print('[Error] Only Characters are accepted\n')
            continue

    while True:
        change_size = str(input('Change the size of the image? [y/n]: '))
        change_size.lower()

        if change_size == 'y':
            print('The size will have the same dimesions. Default: 250x250')
            while True:
                try:
                    image_size_inp = int(input('Enter the dimesion: '))
                    image_size = image_size_inp
                    break
                except AttributeError:
                    print(f'[Error] Interger expected not {type(image_size_inp)} ; enter value again. Otherwise, press "n" to pass default values\n')
                    continue
                except Exception as e:
                    print(e)
                    continue

            break

        elif change_size == 'n':
            image_size = 250
            break

        else:
            print('[Error] Only Characters are accepted\n')
            continue

    file(name, convert_inp, image_size)

if __name__ == '__main__':
    decor()
    main()
