<<<<<<< HEAD
import os
import time

def limpar_tela():      #Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    limpar_tela()
    print("=" * 50)
    print("🛒 SISTEMA DE LOJA ONLINE 🛍️".center(50))
    print("=" * 50)
    print("\nDesenvolvido por:")
    print("👤 Kaynan de Oliveira Barbosa")
    print("👤 Rafael Covre Vilque")
    print("👤 Ricardo Cardeais")
    print("👤 Renato Oliveira de Jesus")
    print("👤 Yuri Gabriel Amorim dos Santos\n")

    print("Carregando o sistema", end = "", flush=True)
    for i in range(3):  # animação de "..."
        time.sleep(0.7)
        print(".", end="", flush=True)
    
    time.sleep(1.0)
=======
import os
import time

def limpar_tela():      #Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')

def splash_screen():
    limpar_tela()
    print("=" * 50)
    print("🛒 SISTEMA DE LOJA ONLINE 🛍️".center(50))
    print("=" * 50)
    print("\nDesenvolvido por:")
    print("👤 Kaynan de Oliveira Barbosa")
    print("👤 Rafael Covre Vilque")
    print("👤 Ricardo Cardeais")
    print("👤 Renato Oliveira de Jesus")
    print("👤 Yuri Gabriel Amorim dos Santos\n")

    print("Carregando o sistema", end = "", flush=True)
    for i in range(3):  # animação de "..."
        time.sleep(0.7)
        print(".", end="", flush=True)
    
    time.sleep(1.0)
>>>>>>> ab8d791e403492db0f630b247e948eb552250b33
    limpar_tela()