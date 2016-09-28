#!/bin/env python
#coding utf-8
'''RUN system CoMmanDS in Multi-Processing'''
import sys
import os
import subprocess
import pp
from optparse import OptionParser

__version__ = '1.0'
def file2list(cmd_file, sep="\n"):
	if not os.path.exists(cmd_file) or not os.path.getsize(cmd_file):
		cmd_list = []
	else:
		f = open(cmd_file, 'r')
		cmd_list = f.read().split(sep)
	return [cmd for cmd in cmd_list if cmd]

def run_cmd(cmd):
	job = subprocess.Popen(cmd,stdout=subprocess.PIPE,\
							stderr=subprocess.PIPE,shell=True)
	output = job.communicate()
	status = job.poll()
	return output + (status,)

def submit_pp(cmd_file, processors=1, cmd_sep="\n", cont=True):
	if not '\n' in cmd_sep:
		cmd_sep += '\n'
	if not os.path.exists(cmd_file):
		raise IOError('Commands file : %s does NOT exist.'% (cmd_file, ))
	cmd_cpd_file = cmd_file + '.completed'
	cmd_list = file2list(cmd_file, cmd_sep)
	cmd_cpd_list = file2list(cmd_cpd_file, cmd_sep)
	if cont:
		cmd_uncpd_list = sorted(list(set(cmd_list)-set(cmd_cpd_list)), \
							key=lambda x: cmd_list.index(x))

	else:
		cmd_uncpd_list = sorted(list(set(cmd_list)), \
								key=lambda x: cmd_list.index(x))
		# not continue, so NONE completed
		cmd_cpd_list = []

	print '''
	total commands:\t%s
	skipped commands:\t%s
	retained commands:\t%s
	''' % (len(set(cmd_list)), \
	len(set(cmd_list))-len(cmd_uncpd_list), \
	len(cmd_uncpd_list))

	# start pp
	ppservers = ()
	job_server = pp.Server(processors, ppservers=ppservers)
	jobs = [(cmd, job_server.submit(run_cmd, (cmd,), (), ('subprocess',))) \
			for cmd in cmd_uncpd_list]
	# recover stdout, stderr and exit status
	cmd_out_file, cmd_err_file, cmd_warn_file = \
	cmd_file + '.out', cmd_file+'.err', cmd_file+'.warning'
	if cont:
		i = len(set(cmd_list))-len(cmd_uncpd_list)
		mode = 'a'
	else:
		i = 0
		mode = 'w'
	f = open(cmd_cpd_file, mode)
	f_out = open(cmd_out_file, mode)
	f_err = open(cmd_err_file, mode)
	f_warn = open(cmd_warn_file, mode)
	for cmd, job in jobs:
		i += 1
#		f = open(cmd_cpd_file, 'a')
#		f_out = open(cmd_out_file, 'a')
#		f_err = open(cmd_err_file, 'a')
#		f_warn = open(cmd_warn_file, 'a')
		f.write(cmd + cmd_sep)
		out, err, status = job()
		f_out.write('CMD_%s_STDOUT:\n' % i + out + cmd_sep)
		f_err.write('CMD_%s_STDERR:\n' % i + err + cmd_sep)
		if not status == 0:
			f_warn.write(cmd + cmd_sep)
	f.close()
	f_out.close()
	f_err.close()
	f_warn.close()

	job_server.print_stats()

def main():
	usage = __doc__ + "\npython %prog [options] <commands.list>"
	parser = OptionParser(usage, version="%prog " + __version__)
	parser.add_option("-p","--processors", action="store",type="int",\
					dest="processors", default=2, \
					help="number of processors [default=%default]")
	parser.add_option("-s","--separation", action="store", type="string",\
					dest="separation", default='\n', \
					help='separation between two commands [default="\\n"]')
	parser.add_option("-c","--continue", action="store", type="int",\
					dest="to_be_continue", default=1, \
					help="continue [1] or not [0] [default=%default]")
	(options,args)=parser.parse_args()
	if not args:
		parser.print_help()
		sys.exit()
	cmd_file = args[0]
	processors = options.processors
	separation = options.separation
	to_be_continue = options.to_be_continue
	submit_pp(cmd_file, processors=processors, \
				cmd_sep=separation, cont=to_be_continue)

if __name__ == '__main__':
	main()
