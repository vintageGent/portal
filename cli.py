import argparse
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich import print as rprint

console = Console()

def display_banner():
    banner = r"""
    [bold cyan]
      _____           _        _ 
     |  __ \         | |      | |
     | |__) |__  _ __| |_ __ _| |
     |  ___/ _ \| '__| __/ _` | |
     | |  | (_) | |  | || (_| | |
     |_|   \___/|_|   \__\__,_|_|
                                 
    [bold white]Simple. Secure. Fast.[/]
    [/bold cyan]
    """
    console.print(Panel(banner, border_style="cyan"))
    console.print("[italic]Welcome to Portal! A simple, secure, P2P file transfer tool for your local network.[/italic]\n")

def check_certs():
    """Checks for certificates and generates them if missing."""
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        console.print("[yellow]certs not found. Generating self-signed certificate...[/]")
        try:
            # Using basic openssl command
            subprocess.run(
                ["openssl", "req", "-x509", "-newkey", "rsa:2048", 
                 "-keyout", "key.pem", "-out", "cert.pem", 
                 "-sha256", "-days", "365", "-nodes", 
                 "-subj", "/CN=portal"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            console.print("[green]Certificates generated successfully![/]")
        except FileNotFoundError:
             console.print("[bold red]Error: 'openssl' command not found. Please install openssl to generate certificates.[/]")
             sys.exit(1)
        except subprocess.CalledProcessError:
             console.print("[bold red]Error: Failed to generate certificates.[/]")
             sys.exit(1)

def display_help():
    console.print(Panel("""
[bold]PORTAL - USAGE GUIDE[/]

[bold cyan]1. Receiver Mode[/]
   - Use this on the computer that will [bold]RECEIVE[/] files.
   - It will start a secure server and announce itself on the network.
   - [yellow]Port[/]: Default is 8080. Change if needed.
   - [yellow]Output Dir[/]: Where files will be saved (default is current folder).

[bold cyan]2. Sender Mode[/]
   - Use this on the computer [bold]SENDING[/] the files.
   - You just need to provide the path to the file or folder.
   - [green]Tip[/]: If you send a folder, Portal automatically zips it for you!

[bold cyan]3. How it works[/]
   - Portal uses Zeroconf (Bonjour) to find other computers automatically.
   - Transfers are encrypted with SSL.
   - No internet required! It all happens on your WiFi/LAN.
    """, title="Help & Walkthrough", border_style="green"))
    input("\nPress Enter to return to menu...")

def run_interactive():
    """Runs the interactive menu."""
    while True:
        display_banner()
        console.print("[bold]=== PORTAL MENU ===[/]")
        console.print("1. Receive File")
        console.print("2. Send File")
        console.print("3. Help / Usage Guide")
        console.print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ")
        
        if choice == '1':
            console.print("[dim]Starting Receiver (Auto-finding port)...[/]")
            out_dir = input("Enter output directory (default: .): ") or "."
            
            from portal import start_receiver
            # Port logic is now handled in portal.py's start_receiver via find_available_port
            start_receiver(8080, out_dir)
            input("\nPress Enter to return to menu...")
            
        elif choice == '2':
            path = input("Enter path to file or directory: ")
            if not path:
                console.print("[red]Path is required![/]")
                time.sleep(1)
                continue
                
            from sender import start_sender
            start_sender(path)
            input("\nPress Enter to return to menu...")
            
        elif choice == '3':
            display_help()
            
        elif choice == '4':
            console.print("[green]Goodbye![/]")
            sys.exit(0)
        else:
            console.print("[red]Invalid choice.[/]")
            import time
            time.sleep(1)

def main():
    check_certs()
    
    if len(sys.argv) == 1:
        run_interactive()
        return

    display_banner()
    
    parser = argparse.ArgumentParser(description="Portal: P2P File Transfer")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Receive Command
    receive_parser = subparsers.add_parser("receive", help="Start accepting files")
    receive_parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    receive_parser.add_argument("--out", default=".", help="Output directory")

    # Send Command
    send_parser = subparsers.add_parser("send", help="Send a file")
    send_parser.add_argument("path", help="Path to file or directory")
    send_parser.add_argument("--timeout", type=int, default=30, help="Discovery timeout")

    args = parser.parse_args()
    
    # Lazy import to speed up initial load and banner display
    if args.command == "receive":
        from portal import start_receiver
        start_receiver(args.port, args.out)
    elif args.command == "send":
        from sender import start_sender
        start_sender(args.path, args.timeout)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
