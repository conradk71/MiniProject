# MiniProject
Python Wrapper Pipeline

Required Programs: Python3, SPAdes, Prokka, Bowtie2, TopHat, Cufflinks

Instructions: Download Wrapper.py and move to desired location. Use terminal command: python3 Wrapper.py. This will execute the Wrapper/Pipeline, which will generate a new directory for results called ~/OptionA_Conrad_Kurowski in the current path. 
WARNING: this pipeline uses computationally intensive programs. Please allow pipeline to fully execute before attempting to close. Some steps, such as TopHat, can take hours to complete. 

Output:
OptionA.log file is written to the directory ~/OptionA_Conrad_Kurowski when the pipeline is finished. This log file contains information about the assembly and annotation, and also linux commands used for invidual programs. Option1.fpkm log file is also written. This file contains seqname, start-end, and FPKM for each record in the Cufflinks output file. 

No test data is provided for this pipeline. :(
