# ==========================================
# CYBERTOOLS - IP MANAGER
# Developed by Sebastião Esteves
# GitHub: sebas
# Version: 1.0
# Status: In Development
# ==========================================

import os
import ipaddress
import subprocess

if not os.path.exists('ip_list.txt'):
    with open('ip_list.txt', 'w', encoding='utf-8') as arquivo:
        pass


def adicionar_ip():
    ip = input('Enter the IP address to add: ')
    nome = input('Enter the device name: ')
    if not nome.strip():
        print('The device name cannot be empty.')
        return
    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
        print(f'Invalid IP address: {ip}')
        return
    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
        ips = arquivo.read().splitlines()
    if any(linha.split(' - ')[0] == ip for linha in ips):
        print(f'IP {ip} is already registered.')
    else:
        with open('ip_list.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(ip + ' - ' + nome + '\n')
        print(f'IP {ip} added successfully.')


def remover_ip():
    while True:
        ip = input('Enter the IP address to remove: ')
        if ip == '0':
            break
        removido = False
        with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        with open('ip_list.txt', 'w', encoding='utf-8') as arquivo:
            for linha in linhas:
                if linha.strip().split(' - ')[0] != ip:
                    arquivo.write(linha)
                else:
                    removido = True
        if removido == True:
            print(f'IP {ip} removed successfully.')
            break
        else:
            print('Error! Invalid or non-existent IP.')
            print('Try again or enter 0 to cancel.')


def listar_ips():
    print('Registered IP addresses:')

    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            if ' - ' not in linha:
                continue

            ip, nome = linha.strip().split(' - ', 1)
            print(f'Device: {nome} | IP: {ip}')


def pesquisar_ip():
    nome_pesquisa = input('Enter the device name: ').strip().lower()
    encontrado = False

    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            ip, nome = linha.strip().split(' - ', 1)

            if nome.strip().lower() == nome_pesquisa:
                print(f'Device: {nome} | IP: {ip}')
                encontrado = True

    if not encontrado:
        print(f'Device "{nome_pesquisa}" not found.')


def verificar_ip():
    ip = input('Enter the IP address to check: ')

    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
        print('Invalid IP address!')
        return

    resultado = subprocess.run(
        ['ping', '-c', '1', '-W', '2', ip],
        capture_output=True,
        text=True
    )

    if resultado.returncode == 0:
        print('IP ONLINE')
    else:
        print('IP NO RESPONSE')

    e = input('Would you like to add this IP? [Y/n] ').strip().upper()
    if not e:
        return
    if e == 'Y':
        while True:
            nome = input('Enter the device name: ')
            if not nome.strip():
                print('The device name cannot be empty.')
            else:
                with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
                    ips = arquivo.read().splitlines()
                if any(linha.split(' - ')[0] == ip for linha in ips):
                    print(f'IP {ip} is already registered.')
                    break
                else:
                    with open('ip_list.txt', 'a', encoding='utf-8') as arquivo:
                        arquivo.write(ip + ' - ' + nome + '\n')
                    print(f'IP {ip} added successfully.')
                    break


def descobrir_equipamentos():
    print('\n=== NETWORK DEVICES ===')

    try:
        resultado = subprocess.run(
            ['ip', '-4', 'route', 'show', 'default'],
            capture_output=True,
            text=True,
            check=True
        )

        interface = resultado.stdout.split(' dev ')[1].split()[0]

        resultado = subprocess.run(
            ['ip', '-4', '-o', 'addr', 'show', 'dev', interface],
            capture_output=True,
            text=True,
            check=True
        )

        endereco = resultado.stdout.split(' inet ')[1].split()[0]
        rede = ipaddress.IPv4Interface(endereco).network

        print(f'Network: {rede}')
        print(f'Interface: {interface}\n')

        if rede.num_addresses > 256:
            print('Network too large for this scan.')
            return

        with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
            ips_guardados = {}
            for linha in arquivo:
                if ' - ' in linha:
                    ip, nome = linha.strip().split(' - ', 1)
                    ips_guardados[ip] = nome

        encontrados = 0

        for ip in rede.hosts():
            ip = str(ip)

            resultado = subprocess.run(
                ['ping', '-c', '1', '-W', '1', ip],
                capture_output=True,
                text=True
            )

            if resultado.returncode == 0:
                encontrados += 1
                nome = ips_guardados.get(ip, 'Unknown')
                print(f'{ip} | {nome} | RESPONDING')

        print(f'\nTotal devices found: {encontrados}')

    except (OSError, subprocess.CalledProcessError, IndexError, ValueError):
        print('Unable to identify or scan the network.')


print('=' * 45)
print('               CYBERTOOLS')
print('               IP MANAGER')
print('=' * 45)
print('Developed by: Sebastião Esteves')
print('GitHub: sebas')
print('Version: 1.0')
print('Status: In Development')
print('=' * 45)

print('0. Exit')
print('1. Add IP address')
print('2. Remove IP address')
print('3. List IP addresses')
print('4. Search IP by device name')
print('5. Check IP connectivity')
print('6. Discover network devices')

while True:
    op = input('Choose an option: ')
    if op == '0':
        print('Exiting...')
        break
    elif op == '1':
        adicionar_ip()
    elif op == '2':
        remover_ip()
    elif op == '3':
        listar_ips()
    elif op == '4':
        pesquisar_ip()
    elif op == '5':
        verificar_ip()
    elif op == '6':
        descobrir_equipamentos()
    else:
        print('Invalid option. Please try again.')
