# A script to watch a folder for images getting added
#
# the orginal will be copied to a folder (for safety...)
# logos and/or text added to specified positions and saved in a print folder
# images resized for web usage

    # Check for parameters
    # Usage:
    # photos.py folder-to-watch folder-to-backup [-w folder-for-web ] [options]
    #
    # Options
    # -l filename position [size] add logo to position. Position ne, n, nw, w, sw, s, se, e. Size will resized
    # -t text position [-bc background colour] [-tc text colour] [-ts shadow] [-tf text font]
    # -ignore  ignore any images already in folder 

ignore_existing=true
path_to_watch="new/"

def main():
    
    
    if ignore_existing:
        before = dict {}
    else:
        before = dict ([(f, None) for f in os.listdir (path_to_watch)])
        
    