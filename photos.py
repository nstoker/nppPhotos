# A script to watch a folder for images getting added
#
# the orginal will be copied to a folder (for safety...)
# logos and/or text added to specified positions and saved in a print folder
# images resized for web usage

    # Check for parameters
    # Usage:
    # photos.py folder-to-watch folder-for-print folder-for-web  [options]
    #
    # Options
    # -l filename position [size] add logo to position. Position ne, n, nw, w, sw, s, se, e. Size will resized
    # -t text position [-bc background colour] [-tc text colour] [-ts shadow] [-tf text font]
    # -ignore  ignore any images already in folder 

import sys
import time
import shutil
import argparse
import os

dummyRun=True #False
facebook=False
ignore_existing=False
path_to_watch="new/"
path_to_print="forPrinting/"
path_to_upload="forUploading/"
twitter=False

def main(argv):
    global path_to_watch
    global path_to_print
    global path_to_upload
    process_initial_photos=True
    dry_run=False
    
    parser=argparse.ArgumentParser(
        description='Add banners and/or text to existing photographs and converting to a smaller image size for uploading to social media sites. ',
        epilog='position can be one of n, ne, e, se, s, sw, w or nw')
    parser.add_argument("watch", help="Folder to watch for new photos")
    parser.add_argument("forPrinting", help="Folder to put modified pictures into")
    parser.add_argument("forUpload", help="Folder to put photos for upload")
    parser.add_argument("-initial", help="Add banners to files already in folder (default off)", action="store_true")
    parser.add_argument("--dry-run", help="Do a dry run without creating/adding logos or text. Displays commands to imagemagick", action="store_true")
    parser.add_argument("-logo", help="Add image at position", action="append", nargs=2, metavar=('filename','position'))
    parser.add_argument("-text", help="Add text at position", action="append", nargs=2, metavar=('text','position'))
    
    args=parser.parse_args()
    
    path_to_watch=args.watch
    path_to_print=args.forPrinting
    path_to_upload=args.forUpload
    process_initial_photos=args.initial
    
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    if process_initial_photos:
        bannerise(before)
    else:
        print "Ignoring files already in the folder"
    if args.text:
        print args.text
    else:
        print "No text to be added"
    if args.logo:
        print args.logo
    else:
        print "No logos to be added"
    
    if not(args.text or args.logo):
        print "Just doing resize - no logos or text will be added"
    
    print "\nScanning %s for new images, printable versions going in %s and uploadable versions saved in %s" %(path_to_watch,path_to_print,path_to_upload)
    while 1:
      time.sleep (1)
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in after if not f in before]
      #removed = [f for f in before if not f in after]
      if added: 
          print "Added: ", ", ".join (added)
          bannerise(added)
      #if removed: print "Removed: ", ", ".join (removed)
      print "Waiting for more photo's to be added (snoozing for 10s)"
      before = after
      break

def bannerise(photos):
    for p in photos:
        print "Imagine the effect on %s" %(p)

    

main(sys.argv)