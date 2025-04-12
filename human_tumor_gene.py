"""
Human Tumor Gene Sequences
This file contains DNA sequences for common tumor genes and visualization functions.
"""

import pymol
from pymol import cmd

# Common tumor gene sequences
TUMOR_GENES = {
    'TP53': {
        'sequence': """
        ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAAGCAATGGATGATTTGATGCTGTCCCCGGACGATATTGAACAATGGTTCACTGAAGACCCAGGTCCAGATGAAGCTCCCAGAATGCCAGAGGCTGCTCCCCCCGTGGCCCCTGCACCAGCAGCTCCTACACCGGCGGCCCCTGCACCAGCCCCCTCCTGGCCCCTGTCATCTTCTGTCCCTTCCCAGAAAACCTACCAGGGCAGCTACGGTTTCCGTCTGGGCTTCTTGCATTCTGGGACAGCCAAGTCTGTGACTTGCACGTACTCCCCTGCCCTCAACAAGATGTTTTGCCAACTGGCCAAGACCTGCCCTGTGCAGCTGTGGGTTGATTCCACACCCCCGCCCGGCACCCGCGTCCGCGCCATGGCCATCTACAAGCAGTCACAGCACATGACGGAGGTTGTGAGGCGCTGCCCCCACCATGAGCGCTGCTCAGATAGCGATGGTCTGGCCCCTCCTCAGCATCTTATCCGAGTGGAAGGAAATTTGCGTGTGGAGTATTTGGATGACAGAAACACTTTTCGACATAGTGTGGTGGTGCCCTATGAGCCGCCTGAGGTTGGCTCTGACTGTACCACCATCCACTACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTGGAAGACTCCAGTGGTAATCTACTGGGACGGAACAGCTTTGAGGTGCGTGTTTGTGCCTGTCCTGGGAGAGACCGGCGCACAGAGGAAGAGAATCTCCGCAAGAAAGGGGAGCCTCACCACGAGCTGCCCCCAGGGAGCACTAAGCGAGCACTGCCCAACAACACCAGCTCCTCTCCCCAGCCAAAGAAGAAACCACTGGATGGAGAATATTTCACCCTTCAGATCCGTGGGCGTGAGCGCTTCGAGATGTTCCGAGAGCTGAATGAGGCCTTGGAACTCAAGGATGCCCAGGCTGGGAAGGAGCCAGGGGGGAGCAGGGCTCACTCCAGCCACCTGAAGTCCAAAAAGGGTCAGTCTACCTCCCGCCATAAAAAACTCATGTTCAAGACAGAAGGAA
        """,
        'description': 'TP53 tumor suppressor gene, commonly mutated in various cancers',
        'common_mutations': ['R175H', 'R248W', 'R273H', 'R282W']
    },
    'BRCA1': {
        'sequence': """
        ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCGTAACTTGCAAAAGAAATATCATCAGAAATGTGAAACCAACACATAAAATGAAGAGGAAAAATCTGATTCAAAGAGGCAGAGAAAGATACAGCTGCAGAAAGGATGAAGGGGCTGCATTAATATAGGTGAAAACCCATCTAGTGATTGTAATGGATATGGGAAAACTTGAATCCGATGATTCACTTTATATCACTTTAATTGTTACTCATTCAAAATATTACAGGGCTACTATGTCCAAATGTGTTAGAGGTATTTTGGGGAACCCAGATGCCTGGTTTATAGACACTAAGGATGGGGAAATTTATATGTGGCAGCAAAACAAGGGGATCAAGCCATTTGTCGAAACTGGCGAGAGACAAAAACAATTTTTAGAACTGGCAGTGACAATAATTTCCGAATATCCATCTCTTCTTACAATGCCTACTAATTTTACTACTTCAAATCTTGATACAGTCACTGAAAGTGATATTTGGATTATTTTATAAACTACATTAAGTAATGTGTGTTTCTAGATGTCTTTACTGAAAGTGCTTTACATATCAGCATCTGAATTCTTTGCCCCAGCCTATTCCTCTCCCTCAACTTTGTGCAGCCTCATGTCACTCTCCTCCATCCAGTTACGTCTTCCTCGTCGATGAAATCCAAGAAAAAGGCTGCCACCAACTAAGAATGGATAGAATAAAAGCAAGTTTGAATCATCAGCTCAGGCAGACAGTGGTTTCAGCCGGGTTTCTGCTGTGTCCAGGAAAGCTTGTTTTTTTCGAGACATGGCTTTACATGTGTTGATCTGCCTTAATAAATCTAAACGAAAATAATTCCGTAAAAATTGAAACTTATCAGATATGTTAATCCTTTAAAAAGAAAAACCTATAACCCAGCATGGAATAAATCTTTGTGCCATTTATTTTATGAAGGACTCAGATATACCCATCGGAAGGTCTGATGATTTCTATGGAGGCAGGGTCTCATGCTGACGGTGGACAGATGGTTCTGCACCTGGTTGGAGGATTCAGCATGGAAAGGGTACAAAGCATGTGAAACGGGAAGAATCAATTCTGTTTATTTCATTCATATGCTTAGTCTCATTGTTTTATACATTCATTTTCTTAATTTAGTTCATATGTAAATAATGGCTCCTTCGCACTTCTTAACAAGATCAATGTACTTTGGTGTTTCTTTATGAGCAGTACTAAAATGGACTATTTTATTTCTTTTATGTTCAGCATGTAATAATACAGTTGACTTAGGCCACTTTGCAAGCCTGTGAAAGAAAATAAACAAATTAGCCCTAGGTCAAATGGATATGGAGAAACCCATTCAGGGATATACAGATGGGTCAAATTCAATGCAGGGTTCTGGGGAGAGTCAATGGAGTTTCCATACAGCTTGTCTTAGACCTATCTATTCCTCTCCCTAGTATATTTTGAAATGTACAATAAATTATTATGTGCTGTATTTTATGAGACTCAAGCTTCCTCTTTAGATTCCATTTAAATAACACTCTCCATTGCACAGTAAAAGATAATTCCTCCAAAACAGATCATGCTTGCTCCCATCCAGTCAGGAGGTGCG
        """,
        'description': 'BRCA1 breast cancer susceptibility gene',
        'common_mutations': ['185delAG', '5382insC', 'C61G']
    },
    'KRAS': {
        'sequence': """
        ATGACTGAATATAAACTTGTGGTAGTTGGAGCTGGTGGCGTAGGCAAGAGTGCCTTGACGATACAGCTAATTCAGAATCATTTTGTGGACGAATATGATCCAACAATAGAGGTGTTTACAGCTGTAGTAAAAACTTGTGGTCAAGAATGGTCCTGCATCAGATAATTACCTTTATTGTGATCATGTCATTAAAAATGGTAGAGCCGGAGGCGTAGGCAAACCATTTGAATAAGCTTGATTGACACAGGCAGTTTATTGTGTGGCGAGTACCATGCTGAAAATGACTGAATATAAACTTGTGGTAGTTGGAGCTGGTGGCGTAGGCAAGAGTGCCTTGACGATACAGCTAATTCAGAATCATTTTGTGGACGAATATGATCCAACAATAGAGGTGTTTACAGCTGTAGTAAAAACTTGTGGTCAAGAATGGTCCTGCATCAGATAATTACCTTTATTGTGATCATGTCATTAAAAATGGTAGAGCCGGAGGCGTAGGCAAACCATTTGAATAAGCTTGATTGACACAGGCAGTTTATTGTGTGGCGAGTACCATGCTGAAA
        """,
        'description': 'KRAS oncogene, commonly mutated in pancreatic and colorectal cancers',
        'common_mutations': ['G12D', 'G12V', 'G13D']
    }
}

def analyze_tumor_gene(gene_name, sequence):
    """Analyze tumor gene sequence for features and mutations."""
    try:
        sequence = sequence.strip().replace('\n', '')
        length = len(sequence)
        gc_content = (sequence.count('G') + sequence.count('C')) / length * 100
        
        print(f"\nTumor Gene Analysis for {gene_name}:")
        print(f"Description: {TUMOR_GENES[gene_name]['description']}")
        print(f"Sequence Length: {length} nucleotides")
        print(f"GC Content: {gc_content:.2f}%")
        
        # Find potential mutation sites
        mutation_sites = []
        for i in range(len(sequence) - 2):
            if sequence[i:i+3] in ['CGG', 'TGG']:
                mutation_sites.append(i)
        
        if mutation_sites:
            print("\nPotential Mutation Sites:")
            for site in mutation_sites:
                print(f"Position {site}: {sequence[site:site+3]}")
        
        print("\nCommon Mutations:")
        for mutation in TUMOR_GENES[gene_name]['common_mutations']:
            print(f"- {mutation}")
        
        return sequence
        
    except Exception as e:
        print(f"Error in tumor gene analysis: {str(e)}")
        return None

def visualize_in_pymol(gene_name, sequence):
    """Create PyMOL visualization of the gene sequence."""
    try:
        # First delete any existing objects with the same name
        cmd.delete(gene_name)
        
        # Create a simple DNA helix using built-in objects
        cmd.create(gene_name, "1bna")
        
        # Set up visualization
        cmd.color("blue", gene_name)
        cmd.show("cartoon", gene_name)
        cmd.set("cartoon_ring_mode", 3)
        cmd.set("cartoon_ring_finder", 1)
        cmd.set("cartoon_ring_transparency", 0.5)
        
        # Add sequence information
        cmd.set_title(f"{gene_name} Tumor Gene")
        
        # Highlight mutation sites
        for i in range(len(sequence) - 2):
            if sequence[i:i+3] in ['CGG', 'TGG']:
                # Map sequence position to structure residue
                resi = (i % 12) + 1  # DNA has 12 base pairs
                cmd.select(f"{gene_name}_mut_{i}", f"{gene_name} and resi {resi}")
                cmd.color("red", f"{gene_name}_mut_{i}")
                cmd.show("sticks", f"{gene_name}_mut_{i}")
        
        print(f"\nVisualization created in PyMOL for {gene_name}")
        print("Use PyMOL commands to explore the structure:")
        print("  - rotate: Left click and drag")
        print("  - zoom: Right click and drag")
        print("  - pan: Middle click and drag")
        print("\nMutation sites are highlighted in red")
        
    except Exception as e:
        print(f"Error in visualization: {str(e)}")
        print("Trying alternative visualization method...")
        try:
            # Alternative visualization using simple objects
            cmd.delete(gene_name)
            cmd.create(gene_name, "1bna")
            cmd.color("blue", gene_name)
            cmd.show("sticks", gene_name)
            print("Created simple stick visualization")
        except Exception as e2:
            print(f"Alternative visualization also failed: {str(e2)}")
            print("Please make sure PyMOL is properly initialized and the PDB structure 1bna is available")

def lynn_tumor_analyze(gene_name):
    """PyMOL command to analyze a tumor gene."""
    try:
        if gene_name not in TUMOR_GENES:
            print(f"Error: Gene {gene_name} not found. Available genes: {', '.join(TUMOR_GENES.keys())}")
            return False
            
        sequence = TUMOR_GENES[gene_name]['sequence']
        clean_sequence = analyze_tumor_gene(gene_name, sequence)
        
        if clean_sequence:
            visualize_in_pymol(gene_name, clean_sequence)
            return True
        return False
        
    except Exception as e:
        print(f"Error analyzing tumor gene: {str(e)}")
        return False

# Register commands with PyMOL
cmd.extend("lynn_tumor_analyze", lynn_tumor_analyze)

print("\n=== Tumor Gene Analysis Plugin ===")
print("Command: lynn_tumor_analyze [gene_name]")
print("Available genes: TP53, BRCA1, KRAS")

def analyze_long_dna_sequence(sequence):
    """Analyze a long DNA sequence for potential mutations and design guide RNAs."""
    try:
        # Clean the sequence
        sequence = sequence.strip().replace('\n', '').replace(' ', '')
        length = len(sequence)
        
        print(f"\n=== Long DNA Sequence Analysis ===")
        print(f"Sequence Length: {length} nucleotides")
        print(f"GC Content: {(sequence.count('G') + sequence.count('C')) / length * 100:.2f}%")
        
        # Find potential mutation sites
        mutation_sites = []
        mutation_patterns = {
            'CpG': 'CG',  # CpG islands are common mutation sites
            'Tandem repeat': r'(.)\1{2,}',  # Tandem repeats
            'Microsatellite': r'([ACGT])\1{4,}',  # Microsatellite regions
            'Palindromic': r'([ACGT]{4,}).*?\1',  # Palindromic sequences
            'Stop codon': ['TAA', 'TAG', 'TGA'],  # Stop codons
            'Splice site': ['GT', 'AG']  # Splice sites
        }
        
        print("\nPotential Mutation Sites:")
        for pattern_name, pattern in mutation_patterns.items():
            if isinstance(pattern, str):
                # For regex patterns
                import re
                matches = re.finditer(pattern, sequence)
                for match in matches:
                    pos = match.start()
                    seq = match.group()
                    mutation_sites.append({
                        'position': pos,
                        'type': pattern_name,
                        'sequence': seq
                    })
            else:
                # For list patterns
                for motif in pattern:
                    pos = sequence.find(motif)
                    while pos != -1:
                        mutation_sites.append({
                            'position': pos,
                            'type': pattern_name,
                            'sequence': sequence[pos:pos+len(motif)]
                        })
                        pos = sequence.find(motif, pos + 1)
        
        # Sort mutation sites by position
        mutation_sites.sort(key=lambda x: x['position'])
        
        # Print mutation sites
        for site in mutation_sites:
            print(f"\nPosition {site['position']}:")
            print(f"Type: {site['type']}")
            print(f"Sequence: {site['sequence']}")
            
            # Design guide RNAs for this mutation site
            print("\nPotential Guide RNAs:")
            pam_pattern = r'[ATCG]GG'
            context_size = 30
            
            # Get sequence context around mutation
            start = max(0, site['position'] - context_size)
            end = min(len(sequence), site['position'] + context_size)
            context = sequence[start:end]
            
            # Find PAM sites
            import re
            pam_sites = re.finditer(pam_pattern, context)
            
            guides_found = False
            for pam_site in pam_sites:
                pam_pos = pam_site.start() + start
                if pam_pos >= 20:
                    guide_start = pam_pos - 20
                    guide = sequence[guide_start:pam_pos]
                    
                    # Check if guide overlaps with mutation
                    if guide_start <= site['position'] < pam_pos:
                        guides_found = True
                        print(f"Guide RNA: {guide}")
                        print(f"PAM Position: {pam_pos}")
                        print(f"GC Content: {(guide.count('G') + guide.count('C')) / len(guide) * 100:.1f}%")
            
            if not guides_found:
                print("No suitable guide RNAs found near this mutation site")
        
        return True
        
    except Exception as e:
        print(f"Error analyzing DNA sequence: {str(e)}")
        return False

def lynn_dna_analyze(sequence):
    """PyMOL command to analyze a DNA sequence."""
    try:
        # Remove quotes if present
        sequence = sequence.strip().strip('"').strip("'")
        return analyze_long_dna_sequence(sequence)
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Register commands with PyMOL
cmd.extend("lynn_dna_analyze", lynn_dna_analyze)

print("\n=== DNA Analysis Plugin ===")
print("Command: lynn_dna_analyze [sequence]")
print("This will analyze the sequence for mutations and design guide RNAs") 