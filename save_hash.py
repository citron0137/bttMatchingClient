import argparse
import os, sys
from PIL import Image
import imagehash


def check_arg(args=None):
    parser = argparse.ArgumentParser(description='save hashes of frames into a txt hashfile')
    parser.add_argument('-f', '--folder',
                        help='the folder containing frames',
                        )
    
    results = parser.parse_args(args)
    return results.folder

def hashing(folder):
	org_dic = {}
	count = 0
	img_count = 0
	
	try :
		#0 : black box doesn't exist
		#1 : black box exists
		black_flag = black_box_check(folder)

		#number of frames in the folder
		img_count = len(os.listdir(folder))

		hashfile = folder + '/"' + folder.split('/"')[-1] + '.hash'

		print ("================== extract imghash ==================\n")

		img_extension = ['png', 'jpg', 'bmp']

		for filename in os.listdir(folder):
			file_ext = filename.split('.')[-1]
			if file_ext in img_extension:
				count += 1
				
				org_img = Image.open(folder + "/" + filename)
				phash = img_resize(org_img, black_flag)
				org_dic[phash] = filename
				
				printProgress(count, img_count, "", "", 1, 50)

		print ("\n=============== save imagehash info ==================\n")

		with open(hashfile, "w") as f:
			for key,value in org_dic.items():
				f.write(str(key) + " : " + str(value)+ "\n")

	except OSError as os_error:
		print ("OSError : " ,os_error)

	return 0

def black_box_check(file_path):

	black_box_list = []
	black_flag = 1
	count = 0
	try :
		for filename in os.listdir(file_path): #원본 이미지에서 검정박스 여부 확인
			#If the extension is an image file
			if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.bmp') :
				img = Image.open(file_path + "/" + filename)
				cropped_img = crop_img(img)
				extrema = cropped_img.convert("L").getextrema()
				
				if sum(extrema) in range(0,30):
					black_box_list.append("O")
					count = count + 1		
				else:
					black_box_list.append("X")
					count = count + 1

				if (count >= 100):
					break
	except OSError as os_error:
		print ("OSError" ,os_error)
		pass

	for black_box in black_box_list:
		if (black_box == "X"):
			black_flag = 0
			break

	return black_flag


def crop_img(img):
	
	img_width, img_height = img.size
	crop_img = ''
	#if width == 1920 and height == 1080 => rate 0.125
	if (img_width == 1920 or img_width == 1280 or img_width == 720):
		crop_img = img.crop(( int(img_width//2) - int(img_width/10) , 0, int(img_width//2) + int(img_width/10) , int(img_height * 0.05)))
	else:
		with open('error_log.txt', 'a') as f:
			f.write("image width error : " + str(img.filename).replace('.//', '') + " : " + str(img_width) + " " + str(img_height) + '\n')
		crop_img = img
	return crop_img


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100): 
	formatStr = "{0:." + str(decimals) + "f}" 
	percent = formatStr.format(100 * (iteration / float(total))) 
	filledLength = int(round(barLength * iteration / float(total))) 
	bar = '#' * filledLength + '-' * (barLength - filledLength) 
	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)), 

	if iteration == total: 
		sys.stdout.write('\n') 
	sys.stdout.flush()

#이미지 리사이즈하기
def img_resize(img, img_black_flag):
	#검정 박스가 있는 경우
	width, height = img.size

	if img_black_flag:

		if ( (width == 1920 and ( 1030 <= height or height <= 1080) or 
			(width == 1280 and (685 <= height or height <= 720) ))):
			cropped_img = img.crop((0, int(height * 0.125), width, height - int(height * 0.125) ))
			cropped_img = cropped_img.resize((1920, 1080), Image.ANTIALIAS)
			phash = imagehash.phash(cropped_img)
		
		elif (width == 720 and 455 <= height and height <= 480):
			#cropped_img = img.crop((width//2 - 250, height//2 - 150, width//2 + 250, height//2 + 150))
			cropped_img = img.crop((0,  int(height * 0.075), width, height - int(height * 0.075) ))
			cropped_img = cropped_img.resize((1920, 1080), Image.ANTIALIAS)
			phash = imagehash.phash(cropped_img)

		#아직 구현 안됨
		else :
			with open('error_log.txt', 'a') as f:
				f.write("blackbox error : " + str(img.filename).replace('.//', '') + " : " + str(img_width) + " " + str(img_height) + '\n')

	#이미지의 검정 박스가 존재하지 않는 경우
	else :
		img = img.resize((1920, 1080), Image.ANTIALIAS)
		phash = imagehash.phash(img)
	
	return phash

if __name__ == '__main__':
	folder = check_arg(sys.argv[1:])
	hashing(folder)