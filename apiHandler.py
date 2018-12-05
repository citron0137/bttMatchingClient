######################################################################################
#
#   Api Handler (for bttMasterApiServer)
#		#fork from call_rest.py
#
#   function list
#       * get data from db
#       * insert, delete, update db data
#       * .torrent file download n update status
#
######################################################################################

import requests
import urllib

class Rest:

	def __init__(self):
		self.base_url = 'http://13.209.99.61:8080/'

	def get(self, param):
		response = requests.get(self.base_url + param)
		data = response.json()

		return data

	def post(self, query, data):
		try:
			response = requests.post(self.base_url+query, json=data)
		except Exception as e:
			print(self.base_url+query)
			print(e)
		return response

	def patch(self, param):
		response = requests.patch(self.base_url + param)
		data = response.json()

		return data

	def downloadTorrentBySeq(self, seq, directory):
		param = "torrent_file/"+seq
		torrentFileInfo=self.get(param)
		fileName = torrentFileInfo["infohash"]
		url = self.base_url + "torrent_file/downloadFile/"+fileName ## Later we should change
		url = urllib.request.quote(url.encode('utf8'), '/:')
		url = url.replace(" ","%20")
		print(url)
		try:
			path = directory + '/'+ fileName
			urllib.request.urlretrieve(url, path)
			return path
		except Exception as e:
			print(e)
			return url


	'''
	If result is
		'None' means there is no row not processed.
		a list means the seq #s not processed'''


	def torrentIsNone(self):
		param = "torrent_file/"
		try:
			data = self.get(param)
		except requests.exceptions.RequestException as e:
			print(e)
			sys.exit(1)

		seqs = []
		for row in data:
			if row['state'] == 0:
				seqs.append([row['seq'], row['infohash']])

		if len(seqs) > 0:
			return seqs
		else:
			return None


	def updateTorrentState(self, seq, state):
		status_dict = {'none' : '0', 'analyzing' : '1', 'done' : '2', 'fail' : '3'}
		response = self.patch('torrent_file/'+str(seq)+'/?state='+status_dict[state])
		return response


	def insertSubfile(self, tseq, file, size, ext):
		postdata = {'torrent_file_seq':tseq, 'file_name':file, 'file_size':size, 'file_extension':ext}
		print(postdata)

		response = self.post('sub_file', postdata)
		return response


	def sendHashFile(self, filePath):
		try:
			with open(filePath,'rb') as file:
				postFile = {'file' : file}
				print(file)
				response = requests.post(self.base_url+'hash_file/uploadFile', files=postFile)
				#response = requests.post(self.base_url+'hash_file/upload', files=postFile)
				print(response)
		except Exception as e:
			print(e)

		return response



if __name__ == '__main__':
	for i in range(8736,9000):
		response = Rest().updateState(i,'none')

	#Rest().sendFile('./frames/"On.Your.Wedding.Day.2018.720p.HDRip.H264.AAC-PCHD.mp4"/"On.Your.Wedding.Day.2018.720p.HDRip.H264.AAC-PCHD.mp4".hash')

	#response = Rest().updateState(36, 'fail')