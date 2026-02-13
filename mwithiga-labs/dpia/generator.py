import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Add shared reporter back in later
# from mwithiga_labs.shared.reporter import save_report

console = Console()

def display_banner():
    banner = """
    [bold green]
     _____  _____          _____ _     _      _     _ 
    |  __ \|  __ \        / ____| |   (_)    | |   | |
    | |  | | |__) |______| (___ | |__  _  ___| | __| |
    | |  | |  ___/|______|\\___ \\| '_ \\| |/ _ \\ |/ _` |
    | |__| | |            ____) | | | | |  __/ | (_| |
    |_____/|_|           |_____/|_| |_|_|\\___|_|\\__,_|
    [/bold green]
    [italic]DPA Shield: Automated DPIA Generator (v1.0)[/italic]
    """
    console.print(Panel(banner, border_style="green"))

def run_dpia():
    os.system('clear')
    display_banner()
    
    console.print("[bold yellow]This assessment will help you determine if your data processing requires an official DPIA under the Kenya Data Protection Act 2019.[/bold yellow]\n")

    results = {}
    
    # 1. Context
    results['company_name'] = Prompt.ask("Company Name")
    results['project_name'] = Prompt.ask("Project/Process Name")
    
    # 2. Screening Questions (ODPC Triggers)
    console.print("\n[bold cyan]Section A: Screening (DPIA Triggers)[/bold cyan]")
    
    triggers = [
        ("Large-scale processing of sensitive personal data?", "sensitive_data"),
        ("Use of new or emerging technologies (AI, biometrics)?", "new_tech"),
        ("Automated decision-making with significant legal effects?", "automated_decisions"),
        ("Public monitoring (CCTV, systematic observation)?", "public_monitoring"),
        ("Cross-border data transfers outside of Kenya?", "cross_border")
    ]
    
    risk_score = 0
    results['triggers'] = []
    
    for q, key in triggers:
        if Confirm.ask(q):
            results['triggers'].append(q)
            risk_score += 1
            
    # 3. Assessment
    console.print("\n[bold cyan]Section B: Data Map[/bold cyan]")
    results['data_types'] = Prompt.ask("What types of personal data are you collecting? (e.g. Emails, Health, Financials)")
    results['retention'] = Prompt.ask("How long will this data be stored? (Retention Period)")
    
    # Generate Report Preview
    os.system('clear')
    display_banner()
    
    table = Table(title="DPIA Risk Assessment Summary")
    table.add_column("Requirement", style="cyan")
    table.add_column("Status", style="magenta")
    
    table.add_row("Official DPIA Mandatory?", "YES (High Risk)" if risk_score >= 1 else "NO (Low Risk)")
    table.add_row("Risk Triggers Found", str(risk_score))
    table.add_row("Primary Data Category", results['data_types'])
    
    console.print(table)
    
    if risk_score >= 1:
        console.print("\n[bold red][!] ACTION REQUIRED:[/bold red] You must submit an official DPIA report to the ODPC before starting this project.")
    else:
        console.print("\n[bold green][√] RECOMMENDATION:[/bold green] Maintain basic record of processing. No mandatory DPIA filing identified.")

    # In future: save to PDF/HTML
    console.print("\n[dim]The full DPIA report logic (Appendix C compatibility) will be implemented next.[/dim]")

if __name__ == "__main__":
    run_dpia()
