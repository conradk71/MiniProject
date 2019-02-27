import os
import csv

#creating directory "OptionA_Conrad_Kurowski" in users' path, and moving to that directory
path = os.getcwd()
os.mkdir(path+'/OptionA_Conrad_Kurowski')
os.chdir(path+'/OptionA_Conrad_Kurowski')
path = os.getcwd()
#updating path string to new path

def Setup():
    wget_command = 'wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR818/SRR8185310/SRR8185310.sra'
    fastq_dump = 'fastq-dump -I --split-files SRR8185310.sra'
    os.system(wget_command)
    os.system(fastq_dump)
    #setup downloads SRR8185310.sra and fastq_dumps the sra file

def run_spades():
    spades_command = 'spades.py'
    spades_command += ' -k 33,55,77,99,127 -t 2 --only-assembler -s '+path+'/SRR8185310_1.fastq -o '+path+'/SPAdes'
    with open('OptionA.log','w') as output:
        output.write(spades_command)
    os.system(spades_command)
    #writes spades command to log file and executes 

def Prokka():
    prokka_command = 'prokka'
    prokka_command += ' --outdir '+path+'/Prokka'+' --genus Escherichia --prefix Ecoli '+path+'/SPAdes/contigs.fasta'
    with open('OptionA.log', 'a') as output:
        output.write(prokka_command)
    os.system(prokka_command)
    #writes prokka command to log file and executes

def Script1():
    seq_list = []
    stseq = ''
    #originally, did not realize we could import and use Seq.IO; however, decided to keep this code because it works just fine
    #script to count contigs and basepairs
    for line in open(path+'/SPAdes/contigs.fasta'):
        if line[0] == '>':
            if stseq != '':
                seq_list.append(stseq)
                stseq = ''
        else:
            stseq = stseq + line.strip('\n')
    seq_list.append(stseq) 

    long = []
    for seq in seq_list:
        if (len(seq))>1000:
            long.append(seq)
    number = len(long)
    print("There are %d contigs > 1000 in the assembly"%(number))

    total = 0
    for seq in long:
        count = len(seq)
        total = total + count
        count = 0
    print("There are %d bp in the assemlbly"%(total))
    #write out to the log file
    with open('OptionA.log', 'a') as output:
        output.write("There are %d contigs > 1000 in the assembly"%(number))
        output.write("There are %d bp in the assembly"%(total))
        output.close()

def Script3():
    for line in open(path+'/Prokka/Ecoli.txt'):
        with open('OptionA.log', 'a') as output:
            output.write(line)
            #script to write out Ecoli.txt to the log file

def Script2():
    #script to retrieve #CDS and #tRNAs
    cds = ''
    tRNAs = ''
    i = 0
    for line in open(path+'/Prokka/Ecoli.txt'):
        if (line[0] == 'C') % (line[2] == 'D'):
            cds = line[5:9]
        if (line[0] == 't') & (line[1] == 'R'):
            tRNAs = line[6:8]
    rCDS = 4140
    rtRNAs = 89
    cds = int(cds)
    tRNAs = int(tRNAs)
    diff = 0
    diff1 = 0
    diff = rCDS - cds
    diff1 = rtRNAs - tRNAs
    #comparisons to determine more/less
    if (diff) > 0:
        comp = "less"
    if (diff) < 0:
        comp = "more"
        diff = diff * -1
    if (diff1) > 0:
        comp1 = "less"
    if (diff1) < 0:
        comp1 = "more"
        diff = diff * -1
    
    print("Prokka found %d %s CDS and %d %s tRNA than the RefSeq"%(diff,comp,diff1,comp1))
    #write this data out to the log file
    with open('OptioA.log', 'a') as output:
        output.write("Prokka found %d %s CDS and %d %s tRNA than the RefSeq"%(diff,comp,diff1,comp1))

def bowtie_build():
    #builds initial index using reference genome
    os.system("wget ftp://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Escherichia_coli_K_12_substr__MG1655_uid57779/NC_000913.fna")
    bowtie_command = 'bowtie2-build NC_000913.fna EcoliK12'
    os.system(bowtie_command)
    #maps transcriptome reads to the index we just created, generating sam file
    os.system("wget ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/SRR/SRR141/SRR1411276/SRR1411276.sra")
    os.system('fastq-dump -I --split-files SRR1411276.sra')
    bowtie_command2 = 'bowtie2 -x EcoliK12 -U SRR1411276_1.fastq -S EcoliK12.sam'
    os.system(bowtie_command2)


output_path = '/home/ckurowski/Script/TopHat'
def TopHat():
    tophat_command = 'tophat2 --no-novel-juncs -o '+path+'/TopHat'+' EcoliK12 -SRR8185310_1.fastq'
    #copying reference.fna to rename as the same name as the index (EcoliK12), as well as changing file type from .fna to .fa
    os.system('cp NC_000913.fna EcoliK12.fa')
    os.system('tophat2 --no-novel-juncs -o '+path+'/TopHat EcoliK12 SRR1411276_1.fastq')

    
def Cufflinks():
    #runs cufflinks on accepted_hits.bam
    os.chdir(path+'/TopHat')
    cufflinks_command = 'cufflinks accepted_hits.bam'
    os.system(cufflinks_command)
    
def Script4():
    #wonky way to retrieve gene_id, locus(location), and FPKM value
    with open (path+'/TopHat/isoforms.fpkm_tracking','r') as csv_file:
        with open ('Option1.fpkm','w') as csv_out:
            reader = csv.DictReader(csv_file, delimiter = '\t')
            for row in reader:
                line = (row["gene_id"]+'\t'+row["locus"]+'\t'+row["FPKM"]+'\n')
                csv_out.write(line)
    
    
Setup()
run_spades()
Script1()
Prokka()
Script3()
Script2()
bowtie_build()
TopHat()
Cufflinks()
Script4()