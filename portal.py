import socket
import time
import ssl
import struct
import os
import threading
from zeroconf import ServiceInfo, Zeroconf
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.panel import Panel

console = Console()

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def handle_connection(conn, addr, output_dir):
    """Handles an incoming file transfer connection."""
    console.print(f"[green]Connection accepted from {addr}[/]")
    try:
        # 1. Receive filename
        filename_bytes = conn.recv(1024)
        filename = filename_bytes.decode().strip()
        filename = os.path.basename(filename) # Sanitize
        
        # 2. Receive file size
        filesize_bytes = conn.recv(8)
        filesize = struct.unpack('>Q', filesize_bytes)[0]
        
        save_path = os.path.join(output_dir, filename)
        
        # 3. Receive file content with Rich Progress
        bytes_received = 0
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[filename]}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            task_id = progress.add_task("Downloading", total=filesize, filename=filename)
            
            with open(save_path, 'wb') as f:
                while bytes_received < filesize:
                    chunk_size = 4096
                    remaining = filesize - bytes_received
                    if remaining < chunk_size:
                        chunk_size = remaining
                        
                    chunk = conn.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
                    bytes_received += len(chunk)
        
        console.print(f"[bold green]\u2714 File saved to:[/][white] {save_path}[/]")
        # 4. Send confirmation
        conn.sendall(b'OK')

    except Exception as e:
        console.print(f"[bold red]Error during transfer: {e}[/]")
    finally:
        conn.close()

def start_receiver(port, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    service_type = "_portal._tcp.local."
    service_name = f"Portal on {socket.gethostname()}._portal._tcp.local."
    ip_address = get_ip_address()

    # SSL Context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    if not os.path.exists('cert.pem') or not os.path.exists('key.pem'):
        console.print("[red]Certificates not found! Please run via 'cli.py' to generate them.[/]")
        return
        
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # Register Service
    info = ServiceInfo(
        type_=service_type, name=service_name,
        addresses=[socket.inet_aton(ip_address)], port=port,
    )
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_address, port))
    server_socket.listen(5)
    
    console.print(Panel(
        f"[bold]Receiver Active[/]\n"
        f"IP: [cyan]{ip_address}[/]\n"
        f"Port: [cyan]{port}[/]\n"
        f"Saving to: [yellow]{os.path.abspath(output_dir)}[/]",
        title="Portal Listening",
        border_style="green"
    ))
    console.print("[dim]Press Ctrl+C to stop...[/]")

    try:
        while True:
            conn, addr = server_socket.accept()
            try:
                secure_conn = context.wrap_socket(conn, server_side=True)
                thread = threading.Thread(target=handle_connection, args=(secure_conn, addr, output_dir))
                thread.start()
            except ssl.SSLError as e:
                console.print(f"[red]SSL Error: {e}[/]")
                conn.close()
    except KeyboardInterrupt:
        console.print("\n[yellow]Shutting down Portal...[/]")
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()
        server_socket.close()

if __name__ == "__main__":
    # Fallback to default args if run directly
    start_receiver(8080, ".")