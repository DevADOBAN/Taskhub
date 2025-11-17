import http.server
import socketserver
import webbrowser
import os

# --- Configurações ---
PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}/"
# --------------------

# Verifica se o index.html existe
if not os.path.exists("index.html"):
    print("Erro: Arquivo 'index.html' não encontrado.")
    print("Verifique se você está rodando este script da pasta 'taskhub-frontend'.")
    exit()

# Prepara o servidor
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"🚀 Iniciando servidor do Front-End em {URL}")

try:
    # 1. Abre o navegador primeiro
    webbrowser.open_new(URL)
    
    # 2. Inicia o servidor e o mantém rodando
    httpd.serve_forever()

except KeyboardInterrupt:
    print("\nServidor do Front-End desligado.")
    httpd.shutdown()