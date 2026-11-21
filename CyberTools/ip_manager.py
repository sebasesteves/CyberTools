import os
import ipaddress
import subprocess

  
if not os.path.exists('ip_list.txt'):
    with open('ip_list.txt', 'w', encoding='utf-8') as arquivo:
        pass

def adicionar_ip():
    ip = input('Digite o IP a ser adicionado: ')
    nome = input('Digite o nome do IP: ')
    if not nome.strip():
        print('O nome não pode estar vazio.')
        return
    try:
                ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
                print(f'IP {ip} inválido.')
                return
    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
                ips = arquivo.read().splitlines()
    if any(linha.split(' - ')[0] == ip for linha in ips):
        print(f'IP {ip} já está cadastrado.')
    else:
        with open('ip_list.txt', 'a', encoding='utf-8') as arquivo:
            arquivo.write(ip + ' - ' + nome + '\n')
        print(f'IP {ip} adicionado com sucesso.')

def remover_ip():
    while True:
        ip = input('Digite o IP a ser removido: ')
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
            print(f'IP {ip} removido com sucesso.')
            break
        else:
            print('Erro! Ip errado ou inexistente')
            print('Digite outra vez ou encerre digitando 0')

def listar_ips():
    print('IPs cadastrados:')

    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            if ' - ' not in linha:
                continue

            ip, nome = linha.strip().split(' - ', 1)
            print(f'Nome: {nome} | IP: {ip}')

def pesquisar_ip():
    nome_pesquisa = input('Nome do equipamento: ').strip().lower()
    encontrado = False

    with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            ip, nome = linha.strip().split(' - ', 1)

            if nome.strip().lower() == nome_pesquisa:
                print(f'Nome: {nome} | IP: {ip}')
                encontrado = True

    if not encontrado:
        print(f'Equipamento com nome "{nome_pesquisa}" não encontrado.')

def verificar_ip():
    ip = input('Digite o IP a verificar: ')
    
    try:
        ipaddress.IPv4Address(ip)
    except ipaddress.AddressValueError:
        print('IP inválido!')
        return
    
    resultado = subprocess.run(
                ['ping', '-c', '1', '-W', '2', ip],
                capture_output=True,
                text=True
            )
    
    if resultado.returncode == 0:
        print('IP ONLINE')
    else:
        print('IP SEM RESPOSTA')
    e = input('Deseja adicionar o Ip? [S/n]').strip().upper()
    if not e:
        return
    if e == 'S':
        while True:
            nome = input('Digite o nome do IP: ')
            if not nome.strip():
                print('O nome não pode estar vazio.')
            else:
                with open('ip_list.txt', 'r', encoding='utf-8') as arquivo:
                    ips = arquivo.read().splitlines()
                if any(linha.split(' - ')[0] == ip for linha in ips):
                    print(f'IP {ip} já está cadastrado.')
                    break
                else:
                    with open('ip_list.txt', 'a', encoding='utf-8') as arquivo:
                        arquivo.write(ip + ' - ' + nome + '\n')
                    print(f'IP {ip} adicionado com sucesso.')
                    break

def descobrir_equipamentos():
    print('\n=== EQUIPAMENTOS DA REDE ===')

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

        print(f'Rede: {rede}')
        print(f'Interface: {interface}\n')

        if rede.num_addresses > 256:
            print('Rede demasiado grande para esta verificação.')
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
                nome = ips_guardados.get(ip, 'Desconhecido')
                print(f'{ip} | {nome} | RESPONDE')

        print(f'\nTotal encontrado: {encontrados}')

    except (OSError, subprocess.CalledProcessError, IndexError, ValueError):
        print('Não foi possível identificar ou verificar a rede.')
         
print('0. Sair')
print('1. Adicionar IP')
print('2. Remover IP')
print('3. Listar IPs')
print('4. Pesquisar IP pelo nome')
print('5. Verificar se um IP está online')
print('6. Descobrir Equipamentos')

while True:
    op = input('Escolha uma opção: ')
    if op == '0':
        print('Saindo...')
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
        print('Opção inválida. Tente novamente.')
