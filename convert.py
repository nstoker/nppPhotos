#!/usr/bin/python
# Script to add banners and logos to photographs for printing and uploading.
import sys
# import time
# import shutil
import argparse
import os
from subprocess import call
from time import sleep
from collections import deque

path_to_watch = "new/"
path_to_print = "forPrint/"
path_to_upload = "forUpload/"
bannerText = ""
logoSet = {}
imageMagicBanners = ""
dryRun = False
verbosity = 0
initialPhotos = False
onceOnly = False
uploadList = deque()
  
def commandLine(args):
  global path_to_watch
  global path_to_print
  global path_to_upload
  global bannerText
  global logoSet
  global imageMagicBanners
  global dryRun
  global verbosity
  global initialPhotos
  global onceOnly
  
  parser=argparse.ArgumentParser(
      description='Add banners and/or text to existing photographs and converting to a smaller image size for uploading to social media sites. ',
      epilog='position can be one of north, northeast, east, southeast, south, southwest, west or northwest')
  parser.add_argument("watch", help="Folder to watch for new photos")
  parser.add_argument("printFolder", help="Folder to put modified pictures into")
  parser.add_argument("uploadFolder", help="Folder to put photos for upload")
  parser.add_argument("-i","--initial", help="Add banners to files already in folder (default off)", action="store_true")
  parser.add_argument("-1","--once",help="Run once only. Only valid if -initial is set", action="store_true")
  parser.add_argument("-d","--dry-run", help="Do a dry run without creating/adding logos or text. Displays commands to imagemagick", action="store_true")
  parser.add_argument("-l","--logo", help="Add image at position", action="append", nargs=2, metavar=('filename','position'))
  parser.add_argument("-t","--text", help="Add text at position", action="append", nargs=2, metavar=('text','position'))
  parser.add_argument("-m","--move", help="Move orginals to folder when completed",nargs=1, metavar=('foldername'))
  parser.add_argument("-v","--verbose", help="Display more details about progress", action="store_true")
  
  args=parser.parse_args()
  
  path_to_watch=args.watch
  path_to_print=args.printFolder
  path_to_upload=args.uploadFolder
  
  if not(path_to_watch.endswith("\\") or path_to_watch.endswith("/")):
      parser.print_help()
      print
      print "Error: make sure that the trailing directory markers are included"
      exit(1)
  
  if args.text:
    textToImage(args.text)
    
  if args.logo:
      logoSet.update(dict(args.logo))

  if logoSet:
      imageMagicBanners=imageConvert()
          
  initialPhotos=args.initial
  dryRun = args.dry_run
  verbosity = args.verbose
  initialPhotos = args.initial
  onceOnly = args.once

def printVersion(photos):
  count=0
  for p in photos:
    if p.lower() == ".ds_store":
      continue
    
    count+=1
    print "%i/%i Preparing %s for print" %(count,len(photos),p)
    addToUploadList(p)
    
    fname=os.path.splitext(p)[0]
    if os.path.splitext(p)[1].lower()==".orf":
        fname+= ".jpg"
    else:
        fname+= os.path.splitext(p)[1]
    
    srcF   = os.path.join(os.path.dirname(path_to_watch),p)
    printF = os.path.join(os.path.dirname(path_to_print),fname)
    
    
    cmd = "convert " + srcF + imageMagicBanners  + " -bordercolor none -border 100x100 " + printF 
    
    if dryRun:
        print "print command '%s'" %(cmd)
    else:
        if verbosity:
            print
            print "adding banners with '%s'" %(cmd)
            
        callImageMagick(cmd)
        
def uploadVersion(toUpload):
  if len(toUpload):
    p=toUpload.popleft()

    print "Preparing %s for upload (%i left to process)" %(p,len(toUpload))
    caption = p 
    fname=os.path.splitext(p)[0]
    if os.path.splitext(p)[1].lower()==".orf":
        fname+= ".jpg"
    else:
        fname+= os.path.splitext(p)[1] 
    srcF    = os.path.join(os.path.dirname(path_to_watch),p) 
    # printF  = os.path.join(os.path.dirname(path_to_print),fname)
    uploadF = os.path.join(os.path.dirname(path_to_upload),fname)
    
    cmd = "convert " + srcF + imageMagicBanners + " -bordercolor grey -border 40x40 " + uploadF
    
    # First get a clean master
    if dryRun:
      print "Upload part 1 %s" %(cmd)
    else:
      if verbosity:
        print "Upload part 1 %s" %(cmd)
        
      callImageMagick(cmd)
    
      # Now convert to the upload version
    cmd = "convert -caption '%s' %s -thumbnail 640x480 -gravity center -bordercolor Lavender -background navy +polaroid %s" %(caption,uploadF,uploadF)
    
    if dryRun:
      print "Upload command '%s'" %(cmd)
    else:
      if verbosity:
        print 
        print "preparing upload with '%s'" %(cmd)
      
      callImageMagick(cmd)
        
def addToUploadList(filename):
  global uploadList
  uploadList.append(filename)

def callImageMagick(cmd):
    rv= os.system(cmd)
    if not rv==0:
        print "Error from imagemagick. "
        exit(1)
  
def textToImage(text):
  # Create the text banners
  global logoset
  
  # A better way of doing this is *really* needed
  for i in range(len(text)):        
      cmd = "convert -size 2000x300 xc:pink -pointsize 300 -gravity center -undercolor royalblue -stroke none -strokewidth 1 -fill gold -annotate +0+0 ' " + text[i][0] +" ' -trim +repage -shave 1x1 text%s.jpg" %(i)
      if dryRun:
          print "BuildLogos cmd is %s" %(cmd)
      else:
          if verbosity:
              print
              print "textLogos imageMagick command is %s" %(cmd)
              
          call( [cmd], shell=True)

      logoSet["text%s.jpg"%(i)]=text[i][1]    
  
def main():
  added = {}
  before = {}

  
  if len(logoSet)==0:
    print "No text or logos are being added"
  else:
    print "Logo list is", ", ".join(logoSet)
    
  if not initialPhotos:
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
  
  while 1:
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    
    if added:
      print "Added photos: ", ", ".join (added)
      sleep(5)
      printVersion(added)
      print "Main photographs converted, waiting for more to be added to folder. Started background processing for upload photographs"
      

    if onceOnly and len(uploadList)==0:
      print "Only running once - everything done now"
      break
    elif len(uploadList)>0:
      uploadVersion(uploadList)
      print "Main photographs converted, waiting for more to be added to folder"
    else:
      sleep(10)
      
    before = after


def getLocation(position):
  directions = {"n":"north","ne":"northeast","e":"east","se":"southeast","s":"south","sw":"southwest","w":"west","nw":"northwest"}

  if directions.has_key(position):
    position=directions[position]

  return position

def imageConvert():
    cmd=""
    for l in logoSet:
        cmd+=" -gravity " + getLocation(logoSet[l]) + " " + l + " -composite "
    return cmd 
    
if __name__ == "__main__":
  commandLine(sys.argv)
  main()
