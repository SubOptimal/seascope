import subprocess

def ct_query(filename):
	cmd = 'ctags -n -x -u'
	args = cmd.split()
	args.append(filename)
	proc = subprocess.Popen(args, stdout=subprocess.PIPE)
	(out_data, err_data) = proc.communicate()
	out_data = out_data.split('\n')
	res = []
	for line in out_data:
		if (line == ''):
			break
		line = line.split()
		line = [line[0], line[2], line[1]]
		res.append(line)
	return res
