import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# === CONFIGURABLE ===
START_PORT = 1
END_PORT = 65535  # Inclusive
THREADS = 500
TIMEOUT = 0.5  # seconds

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(TIMEOUT)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"[+] {ip}:{port} is OPEN")  # Verbose output here
                return port
    except:
        pass
    return None

def scan_ip(ip):
    print(f"[>] Scanning {ip}...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(START_PORT, END_PORT + 1)}
        for future in as_completed(futures):
            port = future.result()
            if port:
                open_ports.append(port)
    return open_ports

def load_ips(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main(ip_file):
    ip_list = load_ips(ip_file)
    for ip in ip_list:
        open_ports = scan_ip(ip)
        if open_ports:
            print(f"[!] {ip} open ports summary: {', '.join(map(str, open_ports))}")
        else:
            print(f"[-] {ip} has no open ports in range {START_PORT}-{END_PORT}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} ip_list.txt")
        sys.exit(1)
    main(sys.argv[1])
