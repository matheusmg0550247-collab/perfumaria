import streamlit as st
import base64
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CAMINHOS ---
# Garante que o Python ache a pasta onde quer que ela esteja
PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(PASTA_ATUAL, "imagens")

# --- 3. DADOS DOS PRODUTOS (AGORA PROCURANDO .JPG) ---
produtos = [
    {
        "nome": "Royal Elixir Gold", 
        "arquivo": "Perfume1.jpg",  # <--- MUDADO PARA .jpg
        "preco": 299.90, 
        "desc": "Notas de ouro e especiarias raras."
    },
    {
        "nome": "Black Orchid Intense", 
        "arquivo": "Perfume2.jpg", 
        "preco": 350.00, 
        "desc": "Orquídea negra profunda e misteriosa."
    },
    {
        "nome": "Velvet Santal Wood", 
        "arquivo": "Perfume3.jpg", 
        "preco": 420.00, 
        "desc": "Sândalo aveludado e envolvente."
    },
    {
        "nome": "Imperial Amber", 
        "arquivo": "Perfume4.jpg", 
        "preco": 380.00, 
        "desc": "Âmbar imperial com toque cítrico."
    },
]

# --- 4. FUNÇÃO SIMPLES DE CARREGAR IMAGEM ---
def carregar_imagem(nome_arquivo):
    caminho = os.path.join(PASTA_IMAGENS, nome_arquivo)
    if not os.path.exists(caminho):
        return None
    with open(caminho, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode('utf-8')

# --- 5. LÓGICA DE NAVEGAÇÃO ---
if 'idx' not in st.session_state: st.session_state.idx = 0

def proximo(): st.session_state.idx = (st.session_state.idx + 1) % len(produtos)
def anterior(): st.session_state.idx = (st.session_state.idx - 1 + len(produtos)) % len(produtos)

# Carrega dados atuais
visor_b64 = carregar_imagem("Visor.jpg")
produto_atual = produtos[st.session_state.idx]
img_produto_b64 = carregar_imagem(produto_atual["arquivo"])

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- 6. CSS DE LUXO & ALINHAMENTO PERFEITO ---
bg_visor = f"url('data:image/jpg;base64,{visor_b64}')" if visor_b64 else "#111"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

    .stApp {{ background-color: #000000; color: #d4af37; }}
    
    /* TÍTULO */
    .brand-title {{
        font-family: 'Cinzel', serif; font-size: 3.5rem; text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px; letter-spacing: 4px; margin-top: -20px;
    }}

    /* --- ALINHAMENTO VERTICAL DAS COLUNAS LATERAIS --- */
    /* Isso força o texto da esquerda e o contato da direita a ficarem no meio da tela */
    [data-testid="column"] {{
        display: flex;
        flex-direction: column;
        justify-content: center; 
    }}

    /* ESQUERDA (Texto) */
    .left-content {{
        padding-right: 30px; 
        border-right: 1px solid #333; 
        text-align: justify;
    }}
    .panel-text {{ font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #aaa; line-height: 1.6; }}

    /* CENTRO (Visor) */
    .visor-wrapper {{
        width: 100%; max-width: 700px; /* Tamanho controlado */
        aspect-ratio: 16/9; 
        margin: 0 auto;
        background-image: {bg_visor}; 
        background-size: cover; 
        background-position: center;
        border-radius: 4px; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        position: relative;
        margin-bottom: 20px;
    }}
    
    /* Perfume dentro do visor */
    .perfume-img {{
        position: absolute; 
        top: 50%; left: 50%; 
        transform: translate(-50%, -45%);
        height: 55%; width: auto; 
        filter: drop-shadow(0 15px 20px rgba(0,0,0,0.9));
        transition: all 0.5s;
    }}

    /* INFO PRODUTO */
    .prod-name {{ font-family: 'Cinzel', serif; font-size: 2.2rem; color: #fff; text-align: center; }}
    .prod-desc {{ font-family: 'Playfair Display', serif; color: #888; text-align: center; font-style: italic; font-size: 1rem; margin-bottom: 10px; }}
    .price-box {{ text-align: center; margin-bottom: 20px; }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.2rem; margin-right: 10px; }}
    .new {{ color: #d4af37; font-size: 2.8rem; font-weight: bold; }}

    /* BOTÕES */
    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; width: 100%; padding: 0.8rem;
        text-transform: uppercase; transition: 0.3s; letter-spacing: 2px;
    }}
    div.stButton > button:hover {{ background: rgba(212, 175, 55, 0.15); color: #fff; border-color: #fff; }}

    /* DIREITA (Contato) */
    .right-content {{
        background: #0a0a0a; padding: 30px; border-radius: 8px; 
        text-align: center; border: 1px solid #222;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .wa-btn {{
        display: block; background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        padding: 12px; border-radius: 50px; text-decoration: none; font-weight: bold; font-family: sans-serif;
        margin-top: 15px; transition: 0.3s; font-size: 0.9rem;
    }}
    .wa-btn:hover {{ transform: scale(1.02); color: white; }}

</style>
""", unsafe_allow_html=True)

# --- 7. RENDERIZAÇÃO DO LAYOUT ---

st.markdown('<div class="brand-title">AURUM SCENTS</div>', unsafe_allow_html=True)

# Definição das colunas com proporção ajustada
col_esq, col_meio, col_dir = st.columns([2.5, 5, 2.5], gap="large")

# --- CONTEÚDO ESQUERDA ---
with col_esq:
    st.markdown("""
    <div class="left-content">
        <h3 style="color:#d4af37; font-family:'Cinzel'; text-align:center; font-size:1.4rem;">A Essência do Luxo</h3>
        <br>
        <p class="panel-text">
            Na Aurum Scents, a fragrância é uma assinatura invisível. Nossa curadoria busca ingredientes raros para despertar sensações únicas.
        </p>
        <p class="panel-text">
            Cada frasco é uma promessa de distinção e elegância atemporal.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- CONTEÚDO CENTRAL ---
with col_meio:
    # Visor e Perfume
    if not visor_b64:
        st.error("⚠️ Visor.jpg não encontrado na pasta 'imagens'.")
    
    # Tenta carregar imagem, se não tiver usa GIF transparente
    src = f"data:image/jpeg;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    
    st.markdown(f"""
    <div class="visor-wrapper">
        <img src="{src}" class="perfume-img">
    </div>
    """, unsafe_allow_html=True)
    
    # Botões de Navegação (Bem alinhados)
    c1, c2, c3 = st.columns([1, 0.1, 1])
    with c1: st.button("❮ ANTERIOR", on_click=anterior)
    with c3: st.button("PRÓXIMO ❯", on_click=proximo)

    # Info do Produto
    st.markdown(f"""
    <div style="margin-top: 20px;">
        <div class="prod-name">{produto_atual['nome']}</div>
        <div class="prod-desc">{produto_atual['desc']}</div>
        <div class="price-box">
            <span class="old">De R$ {preco_antigo:.2f}</span>
            <span class="new">R$ {preco_atual:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- CONTEÚDO DIREITA ---
with col_dir:
    link = f"https://wa.me/5531992051499?text=Tenho%20interesse%20no%20{produto_atual['nome']}"
    st.markdown(f"""
    <div class="right-content">
        <div style="color:#d4af37; font-family:'Cinzel'; font-size:1.4rem; margin-bottom:5px;">JERRY BOMBETA</div>
        <div style="color:#666; font-size:0.9rem; margin-bottom:15px;">Specialist Fragrance Consultant</div>
        <div style="color:#fff; font-weight:bold;">📞 (31) 99205-1499</div>
        <a href="{link}" target="_blank" class="wa-btn">CHAMAR NO WHATSAPP</a>
    </div>
    """, unsafe_allow_html=True)
