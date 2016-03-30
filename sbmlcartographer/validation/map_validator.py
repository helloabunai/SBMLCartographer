########################################################
##  Alastair Maxwell 		                          ##
##  alastair.maxwell@glasgow.ac.uk                    ##
##  University of Glasgow, Scotland                   ##
##  Keio University, Japan                            ##
########################################################

## Code slightly adapted from Systems Biology Markup Language
## http://sbml.org/validator/api/#python
## Majority credit to the following authors:

## @author  Akiya Jouraku (translated from libSBML C++ examples)
## @author  Ben Bornstein
## @author  Michael Hucka
## This sample program is distributed under a different license than the rest
## of libSBML.  This program uses the open-source MIT license, as follows:
##
## Copyright (c) 2013-2014 by the California Institute of Technology
## (California, USA), the European Bioinformatics Institute (EMBL-EBI, UK)
## and the University of Heidelberg (Germany), with support from the National
## Institutes of Health (USA) under grant R01GM070923.  All rights reserved.
##
## Permission is hereby granted, free of charge, to any person obtaining a
## copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
## THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.
##
## Neither the name of the California Institute of Technology (Caltech), nor
## of the European Bioinformatics Institute (EMBL-EBI), nor of the University
## of Heidelberg, nor the names of any contributors, may be used to endorse
## or promote products derived from this software without specific prior
## written permission.

class ValidationFlow:

	def __init__(self):

		self.hi = 'hi'

##TODO turn this into a class which takes in validator type (off/online) as input, recycle code..

import os.path
import time
import libsbml

numinvalid = 0

def setnuminvalid(n):
    global numinvalid
    numinvalid += n


def getnuminvalid():
    return numinvalid


def offlinevalidate(appdir, config):

    sbmlfile = config.config_dict['@reaction_map']

    start = time.time()
    sbmldoc = libsbml.readSBML(sbmlfile)
    stop = time.time()
    timeread = (stop - start)*1000
    errors = sbmldoc.getNumErrors()

    seriouserrors = False

    numreaderr = 0
    numreadwarn = 0
    errmsgread = ""

    if errors > 0:
        for i in range(errors):
            severity = sbmldoc.getError(i).getSeverity()
            if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
                seriouserrors = True
                numreaderr += 1
            else:
                numreadwarn += 1

            errmsgread = sbmldoc.getErrorLog().toString()

    ## If serious errors are encountered while reading an SBML document, it
    ## does not make sense to go on and do full consistency checking because
    ## the model may be nonsense in the first place.

    numccerr = 0
    numccwarn = 0
    errmsgcc = ""
    skipcc = False
    timecc = 0.0

    if seriouserrors:
        skipcc = True
        errmsgread += "Further consistency checking and validation aborted."
        setnuminvalid(1)
    else:
        sbmldoc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, False)
        start = time.time()
        failures = sbmldoc.checkConsistency()
        stop = time.time()
        timecc = (stop - start)*1000

        if failures > 0:

            isinvalid = False
            for i in range(failures):
                severity = sbmldoc.getError(i).getSeverity()
                if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
                    numccerr += 1
                    isinvalid = True
                else:
                    numccwarn += 1

            if isinvalid:
                setnuminvalid(1)

            errmsgcc = sbmldoc.getErrorLog().toString()

    ## Save results to string
    ## Output string to file

    validationresult = "                 filename : %s" % sbmlfile + "\n"
    validationresult += "         file size (byte) : %d" % os.path.getsize(sbmlfile) + "\n"
    validationresult += "           read time (ms) : %f" % timeread + "\n"

    if not skipcc:
        validationresult += "        c-check time (ms) : %f" % timecc + "\n"
    else:
        validationresult += "        c-check time (ms) : skipped" + "\n"

    validationresult += "      validation error(s) : %d" % (numreaderr + numccerr) + "\n"
    if not skipcc:
        validationresult += "      consistency error(s): %d" % numccerr + "\n"
    else:
        validationresult += "     consistency error(s): skipped" + "\n"

    validationresult += "    validation warning(s) : %d" % (numreadwarn + numccwarn) + "\n"
    if not skipcc:
        validationresult += "    consistency warning(s): %d" % numccwarn + "\n"
    else:
        validationresult += "   consistency warning(s): skipped" + "\n"

    if errmsgread or errmsgcc:
        validationresult += "\n"
        validationresult += "===== validation error/warning messages =====\n"
    if errmsgread:
        validationresult += errmsgread + "\n"
    if errmsgcc:
        validationresult += "*** consistency check ***\n"
        validationresult +=  errmsgcc + "\n"

    valoutfile = (appdir + "/output/validation_out.txt")
    validationoutput = open(valoutfile, "w")
    validationoutput.write(validationresult)
    validationoutput.close()