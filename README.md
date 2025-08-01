# Python_IP_Portscanner
Lightweight Python IP and open Port scanner

The python application take a text file IP addresses and performs a fast scan of the IP's for all TCP ports
If a port is found to be open, it will display the open port.

usage:
usage: portscan.py [-h] [-p PORTS] [--full-scan] [-o OUTPUT] [-t THREADS] [--timeout TIMEOUT] targe
usage: python3 tcp_scanner.py 192.168.1.0/24 -p 22,80,443 -o open_ports.txt (with supplied subnet)
usage: python3 tcp_scanner.py live_hosts.txt -p 21-25,80,443,3306 -o open_ports.txt

If Both -p and --full-scan are provided, prioritizes fullscan 
INPUT.txt
172.16.XXX.XXX</br>
172.16.XXX.XXX</br>
192.168.XXX.XXX</br>
10.0.XXX.XXX</br>
