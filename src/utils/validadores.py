# src/utils/validadores.py

def ler_numero_inteiro(mensagem):
    """Lê um número inteiro do usuário, garantindo que seja válido."""
    while True:
        valor = input(mensagem)
        if valor.isdigit():
            return int(valor)
        print("❌ Valor inválido! Digite apenas números inteiros.")

def ler_numero_decimal(mensagem):
    """Lê um número decimal (float) do usuário, garantindo que seja válido."""
    while True:
        valor = input(mensagem)
        try:
            return float(valor)
        except ValueError:
            print("❌ Valor inválido! Digite apenas números (use ponto para decimais).")

def ler_telefone(mensagem):
    """Lê o telefone, aceitando apenas números e validando o tamanho."""
    while True:
        telefone = input(mensagem).strip()
        if telefone.isdigit() and 8 <= len(telefone) <= 11:
            return telefone
        else:
            print("❌ Telefone inválido! Digite apenas números (com DDD). Ex: 27988887777")


def formatar_telefone(numero):
    """Formata o telefone no padrão brasileiro (DDD e hífen)."""
    # Remove espaços e possíveis símbolos extras
    numero = numero.strip().replace(" ", "")

    if len(numero) == 8:
        # Telefone sem DDD (fixo antigo)
        return f"{numero[:4]}-{numero[4:]}"
    elif len(numero) == 9:
        # Telefone sem DDD (celular antigo)
        return f"{numero[:5]}-{numero[5:]}"
    elif len(numero) == 10:
        # Telefone com DDD (fixo)
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    elif len(numero) == 11:
        # Telefone com DDD (celular)
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    else:
        # Caso não se encaixe em nenhum formato conhecido
        return numero
