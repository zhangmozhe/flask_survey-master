from PIL import Image
import os

def convert():
    for index in range(1, 21):
        dir_current = os.getcwd() + "/"+ str(index) +"/"
        for filename in os.listdir(dir_current):
            if filename.endswith(".png"):
                name = filename.split('.')
                name = name[0]
                print name
                file = Image.open(dir_current + filename)
                file.save(dir_current + name + '.jpg')


if __name__=="__main__":
    convert()