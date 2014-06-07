nppPhotos
=========

This script was prompted by a need to add images and text to photographs taken at events.

The basic requirements were to:

* Monitor a folder
* For each photo added
	* Add the logo(s) to the photograph
	* Add text to the photograph
	* Create a version for uploading at reduced size
	
Additional ideas (not yet implemented) include:
* Tweet photos (being mindful of the 100/hour and [2400/day](https://support.twitter.com/articles/15364-twitter-limits-api-updates-and-following))
* Upload to a facebook album
* Give a choice of layouts for the uploadable version

Command Line
=======

usage: photos.py [-h] [-i] [-1] [-d] [-l filename position] [-t text position]
                 [-m foldername] [-v]
                 watch forPrinting forUpload

Add banners and/or text to existing photographs and converting to a smaller
image size for uploading to social media sites.

positional arguments:
  watch                 Folder to watch for new photos
  forPrinting           Folder to put modified pictures into
  forUpload             Folder to put photos for upload

optional arguments:
  -h, --help            show this help message and exit
  -i, --initial         Add banners to files already in folder (default off)
  -1, --once            Run once only. Only valid if -initial is set
  -d, --dry-run         Do a dry run without creating/adding logos or text.
                        Displays commands to imagemagick
  -l filename position, --logo filename position
                        Add image at position
  -t text position, --text text position
                        Add text at position
  -m foldername, --move foldername
                        Move orginals to folder when completed
  -v, --verbose         Display more details about progress

position can be one of north, northeast, east, southeast, south, southwest,
west or northwest


Other notes
=======

Ideas for further image manipulation
[Lots including stacked polaroids](http://www.imagemagick.org/Usage/thumbnails/).
