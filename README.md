# Portal

Hey there, fellow seeker! I'm Mwithiga.

I built Portal to solve a persistent frustration: the friction of moving files between machines on the same network. I wanted something that felt like a "portal"—instant, secure, and requiring zero configuration. 

Portal is my exploration into P2P networking and encryption. It is a zero-configuration, secure file transfer tool designed for speed and simplicity. By using local network discovery (mDNS) and automated SSL encryption, it allows you to move files between machines instantly through a professional, interactive CLI.

## The Development Journey

The main challenge I faced was handling the technical complexities of discovery and security without burdening the user. Most file-sharing tools require manual IP entry or complex setup. I wanted to eliminate that.

By implementing Multicast DNS (mDNS) through the `zeroconf` library, I allowed instances of Portal to "find" each other automatically on a local network. Security was the next priority; I automated the generation of SSL certificates to ensure that every transfer is encrypted from end to end, without the user ever needing to touch a configuration file.

This project was a great exercise in balancing robust backend networking with a clean, user-friendly frontend. Using the `rich` library allowed me to create a terminal interface that feels modern and provides real-time feedback through progress bars and status updates.

## How it Works (The "Push" Model)

Think of Portal like **passing a sealed note** to a friend in class.

*   **You (The Sender):** Choose exactly *which* note (file) to pass.
*   **They (The Receiver):** Just hold out their hand (open Portal) to take it.

**Why this way?**
It's safer. Instead of letting someone browse your computer to "pull" what they want, you explicitly "push" **only** the file you want to share. Nothing else on your computer is seen or touched.

## Features

- **Zero Configuration**: Automatically discovers other Portal instances on the local network.
- **End-to-End Encryption**: Every transfer is secured with automated SSL/TLS.
- **Interactive CLI**: A user-friendly menu system for sending and receiving files.
- **Automatic Compression**: Transparently zips folders before transmission to ensure efficient transfers.

## Getting Started

To get started with Portal, follow these steps to set up the environment on each machine.

### Prerequisites

- Python 3.x
- `pip`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vintageGent/portal.git
   cd portal
   ```
2. Set up the environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 2. How to Use

**Step A: The Receiver (The destination computer)**
1.  Run the app: `python3 cli.py`
2.  Select **Option 1: Receive File**.
3.  That's it! It's now waiting.

**Step B: The Sender (The source computer)**
1.  Run the app: `python3 cli.py`
2.  Select **Option 2: Send File**.
3.  It will ask: `Enter path to file or directory`.
    *   **Tip:** You can just drag and drop the file into the terminal window to get the path!
4.  Portal will find the Receiver automatically and beams the file over. 🚀
3. **Help**: Provides a quick walkthrough of the tool's capabilities.

## A Personal Connection

Portal represents my commitment to the "seeker" philosophy—finding elegant solutions to common problems. It turns the complex task of secure P2P networking into a seamless experience, allowing the focus to remain on the content being shared, rather than the mechanism of sharing.
Portal represents my commitment to the "seeker" philosophy—finding elegant solutions to common problems. It turns the complex task of secure P2P networking into a seamless experience, allowing the focus to remain on the content being shared, rather than the mechanism of sharing.
