# Portal

Hey there, fellow seeker! I'm Mwithiga, and on this adventure, I asked myself: "What if cross-transfer of files from Windows to Linux was easy and user-friendly?" Something my non-techy buddies would simply understand. I went to my mentor and asked this question, which we later debated, hence the birth of Portal—a simple, secure, cross-platform command-line tool for peer-to-peer file transfers on a local network.

## Features

- **Automatic Discovery:** Uses Zeroconf (Bonjour) to automatically find other devices without needing to know IP addresses.
- **Secure Transfer:** Encrypts all file transfers using SSL/TLS with self-signed certificates.
- **Cross-Platform:** Written in Python, it runs on Linux, macOS, and Windows.
- **Peer-to-Peer:** Files are sent directly between your devices, not through a third-party server.

## Project Setup

1.  **Create a Virtual Environment:** This keeps the project's dependencies isolated.
    ```bash
    python3 -m venv venv
    ```

2.  **Activate the Environment:**
    ```bash
    # On Linux/macOS
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Generate Security Certificate:** Create the self-signed certificate needed for encrypted transfers.
    ```bash
    openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "/CN=portal"
    ```

## Usage

You will need two terminals open to test the application.

1.  **Start the Receiver:** In your first terminal, start the listener. It will wait for incoming files.
    ```bash
    python portal.py
    ```

2.  **Send a File:** In your second terminal, use the `sender.py` script, providing the path to the file you want to send.
    ```bash
    python sender.py /path/to/your/file.txt
    ```
    The file will be received and saved as `received_file.txt` in the project directory.

## The Development Journey

My goal was simple, but the path to a reliable tool had some classic networking challenges. Here's how I navigated them.

### The First Hurdle: The Race Condition

My first real challenge was a classic race condition. My initial script had the sender send the file and immediately close the connection. This was too fast for the receiver, which would often crash with a `Connection reset by peer` error because it was trying to read from a connection that was already closed.

### The Second Hurdle: The Deadlock

To solve this, I implemented a handshake: the receiver would send back an "OK" to confirm the transfer. This seemed smart, but it created a new, even trickier problem: a deadlock. The receiver was now waiting for the connection to close to know the file was done, while the sender was waiting for the "OK" message before it would close the connection. Both programs were stuck, waiting for each other.

### The Final Solution: A Better Protocol

I realized the root issue was the lack of a clear "end-of-file" signal within an open connection. The final, and correct, solution was to build a more robust protocol. Now, the sender first sends the filename and the exact file size. This way, the receiver knows exactly how much data to expect, reads it all, and *then* confidently sends back the "OK" confirmation. This approach removed all the ambiguity and finally made the transfer reliable.