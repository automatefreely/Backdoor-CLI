# Backdoor CLI
Backdoor CLI is a simple backdoor written in python3. It allows you to execute commands on a remote machine through internet. It is a simple reverse shell with a few extra features.

## Features
### Current Features
- Execute commands on a remote machine and get the output
- Download files from the remote machine
- Upload files to the remote machine
- Screen capture the remote machine and save it as an image
- Keylogger
- Persistence

### Future Features
- Webcam capture
- Audio capture
- Automatic persistence
- Automatic setup process
- Execute commands on multiple hosts
- Download files from multiple hosts
- Upload files to multiple hosts
- Screen Recording capture

## Installation
### Requirements
- Python3
- Python3-pip

### Changes in code before installation
- Change the IP address in the server.py and backdoor.pyw file to your IP address
- Change the port number in the server.py file to your desired port number

### Installation
1. Clone the repository
```bash
git clone
```
2. Install the requirements
```bash
pip3 install -r requirements.txt
```
3. Run the server on your machine
```bash
python3 server.py
```
4. Run the backdoor.pyw on the remote machine (Host) to get the connection. The backdoor will run in the background and try to connect to the server every 10 seconds (Which can be change by changing the constant defined in backdoor.pyw).
```bash
python3 client.py
```
Note: Requirement need to be installed on both the machines. Or you can use PyInstaller to create an executable file of backdoor.pyw and run it on the remote machine (Host).

## Usage
### Commands
- help: Display the help menu
- exit: Exit the program
- cd *Directory*: Change the directory
- upload *File Path*: Upload the file to the remote machine at current location which can be change using cd
- download *File Path*: Download the file from the remote machine at current location
- keylog_start: Start the keylogger
- keylog_dump: Dump the keylogger data
- keylog_stop: Stop the keylogger
- screenshot: Take a screenshot of the remote machine
- Default: Execute the command on the remote machine

