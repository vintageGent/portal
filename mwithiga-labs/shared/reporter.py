import os
from datetime import datetime
from rich.console import Console

console = Console()

DEFAULT_REPORTS_DIR = "/home/seeker/portal/reports"

def ensure_reports_dir():
    if not os.path.exists(DEFAULT_REPORTS_DIR):
        os.makedirs(DEFAULT_REPORTS_DIR)
        console.print(f"[dim][*] Created reports directory: {DEFAULT_REPORTS_DIR}[/dim]")

def get_report_filename(prefix, extension):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def save_report(content, prefix, extension, binary=False):
    ensure_reports_dir()
    filename = get_report_filename(prefix, extension)
    filepath = os.path.join(DEFAULT_REPORTS_DIR, filename)
    
    mode = 'wb' if binary else 'w'
    with open(filepath, mode) as f:
        f.write(content)
    
    console.print(f"\n[bold green][√] Report saved to:[/] [cyan]{filepath}[/]")
    return filepath
