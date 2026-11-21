# ==========================================
# CYBERTOOLS - TCP PORT SCANNER
# Developed by Sebastião Esteves
# GitHub: sebas
# Version: 1.0
# Status: In Development
# ==========================================

import socket
import subprocess

lserv = dict()
portasta = dict()
portas_abertas = list()
total_portas = 65535
portas_analisadas = 0
tamanho_barra = 20

def identificar_processos():
    resultado = subprocess.run(
        ["ss", "-tlnp"],
        capture_output=True,
        text=True
    )
    for linha in resultado.stdout.splitlines()[1:]:
        partes = linha.split()

        if len(partes) >= 4:
            endereco = partes[3]
            porta = endereco.rsplit(":", 1)[-1]
            if 'users:(("' in linha and "pid=" in linha:
                processo = linha.split('(("')[1].split('"')[0]
                pid = linha.split("pid=")[1].split(",")[0]

                lserv[int(porta)] = {"processo": processo, "pid": int(pid)}
    return lserv

processos = identificar_processos()

print('=' * 45)
print('           CYBERTOOLS')
print('          TCP PORT SCANNER')
print('=' * 45)
print('Developed by: Sebastião Esteves')
print('GitHub: sebas')
print('Version: 1.0')
print('Status: In Development')
print('=' * 45)

ip = input('Enter the IP address to scan: ')

for porta in range(1, total_portas + 1):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(0.5)

    resultado = cliente.connect_ex((ip, porta))

    if resultado == 0:
        portas_abertas.append(porta)
        informacoes = processos.get(porta)

        try:
            servico = socket.getservbyport(porta, "tcp")
        except OSError:
            servico = "Unknown"

        portasta[porta] = servico
        print(f"[OPEN] Port {porta} | Service: {servico}")

        if informacoes:
            print(f"Process: {informacoes['processo']}")
            print(f"PID: {informacoes['pid']}")
        else:
            print("Process: Not identified")

    cliente.close()
    portas_analisadas += 1
    percentagem = portas_analisadas / total_portas * 100
    preenchidos = int(portas_analisadas / total_portas * tamanho_barra)
    vazios = tamanho_barra - preenchidos

    barra = "█" * preenchidos + "-" * vazios

    print(f"\rProgress: [{barra}] {percentagem:.2f}%", end="", flush=True)

print("\nScan completed.")
print('=' * 30)
print('SCAN RESULTS')

if portasta:
    for porta, dados in sorted(portasta.items()):
        print(f'Port {porta}: Service {dados}')
else:
    print('No open ports found.')

print(f'Total: {len(portas_abertas)} open ports.')
print(f'Ports scanned: {portas_analisadas}')
