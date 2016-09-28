## RunCmdsMP
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
	bowtie2 -x ref.fa -1 c.1.fq -2 c.2.fq -S c.sam
	bowtie2 -x ref.fa -1 d.1.fq -2 d.2.fq -S d.sam
	....
you can run them parallelly using RunCmdsMP:  

	python RunCmdsMP.py commands.list
These commands will run two by two (default), and each command uses one processor.
You can use more processors, e.g.:

	python RunCmdsMP.py commands.list -p 8
When all commands are finished, four files will be created:
	
	commands.list.completed		completed commands
	commands.list.err			stderr from the commands
	commands.list.out			stdout from the commands
	commands.list.warning		commands with exit status not equal to 0
	
If the run is unexpectedly halted, you can continue to run:
	
	python RunCmdsMP.py commands.list -c 1
or

	python RunCmdsMP.py commands.list
or some errors occured:

	python RunCmdsMP.py commands.list.warning
	
Not only "\n" but also other characters could be used as the separator. For a command list file (e.g. commands.list) like this:

	bowtie2 -x ref.fa -1 a.1.fq -2 a.2.fq -S a.sam
	samtools view -bS a.sam | samtools sort - a.sort
	^-^
	bowtie2 -x ref.fa -1 b.1.fq -2 b.2.fq -S b.sam
	samtools view -bS b.sam | samtools sort - b.sort
	^-^
	bowtie2 -x ref.fa -1 c.1.fq -2 c.2.fq -S c.sam
	samtools view -bS c.sam | samtools sort - c.sort
	^-^
	bowtie2 -x ref.fa -1 d.1.fq -2 d.2.fq -S d.sam
	samtools view -bS d.sam | samtools sort - d.sort
	^-^
	....
you can run:

	python RunCmdsMP.py commands.list -s "^-^"
	
The command list file can be easily creadted using a loop in Linux shell:

	cat sample.list | while read SAMPLE
	do
		echo "bowtie2 -x ref.fa -1 $SAMPLE.1.fq -2 $SAMPLE.2.fq -S $SAMPLE.sam"
		echo "samtools view -bS $SAMPLE.sam | samtools sort - $SAMPLE.sort"
		echo "^-^"
	done > commands.list
or using other any mehtods.
	
In sample.list, there is:

	a
	b
	c
	d
	...

#中文教程
首先做一个要运行的命令文件(commands.list),设定好命令块间的分隔符,然后运行即可:

	python RunCmdsMP.py commands.list
	
比如说有个命令文件如下:

	bowtie2 -x ref.fa -1 a.1.fq -2 a.2.fq -S a.sam
	samtools view -bS a.sam | samtools sort - a.sort
	^-^
	bowtie2 -x ref.fa -1 b.1.fq -2 b.2.fq -S b.sam
	samtools view -bS b.sam | samtools sort - b.sort
	^-^
	bowtie2 -x ref.fa -1 c.1.fq -2 c.2.fq -S c.sam
	samtools view -bS c.sam | samtools sort - c.sort
	^-^
	bowtie2 -x ref.fa -1 d.1.fq -2 d.2.fq -S d.sam
	samtools view -bS d.sam | samtools sort - d.sort
	^-^
	....
继续之前中断的继续运行, 分配8个核, 运行如下:

	python RunCmdsMP.py commands.list -s "^-^" -p 8 -c 1
	
本程序的特点是可断点续行, 可指定命令分隔符, 可回收标准错误和标准输出, 可回收退出状态非0的命令.
