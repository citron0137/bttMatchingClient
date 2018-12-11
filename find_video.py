import argparse
import os, sys

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='find a video file in sub files of the torrent')
    parser.add_argument('-t', '--target',
                        help='directory path of being searched',
                        )
    
    results = parser.parse_args(args)
    return results.target

def find_video(target):
	extensions = ['avi','mp4', 'mkv', 'asf', 'mpeg']

	print(os.listdir(target))

	for path,dirs,files in os.walk(target):
		for file in files:
			extension = file.split('.')[-1]
			if extension in extensions:
				sizeMB = int(os.path.getsize(path+'/'+file) / 1024 / 1024)
				return [file,path,extension,sizeMB,target]

	return 0

if __name__ == '__main__':
	target = check_arg(sys.argv[1:])
	find_video(target)