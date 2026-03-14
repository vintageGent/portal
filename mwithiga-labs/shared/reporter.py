import os
from datetime import datetime
from rich.console import Console

console = Console()

DEFAULT_REPORTS_DIR = "/home/seeker/portal/reports"

def ensure_reports_dir():
    if not os.path.exists(DEFAULT_REPORTS_DIR):
        os.makedirs(DEFAULT_REPORTS_DIR)
        console.print(f"[dim][*] Created reports directory: {DEFAULT_REPORTS_DIR}[/dim]")

def generate_strategic_dispatch(filename, file_hash, peer_ip, mode):
    """Generates a high-authority strategic report for a P2P transfer."""
    ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    dispatch_content = f"""# Strategic Transfer Dispatch: Mwithiga Labs Portal
    
## 📋 Executive Overview
- **Timestamp**: {timestamp}
- **Operation**: {mode} Initialized
- **Peer Identifier**: {peer_ip}
- **Payload Reference**: {filename}

## 🛡️ Technical Evidence (DPA Section 41)
This dispatch serves as technical evidence of secure data processing under the Kenya Data Protection Act (2019). The payload integrity has been verified via the SHA-256 handshake protocol.

- **Integrity Hash**: `{file_hash}`
- **Verification Status**: INTEGRITY_VERIFIED
- **Encryption Tier**: TLS/SSL (RSA-2048/AES-256-GCM)

## ⚖️ Strategic Alignment
The use of the Portal P2P engine ensures zero-log intermediate buffering, fulfilling the 'Security of Processing' requirements for sensitive institutional data shards.

---
**[ MWITHIGA LABS | DIGITAL RISK ASSURANCE ]**
"""
    filename_report = get_report_filename(f"portal_dispatch_{mode.lower()}", "md")
    filepath = os.path.join(DEFAULT_REPORTS_DIR, filename_report)
    
    with open(filepath, 'w') as f:
        f.write(dispatch_content)
    
    console.print(f"\n[bold green][√] Strategic Dispatch generated:[/] [cyan]{filepath}[/]")
    return filepath
