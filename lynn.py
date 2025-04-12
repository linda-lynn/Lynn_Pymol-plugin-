#!/usr/bin/env python3
"""
Lynn - A drug delivery AI for tumor targeting with chemistry knowledge.
"""

import os
import sys
import json
import time
import requests
from rich.console import Console
from rich.markdown import Markdown
from rich import print as rprint
from rich.panel import Panel
from dotenv import load_dotenv
from rich.prompt import Prompt
from typing import List, Dict, Optional
import openai

# Import chemistry knowledge module
import chem_knowledge

# Load environment variables
load_dotenv()

# Initialize console
console = Console()

class LynnAI:
    def __init__(self):
        self.console = Console()
        self.name = "Lynn"
        self.version = "1.0.0"
        self.history = []
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.deepseek_api_key:
            self.console.print("[red]Warning: DEEPSEEK_API_KEY not found in .env file. Some features may be limited.[/red]")
        
        # Set up OpenAI client
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            self.console.print("[red]Warning: OPENAI_API_KEY not found in .env file.[/red]")
            self.console.print("[yellow]Please create a .env file with your OpenAI API key.[/yellow]")
            self.console.print("Example: OPENAI_API_KEY=your-api-key-here")
            sys.exit(1)
        
        openai.api_key = self.openai_api_key
        
        # System prompt for the AI
        self.system_prompt = """
        You are Lynn, an AI assistant specializing in drug delivery systems and tumor targeting.
        Your expertise includes:
        - Various drug delivery systems (liposomes, nanoparticles, etc.)
        - Tumor targeting mechanisms
        - Tumor microenvironment
        - Specific anticancer drugs
        - EPR effect and other delivery concepts
        
        Provide accurate, scientific information based on the latest research.
        """
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict:
        """Load the knowledge base from JSON file."""
        try:
            with open('chem_knowledge.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.console.print("[red]Warning: chem_knowledge.json not found. Using empty knowledge base.[/red]")
            return {}
            
    def _get_local_knowledge(self, query: str) -> Optional[str]:
        """Search local knowledge base for relevant information."""
        query = query.lower()
        for category, items in self.knowledge_base.items():
            for item in items:
                if query in item['name'].lower() or query in item['description'].lower():
                    return f"From local knowledge base:\n{item['description']}"
        return None

    def _call_deepseek_api(self, messages: List[Dict]) -> str:
        """Call DeepSeek API for enhanced responses."""
        if not self.deepseek_api_key:
            return "API key not configured. Using local knowledge only."
            
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-coder",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            self.console.print(f"[red]Error calling DeepSeek API: {str(e)}[/red]")
            return "Error getting response from DeepSeek API. Using local knowledge only."

    def generate_response(self, user_input: str) -> str:
        """Generate response using OpenAI API with enhanced chemistry knowledge"""
        try:
            # Get local chemistry knowledge
            local_knowledge = self._get_local_knowledge(user_input)
            
            # Update conversation history
            self.history.append({"role": "user", "content": user_input})
            
            # Prepare messages with system prompt
            messages = [
                {"role": "system", "content": self.system_prompt},
            ]
            
            # Add local knowledge if available
            if local_knowledge:
                messages.append({
                    "role": "system", 
                    "content": f"Relevant chemistry knowledge:\n{local_knowledge}"
                })
            
            # Add conversation history (last 10 exchanges)
            messages.extend(self.history[-10:])
            
            # Generate response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message['content']
            self.history.append({"role": "assistant", "content": answer})
            return answer
            
        except Exception as e:
            console.print(f"[bold red]Error generating response: {e}[/bold red]")
            return "I'm having trouble connecting to my knowledge base. Please try again."

    def welcome(self):
        """Display welcome message"""
        console.print(Panel.fit(
            f"[bold green]{self.name} v{self.version}[/bold green]\n"
            "[yellow]A drug delivery AI for tumor targeting with chemistry knowledge[/yellow]\n"
            "Type 'exit' or 'quit' to end the session."
        ))
    
    def get_web_info(self, query):
        """Search the web for relevant information (simplified)"""
        try:
            # Using a search API would be better, but this is a simplified example
            search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(search_url)
            return response.json()
        except Exception as e:
            console.print(f"[red]Error searching web: {e}[/red]")
            return None
    
    def get_local_knowledge(self, query):
        """Get relevant information from local chemistry knowledge base"""
        knowledge_info = {}
        
        # Check for relevant keywords to determine which knowledge to include
        if any(term in query.lower() for term in ["liposome", "micelle", "dendrimer", "nanoparticle", "delivery system"]):
            knowledge_info["delivery_systems"] = chem_knowledge.get_info("delivery_systems")
        
        if any(term in query.lower() for term in ["target", "targeting", "epr", "receptor", "ligand"]):
            knowledge_info["targeting"] = chem_knowledge.get_info("targeting_mechanisms")
        
        if any(term in query.lower() for term in ["tumor", "microenvironment", "ph", "hypoxia"]):
            knowledge_info["tumor_environment"] = chem_knowledge.get_info("tumor_microenvironment")
        
        if any(term in query.lower() for term in ["drug", "doxorubicin", "paclitaxel", "cisplatin", "gemcitabine"]):
            knowledge_info["drugs"] = chem_knowledge.get_info("anticancer_drugs")
        
        return knowledge_info
    
    def run(self):
        """Run the main interaction loop"""
        self.welcome()
        
        console.print("\n[bold cyan]Setting up chemistry knowledge base...[/bold cyan]")
        time.sleep(1)
        console.print("[bold green]Knowledge base initialized![/bold green]")
        
        while True:
            try:
                query = Prompt.ask("\n[bold yellow]You:[/bold yellow]")
                
                if query.lower() in ['exit', 'quit', 'bye']:
                    console.print("\n[bold green]Thank you for using Lynn. Goodbye![/bold green]")
                    break
                
                console.print("\n[bold cyan]Lynn:[/bold cyan] ", end="")
                
                # Simple loading animation
                with console.status("[bold green]Thinking...[/bold green]"):
                    response = self.generate_response(query)
                
                # Display the formatted response
                console.print(Markdown(response))
                
            except KeyboardInterrupt:
                console.print("\n\n[bold red]Session interrupted. Exiting...[/bold red]")
                break
            except Exception as e:
                console.print(f"\n[bold red]Error: {e}[/bold red]")


if __name__ == "__main__":
    lynn = LynnAI()
    lynn.run() 