from datetime import datetime

# 2. Testes básicos (usando print e type)
mensagem_boas_vindas = "Iniciando o script..."
print(mensagem_boas_vindas)
print("Tipo da variável:", type(mensagem_boas_vindas))

# 3. Primeiro programa (pergunta o nome e diz "Oi!")
nome = input("Qual é o seu nome? ")

# Desafio Extra: Pegar a hora atual com a biblioteca datetime
hora_atual = datetime.now().strftime("%H:%M")

# Exibir a saudação personalizada com a hora
print(f"Oi, {nome}! Agora são {hora_atual}.")