from img_info import IMAGE_PER_GROUP, SOURCE_PER_GROUP, GROUP_NUM, DISTORTION_TYPES, DISTORTION_LEVELS, IMAGE_NUM
import os
from random import randint, shuffle

directory = os.path.dirname(os.path.abspath(
    __file__)) + '/static/img-display-protocol'


def generate_index():
    f = open(directory + '/workfile.txt', 'w')
    for img_index in range(1, IMAGE_NUM + 1):
        for distortion_type in DISTORTION_TYPES:
            for distortion_level in range(1, DISTORTION_LEVELS + 1):
                f.write("%2d %12s %2d \n" %
                        (img_index, distortion_type, distortion_level))
    f.close()


def batch_index():
    for i in range(1, IMAGE_NUM + 1):
        IMAGE_FILE_ROOT = os.path.dirname(os.path.abspath(
            __file__)) + '/static/img-display-protocol'
        with open(os.path.join(IMAGE_FILE_ROOT, 'workfile.txt')) as f:
            lines = f.readlines()
            f.close()
        shuffle(lines)
        print lines
        with open(os.path.join(IMAGE_FILE_ROOT, str(i) + '.txt'), 'w+') as g:
            g.writelines(lines)
            g.close()

def group_images():
    f = open(directory + '/workfile.txt', 'r')
    lines = f.readlines()
    shuffle(lines)

    for group in range(0, GROUP_NUM):
        g = open(directory + '/group'+ str(group) + '.txt', 'w')
        sublines = lines[(group * IMAGE_PER_GROUP):((group + 1) * IMAGE_PER_GROUP)]
        sublines.append(sublines[0])
        sublines.append(sublines[1])
        g.writelines(sublines)
        g.close()


def clear_index():
    os.chdir(directory)
    filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
    for f in filelist:
        os.remove(f)


if __name__ == "__main__":
    clear_index()
    generate_index()
    group_images()
