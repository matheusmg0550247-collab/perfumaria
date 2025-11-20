import streamlit as st
import base64

# Configuração da Página
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="✨",
    layout="centered"
)

# --- DADOS DOS PRODUTOS ---
# Substitua os nomes dos arquivos pelas suas imagens reais na pasta 'images'
produtos = [
    {"nome": "Elysium Gold", "imagem": "images/perfume1.png", "preco": 250.00},
    {"nome": "Royal Oud", "imagem": "images/perfume2.png", "preco": 420.00},
    {"nome": "Velvet Amber", "imagem": "images/perfume3.png", "preco": 310.00},
    # Adicione mais perfumes aqui
]

# --- GERENCIAMENTO DE ESTADO (Sessão) ---
if 'index_produto' not in st.session_state:
    st.session_state.index_produto = 0

def proximo_produto():
    if st.session_state.index_produto < len(produtos) - 1:
        st.session_state.index_produto += 1
    else:
        st.session_state.index_produto = 0 # Volta pro inicio

def produto_anterior():
    if st.session_state.index_produto > 0:
        st.session_state.index_produto -= 1
    else:
        st.session_state.index_produto = len(produtos) - 1 # Vai pro final

# --- FUNÇÕES AUXILIARES ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Carregar imagens em base64 para usar no CSS
bg_visor = get_base64_image("images/Visor.jpg")
img_atual_path = produtos[st.session_state.index_produto]["imagem"]
img_perfume = get_base64_image(img_atual_path)

# Dados do produto atual
produto_atual = produtos[st.session_state.index_produto]
preco_promo = produto_atual["preco"]
preco_original = preco_promo + 100.00

# --- CSS PERSONALIZADO (ESTILO LUXO) ---
st.markdown(f"""
<style>
    /* Importar fonte elegante */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:wght@400;700&display=swap');

    /* Fundo geral escuro para destacar o visor */
    .stApp {{
        background-color: #1a1a1a;
        color: #d4af37; /* Dourado */
    }}

    /* Header / Logo */
    .header-logo {{
        font-family: 'Cinzel', serif;
        text-align: center;
        font-size: 3.5em;
        color: #d4af37;
        text-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5);
        margin-bottom: 10px;
        letter-spacing: 4px;
        border-bottom: 1px solid #d4af37;
        padding-bottom: 15px;
    }}

    /* Container do Visor */
    .visor-container {{
        position: relative;
        width: 100%;
        max-width: 500px;
        aspect-ratio: 1/1.1; /* Ajuste conforme a proporção da sua imagem Visor.jpg */
        margin: 0 auto;
        background-image: url("data:image/jpg;base64,{bg_visor}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* Imagem do Perfume dentro do Visor */
    .perfume-img {{
        width: 45%; /* Tamanho do perfume em relação ao visor */
        height: auto;
        margin-top: -20px; /* Ajuste fino para centralizar na parte iluminada */
        filter: drop-shadow(0 10px 10px rgba(0,0,0,0.5));
        transition: all 0.5s ease;
    }}
    
    /* Preços */
    .price-container {{
        text-align: center;
        margin-top: 20px;
        font-family: 'Playfair Display', serif;
    }}
    
    .promo-price {{
        font-size: 2.5em;
        color: #fff;
        font-weight: bold;
        text-shadow: 0 0 10px #d4af37;
    }}
    
    .old-price {{
        font-size: 1.2em;
        color: #888;
        text-decoration: line-through;
        margin-top: -10px;
    }}

    /* Botões Customizados */
    .stButton button {{
        background-color: transparent;
        border: 1px solid #d4af37;
        color: #d4af37;
        font-family: 'Cinzel', serif;
        transition: 0.3s;
        width: 100%;
    }}
    .stButton button:hover {{
        background-color: #d4af37;
        color: #000;
        border-color: #fff;
    }}

    /* Footer Contato */
    .footer-contact {{
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #333;
        text-align: center;
        font-family: 'Playfair Display', serif;
        background-color: #111;
        border-radius: 10px;
    }}
    .contact-name {{
        font-size: 1.5em;
        color: #d4af37;
    }}
    .contact-phone {{
        font-size: 1.8em;
        color: #fff;
        font-weight: bold;
        text-decoration: none;
    }}
    .contact-cta {{
        color: #aaa;
        font-size: 0.9em;
    }}
</style>
""", unsafe_allow_html=True)

# --- LAYOUT DA PÁGINA ---

# 1. Logo
st.markdown('<div class="header-logo">AURUM SCENTS</div>', unsafe_allow_html=True)

# 2. Visor e Perfume
# Se não tiver imagem do visor carregada, avisa o usuário
if not bg_visor:
    st.error("⚠️ Imagem 'Visor.jpg' não encontrada na pasta 'images'.")
else:
    # Se não tiver imagem do perfume, usa um placeholder transparente
    img_src = f"data:image/png;base64,{img_perfume}" if img_perfume else "https://via.placeholder.com/300x400/000000/FFFFFF?text=Sem+Imagem"
    
    st.markdown(f"""
    <div class="visor-container">
        <img src="{img_src}" class="perfume-img">
    </div>
    """, unsafe_allow_html=True)

# 3. Botões de Navegação
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("❮ ANTERIOR", on_click=produto_anterior)
with col3:
    st.button("PRÓXIMO ❯", on_click=proximo_produto)

# 4. Preços
st.markdown(f"""
<div class="price-container">
    <div class="promo-price">R$ {preco_promo:.2f}</div>
    <div class="old-price">De R$ {preco_original:.2f}</div>
    <div style="color: #d4af37; margin-top:10px; font-style:italic;">{produto_atual['nome']}</div>
</div>
""", unsafe_allow_html=True)

# 5. Contato Footer
whatsapp_link = "https://wa.me/5531992051499?text=Olá,%20vim%20pelo%20site%20da%20Aurum%20Scents!"

st.markdown(f"""
<div class="footer-contact">
    <div class="contact-cta">Fale com nosso especialista</div>
    <div class="contact-name">Jerry Bombeta</div>
    <a href="{whatsapp_link}" target="_blank" class="contact-phone">
        📞 (31) 99205-1499
    </a>
</div>
""", unsafe_allow_html=True)
