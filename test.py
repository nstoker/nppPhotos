from time import sleep
from subprocess import call
from datetime import datetime
import sys
import os
import time
import shutil
import argparse
from PIL import Image
    
path_to_watch = "new/"
#path_to_watch = "/Users/ns/Dropbox/Pirates/new/"
path_to_raw = "original/"
path_to_print = "forPrinting/"
#path_to_print = "/Users/ns/Dropbox/Pirates/forPrinting/"
path_to_upload = "forUploading/"
process_initial_photos=True
shellCmd = False
message_text="28 June 2014"
    
def copyFile(fileName, srcPath, destPath):
    old_name=os.path.join(os.path.dirname(srcPath),fileName)
    new_name=os.path.join(os.path.dirname(destPath),fileName)
    shutil.copy(old_name,new_name)

def addLogo(logo,gravity):
    cmd=" -gravity " + gravity + " " + logo + " -composite "
    
    return cmd
    
def addText(text,gravity,width,height):
    #-font Palatino-Bold -pointsize 72 -draw "text 25,60 'Linux and Life'" -channel RGBA -gaussian 0x6 -fill black -stroke red -draw "text 20,55 'Linux and Life'"
    cmd = " -background RoyalBlue5 -fill white -gravity center -size " + width+"x"+height 
    cmd+= " caption: ' " + text + " ' + swap "
    
    return cmd    
        
def bannerise(added):
    for f in added:

        if (f==".DS_Store"):
            continue

        print "Processing %s ..." %(f)
        copyFile(f, path_to_watch, path_to_raw)
        srcF = os.path.join(os.path.dirname(path_to_watch),f)
        fname=os.path.splitext(f)[0]
        
        if os.path.splitext(f)[1].lower()==".orf":
            fname+= ".jpg"
        else:
            fname+= os.path.splitext(f)[1]
        bannerF = os.path.join(os.path.dirname(path_to_print),fname)
        #im=Image.open(srcF)
        #width,height = im.size()
        #+ addLogo("logo2.jpg","east")
        #cmd= " convert " + srcF + " -gravity southwest logo1.jpg -composite -gravity southeast logo2.jpg -composite "  + bannerF
        cmd= " convert " + srcF + addLogo("logo1.jpg","southwest") + addLogo("logo2.jpg","southeast")
        cmd+= addLogo("text.jpg","south") + " -bordercolor none -border 100x100 " + bannerF
        if shellCmd:
            call( [cmd],shell=True)
        else:
            print "Silent mode: (%s)" %(cmd)
        
        # And finally resize the image to 640x480 for uploading to the web
        fname=os.path.splitext(fname)[0].lower() + "_sml" + os.path.splitext(fname)[1].lower()
        webF = os.path.join(os.path.dirname(path_to_upload),fname)
        cmd="convert -caption '" + os.path.splitext(fname)[0] + "' " + srcF + addLogo("logo1.jpg","southwest") + addLogo("logo2.jpg","southeast") + addLogo("text.jpg","south") + " -gravity center -background none +polaroid " + webF + " | convert " + webF + " -resize 640x480 " + webF
        if shellCmd:
            call( [cmd],shell=True)
        else:
            print "Silent mode: (%s)" %(cmd)
        
        # a new finally - modify printable version to have a border
        cmd = "convert " + bannerF +  " -bordercolor none -border 100x100 " + bannerF
        
        print "\t%s done." %(f)


            
# Borrowed code for ideas
def photo_tweet():  
    i = datetime.now()  
    now = i.strftime('%Y%m%d-%H%M%S')  
    tweettime = i.strftime('%Y/%m/%d %H:%M:%S')  
    photo_name = now + '.jpg'  
    cmd = 'raspistill -t 500 -w 1024 -h 768 -o /home/pi/' + photo_name      
    print 'cmd ' +cmd  
    print "about to take photo"  
    call ([cmd], shell=True)  
    print "photo taken"  
    photo_path = '/home/pi/' + photo_name  
    status = tweet_text + ' #optionalhashtag ' + tweettime   
  
# Add text overlay of data on the photo we just took  
    print "about to set overlay_text variable"
    overlay_text = "/usr/bin/convert %s -pointsize 36 -fill white -annotate +40+728 '%s' -pointsize 36 -fill white -annotate +40+630 '%s' %s" % (photo_path, tweettime, "Your Text annotation here", photo_path)
  
    print "overlaying text"  
    call ([overlay_text], shell=True)  
  
    print "adding your logo" # you'll need a file called overlay.png in /home/pi  
    overlay_text = '/usr/bin/convert '+ photo_path + ' /home/pi/overlay.png -geometry +1+1 -composite ' + photo_path  
    call ([overlay_text], shell=True)  
    print "added logo 1"  
  
    print "tweeting photo"  
    api.update_with_media(photo_path, status=status)      
    print "photo tweeted, deleting .jpg"  
    cmd = 'rm ' + photo_path   
    call ([cmd], shell=True) 

def parameters():
    print sys.argv[0], "-i<folder to monitor> -p<folder> -u<folder> -o<folder>"
    print "\t-a"
    print "i folder\tFolder to monitor for new photographs"
    print "p folder\tFolder to put printable photographs"
    print "u folder\tFolder to put uploadable images"
    print "o folder\tFolder to save orginal images"
    print 
    print "a\tProcess orginal contents of folder"
    
    print

def main(argv):
    
    print "Looking for new images in %s \n\tsaving to %s\n\tprintable version at %s\n\tweb upload version %s" %(path_to_watch, path_to_raw, path_to_print, path_to_upload)
    
    # Create text banner first as image...
    cmd = "convert -size 2000x300 xc:pink -pointsize 300 -gravity center -undercolor royalblue -stroke none -strokewidth 1 -fill gold -annotate +0+0 ' " + message_text +" ' -trim +repage -shave 1x1 text.jpg"
    call( [cmd], shell=True)
    
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    print "Initial images ", ", ".join(before)
    
    notify=True
    if process_initial_photos:
        bannerise(before)
    else:
        print "not processing images already in the folder"
    while 1:
        after = dict ([(f, None) for f in os.listdir (path_to_watch)])
        added = [f for f in after if not f in before]
        #removed = [f for f in before if not f in after]
        if added: 
            print "Added: ", ", ".join (added)
            bannerise(added)
            notify=True
        #if removed: print "Removed: ", ", ".join (removed)
        
        if notify:
            print "Waiting for more photo's to be added to %s." %(path_to_watch)
            notify=False
        before = after
        break
        time.sleep (10)
        

if __name__ == "__main__":
    print
    print sys.argv[0], "running"
    print
    main(sys.argv[1:])


