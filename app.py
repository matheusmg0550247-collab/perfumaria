import streamlit as st
import base64
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents - Perfumaria de Luxo",
    page_icon="⚜️",
    layout="centered"
)

# --- CONFIGURAÇÃO DOS PRODUTOS ---
# Aqui você define seus produtos. 
# Certifique-se que as imagens estão dentro da pasta 'images/' 
# e que os nomes dos arquivos (ex: perfume1.png) batem exatamente.
produtos = [
    {
        "nome": "Royal Elixir Gold",
        "imagem": "images/perfume1.png", # Substitua pelo nome real do arquivo na pasta images
        "preco": 299.90
    },
    {
        "nome": "Black Orchid Intense",
        "imagem": "images/perfume2.png", # Substitua pelo nome real do arquivo na pasta images
        "preco": 350.00
    },
    {
        "nome": "Velvet Santal Wood",
        "imagem": "images/perfume3.png", # Substitua pelo nome real do arquivo na pasta images
        "preco": 420.00
    },
    # Adicione mais produtos copiando o bloco acima
]

# --- FUNÇÕES UTILITÁRIAS ---

def get_img_as_base64(file_path):
    """Converte imagem para base64 para usar no HTML/CSS"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- GERENCIAMENTO DE ESTADO (NAVEGAÇÃO) ---
if 'idx' not in st.session_state:
    st.session_state.idx = 0

def proximo():
    if st.session_state.idx < len(produtos) - 1:
        st.session_state.idx += 1
    else:
        st.session_state.idx = 0

def anterior():
    if st.session_state.idx > 0:
        st.session_state.idx -= 1
    else:
        st.session_state.idx = len(produtos) - 1

# --- CARREGAMENTO DE RECURSOS ---

# 1. Carregar Fundo do Visor (Visor.png na raiz)
visor_path = "Visor.png" 
visor_b64 = get_img_as_base64(visor_path)

# 2. Carregar Imagem do Produto Atual (Pasta images/)
produto_atual = produtos[st.session_state.idx]
img_produto_path = produto_atual["imagem"]
img_produto_b64 = get_img_as_base64(img_produto_path)

# 3. Cálculos de Preço
preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- ESTILIZAÇÃO CSS (LUXO / OLD MONEY) ---
# Define o background do visor. Se a imagem não existir, usa um cinza escuro.
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "none"
bg_color_fallback = "#2c2c2c" if not visor_b64 else "transparent"

st.markdown(f"""
<style>
    /* Importando fontes elegantes */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    /* Fundo Geral do App */
    .stApp {{
        background-color: #0e0e0e;
        color: #e5c15d; /* Dourado suave */
    }}

    /* LOGO DA EMPRESA */
    .logo-container {{
        text-align: center;
        margin-bottom: 20px;
        padding-bottom: 20px;
        border-bottom: 1px solid #333;
    }}
    .brand-name {{
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin: 0;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.5);
    }}
    .brand-subtitle {{
        font-family: 'Playfair Display', serif;
        font-size: 1rem;
        color: #888;
        letter-spacing: 2px;
        margin-top: -5px;
    }}

    /* VISOR CENTRAL */
    .visor-stage {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }}
    
    .visor-frame {{
        position: relative;
        width: 100%;
        max-width: 500px;
        aspect-ratio: 1 / 1.1; /* Ajuste a proporção conforme sua imagem Visor.png */
        background-image: {bg_visor_css};
        background-color: {bg_color_fallback};
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* Imagem do perfume flutuando no visor */
    .perfume-display {{
        width: 50%; /* O perfume ocupa 50% da largura do visor */
        height: auto;
        z-index: 10;
        filter: drop-shadow(0px 15px 10px rgba(0,0,0,0.6));
        transition: transform 0.5s ease;
        margin-top: -5%; /* Ajuste fino vertical */
    }}
    
    .perfume-display:hover {{
        transform: scale(1.05);
    }}

    /* ÁREA DE PREÇO */
    .price-tag {{
        text-align: center;
        font-family: 'Playfair Display', serif;
        margin-top: 15px;
    }}
    .price-old {{
        color: #666;
        text-decoration: line-through;
        font-size: 1.2rem;
    }}
    .price-new {{
        color: #e5c15d;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0px 0px 15px rgba(229, 193, 93, 0.3);
    }}
    .product-title {{
        font-family: 'Cinzel', serif;
        font-size: 1.5rem;
        color: #fff;
        margin-bottom: 5px;
    }}

    /* BOTÕES PERSONALIZADOS */
    div.stButton > button {{
        background-color: transparent;
        border: 1px solid #e5c15d;
        color: #e5c15d;
        font-family: 'Cinzel', serif;
        width: 100%;
        border-radius: 0px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        background-color: #e5c15d;
        color: #000;
        border-color: #fff;
        box-shadow: 0 0 10px #e5c15d;
    }}

    /* FOOTER DE CONTATO (JERRY) */
    .footer-box {{
        margin-top: 50px;
        padding: 30px;
        background: linear-gradient(180deg, rgba(20,20,20,0) 0%, rgba(30,30,30,1) 100%);
        border-top: 1px solid #333;
        text-align: center;
        border-radius: 10px;
    }}
    .contact-label {{
        color: #888;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}
    .contact-name {{
        font-family: 'Cinzel', serif;
        font-size: 2rem;
        color: #fff;
        margin: 10px 0;
    }}
    .whatsapp-btn {{
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 12px 30px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        font-family: sans-serif;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
        transition: 0.3s;
    }}
    .whatsapp-btn:hover {{
        background-color: #1ebd59;
        transform: translateY(-2px);
        color: white !important;
        text-decoration: none;
    }}
</style>
""", unsafe_allow_html=True)

# --- RENDERIZAÇÃO VISUAL (FRONT-END) ---

# 1. Header e Logo
st.markdown("""
    <div class="logo-container">
        <div class="brand-name">AURUM SCENTS</div>
        <div class="brand-subtitle">ESSÊNCIA E SOFISTICAÇÃO</div>
    </div>
""", unsafe_allow_html=True)

# 2. Visor e Produto
if not visor_b64:
    st.error("⚠️ Erro: Arquivo 'Visor.png' não encontrado na raiz do projeto.")
else:
    # Define a imagem do perfume (ou placeholder se falhar)
    src_img = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "https://via.placeholder.com/300x500/000000/FFFFFF?text=Sem+Imagem"
    
    st.markdown(f"""
        <div class="visor-stage">
            <div class="visor-frame">
                <img src="{src_img}" class="perfume-display">
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3. Navegação (Botões Laterais)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("❮ ANTERIOR", on_click=anterior)
with col3:
    st.button("PRÓXIMO ❯", on_click=proximo)

# 4. Informações do Produto
st.markdown(f"""
    <div class="price-tag">
        <div class="product-title">{produto_atual['nome']}</div>
        <div class="price-old">De R$ {preco_antigo:.2f}</div>
        <div class="price-new">R$ {preco_atual:.2f}</div>
    </div>
""", unsafe_allow_html=True)

# 5. Footer (Contato Jerry)
# Formata o link do WhatsApp
telefone = "5531992051499"
msg = f"Olá Jerry! Gostaria de comprar o perfume {produto_atual['nome']}."
link_wa = f"https://wa.me/{telefone}?text={msg.replace(' ', '%20')}"

st.markdown(f"""
    <div class="footer-box">
        <div class="contact-label">Atendimento Exclusivo</div>
        <div class="contact-name">Jerry Bombeta</div>
        <div>📞 (31) 99205-1499</div>
        <br>
        <a href="{link_wa}" target="_blank" class="whatsapp-btn">
            COMPRAR AGORA PELO WHATSAPP
        </a>
    </div>
""", unsafe_allow_html=True)
