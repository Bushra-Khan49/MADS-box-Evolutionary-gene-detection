
MEGA (Molecular Evolutionary Genetics Analysis) Computational Core
Authors: Koichiro Tamura, Glen Stecher, and Sudhir Kumar
URL: http://www.megasoftware.net/
License: See the usageAgreement.txt file
 
MEGA-CC is the command-line version of MEGA that implements its core
analysis functions and is useful for iterative and automated execution.
MEGA-CC requires as input, a MEGA Analysis Options (.mao) file which can only
be generated using the MEGA X GUI application. The .mao file specifies the 
analysis to run as well as the analysis settings to use. If you do not already
have MEGA X, it can be downloaded from http://www.megasoftware.net. The MEGA X
GUI application also contains documentation and a tutorial for using MEGA-CC.

An example of how to run MEGA-CC is:

  megacc -a myMaoFile.mao -d mySequenceAlignment.fas -o myOutput

In addition to the megacc binary executable, a folder of example data 
files (Examples), a usageAgreement.txt file, and a man page (megacc.1) are included in the MEGA-CC
archive.

