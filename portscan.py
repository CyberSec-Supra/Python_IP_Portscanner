#!/usr/bin/env python3

import socket
import ipaddress
import argparse
import concurrent.futures
import os

def scan_port(ip, port, timeout=1.0):
    try:
        with socket.create_connection((str(ip), int(port)), timeout=timeout):
            return f"{ip}:{port}"
    except:
        return None

def expand_targets(target_input):
    if os.path.isfile(target_input):
        with open(target_input, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
        return [ipaddress.ip_address(line) for line in lines]
    else:
        try:
            return list(ipaddress.ip_network(target_input, strict=False).hosts())
        except ValueError:
            return [ipaddress.ip_address(target_input)]

def expand_ports(port_range):
    ports = set()
    for part in port_range.split(','):
        if '-' in part:
            start, end = part.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def main():
    parser = argparse.ArgumentParser(description="Threaded TCP Port Scanner with Full Scan Option")
    parser.add_argument("target", help="IP/subnet or path to IP list file (e.g. 192.168.1.0/24 or live_hosts.txt)")
    parser.add_argument("-p", "--ports", default="22,80,443,445,3389", help="Ports or ranges (e.g. 80,443,8000-8100)")
    parser.add_argument("--full-scan", action="store_true", help="Scan all 65535 ports")
    parser.add_argument("-o", "--output", help="Output file for open ports")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout (default: 1.0s)")
    args = parser.parse_args()

    targets = expand_targets(args.target)
    ports = list(range(1, 65536)) if args.full_scan else expand_ports(args.ports)

    print(f"[*] Scanning {len(targets)} IPs across {len(ports)} ports with {args.threads} threads...")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_target = {
            executor.submit(scan_port, ip, port, args.timeout): (ip, port)
            for ip in targets
            for port in ports
        }

        for future in concurrent.futures.as_completed(future_to_target):
            result = future.result()
            if result:
                print(f"[+] Open: {result}")
                open_ports.append(result)

    if args.output:
        with open(args.output, "w") as f:
            for entry in open_ports:
                f.write(entry + "\n")
        print(f"\n[+] Results saved to: {args.output}")
    else:
        print(f"\n[+] {len(open_ports)} open ports found.")

if __name__ == "__main__":
    main()
