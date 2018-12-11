######################################################################################
#
#   Main Stream File
#
#   Argv required 
#       Argv[1] : 'torrent_file seq'
#
#
#
######################################################################################
import sys
import os

import apiHandler
import torrentDownloader
import find_video
import iframe_extraction
import save_hash
import compare_hash

if __name__ == '__main__':
    #setting
    masterApi = apiHandler.Rest()
    
    os.mkdir('tmp')
    os.mkdir('tmp/torrent')
    os.mkdir('tmp/subFiles')
    os.mkdir('tmp/frames')
    
#start
    torrentSeq = sys.argv[1] #get torrent seq
    masterApi.updateTorrentState(torrentSeq, 'analyzing')   # torrent status update
    torrentFilePath = masterApi.downloadTorrentBySeq(torrentSeq, './tmp/torrent/')# torrent file download
    print(torrentFilePath)
    torrentFileName = torrentFilePath.split("/")[-1]

    #TODO download via torrent
    progress=0
    with open('downloadSubFile.log','a+') as f:
        progress = torrentDownloader.downloadSubFile('tmp/torrent/', torrentFilePath.split('/')[-1], 'tmp/subFiles',f)
    print(progress)

    #TODO find video file in downloaded files
    videos=[]
    videos.append(find_video.find_video('tmp/subFiles/'))
    print(videos)

    
    for video in videos:
        #TODO upload sub_file
        masterApi.insertSubfile(torrentSeq,video[0],video[3],video[2])

        #TODO extract frame from video file
        iframe_extraction.iframe_extract(video[1]+'/'+video[0],'tmp/frames')
        
        #TODO extract hash from framfile
        save_hash.hashing('tmp/frames'+'/'+video[0])

        #TODO matching frame hash wiht original hash #TODO uploade matched data
        compare_hash.compare('tmp/frames'+'/'+video[0]+'/'+video[0]+'.hash')

        

    #TODO delete folder
    os.system('rm -rf tmp')
