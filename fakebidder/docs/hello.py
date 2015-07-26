import os

"""
Open additional data files using the absolute path,
otherwise it doesn't always find the file.
"""
# The absolute path of the directoy for this file:
_ROOT = os.path.abspath(os.path.dirname(__file__))

class Hello(object):
    def say_hello(self):
        return "Hello, World!"
    def open_image(self):
        print("Reading image.gif contents:")

        # Get the absolute path of the image's relative path:
        absolute_image_path = os.path.join(_ROOT, 'images/hello.gif')

        with open(absolute_image_path, "r") as f:
            for line in f:
                print(line)
