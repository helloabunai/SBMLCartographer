########################################################
##  Alastair Maxwell 		                          ##
##  alastair.maxwell@glasgow.ac.uk                    ##
##  University of Glasgow, Scotland                   ##
##  Keio University, Japan                            ##
########################################################

##
## Standard libraries
import sys
import os
import argparse
import logging as log

##
## App backend stuff
from backend import Colour as clr
from . import validation
from . import transmute

##
## Globals
VERBOSE = False
LOGGING = True
DEF_OUT = os.path.join(os.path.expanduser('~'),'SBMLC')

class SBMLCartographer:

	def __init__(self):

		##
		## Argparse for i/o
		self.parser = argparse.ArgumentParser(prog='sbmlc')
		input_group = self.parser.add_mutually_exclusive_group(required=True)
		input_group.add_argument('-r', '--reaction', help='Single input. Path to single SBMLC reaction map, or use stdin if left blank.', default=sys.stdin)
		input_group.add_argument('-b', '--batch', help='Multiple inputs. Path to a folder with multiple SMBLC Reaction Maps. No stdin support.')
		self.parser.add_argument('-v', '--verbose', help='Verbose output. If specified, terminal will print information about progress. Default: Off.', action='store_true')
		self.parser.add_argument('-w', '--webverify', help='Use the online SBML standard verification service. Experimental, recommend using offline.')
		self.parser.add_argument('-o', '--output', help='Output. Path to your desired output folder. Default: $HOME.', default=DEF_OUT)
		self.args = self.parser.parse_args()

		##
		## Check for arguments at all
		if not len(sys.argv) > 1:
			log.basicConfig(format='%(message)s', level=log.NOTSET)
			log.error('{}{}{}{}'.format(clr.red,'sbmlc__ ',clr.end,'No arguments provided! Exiting. (try -h)'))
			sys.exit(2)
		if self.args.verbose:
			log.basicConfig(format='%(message)s', level=log.DEBUG)
			log.info('{}{}{}{}'.format(clr.bold,'sbmlc__ ',clr.end,'SBMLCartographer v0.01.'))
			log.info('{}{}{}{}'.format(clr.bold,'sbmlc__ ',clr.end,'alastair.maxwell@glasgow.ac.uk'))

		##
		## Begin processing
		self.sanitise_input()
		#self.validate_reactions()
		#self.extract_compartments()
		#self.transform_data()
		#self.process_output()

	def sanitise_input(self):

		if not 'stdin' in str(self.args.reaction):
			print 'file'
		else:
			print 'stdin', self.args.reaction






def main():
	SBMLCartographer()



