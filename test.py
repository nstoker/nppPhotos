from time import sleep
from subprocess import call
from datetime import datetime
import sys
import os
import time
import shutil

path_to_watch = "new/"
#path_to_watch = "/Users/ns/Dropbox/Pirates/new/"
path_to_raw = "original/"
path_to_print = "forPrinting/"
#path_to_print = "/Users/ns/Dropbox/Pirates/forPrinting/"
path_to_upload = "forUploading/"

def copyFile(fileName, srcPath, destPath):
    old_name=os.path.join(os.path.dirname(srcPath),fileName)
    new_name=os.path.join(os.path.dirname(destPath),fileName)
    shutil.copy(old_name,new_name)

def addLogo(logo,gravity=None):
    cmd=" "
    if gravity=="east":
        cmd= "-gravity east "
    cmd+="-append " + logo + " "
    
    return cmd
    
        
def addBanners(added):
    # Adds banners to pics, 
    for f in added:
        print "Processing %s ..." %(f)
        copyFile(f, path_to_watch, path_to_raw)
        srcF = os.path.join(os.path.dirname(path_to_watch),f)
        destF=os.path.splitext(f)[0]
        
        if os.path.splitext(f)[1].lower()==".orf":
            destF+= ".jpg"
        else:
            destF+= os.path.splitext(f)[1]
        destF = os.path.join(os.path.dirname(path_to_print),destF)
        #+ addLogo("logo2.jpg","east")
        cmd= " convert " + srcF + " -gravity southwest logo1.jpg -composite -gravity southeast logo2.jpg -composite "  + destF
        print cmd
        call( [cmd],shell=True)
        
        
        
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

def main():
    before = dict({})
    #before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
      time.sleep (10)
      after = dict ([(f, None) for f in os.listdir (path_to_watch)])
      added = [f for f in after if not f in before]
      #removed = [f for f in before if not f in after]
      if added: 
          print "Added: ", ", ".join (added)
          addBanners( added)
      #if removed: print "Removed: ", ", ".join (removed)
      before = after
        
print "Main code starts here. But we're not doing anything at present..."
main()

