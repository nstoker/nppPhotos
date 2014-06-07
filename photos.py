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
from subprocess import call
from time import sleep

dryRun=False
facebook=False
ignore_existing=False
path_to_watch="new/"
path_to_print="forPrinting/"
path_to_upload="forUploading/"
twitter=False
bannerText=""
logoSet={}
imageMagicBanners=" "
verbosity=0

def main(argv):
    global path_to_watch
    global path_to_print
    global path_to_upload
    global bannerText
    global logoSet
    global imageMagicBanners
    global dryRun
    global verbosity
    
    process_initial_photos=True
    dry_run=False
    
    parser=argparse.ArgumentParser(
        description='Add banners and/or text to existing photographs and converting to a smaller image size for uploading to social media sites. ',
        epilog='position can be one of north, northeast, east, southeast, south, southwest, west or northwest')
    parser.add_argument("watch", help="Folder to watch for new photos")
    parser.add_argument("forPrinting", help="Folder to put modified pictures into")
    parser.add_argument("forUpload", help="Folder to put photos for upload")
    parser.add_argument("-i","--initial", help="Add banners to files already in folder (default off)", action="store_true")
    parser.add_argument("-1","--once",help="Run once only. Only valid if -initial is set", action="store_true")
    parser.add_argument("-d","--dry-run", help="Do a dry run without creating/adding logos or text. Displays commands to imagemagick", action="store_true")
    parser.add_argument("-l","--logo", help="Add image at position", action="append", nargs=2, metavar=('filename','position'))
    parser.add_argument("-t","--text", help="Add text at position", action="append", nargs=2, metavar=('text','position'))
    parser.add_argument("-m","--move", help="Move orginals to folder when completed",nargs=1, metavar=('foldername'))
    parser.add_argument("-v","--verbose", help="Display more details about progress", action="store_true")
    
    args=parser.parse_args()
    
    path_to_watch=args.watch
    path_to_print=args.forPrinting
    path_to_upload=args.forUpload
    
    if not(path_to_watch.endswith("\\") or path_to_watch.endswith("/")):
        parser.print_help()
        print
        print "Error: make sure that the trailing directory marker is included"
        exit(1)
            
    process_initial_photos=args.initial
    dryRun = args.dry_run
    verbosity = args.verbose
    
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])

    if args.logo:
        logoSet.update(dict(args.logo))
        
    if args.text:
        bannerText=args.text
        textLogos(bannerText)
    
    if logoSet:
        imageMagicBanners=imageConvert()
        
    if process_initial_photos:
        addBannersTo(before)
    
    print "\nScanning %s for new images, printable versions going in %s and uploadable versions saved in %s" %(path_to_watch,path_to_print,path_to_upload)
    
    while 1:        
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        
        if added: 
          print "Added: ", ", ".join (added)
          addBannersTo(added)

        if args.once:
            print "only running once"
            break
            
        print "Waiting for more photo's to be added (snoozing for 10s)"
        before = after
        sleep(10)

def textLogos(text):
    global logoSet
    
    for i in range(len(text)):        
        cmd = "convert -size 2000x300 xc:pink -pointsize 300 -gravity center -undercolor royalblue -stroke none -strokewidth 1 -fill gold -annotate +0+0 '" + text[i][0] +"' -trim +repage -shave 1x1 text%s.jpg" %(i)
        if dryRun:
            print "BuildLogos cmd is %s" %(cmd)
        else:
            if verbosity:
                print
                print "textLogos imageMagick command is %s" %(cmd)
                
            call( [cmd], shell=True)

        logoSet["text%s.jpg"%(i)]=text[i][1]

def imageConvert():
    cmd=""
    for l in logoSet:
        cmd+=" -gravity " + logoSet[l] + " " + l + " -composite "
    
    # and the final border

    return cmd 

def Polariod(src,dest,imageDef,caption):
    # Create polaroid effect
    
    cmd = "convert -caption '%s' %s %s -thumbnail 640x480 -gravity center -bordercolor Lavender -background navy +polaroid %s" %(caption,src,imageConvert(),dest)
    return cmd
    
def addBannersTo(photos):
    for p in photos:
        if p==".DS_Store":
            continue
        
        fname=os.path.splitext(p)[0]
        if os.path.splitext(p)[1].lower()==".orf":
            fname+= ".jpg"
        else:
            fname+= os.path.splitext(p)[1]
        print "fname '%s'" %(fname)
        
        srcF   = os.path.join(os.path.dirname(path_to_watch),p)
        printF = os.path.join(os.path.dirname(path_to_print),fname)
        webF   = os.path.join(os.path.dirname(path_to_upload),fname)
        
        cmd = "convert " + srcF + imageMagicBanners  + " -bordercolor blue -border 100x100 " + printF 
        
        if dryRun:
            print "print command '%s'" %(cmd)
        else:
            if verbosity:
                print
                print "adding banners with '%s'" %(cmd)
                
            callImageMagick(cmd)
            
        #cmd = "convert " + srcF + imageMagicBanners + Polariod() + webF #+ " | convert " + webF + " -resize 640x480 " + webF
        cmd = Polariod(srcF,webF,imageMagicBanners,"Photograph ref: " + p) #+ " | convert " + webF + " -resize 640x480 " + webF
        if dryRun:
            print "resize command: %s" %(cmd)
        else:
            if verbosity :
                print "cmd %s" %(cmd)
                
            callImageMagick(cmd)

def callImageMagick(cmd):
    rv= os.system(cmd)
    if not rv==0:
        print "Error from imagemagick. "
        exit(1)
    

if __name__ == "__main__":
    main(sys.argv)
