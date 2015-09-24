import sys
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo
import os


def get_phylo_tree(fasta_file):
    try:
        cline = ClustalwCommandline("clustalw2", infile=fasta_file)
        stdout, stderr = cline()
        tree = Phylo.read("%s.dnd" % fasta_file, "newick")
        representation_file = '%s.tree' % fasta_file
        with open(representation_file, 'w') as output_file:
            Phylo.draw_ascii(tree, output_file)
        return representation_file
    except Exception, e:
        return 'Error generating phylo tree: %s' % str(e)
    finally:
        files_to_remove = [fasta_file, '%s.dnd' % fasta_file, '%s.aln' % fasta_file]
        for file_name in files_to_remove:
            try:
                os.remove(file_name)
            except:
                pass


if __name__ == "__main__":
    print get_phylo_tree(sys.argv[1])
