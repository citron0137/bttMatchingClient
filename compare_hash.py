import sys
import os
import argparse
import requests
import json
import imagehash

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='compare a hash file with hashes saved in DB server')
    parser.add_argument('-p', '--path',
                        help='the path of hash file',
                        )
    
    results = parser.parse_args(args)
    return results.path

def get_origin_img_list():
	org_dic = {}

	url = "http://13.209.99.61:8080/original_img"
	r = requests.get(url)
	parsed_data = json.loads(r.text)

	for row in parsed_data:
		org_dic[row['original_movie_seq']] = []

	for row in parsed_data:
		org_hash = imagehash.hex_to_hash(row['img_hash'])
		org_img_name = row['img_path'].split('/')[1]
		org_dic[row['original_movie_seq']].append({org_hash : org_img_name})

	return org_dic, parsed_data


def get_target_img_list(hashFile):
	tar_dic = {}

	with open(hashFile, 'r') as f:
		rls = f.readlines()
		for i in rls:
			tar_hash = imagehash.hex_to_hash(i.split(' : ')[0])
			tar_img_name = i.split(' : ')[1]
			tar_dic[tar_hash] = tar_img_name

	return tar_dic

def compare(hashFile):
	org_dic, original_img_list = get_origin_img_list()
	tar_dic = get_target_img_list(hashFile)
	frameCompareDict = {}

	for original_movie_seq, framesList in org_dic.items():
		frameCompareDict[original_movie_seq] = []
		for eachFrame in framesList:
			for oh, oin in eachFrame.items():
				for th, tin in tar_dic.items(): 
					diff_hash = th-oh

					if diff_hash <= 5:
						frameCompareDict[original_movie_seq].append([tin[:-1], oin, diff_hash])

	for original_movie_seq in frameCompareDict:
		print("original movie sequence is " + str(original_movie_seq))
		if len(frameCompareDict[original_movie_seq]) == 0:
			print("Nothing")
		for similarFrame in frameCompareDict[original_movie_seq]:
			print(similarFrame)


if __name__ == '__main__':
	hashFile = check_arg(sys.argv[1:])
	result = compare(hashFile)