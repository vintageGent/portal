import os
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.menu import Menu
from rich.prompt import Prompt

console = Console()

TOOLS = {
    "1": {"name": "Portal", "path": "/home/seeker/portal/cli.py", "desc": "Encrypted Data Transfer Assurance (Local-First)"},
    "2": {"name": "ThreatScope", "path": "/home/seeker/ThreatScopeV2/threatscope.py", "desc": "Perimeter Vulnerability & Risk Assessment"},
    "3": {"name": "Dispatch", "path": "/home/seeker/dispatch/main.py", "desc": "Communications Asset & Contact Intelligence"},
    "4": {"name": "The Lede", "path": "/home/seeker/the-lede/index.html", "desc": "Strategic Intelligence Analysis (Client-side)"},
    "5": {"name": "Digital Exposure Audit", "path": "/home/seeker/dispatch/recon.py", "desc": "Intelligence pivot for institutional & executive exposure"},
}

def display_banner():
    banner = """
    [bold cyan]
    __  ___      _ __    _               __        __        
   /  |/  /_  __(_) /_  / /_  ____ _____ / / ____ _/ /_  _____
  / /|_/ / / / / / __/ / __ \/ __ `/ __ `/ / / __ `/ __ \/ ___/
 / /  / / /_/ / / /_  / / / / /_/ / /_/ / / / /_/ / /_/ (__  ) 
/_/  /_/\__,_/_/\__/ /_/ /_/\__,_/\__, /_/  \__,_/_.___/____/  
                                 /____/                        
    [/bold cyan]
    [italic]Digital Risk & Compliance Intelligence Practice[/italic]
    """
    console.print(Panel(banner, border_style="cyan"))

def launch_tool(tool_id):
    tool = TOOLS.get(tool_id)
    if not tool:
        return

    console.print(f"\n[bold green][*] Launching {tool['name']}...[/bold green]")
    
    if tool['name'] == "The Lede":
        console.print(f"[yellow][!] The Lede is a web tool. Opening in your browser...[/yellow]")
        os.system(f"xdg-open {tool['path']}")
        return

    # For Python tools, we execute them in their respective venvs if possible
    tool_dir = os.path.dirname(tool['path'])
    venv_python = os.path.join(tool_dir, "venv", "bin", "python3")
    
    python_cmd = venv_python if os.path.exists(venv_python) else "python3"
    
    try:
        subprocess.run([python_cmd, tool['path']], cwd=tool_dir)
    except KeyboardInterrupt:
        console.print("\n[yellow][!] Tool session ended.[/yellow]")

def main():
    while True:
        os.system('clear')
        display_banner()
        
        console.print("[bold]Available Tools:[/bold]")
        for key, tool in TOOLS.items():
            console.print(f"[bold cyan]{key}.[/bold cyan] [bold]{tool['name']}[/bold] - [dim]{tool['desc']}[/dim]")
        
        console.print("[bold cyan]Q.[/bold cyan] [bold]Exit[/bold]")
        
        choice = Prompt.ask("\nSelect a tool to deploy", choices=list(TOOLS.keys()) + ["q", "Q"])
        
        if choice.lower() == "q":
            console.print("[bold cyan]Session terminated. Mwithiga Labs Intelligence practice is offline.[/bold cyan]")
            break
            
        launch_tool(choice)

if __name__ == "__main__":
    main()
