import os

# Configuracoes de ambiente
def get_backend_url():
    """Retorna a URL do backend baseada no ambiente"""
    # Se estiver no Streamlit Cloud, usa Railway
    if os.getenv('STREAMLIT_SHARING'):
        return "https://your-backend-url.up.railway.app"
    else:
        # Desenvolvimento local
        return "http://localhost:8000"

BACKEND_URL = get_backend_url()
