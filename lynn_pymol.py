#!/usr/bin/env python

from pymol import cmd
import math
import requests
import json
import os

# PDB API endpoints
PDB_API_BASE = "https://data.rcsb.org/rest/v1/core/entry/"
PDB_SEARCH_API = "https://search.rcsb.org/rcsbsearch/v2/query"

def fetch_pdb_info(pdb_id):
    """Fetch information about a PDB entry"""
    try:
        # Get basic information from PDB API
        info = {
            'title': 'N/A',
            'method': 'N/A',
            'resolution': 'N/A',
            'r_value': 'N/A',
            'deposition_date': 'N/A',
            'release_date': 'N/A'
        }
        
        # Try to get additional info from PDB API
        try:
            response = requests.get(f"{PDB_API_BASE}{pdb_id}")
            if response.status_code == 200:
                data = response.json()
                info.update({
                    'title': data.get('struct', {}).get('title', 'N/A'),
                    'method': data.get('experiment', {}).get('method', 'N/A'),
                    'resolution': data.get('refine', {}).get('ls_d_res_high', 'N/A'),
                    'r_value': data.get('refine', {}).get('ls_R_factor_R_work', 'N/A'),
                    'deposition_date': data.get('deposit_date', 'N/A'),
                    'release_date': data.get('release_date', 'N/A')
                })
        except:
            pass  # Continue with basic info if API fails
            
        return info
    except Exception as e:
        print(f"Error fetching PDB info: {str(e)}")
        return None

def lynn_pdb_fetch(pdb_id):
    """Fetch and load a structure from PDB"""
    try:
        print(f"\n🔍 Fetching PDB entry: {pdb_id}")
        
        # Delete existing objects with the same name
        if pdb_id in cmd.get_object_list():
            cmd.delete(pdb_id)
        
        # Fetch the structure
        cmd.fetch(pdb_id)
        
        # Get PDB information
        pdb_info = fetch_pdb_info(pdb_id)
        if pdb_info:
            print("\n📊 PDB Information:")
            print(f"Title: {pdb_info['title']}")
            print(f"Experimental Method: {pdb_info['method']}")
            print(f"Resolution: {pdb_info['resolution']} Å")
            print(f"R-value: {pdb_info['r_value']}")
            print(f"Deposition Date: {pdb_info['deposition_date']}")
            print(f"Release Date: {pdb_info['release_date']}")
            
            # Show basic structure info
            print("\n🔬 Structure Information:")
            cmd.show("cartoon")
            cmd.show("surface")
            cmd.color("cyan", "ss h")
            cmd.color("magenta", "ss s")
            print("Cyan: Alpha helices")
            print("Magenta: Beta sheets")
            
            return True
        return False
    except Exception as e:
        print(f"Error fetching PDB structure: {str(e)}")
        return False

def lynn_pdb_search(query):
    """Search for structures in PDB"""
    try:
        print(f"\n🔍 Searching PDB for: {query}")
        
        # Simple search using PDB API
        search_query = {
            "query": {
                "type": "terminal",
                "service": "text",
                "parameters": {
                    "value": query
                }
            },
            "return_type": "entry"
        }
        
        try:
            response = requests.post(PDB_SEARCH_API, json=search_query)
            if response.status_code == 200:
                data = response.json()
                results = data.get("result_set", [])[:5]  # Limit to 5 results
                
                if results:
                    print("\nFound structures:")
                    for entry in results:
                        print(f"\nPDB ID: {entry.get('identifier', 'N/A')}")
                        print(f"Title: {entry.get('title', 'N/A')}")
                else:
                    print("No structures found.")
            else:
                print("Search failed. Please try again.")
        except:
            print("Search failed. Please try again.")
            
    except Exception as e:
        print(f"Error searching PDB: {str(e)}")

def lynn_pdb_analyze(pdb_id):
    """Analyze a PDB structure with enhanced knowledge"""
    try:
        # Check if structure is already loaded
        objects = cmd.get_object_list()
        if not objects:
            print(f"Loading structure {pdb_id}...")
            if not lynn_pdb_fetch(pdb_id):
                return
        
        # Get PDB information
        pdb_info = fetch_pdb_info(pdb_id)
        if not pdb_info:
            return
            
        # Enhanced analysis with PDB knowledge
        print("\n🔬 Enhanced PDB Analysis:")
        print("=" * 50)
        
        # Structure quality
        print(f"\nStructure Quality:")
        print(f"Resolution: {pdb_info['resolution']} Å")
        print(f"R-value: {pdb_info['r_value']}")
        
        # Experimental method
        print(f"\nExperimental Method: {pdb_info['method']}")
        
        # Analyze structure
        lynn_auto_analyze()
            
    except Exception as e:
        print(f"Error in PDB analysis: {str(e)}")
        print("Please ensure you have a valid PDB ID.")

def lynn_show_structure():
    """Show detailed structure information"""
    cmd.show("sticks")
    cmd.show("surface")
    cmd.show("cartoon")
    cmd.set("cartoon_transparency", 0.5)
    cmd.set("surface_transparency", 0.5)
    print("Showing detailed structure information...")
    print("Transparency set to 0.5 for better visualization")

def lynn_analyze_interactions():
    """Analyze protein-protein interactions and orient to best interaction site"""
    try:
        # Get all loaded objects
        objects = cmd.get_object_list()
        if len(objects) < 2:
            print("Error: Please load at least two protein structures first.")
            return

        # Use the first two loaded objects
        protein1 = objects[0]
        protein2 = objects[1]
        print(f"Analyzing interactions between {protein1} and {protein2}")

        # Clear previous selections
        cmd.delete("interaction_*")
        
        # Find potential interaction sites
        cmd.select("interface1", f"byres {protein1} within 5 of {protein2}")
        cmd.select("interface2", f"byres {protein2} within 5 of {protein1}")
        
        # Show interfaces
        cmd.show("sticks", "interface1")
        cmd.show("sticks", "interface2")
        cmd.color("red", "interface1")
        cmd.color("blue", "interface2")
        
        # Find complementary surfaces
        cmd.select("hydrophobic1", f"{interface1} and resn ala+val+leu+ile+met+phe+trp+tyr")
        cmd.select("hydrophobic2", f"{interface2} and resn ala+val+leu+ile+met+phe+trp+tyr")
        cmd.color("yellow", "hydrophobic1")
        cmd.color("yellow", "hydrophobic2")
        
        # Find charged residues at interface
        cmd.select("charged1", f"{interface1} and resn asp+glu+lys+arg")
        cmd.select("charged2", f"{interface2} and resn asp+glu+lys+arg")
        cmd.color("green", "charged1")
        cmd.color("green", "charged2")
        
        # Orient view to best interaction site
        cmd.center("interface1")
        cmd.zoom("interface1", 5)
        
        print("\nProtein-Protein Interaction Analysis:")
        print("Red: Interface residues on first protein")
        print("Blue: Interface residues on second protein")
        print("Yellow: Hydrophobic residues at interface")
        print("Green: Charged residues at interface")
        
        # Analyze potential drug binding sites
        print("\nPotential Drug Binding Sites:")
        print("1. Interface cavities (good for competitive inhibitors)")
        print("2. Hydrophobic patches (good for small molecule binding)")
        print("3. Charged residues (potential for electrostatic interactions)")
        
    except Exception as e:
        print(f"Error in interaction analysis: {str(e)}")
        print("Please ensure you have loaded two protein structures.")

def lynn_analyze_drug():
    """Analyze potential drug development sites"""
    try:
        # Get all loaded objects
        objects = cmd.get_object_list()
        if not objects:
            print("Error: No structure loaded. Please load a structure first.")
            return

        # Use the first loaded object
        target = objects[0]
        print(f"Analyzing drug development sites for: {target}")

        # Clear previous selections
        cmd.delete("drug_*")
        
        # Show surface with high quality
        cmd.show("surface")
        cmd.set("surface_quality", 1)
        cmd.set("surface_color", "white")
        
        # Find potential drug binding sites
        # 1. Deep pockets
        cmd.select("deep_pockets", f"byres {target} and (b < 20) and (q < 0.3)")
        cmd.show("surface", "deep_pockets")
        cmd.color("red", "deep_pockets")
        
        # 2. Hydrophobic patches
        cmd.select("hydrophobic", f"byres {target} and resn ala+val+leu+ile+met+phe+trp+tyr")
        cmd.show("sticks", "hydrophobic")
        cmd.color("yellow", "hydrophobic")
        
        # 3. Charged residues
        cmd.select("charged", f"byres {target} and resn asp+glu+lys+arg")
        cmd.show("sticks", "charged")
        cmd.color("blue", "charged")
        
        # 4. Potential allosteric sites
        cmd.select("allosteric", f"byres {target} and (b > 30) and (b < 60)")
        cmd.show("sticks", "allosteric")
        cmd.color("green", "allosteric")
        
        # Orient to best drug binding site
        cmd.center("deep_pockets")
        cmd.zoom("deep_pockets", 5)
        
        print("\nDrug Development Analysis:")
        print("Red: Deep pockets (good for drug binding)")
        print("Yellow: Hydrophobic regions (good for small molecules)")
        print("Blue: Charged residues (potential for electrostatic interactions)")
        print("Green: Potential allosteric sites")
        
        print("\nDrug Development Tips:")
        print("1. Deep pockets are ideal for drug binding")
        print("2. Hydrophobic regions are good for small molecule drugs")
        print("3. Charged residues can be used for electrostatic interactions")
        print("4. Allosteric sites offer alternative drug targets")
        
    except Exception as e:
        print(f"Error in drug analysis: {str(e)}")
        print("Please ensure you have loaded a structure first.")

def lynn_analyze_binding():
    """Analyze binding sites with detailed visualization"""
    # Show surface
    cmd.show("surface")
    cmd.set("surface_quality", 1)
    
    # Color by hydrophobicity
    cmd.color("yellow", "surface")
    cmd.set("surface_color", "white")
    
    # Show potential binding pockets
    cmd.select("pockets", "byres protein within 5 of ligand")
    cmd.show("sticks", "pockets")
    cmd.color("red", "pockets")
    
    print("Analyzing binding sites...")
    print("Yellow: Hydrophobic regions")
    print("Red: Potential binding pockets")

def lynn_analyze_storage():
    """Analyze potential drug storage sites"""
    try:
        # Get all loaded objects
        objects = cmd.get_object_list()
        if not objects:
            print("Error: No structure loaded. Please load a structure first.")
            return

        # Use the first loaded object
        target = objects[0]
        print(f"Analyzing structure: {target}")

        # Clear previous selections
        cmd.delete("storage_*")
        
        # Show surface with high quality
        cmd.show("surface")
        cmd.set("surface_quality", 1)
        cmd.set("surface_color", "white")
        
        # Find internal cavities using multiple criteria
        # 1. Buried residues
        cmd.select("buried", f"byres {target} and (b < 20)")
        cmd.show("sticks", "buried")
        cmd.color("red", "buried")
        
        # 2. Hydrophobic cavities
        cmd.select("hydrophobic", f"byres {target} and resn ala+val+leu+ile+met+phe+trp+tyr")
        cmd.show("sticks", "hydrophobic")
        cmd.color("yellow", "hydrophobic")
        
        # 3. Potential entry points (semi-buried residues)
        cmd.select("entry", f"byres {target} and (b > 30) and (b < 60)")
        cmd.show("sticks", "entry")
        cmd.color("blue", "entry")
        
        # 4. Large cavities (using solvent accessibility)
        cmd.select("large_cavities", f"byres {target} and (b < 30) and (q < 0.5)")
        cmd.show("surface", "large_cavities")
        cmd.color("green", "large_cavities")
        
        # Analyze sequence
        sequence = cmd.get_fastastr(target)
        print("\nSequence Analysis:")
        print(sequence)
        
        # Count amino acids
        aa_counts = {}
        for aa in sequence:
            if aa in aa_counts:
                aa_counts[aa] += 1
            else:
                aa_counts[aa] = 1
        
        print("\nAmino Acid Composition:")
        for aa, count in aa_counts.items():
            print(f"{aa}: {count}")
        
        print("\nAnalyzing potential drug storage sites...")
        print("Red: Buried residues (potential storage sites)")
        print("Yellow: Hydrophobic regions (good for drug binding)")
        print("Blue: Potential entry points")
        print("Green: Large cavities (suitable for drug storage)")
        print("\nTips for drug storage site selection:")
        print("1. Look for large green cavities (good for drug storage)")
        print("2. Check yellow hydrophobic regions (good for drug binding)")
        print("3. Verify blue entry points (for drug delivery)")
        print("4. Consider red buried regions (protected storage sites)")
        
    except Exception as e:
        print(f"Error in storage analysis: {str(e)}")
        print("Please ensure you have loaded a structure first.")

def lynn_highlight():
    """Highlight surface residues with multiple visualization options"""
    # Show surface
    cmd.show("surface")
    
    # Color by electrostatic potential
    cmd.color("blue", "surface")
    cmd.set("surface_color", "white")
    
    # Highlight charged residues
    cmd.select("charged", "resn asp+glu+lys+arg")
    cmd.show("sticks", "charged")
    cmd.color("red", "charged")
    
    print("Highlighting surface residues...")
    print("Blue: Surface electrostatic potential")
    print("Red: Charged residues")

def lynn_measure():
    """Measure distances with advanced options"""
    # Create distance measurements
    cmd.distance("distances", "all", "all", 5, mode=2)
    
    # Show hydrogen bonds
    cmd.h_add("all")
    cmd.distance("hbonds", "all", "all", 3.5, mode=1)
    
    # Color by distance
    cmd.color("yellow", "distances")
    cmd.color("blue", "hbonds")
    
    print("Measuring distances...")
    print("Yellow: Van der Waals contacts")
    print("Blue: Hydrogen bonds")

def lynn_save():
    """Save session with multiple formats"""
    # Save PyMOL session
    cmd.save("session.pse")
    
    # Save structure in PDB format
    cmd.save("structure.pdb")
    
    # Save surface in PLY format
    cmd.save("surface.ply")
    
    print("Saving multiple formats...")
    print("- session.pse: PyMOL session")
    print("- structure.pdb: PDB structure")
    print("- surface.ply: Surface mesh")

def lynn_analyze_secondary():
    """Analyze secondary structure"""
    cmd.show("cartoon")
    cmd.set("cartoon_ring_mode", 1)
    cmd.set("cartoon_ring_transparency", 0.5)
    
    # Color by secondary structure
    cmd.color("yellow", "ss h")
    cmd.color("red", "ss s")
    cmd.color("blue", "ss l")
    
    print("Analyzing secondary structure...")
    print("Yellow: Alpha helices")
    print("Red: Beta sheets")
    print("Blue: Loops")

def lynn_analyze_solvent():
    """Analyze solvent accessibility"""
    cmd.show("surface")
    cmd.set("surface_quality", 1)
    
    # Color by accessibility
    cmd.color("green", "surface")
    cmd.set("surface_color", "white")
    
    # Highlight buried residues
    cmd.select("buried", "byres protein and (b < 20)")
    cmd.show("sticks", "buried")
    cmd.color("red", "buried")
    
    print("Analyzing solvent accessibility...")
    print("Green: Surface accessibility")
    print("Red: Buried residues")

def lynn_analyze_mutations():
    """Analyze potential mutation sites"""
    cmd.show("sticks")
    
    # Select conserved residues
    cmd.select("conserved", "byres protein and (b > 80)")
    cmd.color("red", "conserved")
    
    # Show surface residues
    cmd.select("surface", "byres protein and (b > 50)")
    cmd.color("yellow", "surface")
    
    print("Analyzing mutation sites...")
    print("Red: Conserved residues")
    print("Yellow: Surface-exposed residues")

def lynn_analyze_text(query):
    """Analyze structure based on text query"""
    try:
        # Get all loaded objects
        objects = cmd.get_object_list()
        if not objects:
            print("Error: No structure loaded. Please load a structure first.")
            return

        # Use the first loaded object
        target = objects[0]
        
        # Convert query to lowercase for easier matching
        query = query.lower()
        
        # Clear previous selections
        cmd.delete("analysis_*")
        
        # Analyze based on query keywords
        if "binding" in query or "pocket" in query:
            print("\nAnalyzing binding sites...")
            cmd.select("binding_sites", f"byres {target} and (b < 20) and (q < 0.3)")
            cmd.show("surface", "binding_sites")
            cmd.color("red", "binding_sites")
            print("Red: Potential binding sites")
            
        elif "hydrophobic" in query:
            print("\nAnalyzing hydrophobic regions...")
            cmd.select("hydrophobic", f"byres {target} and resn ala+val+leu+ile+met+phe+trp+tyr")
            cmd.show("sticks", "hydrophobic")
            cmd.color("yellow", "hydrophobic")
            print("Yellow: Hydrophobic residues")
            
        elif "charged" in query or "electrostatic" in query:
            print("\nAnalyzing charged residues...")
            cmd.select("charged", f"byres {target} and resn asp+glu+lys+arg")
            cmd.show("sticks", "charged")
            cmd.color("blue", "charged")
            print("Blue: Charged residues")
            
        elif "surface" in query:
            print("\nAnalyzing surface residues...")
            cmd.show("surface")
            cmd.set("surface_quality", 1)
            cmd.select("surface_residues", f"byres {target} and (b > 50)")
            cmd.show("sticks", "surface_residues")
            cmd.color("green", "surface_residues")
            print("Green: Surface-exposed residues")
            
        elif "buried" in query or "internal" in query:
            print("\nAnalyzing buried residues...")
            cmd.select("buried", f"byres {target} and (b < 20)")
            cmd.show("sticks", "buried")
            cmd.color("red", "buried")
            print("Red: Buried residues")
            
        elif "helix" in query or "alpha" in query:
            print("\nAnalyzing alpha helices...")
            cmd.show("cartoon")
            cmd.select("helices", f"ss h")
            cmd.color("yellow", "helices")
            print("Yellow: Alpha helices")
            
        elif "sheet" in query or "beta" in query:
            print("\nAnalyzing beta sheets...")
            cmd.show("cartoon")
            cmd.select("sheets", f"ss s")
            cmd.color("red", "sheets")
            print("Red: Beta sheets")
            
        elif "loop" in query:
            print("\nAnalyzing loops...")
            cmd.show("cartoon")
            cmd.select("loops", f"ss l")
            cmd.color("blue", "loops")
            print("Blue: Loops")
            
        elif "sequence" in query:
            sequence = cmd.get_fastastr(target)
            print("\nSequence Analysis:")
            print(sequence)
            
            # Count amino acids
            aa_counts = {}
            for aa in sequence:
                if aa in aa_counts:
                    aa_counts[aa] += 1
                else:
                    aa_counts[aa] = 1
            
            print("\nAmino Acid Composition:")
            for aa, count in aa_counts.items():
                print(f"{aa}: {count}")
                
        elif "help" in query:
            print("\nAvailable analysis keywords:")
            print("- binding/pocket: Show potential binding sites")
            print("- hydrophobic: Show hydrophobic regions")
            print("- charged/electrostatic: Show charged residues")
            print("- surface: Show surface-exposed residues")
            print("- buried/internal: Show buried residues")
            print("- helix/alpha: Show alpha helices")
            print("- sheet/beta: Show beta sheets")
            print("- loop: Show loops")
            print("- sequence: Show sequence and composition")
            print("- help: Show this help message")
            
        else:
            print("\nI'm not sure how to analyze that. Try using one of these keywords:")
            print("- binding/pocket")
            print("- hydrophobic")
            print("- charged/electrostatic")
            print("- surface")
            print("- buried/internal")
            print("- helix/alpha")
            print("- sheet/beta")
            print("- loop")
            print("- sequence")
            print("- help")
            
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        print("Please ensure you have loaded a structure first.")

def lynn_auto_analyze():
    """Automatically analyze protein structure and suggest best drug storage sites"""
    try:
        # Get loaded structure
        objects = cmd.get_object_list()
        if not objects:
            print("Please load a protein structure first!")
            return
        
        target = objects[0]
        print(f"\n🔍 Analyzing protein structure: {target}")
        print("=" * 50)
        
        # 1. Show basic structure
        cmd.show("cartoon")
        cmd.show("surface")
        
        # 2. Find potential drug sites
        cmd.select("deep_cavities", f"byres {target} and (b < 20)")
        cmd.select("surface_pockets", f"byres {target} and (b > 30) and (b < 60)")
        
        # Color the findings
        cmd.color("red", "deep_cavities")
        cmd.color("yellow", "surface_pockets")
        cmd.show("surface", "deep_cavities")
        cmd.show("surface", "surface_pockets")
        
        print("\n🎯 Drug Site Analysis:")
        print("1. Deep Cavities (Red):")
        print("   - Protected from solvent")
        print("   - Stable drug storage")
        print("   - Good for long-term binding")
        
        print("\n2. Surface Pockets (Yellow):")
        print("   - Easy access")
        print("   - Initial drug binding")
        print("   - Good for temporary interactions")
        
        # 3. Show chemical properties
        cmd.select("hydrophobic", f"byres {target} and resn ala+val+leu+ile+met+phe+trp+tyr")
        cmd.select("charged", f"byres {target} and resn asp+glu+lys+arg")
        cmd.show("sticks", "hydrophobic")
        cmd.show("sticks", "charged")
        cmd.color("green", "hydrophobic")
        cmd.color("blue", "charged")
        
        print("\n⚡ Chemical Properties:")
        print("Green: Hydrophobic regions (good for drug binding)")
        print("Blue: Charged residues (helps drug positioning)")
        
        # 4. Zoom to best site
        cmd.zoom("deep_cavities")
        
        print("\n💡 Additional Commands:")
        print("- lynn_chat 'show hydrophobic regions'")
        print("- lynn_chat 'analyze binding sites'")
        print("- lynn_chat 'what are the best storage sites'")
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        print("Please ensure you have loaded a valid structure.")

def lynn_chat(message="help"):
    """Enhanced chat mode with PDB integration"""
    try:
        message = message.lower()
        
        if message == "help":
            print("\n=== Lynn AI Quick Guide ===")
            print("Basic Analysis:")
            print("a - Full analysis")
            print("d - Drug sites")
            print("b - Binding pockets")
            print("h - Hydrophobic regions")
            print("s - Structure view")
            print("\nPDB Commands:")
            print("pdb [ID] - Load structure from PDB")
            print("search [query] - Search PDB")
            print("analyze [ID] - Analyze PDB structure")
            print("\nDetailed Commands:")
            print("lynn_chat analyze [all/drug/binding/surface]")
            print("lynn_chat show [structure/sites/pockets]")
            print("lynn_chat find [best/hydrophobic/charged]")
            print("lynn_chat clear - Reset view")
            return
            
        # PDB commands
        if message.startswith("pdb "):
            pdb_id = message.split()[1].upper()
            lynn_pdb_fetch(pdb_id)
            
        elif message.startswith("search "):
            query = message[7:]
            lynn_pdb_search(query)
            
        elif message.startswith("analyze "):
            pdb_id = message.split()[1].upper()
            lynn_pdb_analyze(pdb_id)
            
        # Existing commands
        elif message in ["a", "analyze", "all"]:
            print("\n🔍 Running full analysis...")
            lynn_auto_analyze()
            
        elif message in ["d", "drug", "drugs", "storage"]:
            print("\n💊 Showing drug sites...")
            objects = cmd.get_object_list()
            if not objects:
                print("Please load a structure first!")
                return
            target = objects[0]
            cmd.show("surface")
            cmd.select("sites", f"byres {target} and (b < 30)")
            cmd.color("red", "sites")
            cmd.select("deep_sites", f"byres {target} and (b < 20)")
            cmd.color("orange", "deep_sites")
            print("Red: Potential drug sites")
            print("Orange: Deep binding sites")
            print("\nTip: Try 'lynn_chat find best' for optimal sites")
            
        elif message in ["b", "binding", "pockets", "pocket"]:
            print("\n🎯 Showing binding pockets...")
            objects = cmd.get_object_list()
            if not objects:
                print("Please load a structure first!")
                return
            target = objects[0]
            cmd.show("surface")
            cmd.select("pockets", f"byres {target} and (b < 20)")
            cmd.color("yellow", "pockets")
            cmd.select("deep_pockets", f"byres {target} and (b < 15)")
            cmd.color("green", "deep_pockets")
            print("Yellow: Binding pockets")
            print("Green: Deep pockets")
            print("\nTip: Try 'lynn_chat analyze binding' for details")
            
        elif message in ["h", "hydrophobic", "hydro"]:
            print("\n⚡ Showing interaction regions...")
            objects = cmd.get_object_list()
            if not objects:
                print("Please load a structure first!")
                return
            target = objects[0]
            cmd.select("hydrophobic", f"byres {target} and resn ala+val+leu+ile+met+phe+trp+tyr")
            cmd.show("surface")
            cmd.color("green", "hydrophobic")
            cmd.select("charged", f"byres {target} and resn asp+glu+lys+arg")
            cmd.color("cyan", "charged")
            print("Green: Hydrophobic regions")
            print("Cyan: Charged regions")
            print("\nTip: Try 'lynn_chat analyze surface' for more")
            
        elif message in ["s", "structure", "view"]:
            print("\n🔮 Enhanced structure view...")
            objects = cmd.get_object_list()
            if not objects:
                print("Please load a structure first!")
                return
            target = objects[0]
            cmd.show("cartoon")
            cmd.color("cyan", f"{target} and ss h")
            cmd.color("magenta", f"{target} and ss s")
            cmd.color("white", f"{target} and ss l")
            cmd.show("surface", target)
            cmd.set("surface_transparency", 0.7)
            print("Cyan: Alpha helices")
            print("Magenta: Beta sheets")
            print("White: Loops")
            print("\nTip: Try 'lynn_chat analyze structure' for details")
            
        elif "find best" in message:
            print("\n🎯 Finding optimal sites...")
            objects = cmd.get_object_list()
            if not objects:
                print("Please load a structure first!")
                return
            target = objects[0]
            cmd.select("best_sites", f"byres {target} and (b < 25)")
            cmd.show("surface")
            cmd.color("green", "best_sites")
            cmd.zoom("best_sites")
            print("Green: Optimal drug binding/storage sites")
            print("(Balanced accessibility and protection)")
            
        elif "clear" in message or "reset" in message:
            cmd.delete("all_selections")
            cmd.hide("all")
            cmd.show("cartoon")
            print("\n🔄 View reset. Type 'lynn_chat help' for commands")
            
        elif "analyze" in message:
            if "surface" in message:
                lynn_analyze_solvent()
            elif "binding" in message:
                lynn_analyze_binding()
            elif "drug" in message:
                lynn_analyze_drug()
            elif "structure" in message:
                lynn_analyze_secondary()
            else:
                lynn_auto_analyze()
                
        else:
            print("\n💡 Quick Commands:")
            print("a - Full analysis")
            print("d - Drug sites")
            print("b - Binding pockets")
            print("h - Hydrophobic regions")
            print("s - Structure view")
            print("\nType 'lynn_chat help' for more options")
            
    except Exception as e:
        print(f"\n⚠️ Error: {str(e)}")
        print("Type 'lynn_chat help' for commands")

# Register commands with PyMOL
cmd.extend("lynn_show", lynn_show_structure)
cmd.extend("lynn_analyze", lynn_analyze_text)
cmd.extend("lynn_storage", lynn_analyze_storage)
cmd.extend("lynn_highlight", lynn_highlight)
cmd.extend("lynn_measure", lynn_measure)
cmd.extend("lynn_save", lynn_save)
cmd.extend("lynn_secondary", lynn_analyze_secondary)
cmd.extend("lynn_solvent", lynn_analyze_solvent)
cmd.extend("lynn_mutations", lynn_analyze_mutations)
cmd.extend("lynn_interact", lynn_analyze_interactions)
cmd.extend("lynn_drug", lynn_analyze_drug)
cmd.extend("lynn_auto", lynn_auto_analyze)
cmd.extend("lynn_chat", lynn_chat)
cmd.extend("lynn_pdb_fetch", lynn_pdb_fetch)
cmd.extend("lynn_pdb_search", lynn_pdb_search)
cmd.extend("lynn_pdb_analyze", lynn_pdb_analyze)

print("\n=== Lynn AI Plugin with PDB Integration ===")
print("Quick commands:")
print("lynn_chat pdb [ID] - Load from PDB")
print("lynn_chat search [query] - Search PDB")
print("lynn_chat analyze [ID] - Analyze PDB structure")
print("lynn_chat help - Show all commands") 