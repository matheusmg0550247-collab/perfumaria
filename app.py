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

# --- 2. FUNÇÃO DE BUSCA INTELIGENTE ---
def encontrar_imagem_na_marra(numero_perfume):
    """
    Vasculha a pasta 'imagens' procurando algo que pareça com o perfume desejado.
    Ex: Se procuro perfume 1, ele aceita 'Perfume1.png', 'perfume 1.jpg', 'foto_perfume_1.jpeg'
    """
    # 1. Tenta achar a pasta (testa minúsculo e maiúsculo)
    pasta = "imagens"
    if not os.path.exists(pasta):
        pasta = "Imagens" # Tenta com I maiúsculo
        if not os.path.exists(pasta):
            return None, f"Pasta 'imagens' não encontrada."

    # 2. Lista todos os arquivos da pasta
    try:
        arquivos = os.listdir(pasta)
    except:
        return None, "Erro ao ler pasta."

    # 3. Procura o arquivo
    busca = str(numero_perfume) # Procura pelo número "1", "2", etc.
    
    for arquivo in arquivos:
        nome_lower = arquivo.lower()
        # Se tiver "perfume" E o número desejado no nome, e for imagem...
        if "perfume" in nome_lower and busca in nome_lower:
            if nome_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                return os.path.join(pasta, arquivo), None # ACHOU!

    # Se chegou aqui, não achou
    return None, f"Não achei perfume {numero_perfume} na lista: {arquivos}"

def get_img_as_base64(caminho):
    if not caminho: return None
    try:
        with open(caminho, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode('utf-8')
    except:
        return None

# --- 3. DADOS SIMPLIFICADOS ---
# Agora só indicamos o NÚMERO do perfume. O código se vira para achar a foto.
produtos = [
    {"id": 1, "nome": "Royal Elixir Gold", "preco": 299.90, "desc": "Notas de ouro e especiarias raras."},
    {"id": 2, "nome": "Black Orchid Intense", "preco": 350.00, "desc": "Orquídea negra profunda e misteriosa."},
    {"id": 3, "nome": "Velvet Santal Wood", "preco": 420.00, "desc": "Sândalo aveludado e envolvente."},
    {"id": 4, "nome": "Imperial Amber", "preco": 380.00, "desc": "Âmbar imperial com toque cítrico."},
]

# --- 4. NAVEGAÇÃO ---
if 'idx' not in st.session_state: st.session_state.idx = 0
def proximo(): st.session_state.idx = (st.session_state.idx + 1) % len(produtos)
def anterior(): st.session_state.idx = (st.session_state.idx - 1 + len(produtos)) % len(produtos)

# --- 5. CARREGAMENTO ---
produto_atual = produtos[st.session_state.idx]

# Busca Visor
path_visor = "imagens/Visor.jpg" 
if not os.path.exists(path_visor): path_visor = "imagens/Visor.png" # Tenta png
visor_b64 = get_img_as_base64(path_visor)

# Busca Perfume (Usa a função inteligente)
path_produto, erro_busca = encontrar_imagem_na_marra(produto_atual['id'])
img_produto_b64 = get_img_as_base64(path_produto)

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + 100.00

# --- 6. CSS (LAYOUT) ---
bg_visor_css = f"url('data:image/png;base64,{visor_b64}')" if visor_b64 else "#111"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    .stApp {{ background-color: #000000; color: #d4af37; }}
    .block-container {{ padding-top: 1rem; max-width: 1400px !important; }}
    
    /* TIPOGRAFIA */
    .brand-title {{
        font-family: 'Cinzel', serif; font-size: 4rem; text-align: center;
        background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 5px; margin-bottom: 40px;
    }}
    
    /* PAINEIS LATERAIS ALINHADOS VERTICALMENTE */
    [data-testid="column"] {{ display: flex; flex-direction: column; justify-content: center; }}

    /* ESQUERDA */
    .left-panel {{ padding-right: 30px; border-right: 1px solid #222; text-align: justify; }}
    .panel-text {{ font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #aaa; line-height: 1.8; }}
    
    /* CENTRO - VISOR */
    .visor-wrapper {{
        position: relative; width: 100%; max-width: 800px; aspect-ratio: 16/9; margin: 0 auto;
        background-image: {bg_visor_css}; background-size: cover; background-position: center;
        border-radius: 4px; box-shadow: 0 20px 50px rgba(0,0,0,0.8); margin-bottom: 20px;
    }}
    .perfume-overlay {{
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -45%);
        height: 60%; width: auto; filter: drop-shadow(0 15px 20px rgba(0,0,0,0.8));
        transition: all 0.5s;
    }}
    .perfume-overlay:hover {{ transform: translate(-50%, -48%) scale(1.03); }}

    /* BOTÕES E INFO */
    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; width: 100%; padding: 0.8rem; letter-spacing: 2px; text-transform: uppercase;
    }}
    div.stButton > button:hover {{ background: rgba(212, 175, 55, 0.15); color: #fff; border-color: #fff; }}
    .prod-name {{ font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; text-align: center; }}
    .prod-desc {{ font-family: 'Playfair Display', serif; color: #888; text-align: center; font-style: italic; }}
    .price-box {{ text-align: center; margin-top: 10px; }}
    .old {{ text-decoration: line-through; color: #555; font-size: 1.2rem; margin-right: 10px; }}
    .new {{ color: #d4af37; font-size: 3rem; font-weight: bold; }}

    /* DIREITA */
    .right-panel {{
        background: linear-gradient(145deg, #111, #0a0a0a); padding: 30px; 
        border-radius: 10px; text-align: center; border: 1px solid #222;
    }}
    .wa-btn {{
        display: block; background: linear-gradient(45deg, #25d366, #128c7e); color: white;
        padding: 12px; border-radius: 50px; text-decoration: none; font-weight: bold; font-family: sans-serif;
        margin-top: 20px; transition: 0.3s;
    }}
    .wa-btn:hover {{ transform: scale(1.05); color: white; }}
</style>
""", unsafe_allow_html=True)

# --- 7. ESTRUTURA ---
st.markdown('<div class="brand-header"><h1 class="brand-title">AURUM SCENTS</h1></div>', unsafe_allow_html=True)
col_L, col_C, col_R = st.columns([3, 6, 3], gap="large")

# ESQUERDA
with col_L:
    st.markdown("""
    <div class="left-panel">
        <h3 style="color:#d4af37; font-family:'Cinzel'; margin-bottom:20px;">A Essência do Luxo</h3>
        <p class="panel-text">Na Aurum Scents, a fragrância não é apenas um aroma, é uma assinatura invisível.</p>
        <p class="panel-text">Nossa curadoria busca ingredientes raros para despertar os prazeres da fragrância em sua forma mais pura.</p>
    </div>
    """, unsafe_allow_html=True)

# CENTRO
with col_C:
    # SE NÃO ACHOU IMAGEM, MOSTRA MENSAGEM DE DEBUG NO LUGAR DA IMAGEM
    if not img_produto_b64:
        st.warning(f"⚠️ {erro_busca}")
        # Fallback transparente
        src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
    else:
        src = f"data:image/png;base64,{img_produto_b64}"
        
    st.markdown(f"""
    <div class="visor-wrapper">
        <img src="{src}" class="perfume-overlay">
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 0.2, 1])
    with c1: st.button("❮ ANTERIOR", on_click=anterior)
    with c3: st.button("PRÓXIMO ❯", on_click=proximo)

    st.markdown(f"""
        <div class="prod-name">{produto_atual['nome']}</div>
        <div class="prod-desc">{produto_atual['desc']}</div>
        <div class="price-box">
            <span class="old">De R$ {preco_antigo:.2f}</span>
            <span class="new">R$ {preco_atual:.2f}</span>
        </div>
    """, unsafe_allow_html=True)

# DIREITA
with col_R:
    msg = f"Olá Jerry! Interesse no {produto_atual['nome']}"
    link = f"https://wa.me/5531992051499?text={msg.replace(' ', '%20')}"
    st.markdown(f"""
    <div class="right-panel">
        <div style="color:#d4af37; font-family:'Cinzel'; font-size:1.5rem;">JERRY BOMBETA</div>
        <div style="color:#888; font-size:0.9rem;">Specialist Fragrance Consultant</div>
        <a href="{link}" target="_blank" class="wa-btn">FALAR NO WHATSAPP</a>
        <div style="margin-top:15px; color:#d4af37;">(31) 99205-1499</div>
    </div>
    """, unsafe_allow_html=True)
