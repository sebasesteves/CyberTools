# ==========================================
# CYBERTOOLS - TCP PORT SCANNER
# Developed by Sebastião Esteves
# GitHub: sebas
# Version: 1.0
# Status: In Development
# ==========================================

import datetime
import ipaddress
import json
from pathlib import Path
import socket
import subprocess

HISTORY_FILE = Path(__file__).with_name('historico.json')
TOTAL_PORTS = 65535


def load_history():
    if not HISTORY_FILE.exists():
        return []
    with HISTORY_FILE.open('r', encoding='utf-8') as file:
        history = json.load(file)
    if not isinstance(history, list):
        raise ValueError('History must contain a list.')
    return history


def save_scan(scan):
    history = load_history()
    history.append(scan)
    temporary = HISTORY_FILE.with_suffix('.tmp')
    with temporary.open('w', encoding='utf-8') as file:
        json.dump(history, file, indent=4, ensure_ascii=False)
    temporary.replace(HISTORY_FILE)


def identify_processes():
    processes = {}
    try:
        result = subprocess.run(['ss', '-tlnp'], capture_output=True, text=True, check=True)
    except (OSError, subprocess.SubprocessError):
        return processes
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 4 and 'users:(("' in line and 'pid=' in line:
            try:
                port = int(parts[3].rsplit(':', 1)[-1])
                name = line.split('(("', 1)[1].split('"', 1)[0]
                pid = int(line.split('pid=', 1)[1].split(',', 1)[0].split(')', 1)[0])
                processes[port] = {'process': name, 'pid': pid}
            except (ValueError, IndexError):
                continue
    return processes


def scan():
    target = input('Local IPv4 address [127.0.0.1]: ').strip() or '127.0.0.1'
    try:
        address = ipaddress.IPv4Address(target)
    except ValueError:
        print('Invalid IPv4 address.')
        return
    if not address.is_loopback:
        print('This release supports local loopback diagnostics only.')
        return
    processes = identify_processes()
    started = datetime.datetime.now().isoformat()
    open_ports = []
    services = {}
    for port in range(1, TOTAL_PORTS + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.settimeout(0.5)
            if client.connect_ex((target, port)) == 0:
                open_ports.append(port)
                try:
                    service = socket.getservbyport(port, 'tcp')
                except OSError:
                    service = 'Unknown'
                services[str(port)] = service
                print(f'\n[OPEN] {port} | {service}')
                if port in processes:
                    info = processes[port]
                    print(f"Local process: {info['process']} | PID: {info['pid']}")
        filled = port * 20 // TOTAL_PORTS
        print(f'\rProgress: [{"#" * filled}{"-" * (20-filled)}] {port / TOTAL_PORTS:.2%}', end='', flush=True)
    print(f'\nScan complete. Open ports: {len(open_ports)}')
    # Keep existing history keys for compatibility with the earlier release.
    save_scan({'data_hora': started, 'ip': target, 'portas_abertas': open_ports,
               'total': len(open_ports), 'servico': services,
               'portas_analisadas': TOTAL_PORTS})
    print('Scan saved successfully.')


def show_history():
    history = load_history()
    if not history:
        print('No saved scans.')
    for number, entry in enumerate(history, 1):
        print(f'\n--- Scan {number} ---')
        for key, label in [('data_hora', 'Date'), ('ip', 'IP'), ('portas_abertas', 'Open ports'),
                           ('total', 'Total'), ('servico', 'Services'), ('portas_analisadas', 'Ports checked')]:
            print(f'{label}: {entry.get(key, "Unknown")}')


def main():
    print('=== CyberTool ===')
    while True:
        print('\n0. Exit\n1. Local TCP scan\n2. View history')
        option = input('Choose an option: ').strip()
        try:
            if option == '0':
                return
            if option == '1':
                scan()
            elif option == '2':
                show_history()
            else:
                print('Invalid option.')
        except (OSError, ValueError, AttributeError) as error:
            print(f'Error: {error}')
        except KeyboardInterrupt:
            print('\nOperation cancelled.')


if __name__ == '__main__':
    main()
