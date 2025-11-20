import streamlit as st
import base64
import os
import re

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Aurum Scents",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CATÁLOGO COMPLETO (16 ITENS) ---
# Criei nomes e preços baseados na estética Old Money/Luxo
CATALOGO = {
    1: {"nome": "Royal Elixir Gold", "preco": 299.90, "desc": "Notas de ouro, mel e especiarias raras."},
    2: {"nome": "Black Orchid Intense", "preco": 350.00, "desc": "Orquídea negra profunda e misteriosa."},
    3: {"nome": "Velvet Santal Wood", "preco": 420.00, "desc": "Sândalo aveludado com toque de couro."},
    4: {"nome": "Imperial Amber", "preco": 380.00, "desc": "Âmbar imperial com raspas cítricas."},
    5: {"nome": "Club de Nuit Intense", "preco": 250.00, "desc": "Cítrico amadeirado marcante e viril."},
    6: {"nome": "Midnight Saffron", "preco": 310.00, "desc": "Açafrão noturno com fundo de tabaco."},
    7: {"nome": "Oceanic Leather", "preco": 275.00, "desc": "Couro italiano com brisa marinha."},
    8: {"nome": "Rose of Dubai", "preco": 340.00, "desc": "Rosas damascenas colhidas ao amanhecer."},
    9: {"nome": "Emerald Vetiver", "preco": 290.00, "desc": "Vetiver fresco com notas verdes vibrantes."},
    10: {"nome": "Golden Tobacco", "preco": 450.00, "desc": "Folhas de tabaco cubano e baunilha."},
    11: {"nome": "Pure Musk Absolute", "preco": 220.00, "desc": "Almíscar puro, limpo e sofisticado."},
    12: {"nome": "Celestial Oud", "preco": 550.00, "desc": "Oud raro envelhecido em barris de carvalho."},
    13: {"nome": "Spice Route", "preco": 260.00, "desc": "Pimenta rosa, cardamomo e noz-moscada."},
    14: {"nome": "Vanilla Noir", "preco": 280.00, "desc": "Baunilha negra de Madagascar defumada."},
    15: {"nome": "Cedar & Cognac", "preco": 330.00, "desc": "Cedro nobre banhado em conhaque envelhecido."},
    16: {"nome": "Majestic Iris", "preco": 360.00, "desc": "Íris atalcada com fundo amadeirado suave."},
}

# --- 3. VARREDURA INTELIGENTE DE ARQUIVOS ---
def carregar_produtos_automaticamente():
    produtos_encontrados = []
    # Garante que acha a pasta imagens onde quer que ela esteja
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_imagens = os.path.join(pasta_atual, "imagens")
    
    if not os.path.exists(pasta_imagens):
        st.error(f"❌ Pasta 'imagens' não encontrada em: {pasta_imagens}")
        return []

    arquivos = os.listdir(pasta_imagens)
    
    # Função para pegar o número do nome do arquivo (ex: "Perfume 10.jpg" -> 10)
    def extrair_numero(texto):
        nums = re.findall(r'\d+', texto)
        return int(nums[0]) if nums else 999

    # Filtra arquivos de imagem que tenham "perfume" no nome
    arquivos_validos = [f for f in arquivos if "perfume" in f.lower() and f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    # Ordena pelo número (1, 2, ... 10, 11)
    arquivos_ordenados = sorted(arquivos_validos, key=extrair_numero)

    ids_processados = set() # Para evitar duplicatas (ex: Perfume11.jpg e Perfume11.png)

    for arquivo in arquivos_ordenados:
        numero = extrair_numero(arquivo)
        
        # Se já processamos esse número (ex: pegou o jpg, ignora o png), pula
        if numero in ids_processados:
            continue
            
        # Pega dados do catálogo ou usa genérico se passar de 16
        dados = CATALOGO.get(numero, {
            "nome": f"Edição Limitada Nº {numero}",
            "preco": 0.00,
            "desc": "Fragrância exclusiva."
        })
        
        produtos_encontrados.append({
            "id": numero,
            "nome": dados["nome"],
            "arquivo": os.path.join(pasta_imagens, arquivo),
            "preco": dados["preco"],
            "desc": dados["desc"]
        })
        ids_processados.add(numero)
        
    return produtos_encontrados

def get_img_as_base64(caminho):
    if not caminho or not os.path.exists(caminho): return None
    try:
        with open(caminho, "rb") as f: data = f.read()
        return base64.b64encode(data).decode('utf-8')
    except: return None

# --- 4. INICIALIZAÇÃO ---
produtos = carregar_produtos_automaticamente()

if not produtos:
    st.error("Nenhum perfume encontrado. Verifique se a pasta 'imagens' está junto com o arquivo app.py")
    st.stop()

# Navegação
if 'idx' not in st.session_state: st.session_state.idx = 0
def proximo(): st.session_state.idx = (st.session_state.idx + 1) % len(produtos)
def anterior(): st.session_state.idx = (st.session_state.idx - 1 + len(produtos)) % len(produtos)

# Dados atuais
produto_atual = produtos[st.session_state.idx]
img_produto_b64 = get_img_as_base64(produto_atual["arquivo"])

# Busca Visor (Tenta jpg ou png)
path_base = os.path.dirname(os.path.abspath(__file__))
path_visor = os.path.join(path_base, "imagens", "Visor.jpg")
if not os.path.exists(path_visor):
     path_visor = os.path.join(path_base, "imagens", "Visor.png")
     
visor_b64 = get_img_as_base64(path_visor)

preco_atual = produto_atual["preco"]
preco_antigo = preco_atual + (100 if preco_atual > 0 else 0)

# --- 5. CSS (ESTILO FINAL) ---
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
    
    /* ALINHAMENTO VERTICAL */
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
    
    /* --- O EFEITO MÁGICO --- */
    .perfume-overlay {{
        position: absolute; 
        top: 57%; /* Ajuste fino da altura */
        left: 50%; 
        transform: translate(-50%, -50%);
        height: 55%; 
        width: auto; 
        
        /* Remove o fundo branco do JPG visualmente */
        mix-blend-mode: multiply; 
        filter: contrast(1.1) brightness(0.95);
        
        transition: all 0.5s;
    }}
    
    .perfume-overlay:hover {{ 
        transform: translate(-50%, -52%) scale(1.05); 
        mix-blend-mode: normal; /* Volta ao normal no hover */
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5));
    }}

    /* BOTOES E INFO */
    div.stButton > button {{
        background: transparent; border: 1px solid #d4af37; color: #d4af37;
        font-family: 'Cinzel', serif; width: 100%; padding: 0.8rem; letter-spacing: 2px; text-transform: uppercase;
    }}
    div.stButton > button:hover {{ background: rgba(212, 175, 55, 0.15); color: #fff; border-color: #fff; }}
    
    .prod-name {{ font-family: 'Cinzel', serif; font-size: 2.5rem; color: #fff; text-align: center; }}
    .prod-desc {{ font-family: 'Playfair Display', serif; color: #888; text-align: center; font-style: italic; margin-bottom:15px; }}
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

# --- 6. LAYOUT ---
st.markdown('<div class="brand-header"><h1 class="brand-title">AURUM SCENTS</h1></div>', unsafe_allow_html=True)
col_L, col_C, col_R = st.columns([3, 6, 3], gap="large")

# ESQUERDA
with col_L:
    st.markdown("""
    <div class="left-panel">
        <h3 style="color:#d4af37; font-family:'Cinzel'; margin-bottom:20px;">A Essência do Luxo</h3>
        <p class="panel-text">Na Aurum Scents, a fragrância não é apenas um aroma, é uma assinatura invisível.</p>
        <p class="panel-text">Nossa curadoria busca ingredientes raros para despertar os prazeres da fragrância em sua forma mais pura. Cada frasco é uma promessa de distinção.</p>
    </div>
    """, unsafe_allow_html=True)

# CENTRO
with col_C:
    # Se não achar imagem, usa GIF transparente
    src = f"data:image/jpeg;base64,{img_produto_b64}" if img_produto_b64 else "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        
    st.markdown(f"""
    <div class="visor-wrapper">
        <img src="{src}" class="perfume-overlay">
