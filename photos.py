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
    process_initial_photos=False
    
    parser=argparse.ArgumentParser()
    parser.add_argument("watch", help="Folder to watch for new photos")
    parser.add_argument("forPrinting", help="Folder to put modified pictures into")
    parser.add_argument("forUpload", help="Folder to put photos for upload")
    
    args=parser.parse_args()
    
    path_to_watch=args.watch
    path_to_print=args.forPrinting
    path_to_upload=args.forUpload
    
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    if process_initial_photos:
        bannerise(before)
    
    while 1:
      time.sleep (10)
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in after if not f in before]
      #removed = [f for f in before if not f in after]
      if added: 
          print "Added: ", ", ".join (added)
          bannerise(added)
      #if removed: print "Removed: ", ", ".join (removed)
      print "Waiting for more photo's to be added (snoozing for 10s)"
      before = after

def bannerise(photos):
    print photos

    

main(sys.argv)