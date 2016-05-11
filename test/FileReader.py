#!/usr/bin/env python
# -*- coding:utf-8 -*-

def fileReader(file_name,line_num = 100):
	"get line_nums=100 lines"
	try:
		'do something'
		f1 = open(file_name,'r')
		f2 = open("%s_data.txt"%(file_name),'w')
		while line_num>0:
			line = f1.readline()
			if not line_num:
				break
			f2.write(line)
			f2.flush()

			line_num -= 1
		f1.close()
		f2.close()

	except Exception,e:
		print 'Exception:',e

def main():
	"main function"
	fileReader("activeuids_encoded.txt",1000)

if __name__ == '__main__':
	main()