from time import sleep
from subprocess import call
from datetime import datetime
import sys
import os
import time
import shutil
import argparse
    
path_to_watch = "new/"
#path_to_watch = "/Users/ns/Dropbox/Pirates/new/"
path_to_raw = "original/"
path_to_print = "forPrinting/"
#path_to_print = "/Users/ns/Dropbox/Pirates/forPrinting/"
path_to_upload = "forUploading/"
process_initial_photos=False
shellCmd = True
    
def copyFile(fileName, srcPath, destPath):
    old_name=os.path.join(os.path.dirname(srcPath),fileName)
    new_name=os.path.join(os.path.dirname(destPath),fileName)
    shutil.copy(old_name,new_name)

def addLogo(logo,gravity):
    cmd=" -gravity " + gravity + " " + logo + " -composite "
    
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
        #+ addLogo("logo2.jpg","east")
        #cmd= " convert " + srcF + " -gravity southwest logo1.jpg -composite -gravity southeast logo2.jpg -composite "  + bannerF
        cmd= " convert " + srcF + addLogo("logo1.jpg","southwest") + addLogo("logo2.jpg","southeast") + bannerF
        if shellCmd:
            call( [cmd],shell=True)
        else:
            print "Silent mode: (%s)" %(cmd)
        
        # And finally resize the image to 640x480 for uploading to the web
        fname=os.path.splitext(fname)[0].lower() + "_sml" + os.path.splitext(fname)[1].lower()
        webF = os.path.join(os.path.dirname(path_to_upload),fname)
        cmd = "convert " + bannerF + " -resize 640x480 " + webF
        if shellCmd:
            call( [cmd],shell=True)
        else:
            print "Silent mode: (%s)" %(cmd)
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
    
    global path_to_watch
    global path_to_raw
    global path_to_print
    global path_to_upload 
    global process_initial_photos
    global shellCmd
    
    parser = argparse.ArgumentParser(description="Add banners to photo")
    parser.add_argument("-a", help="process pictures already existing in folder")
    parser.add_argument("-i", help="Folder to watch for pictures",type=string)    
    for opt,arg in opts:
        if opt in ("-a","/a"):
            process_initial_photos=True
        elif opt in ("-h", "--help", "/?"):
            parameters()
            exit()
        elif opt in ("-i","/i"):
            path_to_watch=arg
        elif opt in ("-p","/p"):
            path_to_print=arg
        elif opt in ("-o","/o"):
            path_to_raw=arg
        elif opt in ("-u","/u"):
            path_to_upload=arg
        elif opt in ("-q","/q"):
            imageMagick=False
        elif opt in ("-s","/s"):
            shellCmd=False
            print "should be in silent mode"
        else:
            print "Option ", opt, " not currently implemented"
    print "Looking for new images in %s \n\tsaving to %s\n\tprintable version at %s\n\tweb upload version %s" %(path_to_watch, path_to_raw, path_to_print, path_to_upload)
    
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


