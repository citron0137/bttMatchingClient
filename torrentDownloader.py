######################################################################################
#
#   torrent file downloader
#		#fork from auto_downloader.py
#
######################################################################################

import libtorrent as lt
import time
import argparse
import os, sys

# Command line options
def check_arg(args=None):
    parser = argparse.ArgumentParser(description='download files using libtorrent')
    parser.add_argument('-t', '--torrents_directory',
                        help='directory path of torrent files',
                        )
    parser.add_argument('-o', '--output_directory',
                        help='output path that files will be downloaded')

    results = parser.parse_args(args)
    return (results.torrents_directory,
            results.output_directory,
            )


def download(t_dir, o_dir):
	ses = lt.session()
	ses.listen_on(6881, 6891)
	RATE = 100
	resultDict = {}


	with open('download_log.log','a+') as f:
		try:
			for path, dirs, files in os.walk(t_dir):
				cnt = 0
				for filename in files:
					cnt += 1
					print("Start to download " + filename)
					f.write("\nStart to download " + filename + " / " + str(cnt) + '\n')

					fullpath = os.path.join(path, filename)
					
					try:
						e = lt.bdecode(open(fullpath, 'rb').read())
						info = lt.torrent_info(e)

						#mkdir a directory having same name the torrent	
						save_path = o_dir + '/' + filename

						if not os.path.exists(save_path):
							os.mkdir(save_path)

						params = { 'save_path': save_path, \
						'storage_mode': lt.storage_mode_t.storage_mode_sparse, \
				        'ti': info }

						h = ses.add_torrent(params)
						h.set_sequential_download(False)

						s = h.status()

						#For excluding torrents having no seeds
						cntForTry = 0
						
						while (not s.is_seeding):
							if cntForTry > 120:
								f.write(filename + " : Pass(No or little seeds)\n")
								break

							s = h.status()

							'''
							state_str = ['queued', 'checking', 'downloading metadata', \
							        'downloading', 'finished', 'seeding', 'allocating']
							'''
							down_progress = s.progress * 100
							print('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
							        (down_progress, s.download_rate / 1000, s.upload_rate / 1000, \
							        s.num_peers, s.state))
							f.write('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
							        (down_progress, s.download_rate / 1000, s.upload_rate / 1000, \
							        s.num_peers, s.state)+'\n')

							if down_progress > RATE:
								print(str(RATE) + "%" + " download done")
								ses.remove_torrent(h)
								break

							if s.num_peers < 1:
								cntForTry += 1
							elif s.download_rate / 1000 < 100:
								cntForTry += 1
							
							time.sleep(1)

					#In the case that torrent file itself is wrong. (Almost based on wrong crawling)
					except Exception as e:
						if str(e) == "Success":
							down_progress = 0
							f.write("Fail : wrong torrent file")
							pass

					resultDict[filename] = down_progress
					
		except Exception as e:
			f.write(str(e))

	return (RATE, resultDict)


if __name__ == '__main__':
	t_dir, o_dir = check_arg(sys.argv[1:])
	download(t_dir, o_dir)