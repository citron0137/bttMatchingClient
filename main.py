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


if __name__ == '__main__':
    #setting
    masterApi = apiHandler.Rest()
    '''
    os.mkdir('tmp')
    os.mkdir('tmp/torrent')
    '''
    os.mkdir('tmp/subFiles')
    #start
    torrentSeq = sys.argv[1] #get torrent seq
    masterApi.updateTorrentState(torrentSeq, 'analyzing')   # torrent status update
    torrentFilePath = masterApi.downloadTorrentBySeq(torrentSeq, './tmp/torrent/')# torrent file download

    #TODO download video via torrent
    torrentDownloader.download(torrentFilePath, './tmp/subFiles')

    #TODO extract frame from video file

    #TODO delete video file

    #TODO extract hash from framfile

    #TODO matching frame hash wiht original hash

    #TODO uploade matched data