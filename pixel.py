import subprocess
import sys
import os
from PIL import Image


def checkDir(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def convertToSrgb(in_path, out_path):
    # had to reinstall imagemagick like so:
    # brew reinstall imagemagick --with-little-cms --with-little-cms2
    # and downloaded the profile.icc file from:
    # http://www.color.org/srgbprofiles.xalter
    cmd = ['/usr/local/bin/convert', in_path,
           '-profile', 'sRGB2014.icc', out_path]
    subprocess.call(cmd, shell=False)
    return out_path


def resize(in_path, basewidth, out_path):
    img = Image.open(in_path)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(out_path)
    return out_path


def center_split(in_path, out_path):

    im = Image.open(in_path).convert('RGBA')  # Can be many different formats.
    pix = im.load()

    w, h = im.size
    image = Image.new('RGB', (w, h))
    pixels = image.load()
    for i in range(image.size[0]):  # for every pixel:
        for j in range(image.size[1]):
            pixels[i, j] = pix[int(image.size[0]/2), j]
    # if there is no project folder create a folder
    checkDir('./project')
    image.save("project/"+out_path)  # Save the modified pixels as png

    gap = int(w*0.2 if w < h else h*0.2)
    new_w = w*2+gap*3
    w_percent = (new_w/float(im.size[0]))
    new_h = int((float(im.size[1]) * float(w_percent)))
    frame = Image.new('RGB', (new_w, new_h), (255, 255, 255))
    frame.paste(im, (gap, (frame.size[1]-im.size[1])/2))
    frame.paste(image, (gap*2 + w, (frame.size[1]-im.size[1])/2))
    checkDir('./project')
    frame.save("project/2_frame_double.jpg")


def center_split_with_image(in_path, out_path):
    out_name = ".".join(out_path.split(".")[:-1])
    out_ext = out_path.split(".")[-1]
    im = Image.open(in_path).convert('RGBA')  # Can be many different formats.
    pix = im.load()

    w, h = im.size
    half = int(w/2)
    image = Image.new('RGB', (half*3, h))
    pixels = image.load()
    left = Image.new('RGB', (half, h))
    left_p = left.load()
    middle = Image.new('RGB', (half, h))
    middle_p = middle.load()
    right = Image.new('RGB', (half, h))
    right_p = right.load()

    for i in range(image.size[0]):  # for every pixel:
        for j in range(image.size[1]):
            if i < half:
                pixels[i, j] = pix[i, j]
                left_p[i, j] = pix[i, j]

            elif i < 2*half:
                pixels[i, j] = pix[int(im.size[0]/2), j]
                middle_p[i-half, j] = pix[int(im.size[0]/2), j]
            else:
                pixels[i, j] = pix[i-half, j]
                right_p[i-2*half, j] = pix[i-half, j]

    # Save the modified pixels as png
    checkDir('./project')
    image.save("project/3_"+out_name + "_full." + out_ext)
    # Save the modified pixels as png
    left.save("project/4_"+out_name + "_left." + out_ext)
    # Save the modified pixels as png
    middle.save("project/5_"+out_name + "_middle." + out_ext)
    # Save the modified pixels as png
    right.save("project/6_"+out_name + "_right." + out_ext)


def slit_every_horizontal(in_path, out_dir):
    im = Image.open(in_path).convert('RGBA')  # Can be many different formats.
    pix = im.load()

    w, h = im.size
    for index in range(w):
        image = Image.new('RGB', (w, h))
        pixels = image.load()
        for i in range(image.size[0]):  # for every pixel:
            for j in range(image.size[1]):
                pixels[i, j] = pix[index, j]
        # Save the modified pixels as png
        # if there is no every folder create a folder
        checkDir('./project/' + out_dir)
        image.save("project/"+out_dir+"/every"+'{0:09d}'.format(index)+'.jpg')

    # ffmpeg -framerate 30 -i a%07d.png -vcodec libx264 -vf scale=1080:-2,format=yuv420p output.mp4

    cmd = ['/usr/local/bin/ffmpeg', '-framerate', '30', '-i', 'project/'+out_dir+'/every%09d.jpg',
           '-vcodec', 'libx264', '-vf', 'scale=720:-2,format=yuv420p', 'project/7_every_slit.mp4']
    subprocess.call(cmd, shell=False)

    print('every{'+str('{0:09d}'.format(0)) +
          '..'+str('{0:09d}'.format(w-1))+'}')
    # cmd = ['montage', '-background', '\'#FFFFFF\'', '-fill', '\'gray\'', '-define', 'jpeg:size=200x200', '-geometry', '200x200+2+2', '-auto-orient', out_dir+'/every{'+str('{0:09d}'.format(0))+'..'+str('{0:09d}'.format(w-1))+'}', 'wild.jpg' ]

    w_percent = (200/float(im.size[0]))
    new_h = int((float(im.size[1]) * float(w_percent)))
    # cmd = "montage -background '#FFFFFF' -fill 'gray' -define jpeg:size=200x200 -geometry 200x"+str(new_h)+"+2+2 -auto-orient "+ 'every/every{'+str('{0:09d}'.format(0))+'..'+str('{0:09d}'.format(w-1))+'}.jpg' + "contact-dark.jpg"
    # cmd = "montage -background '#FFFFFF' -fill 'gray' -define jpeg:size=200x200 -geometry 200x"+str(new_h)+"+2+2 -auto-orient "+ 'every/every{'+str('{0:09d}'.format(0))+'..'+str('{0:09d}'.format(w-1))+'}.jpg' + " contact-dark.jpg"
    cmd = "montage -background '#FFFFFF' -define jpeg:size=200x200 -geometry 200x" + \
        str(new_h)+"+2+2 -auto-orient " + \
        'project/every/every*.jpg' + " project/8_contact-sheet.jpg"

    print(cmd)
    subprocess.call(cmd, shell=True)


if __name__ == "__main__":
    input_file = sys.argv[1]
    path = convertToSrgb(input_file, "converted.jpg")
    print('[+] Converted color profile')
    if len(sys.argv) > 2:
        path = resize(path, int(sys.argv[2]), "resized.jpg")
        print('[+] Resized image to width:', sys.argv[2],
              center_split(path, "1_centerSplit.jpg"))
    print('[+] Created slit image of center pixel values',
          center_split_with_image(path, "centerSplitWithImage.jpg"))
    print('[+] Created slit image of center pixel values with image',
          slit_every_horizontal(path, "every"))
    print('[+] Created slit images for every horizontal pixel row')
