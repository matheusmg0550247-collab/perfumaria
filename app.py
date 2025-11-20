import streamlit as st
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA (LAYOUT ORIGINAL) ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. FUNÇÃO "DETETIVE" DE IMAGENS (Resolve o problema do JPG/PNG) ---
def encontrar_arquivo_imagem(nome_base):
    """
    Procura o arquivo na pasta 'imagens' testando várias extensões (.png, .jpg)
    e variações de nome (com espaço, sem espaço, minúsculo).
    """
    pasta = "imagens"
    
    # Lista de tentativas que o código vai fazer
    tentativas = [
        f"{nome_base}.png",
        f"{nome_base}.jpg",
        f"{nome_base}.jpeg",
        f"{nome_base.lower()}.png",       # perfume1.png
        f"{nome_base.lower()}.jpg",       # perfume1.jpg
        f"{nome_base.replace('Perfume', 'Perfume ')}.jpg", # Perfume 1.jpg (com espaço)
        f"{nome_base.replace('Perfume', 'Perfume ')}.png", # Perfume 1.png (com espaço)
    ]

    for arquivo in tentativas:
        caminho_completo = os.path.join(pasta, arquivo)
        if os.path.exists(caminho_completo):
            return caminho_completo
            
    return None # Não achou nada

def get_img_as_base64(caminho_arquivo):
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        return None
    try:
        with open(caminho_arquivo, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode('utf-8')
    except:
        return None

# --- 3. DADOS DOS PRODUTOS ---
# Nota: Use apenas o nome base (ex: "Perfume1"). O código se vira pra achar a extensão.
produtos = [
    {"nome": "Royal Elixir Gold", "arquivo_base": "Perfume1", "preco": 299.90, "desc": "Notas de ouro e especiarias raras."},
    {"nome": "Black Orchid Intense", "arquivo_base": "Perfume2", "preco": 350.00, "desc": "Orquídea negra profunda e misteriosa."},
    {"nome": "Velvet Santal Wood", "arquivo_base": "Perfume3", "preco": 420.00, "desc": "Sândalo aveludado e envolvente."},
    {"nome": "Imperial Amber", "arquivo_base": "Perfume4", "preco": 380.00, "desc": "Âmbar imperial com toque cítrico."},
]

# --- 4. NAVEGAÇÃO ---
if 'idx' not in st.session_state: st.session_state.idx = 0

def proximo(): st.session_state.idx = (st.session_state.idx + 1) % len(produtos)
def anterior(): st.session_state.idx = (st.session_state.idx - 1 + len(produtos)) % len(produtos)

# --- 5. CARREGAMENTO ---
# Tenta achar o visor (pode ser jpg ou png)
path_visor = encontrar_arquivo_imagem("Visor") 
visor_b64 = get_img_as_base64(path_visor)

# Tenta achar o produto atual
produto_atual = produtos[st.session_state.idx]
path_produto = encontrar_arquivo_imagem(produto_atual["arquivo_base"])
img_produto_b64 = get_img_as_base64(path_produto)

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- 6. CSS DE LUXO (LAYOUT ORIGINAL RESTAURADO) ---
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "#111"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    .stApp {{ background-color: #000000; color: #d4af37; }}
    .block-container {{ padding-top: 1rem; max-width: 1400px !important; }}

    /* HEADER */
    .brand-header {{ text-align: center; margin-bottom: 40px; }}
    .brand-title {{
        font-family: 'Cinzel', serif; font-size: 4rem;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0; letter-spacing: 5px;
    }}

    /* ESQUERDA (TEXTO) */
    .left-panel {{ 
        padding-right: 30px; border-right: 1px solid #222; height: 100%; 
        display: flex; flex-direction: column; justify-content: center;
    }}
    .panel-title {{ 
        font-family: 'Cinzel', serif; font-size: 1.5rem; color: #d4af37; 
        margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;
    }}
    .panel-text {{ 
        font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #aaa; 
        line-height: 1.8; text-align: justify; margin-bottom: 20px;
    }}

    /* CENTRO (VISOR) */
    .visor-wrapper {{
        position: relative; width: 100%; max-width: 850px;
        aspect-ratio: 16/9; margin: 0 auto;
        background-image: {bg_visor_css}; background-size: cover; background-position: center;
        border-radius: 4px; box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        margin-bottom: 20px;
    }}
    .perfume-overlay {{
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -45%);
        height: 60%; width: auto; filter: drop-shadow(0 15px 20px rgba(0,0,0,0.8));
        transition: all 0.5s ease-in-out;
    }}
    .perfume-overlay:hover {{ transform: translate(-50%, -48%) scale(1.03); }}

    /* BOTÕES */
    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; padding: 0.8rem; width: 100%;
        transition: 0.3s; text-transform: uppercase; letter-spacing: 2px;
    }}
    div.stButton > button:hover {{
        background: rgba(212, 175, 55, 0.15); color: #fff; border-color: #fff;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.3);
    }}

    /* INFO PRODUTO */
    .info-container {{ text-align: center; margin-top: 20px; }}
    .prod-name {{ font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; margin-bottom: 5px; }}
    .prod-desc {{ font-family: 'Playfair Display', serif; color: #888; font-style: italic; margin-bottom: 10px; }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.3rem; margin-right: 15px; }}
    .new {{ color: #d4af37; font-size: 3.5rem; font-weight: 700; }}

    /* DIREITA (CONTATO) */
    .right-panel {{
        padding: 30px; background: linear-gradient(145deg, #111, #0a0a0a);
        border: 1px solid #222; border-radius: 10px; text-align: center;
        margin-top: 80px; /* Ajuste para alinhar com o visor */
    }}
    .contact-name {{ font-family: 'Cinzel', serif; font-size: 2rem; color: #d4af37; margin-bottom: 20px; }}
    .wa-button {{
        display: inline-block; width: 100%; padding: 15px 0;
        background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        border-radius: 50px; text-decoration: none; font-weight: bold;
        font-family: sans-serif; letter-spacing: 1px;
        box-shadow: 0 5px 15px rgba(37, 211, 102, 0.3); transition: 0.3s;
    }}
    .wa-button:hover {{ transform: translateY(-3px); box-shadow: 0 10px 25px rgba(37, 211, 102, 0.5); color: white !important; }}
</style>
""", unsafe_allow_html=True)

# --- 7. ESTRUTURA (GRID) ---

st.markdown('<div class="brand-header"><h1 class="brand-title">AURUM SCENTS</h1></div>', unsafe_allow_html=True)

col_L, col_C, col_R = st.columns([3, 6, 3], gap="large")

# ESQUERDA
with col_L:
    st.markdown("""
    <div class="left-panel">
        <div class="panel-title">A Essência do Luxo</div>
        <p class="panel-text">
            Na <span style="color:#d4af37">Aurum Scents</span>, a fragrância não é apenas um aroma, é uma assinatura invisível.
        </p>
        <p class="panel-text">
            Nossa curadoria busca os ingredientes mais raros para despertar os prazeres da fragrância em sua forma mais pura. Cada frasco é uma promessa de distinção.
        </p>
    </div>
    """, unsafe_allow_html=True)

# CENTRO
with col_C:
    # Tenta carregar a imagem (GIF transparente se falhar)
    src = f"data:image/png;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    # Aviso de debug se a imagem falhar (discreto)
    if not img_produto_b64:
        st.caption(f"⚠️ Não encontrei: {produto_atual['arquivo_base']} (jpg/png)")

    st.markdown(f"""
    <div class="visor-wrapper">
        <img src="{src}" class="perfume-overlay">
    </div>
    """, unsafe_allow_html=True)

    # Botões
    c_btn1, c_btn2, c_btn3 = st.columns([1, 0.2, 1]) 
    with c_btn1: st.button("❮ ANTERIOR", on_click=anterior, use_container_width=True)
    with c_btn3: st.button("PRÓXIMO ❯", on_click=proximo, use_container_width=True)

    # Info
    st.markdown(f"""
        <div class="info-container">
            <div class="prod-name">{produto_atual['nome']}</div>
            <div class="prod-desc">{produto_atual['desc']}</div>
            <div>
                <span class="old">De R$ {preco_antigo:.2f}</span>
                <span class="new">R$ {preco_atual:.2f}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# DIREITA
with col_R:
    msg = f"Olá Jerry! Estou interessado no perfume {produto_atual['nome']}."
    link_wa = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"
    
    st.markdown(f"""
    <div class="right-panel">
        <div style="color:#fff; font-family:'Cinzel'; margin-bottom:10px;">ATENDIMENTO EXCLUSIVO</div>
        <div class="contact-name">Jerry Bombeta</div>
        <div style="color: #888; margin-bottom: 20px; font-size:0.9rem;">Specialist Fragrance Consultant</div>
        <a href="{link_wa}" target="_blank" class="wa-button">
            FALAR NO WHATSAPP
        </a>
        <div style="margin-top: 20px; color: #d4af37;">📞 (31) 99205-1499</div>
    </div>
    """, unsafe_allow_html=True)
