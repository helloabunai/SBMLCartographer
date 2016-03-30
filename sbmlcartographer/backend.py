## Functions that are used generically/sporadically
## Or otherwise don't belong in the main flow
import os
import datetime

class SBMLCartographerError(Exception):
	pass

class Colour:

	def __init__(self):
		pass

	purple = '\033[95m'
	cyan = '\033[96m'
	darkcyan = '\033[36m'
	blue = '\033[94m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	bold = '\033[1m'
	underline = '\033[4m'
	end = '\033[0m'

class CartographerTest:

	def __init__(self):
		pass

	@staticmethod
	def dircheck(directory):
		if os.path.exists(directory): return True
		else: return False

	@staticmethod
	def filecheck(filepath):
		if os.path.isfile(filepath): return True
		else: return False

	@staticmethod
	def output_tree(outdir_root):
		## Ensures root output is a real directory
		## Generates folder name based on date (for run ident)
		date = datetime.date.today().strftime('%d-%m-%Y')
		time = datetime.datetime.now().strftime('%H%M%S')
		today = date + '-' + time

		## If the user specified root doesn't exist, make it
		## Then make the run directory for datetime
		if not os.path.exists(outdir_root):
			print '{}{}{}{}'.format(Colour.bold, 'sbmlc__', Colour.end, ' Creating output root... ')
			os.mkdir(outdir_root)
		run_dir = outdir_root + '/sbmlc_' + today
		print '{}{}{}{}'.format(Colour.bold, 'sbmlc__', Colour.end, ' Creating instance run directory.. ')
		os.mkdir(run_dir)

		## Inform user it's all gonna be okaaaayyyy
		print '{}{}{}{}{}'.format(Colour.bold, Colour.green, 'sbmlc__', Colour.end, ' Output directories OK!')
		return run_dir