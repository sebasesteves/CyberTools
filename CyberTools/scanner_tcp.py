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

print('='*30)
print('SCANNER DE PORTAS TCP')
print('='*30)

ip = input('Qual ip deseja scanear?')
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
            servico = "Desconhecido"

        portasta[porta] = servico
        print(f"[ABERTA] Porta {porta} | Serviço: {servico}")
        if informacoes:
            print(f"Processo: {informacoes['processo']}")
            print(f"PID: {informacoes['pid']}")
        else:
            print("Processo: Não identificado")
    cliente.close()
    portas_analisadas += 1
    percentagem = portas_analisadas / total_portas * 100
    preenchidos = int(portas_analisadas / total_portas * tamanho_barra)
    vazios = tamanho_barra - preenchidos

    barra = "█" * preenchidos + "-" * vazios

    print(f"\rProgresso: [{barra}] {percentagem:.2f}%", end="", flush=True)
print("\nScan concluído.")
print('=' * 30)
print('RESULTADO DO SCAN')
if portasta:
    for porta, dados in sorted(portasta.items()):
        print(f'Porta {porta}: Servico {dados}')
else:
    print('Nenhuma porta aberta encontrada.')
print(f'Total: {len(portas_abertas)} portas abertas.')
print(f'Portas analisadas: {portas_analisadas}')