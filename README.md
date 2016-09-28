# RunCmdsMP
Run system commands parallelly.


	Usage: RUN system CoMmanDS in Multi-Processing
	python RunCmdsMP.py [options] \<commands.list>

	Options:  
	  --version             show program's version number and exit  
	  -h, --help            show this help message and exit  
	  -p PROCESSORS, --processors=PROCESSORS  
                        number of processors [default=2]  
	  -s SEPARATION, --separation=SEPARATION  
                        separation between two commands [default="\n"]  
	  -c TO_BE_CONTINUE, --continue=TO_BE_CONTINUE  
                        continue [1] or not [0] [default=1]  

# Tutorial in English
If you have a command list file (e.g. commands.list) like this:

		bowtie2 -x ref.fa -1 a.1.fq -2 a.2.fq -S a.sam
		bowtie2 -x ref.fa -1 b.1.fq -2 b.2.fq -S b.sam
		bowtie2 -x ref.fa -1 c.1.fq -2 c.2.fq	-S c.sam
		bowtie2 -x ref.fa -1 d.1.fq -2 d.2.fq	-S d.sam
		....
