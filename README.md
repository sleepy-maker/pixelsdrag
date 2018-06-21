# pixelsdrag

I folked https://github.com/leoneckert/pixelsdrag to make the script compatible with python3.  

There are some requirements. 
   
homebrew  
imagemagick  
Pillow  

```zsh
Install Homebrew
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install imagemagick
$ brew reinstall imagemagick --with-little-cms --with-little-cms2

Install Pillow
$ pip install Pillow

Or
$ pip install -U -r requirements.txt 
```


## How to use
```zsh
$ python pixel.py image_path

example
$ python pixel.py test.jpg
```
