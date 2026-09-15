import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ==========================================
# CONFIGURAÇÕES
# ==========================================

NOME_GRUPO = "Programação 2/26 B/Tarde"
NOME_CONTATO_MENTION = "CarlosPereira"  # Nome exato da pessoa no WhatsApp (sem o @)


# ==========================================
# ABRIR O NAVEGADOR
# ==========================================

options = webdriver.ChromeOptions()

# Salva a sessão para evitar precisar conectar toda hora
options.add_argument(r"--user-data-dir=C:\WhatsAppAutomacao")

driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Abre o WhatsApp Web
driver.get("https://web.whatsapp.com/")

print("WhatsApp Web aberto...")
print("Aguardando o login/conexão do WhatsApp...")


# ==========================================
# AGUARDAR WHATSAPP CARREGAR
# ==========================================

wait = WebDriverWait(driver, 120)

try:
    # Aguarda aparecer a área principal do WhatsApp
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="application"]'))
    )

    print("WhatsApp conectado!")

except Exception as e:
    print("Não foi possível conectar automaticamente.")
    print("Faça a autenticação normalmente e execute novamente.")
    input("Pressione ENTER para continuar...")


# Pequena espera para estabilização
time.sleep(3)


# ==========================================
# PROCURAR O GRUPO
# ==========================================

try:
    print(f"Procurando o grupo: {NOME_GRUPO}")

    # Procura o grupo pelo título no DOM
    grupo = wait.until(
        EC.element_to_be_clickable((By.XPATH, f'//span[@title="{NOME_GRUPO}"]'))
    )

    # Clica no grupo
    grupo.click()

    print("Grupo encontrado e aberto!")

    time.sleep(2)

    # ==========================================
    # ENCONTRAR A CAIXA DE MENSAGEM
    # ==========================================

    # Localiza diretamente a caixa principal de texto da conversa aberta
    caixa_mensagem = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//footer//div[@contenteditable="true"][@role="textbox"]')
        )
    )

    caixa_mensagem.click()

    # ==========================================
    # FAZER A MENÇÃO E ENVIAR
    # ==========================================

    # Digita o @ e o nome para abrir a lista de contatos do grupo
    caixa_mensagem.send_keys(f"@{NOME_CONTATO_MENTION}")

    # Pausa para o WhatsApp carregar a lista flutuante de menções
    time.sleep(1.5)

    # Pressiona TAB ou ENTER para selecionar o primeiro contato da lista
    caixa_mensagem.send_keys(Keys.TAB)

    # Pausa de confirmação da marcação
    time.sleep(0.5)

    # Se quiser adicionar texto após marcar a pessoa, descomente a linha abaixo:
    # caixa_mensagem.send_keys(" Olá, mensagem de teste!")

    # Envia a mensagem
    caixa_mensagem.send_keys(Keys.ENTER)

    print("Mensagem enviada e contato mencionado com sucesso! 🔥")

except Exception as erro:
    print("\nERRO ao tentar enviar mensagem:")
    print(erro)
    print("\nVerifique se o nome do grupo e do contato estão exatamente corretos.")


# ==========================================
# MANTER O NAVEGADOR ABERTO
# ==========================================

input("\nPressione ENTER para fechar o navegador...")
driver.quit()