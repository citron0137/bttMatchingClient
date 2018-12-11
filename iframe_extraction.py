'''
iframe_extract.py - download video and ffmpeg i-frame extraction
Usage: 
(ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c
This code does two things:
1. Download using youtube-dl
2. Extract i-frames via ffmpeg
'''

from __future__ import unicode_literals
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
import os
import subprocess
import argparse

# -s : size

def iframe_extract(inFile,outFolder):

# extract i-frame using ffmpeg
# ffmpeg -i inFile -f image2 -vf \
#   "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr oString%03d.png

    # infile : video file name 
    #          (ex) 'FoxSnowDive-Yellowstone-BBCTwo.mp4'

    #create folder per each file
    with open('frame_log.log','a+') as f:
        inFile = '"' + inFile.replace('/', '"/"') + '"'
        tempIn = inFile.split('/')[-1]
        outFolder = outFolder + '/' + tempIn
        
        f.write("outFolder : " + outFolder + "\n")
        f.write("inFile : " + inFile + "\n\n")

        if not os.path.exists(outFolder):
            os.mkdir(outFolder)
    
    # start extracting i-frames
    inFile = inFile.replace('"','')
    clip = VideoFileClip(inFile)
    movie_length = int(clip.duration)

    if int(movie_length * 0.05) >= 300:
        start = 300
        end = movie_length-300
    else:
        start = int(movie_length * 0.05)
        end = movie_length - (movie_length * 0.05)    

    try:
        if os.path.isfile(inFile):
            imgFilenames = outFolder + '/%05d.png'
            cmd = ["ffmpeg",'-i', inFile,'-f', 'image2','-vf',
                "select='eq(pict_type,PICT_TYPE_I)'",'-vsync','vfr',
                '-ss', str(start), '-t', str(end), imgFilenames]
            # create iframes
            subprocess.call(cmd)
        
        elif os.path.isdir(inFile):
            for file in os.listdir(inFile):
                eachFolder = file.replace(" ","")
                eachFolder = eachFolder.replace("'","")

                try:
                    if not os.path.exists(outFolder + "/'" + eachFolder + "'"):
                        os.system("mkdir "+ outFolder + "/'" + eachFolder + "'")
                except:
                    pass

                imgFilenames = outFolder + "/" + eachFolder + "/%05d.png"

                cmd = ["ffmpeg",'-i', os.path.join(inFile,file), '-f', 'image2','-vf',
                "select='eq(pict_type,PICT_TYPE_I)'",'-vsync','vfr',
                '-ss', str(start), '-t', str(end), imgFilenames]

                # create iframes
                subprocess.call(cmd)
        else:
            print(inFile)
    except Exception as e:
        print(e)


def check_arg(args=None):

# Command line options
# If a path contains blank, you should add ''

    parser = argparse.ArgumentParser(description='extract iframe from downloaded video')
    '''
    parser.add_argument('-u', '--url',
                        help='download url',
                        )
    '''
    parser.add_argument('-o', '--outfolder',
                        help='output folder name for iframe images')
    parser.add_argument('-i', '--infile',
                        help='input to iframe extract')

    results = parser.parse_args(args)
    return (results.infile, results.outfolder)

'''
Usage sample:
    syntax: python iframe_extract.py -i path -o path
'''

if __name__ == '__main__':
    i,o = check_arg(sys.argv[1:])
    #changed_frame_extract(i)
    iframe_extract(i,o)
