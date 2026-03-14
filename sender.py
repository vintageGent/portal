import socket
import time
import sys
import os
import ssl
import struct
import zipfile
import shutil
import hashlib
from datetime import datetime
from mwithiga_labs.shared.reporter import generate_strategic_dispatch
from zeroconf import ServiceBrowser, Zeroconf
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn

console = Console()

class MyServiceListener:
    def __init__(self, file_path):
        self.file_path = file_path
        self.service_info = None
        self.original_path = file_path
        self.temp_zip_path = None
        self.done_event = threading.Event()

    def remove_service(self, zeroconf, type, name):
        pass

    def update_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info and self.service_info is None:
            console.print(f"[bold green]Found Portal service: {name}[/]")
            self.service_info = info
            try:
                self.prepare_and_send()
            finally:
                self.done_event.set()

    def prepare_and_send(self):
        """Prepares the file (zipping if needed) and sends it."""
        file_to_send = self.file_path
        
        # Check if directory
        if os.path.isdir(self.file_path):
            console.print(f"[yellow]'{self.file_path}' is a directory. Zipping it...[/]")
            base_name = os.path.basename(os.path.normpath(self.file_path))
            self.temp_zip_path = shutil.make_archive(base_name, 'zip', self.file_path)
            file_to_send = self.temp_zip_path
            console.print(f"[dim]Created temporary zip: {file_to_send}[/]")

        self.send_file(file_to_send)
        
        # Cleanup temp zip if it was created
        if self.temp_zip_path and os.path.exists(self.temp_zip_path):
            os.remove(self.temp_zip_path)
            console.print("[dim]Temporary zip file removed.[/]")

    def send_file(self, file_path):
        """Connects to the service and sends the file securely."""
        if not self.service_info:
            return

        host = socket.inet_ntoa(self.service_info.addresses[0])
        port = self.service_info.port
        
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        console.print(f"Securely connecting to [cyan]{host}:{port}[/]...")
        try:
            with socket.create_connection((host, port)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    # 0. Send Security Token
                    ssock.sendall(b"PORTAL_SECURE_ACCESS".ljust(1024))
                    auth_res = ssock.recv(1024)
                    if auth_res != b'AUTH_OK':
                        console.print("[bold red]Access Denied: Server rejected security token.[/]")
                        return

                    filesize = os.path.getsize(file_path)
                    filename = os.path.basename(file_path)
                    
                    # Calculate SHA-256 Hash
                    sha256_hash = hashlib.sha256()
                    with open(file_path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
                    file_hash = sha256_hash.hexdigest()

                    console.print(f"Connected. Sending [bold]{filename}[/] ({filesize / (1024*1024):.2f} MB)...")

                    # 1. Send filename
                    ssock.sendall(filename.encode().ljust(1024))

                    # 2. Send filesize
                    ssock.sendall(struct.pack('>Q', filesize))

                    # 2b. Send SHA-256 Hash
                    ssock.sendall(file_hash.encode().ljust(64))

                    # 3. Send file content with Rich Progress
                    with open(file_path, 'rb') as f:
                        with Progress(
                            SpinnerColumn(),
                            TextColumn("[bold blue]{task.fields[filename]}"),
                            BarColumn(),
                            "[progress.percentage]{task.percentage:>3.0f}%",
                            TransferSpeedColumn(),
                            TimeRemainingColumn(),
                            console=console
                        ) as progress:
                            task_id = progress.add_task("Sending", total=filesize, filename=filename)
                            
                            while True:
                                chunk = f.read(4096)
                                if not chunk:
                                    break
                                ssock.sendall(chunk)
                                progress.update(task_id, advance=len(chunk))
                    
                    # 4. Wait for confirmation
                    console.print("\n[dim]Waiting for confirmation...[/]")
                    confirmation = ssock.recv(1024)
                    if confirmation == b'OK':
                        console.print("[bold green]\u2714 Success: Receiver confirmed receipt and integrity.[/]")
                        # Generate Strategic Dispatch for technical evidence
                        generate_strategic_dispatch(filename, file_hash, host, "SEND")
                    elif confirmation == b'INTEGRITY_FAIL':
                        console.print("[bold red]\u2718 Failure: Receiver reported an integrity mismatch![/]")
                    else:
                        console.print("[red]Warning: Receiver sent an unexpected response.[/]")

        except Exception as e:
            console.print(f"[bold red]Failed to send file: {e}[/]")

import threading

def start_sender(path, timeout=30):
    if not os.path.exists(path):
        console.print(f"[bold red]Error: Path '{path}' not found.[/]")
        sys.exit(1)

    zeroconf = Zeroconf()
    listener = MyServiceListener(path)
    browser = ServiceBrowser(zeroconf, "_portal._tcp.local.", listener)

    console.print(f"[yellow]Searching for Portal receivers on the network (Timeout: {timeout}s)...[/]")
    
    # Wait for completion or timeout
    is_done = listener.done_event.wait(timeout)
    
    if not is_done:
        console.print(f"\n[red]Timeout: No Portal receiver found after {timeout} seconds.[/]")
    
    zeroconf.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sender.py <file>")
    else:
        start_sender(sys.argv[1])

