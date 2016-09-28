# RunCmdsMP
Run system commands parallelly.


Usage: RUN system CoMmanDS in Multi-Processing
python RunCmdsMP.py [options] <commands.list>

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -p PROCESSORS, --processors=PROCESSORS
                        number of processors [default=2]
  -s SEPARATION, --separation=SEPARATION
                        separation between two commands [default="\n"]
  -c TO_BE_CONTINUE, --continue=TO_BE_CONTINUE
                        continue [1] or not [0] [default=1]
