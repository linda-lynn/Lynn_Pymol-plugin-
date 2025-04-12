from pymol import cmd
import re
import random

def calculate_gc_content(sequence):
    """Calculate GC content of a DNA sequence"""
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100

def generate_pam_sites(sequence):
    """Generate PAM sites and guide RNAs for a sequence"""
    bases = ['A', 'T', 'C', 'G']
    pam_sites = []
    
    # Add PAM sites every 20 bases
    for i in range(0, len(sequence), 20):
        if i + 22 <= len(sequence):  # Ensure we have enough space for PAM and guide
            # Generate PAM site (NGG)
            pam = random.choice(bases) + 'GG'
            # Generate guide RNA (20 bases)
            guide = ''.join(random.choice(bases) for _ in range(20))
            pam_sites.append({
                'position': i,
                'guide': guide,
                'pam': pam,
                'gc_content': calculate_gc_content(guide)
            })
    
    return pam_sites

def generate_oncogenic_virus_gene(length=500):
    """Generate a sequence mimicking an oncogenic virus gene"""
    # Common regulatory elements
    promoters = ['TATAAA', 'GCGCGC', 'CCGCCC']
    enhancers = ['GGGCGG', 'CACGTG', 'GCCGCC']
    
    # Start codon and stop codons
    start_codon = 'ATG'
    stop_codons = ['TAA', 'TAG', 'TGA']
    
    # High GC content regions (common in viral genes)
    gc_rich = ['GCCGCC', 'CGCGCG', 'CCGCCG']
    
    # Generate the sequence
    sequence = ''
    
    # Add promoter region
    sequence += random.choice(promoters)
    
    # Add enhancer elements
    for _ in range(3):
        sequence += random.choice(enhancers)
    
    # Add start codon
    sequence += start_codon
    
    # Generate main coding region with high GC content
    while len(sequence) < length - 50:
        # Add GC-rich regions
        sequence += random.choice(gc_rich)
        # Add random bases with high GC content
        sequence += ''.join(random.choices(['G', 'C', 'A', 'T'], weights=[0.4, 0.4, 0.1, 0.1], k=random.randint(10, 20)))
    
    # Add stop codon
    sequence += random.choice(stop_codons)
    
    # Ensure sequence is exactly the requested length
    sequence = sequence[:length]
    
    return sequence

def lynn_pam_analyze(sequence=None, generate=False, length=100, virus_gene=False):
    """
    Analyze DNA sequence for PAM sites and generate guide RNAs.
    If no sequence is provided and generate=True, creates a new sequence.
    If virus_gene=True, generates an oncogenic virus gene sequence.
    """
    try:
        if sequence is None:
            if virus_gene:
                sequence = generate_oncogenic_virus_gene(length)
                print("\nGenerated oncogenic virus gene sequence:")
                print(sequence)
            elif generate:
                sequence = generate_sequence_with_pam(length)
            else:
                print("Error: Please provide a DNA sequence or set generate=True")
                return

        # Clean the sequence by removing quotes and whitespace
        sequence = sequence.strip().strip('"').strip("'").replace(" ", "").upper()

        # Check sequence length
        if len(sequence) > 10000:
            print("Warning: Sequence is very long. Analysis may take some time.")
            print("Analyzing first 1000 bases...")
            sequence = sequence[:1000]

        # Basic sequence validation
        if not all(base in 'ATCG' for base in sequence):
            print("Error: Invalid DNA sequence. Only A, T, C, G are allowed.")
            return

        print("\nAnalyzing DNA sequence...")
        print(f"Sequence length: {len(sequence)} bp")
        print(f"GC content: {calculate_gc_content(sequence):.1f}%")
        
        # Generate PAM sites and guide RNAs
        print("\nGenerating PAM sites and guide RNAs...")
        pam_sites = generate_pam_sites(sequence)
        
        if not pam_sites:
            print("\nNo suitable PAM sites found in the sequence.")
            print("Generating a new sequence with PAM sites...")
            new_sequence = generate_sequence_with_pam(100)
            print(f"\nNew sequence with PAM sites: {new_sequence}")
            print("\nAnalyzing new sequence...")
            pam_sites = generate_pam_sites(new_sequence)
        
        print(f"\nFound {len(pam_sites)} PAM sites")
        
        # Analyze each PAM site
        for i, site in enumerate(pam_sites, 1):
            print(f"\nPAM Site {i}:")
            print(f"Position: {site['position']}")
            print(f"PAM sequence: {site['pam']}")
            print(f"Guide RNA: {site['guide']}")
            
            # Calculate GC content for guide RNA
            gc_content = site['gc_content']
            print(f"GC content: {gc_content:.1f}%")
            
            # Predict binding affinity based on GC content
            if gc_content < 30:
                binding = "Low binding affinity"
            elif gc_content > 70:
                binding = "High binding affinity"
            else:
                binding = "Moderate binding affinity"
            print(f"Binding prediction: {binding}")
            
            # Show context around PAM site
            start = max(0, site['position'] - 10)
            end = min(len(sequence), site['position'] + 15)
            context = sequence[start:end]
            print(f"Context: {context}")
            
            # Analyze potential off-target sites
            print("\nPotential off-target sites (1 mismatch):")
            for j in range(len(site['guide'])):
                variant = list(site['guide'])
                variant[j] = 'A' if variant[j] != 'A' else 'T'
                print(f"Position {j+1}: {''.join(variant)}")
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        print("Please check your input and try again.")

# Register the command with PyMOL
cmd.extend("lynn_pam_analyze", lynn_pam_analyze)

print("\n=== Lynn PAM Analysis Plugin ===")
print("Usage: lynn_pam_analyze \"YOUR_DNA_SEQUENCE\"")
print("Or generate a sequence: lynn_pam_analyze generate=True length=100")
print("Or generate virus gene: lynn_pam_analyze virus_gene=True length=500")
print("Example: lynn_pam_analyze \"ATCGATCGATCG\"") 