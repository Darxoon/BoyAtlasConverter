# BoyAtlasConverter

An image atlas extractor for World of Goo 2

## Installation

Make sure you have [Python 3](https://www.python.org/) installed. Download the source code and open the BoyAtlasConverter folder in a command line. Run the following:

    py -m pip install -r requirements.txt

(if you are on Linux, you can likely skip this step. Should you get an error about PIL not being installed, create and activate a venv first and then run the above command.)

## Usage

Before you can extract the atlas, you have to convert it from .image to .png using [boyi_convert](https://github.com/codeshaunted/boyi_convert/releases).

Open the BoyAtlasConverter folder in a command line and run the following:

    py main.py <your atlas.image or .png>

(Note: you can provide the .image to the tool, but you will still have to convert it to a .png first.)

BoyAtlasConverter will extract all of the images in the atlas into a folder with the same name as the atlas.

This does not support rebuilding the atlas, but that's rarely if ever necessary, as you can just convert the .png back to an .image and reference that directly in the relevant resources.xml.
