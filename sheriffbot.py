import copy, datetime, os, sys, timefrom pydc_client import pydc_clientdef filelist_analyse(filename,nick):	try:		print "Filelist download complete :", nick, filename		# Insert TimeStamp into Filename		oldfilename = filename[:-4] # ignore the trailing .bz2		now = datetime.datetime.now()		now = now.strftime(".%Y-%m-%d-%H-%M-%S.")		filename = filename.split(os.sep)		filename[-1] = filename[-1].split(".")		filename[-1][0] = filename[-1][0][1:]		filename[-1] = ".".join(filename[-1][:-2])+now+filename[-1][-2]		filename = os.sep.join(filename)		os.rename(oldfilename,filename)	except OSError:		print "OSError in Callback Function.", nick, filenameif __name__=="__main__":		config_data = { "mode":True, "name":"Lil Wayne", "host":"172.17.23.44","nick":"BigDick","pass":"banana","desc":"","email":"","sharesize":53687091200,"localhost":"172.17.14.6"}	c = pydc_client().configure(config_data).link({"mainchat":sys.stdout.write,"debug":[sys.stdout.write,open("debug.txt","w").write,None][2] }).connect("0/1/0");	c._config["overwrite"] = True	time.sleep(3); # Wait for the connection to established and session to be verified.	# c.cli();	c.connect('1')"""To share files, manually add them using ~self.filelist_add(<path>) and ~self.filelist_generate()"""