import os
import argparse

def list_to_array(lis):
    """
    Converts a python string list into a string bash array format.
    ("<str1>","<str2>","<str3>")
    """
    stringbuilt = ''
    for item in lis[:-1]:
        stringbuilt += '\"'
        stringbuilt += item
        stringbuilt += '\" '
    stringbuilt += '\"'
    stringbuilt += lis[-1]
    stringbuilt += '\"'

    return stringbuilt


def string_output(var, output):
    """
    Transfers a variable and its content (as a string) to an output widget.
    Use a printf statement to pipe into /tmp/output/<output> to properly load content into output.

    var: Python variable to transfer, either string or list
    output: Output parameter name specified in the original widget (in "Outputs" tab)
    """
    
    # Variable is a list, then need to convert it to bash list string
    if type(var) == list:
        var = list_to_array(var)
    
    os.system('printf "{}"  > "/tmp/output/{}"'.format(var, output))



def main():
    parser = argparse.ArgumentParser()

    # Work directory arg
    parser.add_argument('-workdir',
                        type = str,
                        nargs = '+',
                        help = "Work directory where fastq, sam, and count output files are stored.",
                        required = True)

    # Genome directory arg
    parser.add_argument('-genomedir',
                        type = str,
                        nargs = '+',
                        help = "Genome directory where fasta and index files are stored.",
                        required = True)

    # SRA IDs arg
    parser.add_argument('-sraids',
                        type = str,
                        nargs = '+',
                        help = "SRA IDs to download fastq files and use in alignment.",
                        required = True)

    # Index file basename arg
    parser.add_argument('-basename',
                        type = str,
                        nargs = '+',
                        help = "Basename for index files created from fasta (<basename>.<#>.ht2).",
                        required = True)

    args = parser.parse_args()

    # Get flag contents
    work_dir = args.workdir[0]
    genome_dir = args.genomedir[0]
    basename = args.basename[0]
    ids = args.sraids
    print("Work directory: {}".format(work_dir))
    print("Genome directory: {}".format(genome_dir))
    print("Basename: {}".format(basename))
    print("IDs: {}".format(ids))


    # Make directory path of index with basename at genome directory (<genome_dir>/<basename>)
    index_path = "{}/{}".format(genome_dir, basename)

    # Make list of expected downloaded fastq files from SRA IDs for 1st and 2nd mates, as well as unpaired fastq
    fastq1 = ["{}/{}_1.fastq".format(work_dir, sraid) for sraid in ids]
    fastq2 = ["{}/{}_2.fastq".format(work_dir, sraid) for sraid in ids]
    fastq_unpaired = ["{}/{}.fastq".format(work_dir, sraid) for sraid in ids]

    # Make list of expected sam file outputs (outputs after HISAT2 Align step) from SRA IDs
    sam = ["{}/{}.sam".format(work_dir, sraid) for sraid in ids]


    # Load variables as outputs (found in Outputs tab)
    string_output(fastq1, 'mate_1')
    string_output(fastq2, 'mate_2')
    string_output(fastq_unpaired, 'unpaired')
    string_output(sam, 'sam_output')
    string_output(index_path, 'hisat2_idx')

if __name__ == '__main__':
    main()