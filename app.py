import base64
import hashlib
import io
import json
import re
import urllib.parse
import uuid
from datetime import datetime
import requests
import streamlit as st
from PIL import Image
from supabase import create_client

# Configuração da Página
st.set_page_config(
    page_title="TagsInfor | Tecnologia, Hardwares e Acessórios",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================================
# CSS PROFISSIONAL ESTILO E-COMMERCE E NUVEMSHOP
# =====================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Ocultar barra lateral padrão do Streamlit */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 1360px !important;
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        -webkit-text-size-adjust: 100% !important;
        -webkit-tap-highlight-color: transparent !important;
    }

    html, body, .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }

    /* Top Promocional Loja */
    .top-promo-bar {
        background: #F59E0B;
        color: #0F172A;
        font-weight: 700;
        font-size: 0.82rem;
        padding: 7px 16px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
        letter-spacing: 0.2px;
    }
    .top-promo-text {
        font-weight: 800;
        line-height: 1.35;
    }
    .top-links {
        display: flex;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .top-links a { color: #0F172A; text-decoration: none; font-weight: 800; }

    /* Cabeçalho Responsivo (Logo, Slogan e Pílulas de Ação) */
    .header-brand-wrap {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .header-brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    .header-status-badge {
        background: rgba(34, 197, 94, 0.15);
        color: #22c55e;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 2px 9px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .header-slogan-text {
        color: #94A3B8;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.2px;
    }
    .header-actions-wrap {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }
    .header-action-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        text-decoration: none;
        white-space: nowrap;
    }

    /* Faixa de Vantagens */
    .benefits-bar-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(51, 65, 85, 0.7);
        border-radius: 10px;
        padding: 10px 16px;
        margin-top: 6px;
        margin-bottom: 14px;
    }
    .benefits-bar-item {
        text-align: center;
        font-size: 0.8rem;
        font-weight: 700;
        color: #E2E8F0;
    }

    /* Botão Flutuante WhatsApp (acima da barra do Streamlit Cloud) */
    .whatsapp-float-btn {
        position: fixed;
        bottom: calc(74px + env(safe-area-inset-bottom, 0px));
        right: 18px;
        background-color: #25D366;
        color: white !important;
        border-radius: 50%;
        width: 56px;
        height: 56px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.45);
        z-index: 999999;
        text-decoration: none;
        transition: transform 0.2s ease;
    }
    .whatsapp-float-btn:hover {
        transform: scale(1.08);
    }

    /* Logo & Nav */
    .brand-logo {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #FFFFFF;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .brand-dot {
        width: 10px;
        height: 10px;
        background: #F59E0B;
        border-radius: 50%;
        display: inline-block;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(90deg, #1E1B4B 0%, #2563EB 50%, #1D4ED8 100%);
        border-radius: 16px;
        padding: 34px 40px;
        color: #FFFFFF;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.3);
    }
    .hero-text h1 { font-size: 2.3rem; font-weight: 800; margin: 0 0 8px 0; color: #FFFFFF; }
    .hero-text p { font-size: 1.05rem; color: #E0E7FF; margin: 0 0 14px 0; }
    .hero-badges { display: flex; gap: 12px; flex-wrap: wrap; }
    .hero-badge-item {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
    }

    /* Cards Loja */
    .section-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin: 10px 0 20px 0;
        color: #F8FAFC;
    }
    .img-box {
        width: 100%;
        height: 220px;
        border-radius: 10px;
        overflow: hidden;
        background: #0F172A;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .img-box img { width: 100%; height: 100%; object-fit: cover; }
    .badge-status {
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
    .status-estoque { background: rgba(34, 197, 94, 0.15); color: #4ADE80; }
    .status-direto { background: rgba(59, 130, 246, 0.15); color: #60A5FA; }
    .status-afiliado { background: rgba(245, 158, 11, 0.15); color: #FBBF24; }
    .status-esgotado { background: rgba(239, 68, 68, 0.15); color: #F87171; }

    .prod-title { font-weight: 700; font-size: 1rem; color: #F1F5F9; margin-bottom: 6px; line-height: 1.35; min-height: 42px; }
    .prod-desc { color: #94A3B8; font-size: 0.82rem; margin-bottom: 10px; min-height: 34px; }
    .prod-price { font-size: 1.55rem; font-weight: 800; color: #10B981; margin-bottom: 12px; }
    .prod-price small { font-size: 0.8rem; color: #94A3B8; font-weight: 500; margin-left: 4px; }

    /* Admin Nuvemshop / Figma Dark */
    .admin-page-title { font-size: 1.8rem; font-weight: 800; color: #F8FAFC; margin: 0 0 16px 0; }
    .nuvem-card-title { font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 14px; }
    .dropzone-box {
        border: 2px dashed #3B82F6;
        background: rgba(37, 99, 235, 0.08);
        border-radius: 10px;
        padding: 24px;
        text-align: center;
        color: #93C5FD;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .checklist-step {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .btn-whats-pay {
        background-color: #22C55E !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 12px 20px !important;
        text-align: center;
        text-decoration: none;
        display: block;
        width: 100%;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    }

    /* =================================================================
       FIGMA MODERN SIDEBAR STYLING (REAL BUTTONS NAVBAR)
       ================================================================= */
    .figma-sidebar-header {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 4px 14px 4px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 8px;
    }
    .figma-brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #3B82F6, #1D4ED8);
        color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
        flex-shrink: 0;
    }
    .figma-brand-title {
        color: #F8FAFC;
        font-weight: 800;
        font-size: 1.05rem;
        line-height: 1.2;
    }
    .figma-brand-badge {
        font-size: 0.7rem;
        color: #94A3B8;
        font-weight: 600;
        letter-spacing: 0.4px;
    }
    .figma-nav-section-label {
        font-size: 0.68rem;
        letter-spacing: 0.09em;
        color: #64748B;
        font-weight: 800;
        text-transform: uppercase;
        margin: 10px 0 4px 8px;
    }

    /* Compactar espaçamento entre botões do menu lateral */
    [class*="st-key-nav_item_"] {
        margin-bottom: -8px !important;
    }

    /* Botão INATIVO do menu lateral (Tertiary) */
    [class*="st-key-nav_item_"] button[kind="tertiary"],
    [class*="st-key-nav_item_"] button[data-testid="stBaseButton-tertiary"] {
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        min-height: 38px !important;
        transition: all 0.15s ease !important;
    }
    [class*="st-key-nav_item_"] button[kind="tertiary"]:hover,
    [class*="st-key-nav_item_"] button[data-testid="stBaseButton-tertiary"]:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #F8FAFC !important;
        border-color: rgba(59, 130, 246, 0.2) !important;
        transform: translateX(2px);
    }

    /* Botão ATIVO / SELECIONADO do menu lateral (Primary -> Figma Pill Azul) */
    [class*="st-key-nav_item_"] button[kind="primary"],
    [class*="st-key-nav_item_"] button[data-testid="stBaseButton-primary"] {
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 8px 12px !important;
        border-radius: 10px !important;
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        min-height: 38px !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35) !important;
    }

    /* Alinhar ícone e texto perfeitamente à esquerda dentro dos botões de navegação */
    [class*="st-key-nav_item_"] button > div {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 8px !important;
        width: 100% !important;
    }
    [class*="st-key-nav_item_"] button p {
        margin: 0 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        font-size: 0.88rem !important;
    }

    /* Card de Perfil do Usuário no rodapé da barra lateral (Figma) */
    .figma-user-profile {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 12px;
        background: #0F172A;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        margin-top: 10px;
        margin-bottom: 8px;
    }
    .figma-user-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1, #3B82F6);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    .figma-user-info {
        flex: 1;
        overflow: hidden;
    }
    .figma-user-name {
        color: #F8FAFC;
        font-size: 0.85rem;
        font-weight: 700;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .figma-user-role {
        color: #10B981;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* =================================================================
       RESPONSIVIDADE MOBILE COMPLETA (ANDROID & iOS / SAFARI)
       ================================================================= */
    /* Previne o auto-zoom do Safari no iPhone ao tocar em inputs (<16px) */
    @supports (-webkit-touch-callout: none) {
        input, select, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            font-size: 16px !important;
        }
    }

    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 0.5rem !important;
            padding-left: 0.65rem !important;
            padding-right: 0.65rem !important;
            padding-bottom: 4.5rem !important;
        }

        input, select, textarea, [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            font-size: 16px !important;
        }

        /* 1. Barra Topo Amarela Compacta e Centralizada no Celular */
        .top-promo-bar {
            flex-direction: column !important;
            justify-content: center !important;
            text-align: center !important;
            padding: 6px 10px !important;
            gap: 4px !important;
            font-size: 0.7rem !important;
            border-radius: 8px !important;
            margin-bottom: 8px !important;
        }
        .top-promo-text {
            font-size: 0.71rem !important;
            line-height: 1.3 !important;
        }
        .top-links {
            justify-content: center !important;
            gap: 6px 10px !important;
            font-size: 0.67rem !important;
            border-top: 1px solid rgba(15, 23, 42, 0.15) !important;
            padding-top: 4px !important;
            width: 100% !important;
        }

        /* 2. Cabeçalho Principal (Logo + Busca + Botões WhatsApp/Carrinho 50/50) */
        .brand-logo {
            font-size: 1.45rem !important;
        }
        .header-brand-row {
            justify-content: space-between !important;
            width: 100% !important;
        }
        .header-slogan-text {
            font-size: 0.73rem !important;
        }
        .header-actions-wrap {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            width: 100% !important;
            justify-content: stretch !important;
        }
        .header-action-pill {
            width: 100% !important;
            padding: 6px 8px !important;
            font-size: 0.72rem !important;
            box-sizing: border-box !important;
        }

        /* 3. Menu de Navegação Principal e Atalhos do Rodapé em Grade 2x2 Compacta no Celular */
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_loja_nav_"]),
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_ft_"]) {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
        }
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_loja_nav_"]) > [data-testid="stColumn"]:first-child,
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_ft_"]) > [data-testid="stColumn"]:first-child {
            grid-column: 1 / -1 !important;
        }
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_loja_nav_"]) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_ft_"]) > [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: unset !important;
        }
        [class*="st-key-btn_loja_nav_"] button,
        [class*="st-key-btn_ft_"] button {
            min-height: 38px !important;
            padding: 6px 8px !important;
            font-size: 0.78rem !important;
        }
        [class*="st-key-btn_loja_nav_"] button p,
        [class*="st-key-btn_ft_"] button p {
            font-size: 0.78rem !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }

        /* 4. Botões internos (+ Carrinho | Comprar) lado a lado SEM afetar a coluna pai */
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_add_car_"]),
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_exp_add_"]) {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
        }
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_add_car_"]) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-btn_exp_add_"]) > [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: unset !important;
        }

        /* Botões (- | + | Remover) do item do carrinho na mesma linha sem afetar colunas externas */
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-car_dec_"]) {
            display: grid !important;
            grid-template-columns: 1fr 1fr 1.2fr !important;
            gap: 6px !important;
            align-items: center !important;
        }
        [data-testid="stHorizontalBlock"]:not(:has([data-testid="stHorizontalBlock"])):has([class*="st-key-car_dec_"]) > [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: unset !important;
        }

        /* Janela Modal de Detalhes do Produto adaptada para Tela Cheia no Celular */
        [data-testid="stDialog"] [role="dialog"] {
            width: 96vw !important;
            max-width: 96vw !important;
            margin: 8px auto !important;
            border-radius: 16px !important;
        }

        /* 5. Faixa de Vantagens em Grade 2x2 no Celular */
        .benefits-bar-grid {
            grid-template-columns: 1fr 1fr !important;
            gap: 6px !important;
            padding: 8px 10px !important;
            margin-top: 4px !important;
            margin-bottom: 10px !important;
        }
        .benefits-bar-item {
            font-size: 0.7rem !important;
            line-height: 1.25 !important;
        }

        /* 6. Hero Banner e Cards mais Compactos no Celular */
        .hero-banner {
            padding: 18px 16px !important;
            border-radius: 12px !important;
            margin-bottom: 16px !important;
        }
        .hero-text h1 {
            font-size: 1.32rem !important;
            line-height: 1.25 !important;
            margin-bottom: 6px !important;
        }
        .hero-text p {
            font-size: 0.84rem !important;
            margin-bottom: 10px !important;
        }
        .hero-badges {
            gap: 6px !important;
        }
        .hero-badge-item {
            font-size: 0.7rem !important;
            padding: 4px 10px !important;
        }
        .section-title {
            font-size: 1.18rem !important;
            margin: 6px 0 12px 0 !important;
        }
        .img-box {
            height: 185px !important;
        }
        .prod-title {
            font-size: 0.95rem !important;
            min-height: unset !important;
        }
        .prod-desc {
            min-height: unset !important;
        }
        .prod-price {
            font-size: 1.35rem !important;
            margin-bottom: 8px !important;
        }
        .whatsapp-float-btn {
            bottom: calc(78px + env(safe-area-inset-bottom, 0px)) !important;
            right: 14px !important;
            width: 50px !important;
            height: 50px !important;
            font-size: 25px !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# SUPABASE & FUNÇÕES NATIVAS (ISOLADO POR SESSÃO DE USUÁRIO)
# =====================================================================
def init_supabase():
    """
    Cria ou recupera uma instância do cliente Supabase EXCLUSIVA para a sessão do navegador atual
    (evitando que @st.cache_resource compartilhe tokens de autenticação entre usuários diferentes).
    """
    if "_supabase_client_sessao" not in st.session_state:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        st.session_state["_supabase_client_sessao"] = create_client(url, key)
    return st.session_state["_supabase_client_sessao"]


supabase = init_supabase()


def converter_imagem_upload(arquivo_upload) -> str:
    """
    Otimiza a imagem enviada e tenta salvá-la no bucket público 'produtos-midia' do Supabase Storage
    (retornando URL pública leve e rápida). Caso o bucket ainda não exista, faz fallback automático para Base64.
    """
    img = Image.open(arquivo_upload)
    img.thumbnail((900, 900))
    buffer = io.BytesIO()
    if img.mode in ("RGBA", "P"):
        img.save(buffer, format="WEBP", quality=85)
        mime = "image/webp"
        ext = "webp"
    else:
        img = img.convert("RGB")
        img.save(buffer, format="JPEG", quality=85)
        mime = "image/jpeg"
        ext = "jpg"
    raw_bytes = buffer.getvalue()

    try:
        try:
            supabase.storage.create_bucket("produtos-midia", options={"public": True})
        except Exception:
            pass
        nome_arq = f"prod_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
        supabase.storage.from_("produtos-midia").upload(
            path=nome_arq,
            file=raw_bytes,
            file_options={"content-type": mime, "upsert": "true"},
        )
        url_pub = supabase.storage.from_("produtos-midia").get_public_url(nome_arq)
        if isinstance(url_pub, str) and url_pub.startswith("http"):
            return url_pub
    except Exception:
        pass

    b64 = base64.b64encode(raw_bytes).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def gerar_hash_senha(senha_plana: str) -> str:
    """Gera hash SHA-256 seguro para nunca salvar senha em texto puro no banco/fallback."""
    s = (senha_plana or "").strip()
    if not s:
        return ""
    if s.startswith("sha256$"):
        return s
    return "sha256$" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def verificar_senha_cliente(senha_digitada: str, senha_salva: str) -> bool:
    """Verifica senha tanto em hash SHA-256 quanto em formato legado (texto simples)."""
    if not senha_digitada or not senha_salva:
        return False
    s_dig = senha_digitada.strip()
    s_salva = str(senha_salva).strip()
    if s_salva.startswith("sha256$"):
        return gerar_hash_senha(s_dig) == s_salva
    return s_dig == s_salva


def crc16_ccitt(data: str) -> str:
    poly = 0x1021
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ poly) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"


def gerar_pix_bacen(chave: str, nome: str, cidade: str, valor: float, txid: str = "LOJA") -> str:
    def tlv(tag: str, val: str) -> str:
        v_bytes = val.encode("utf-8")
        return f"{tag}{len(v_bytes):02d}{val}"

    gui = tlv("00", "br.gov.bcb.pix")
    key = tlv("01", chave)
    mai = tlv("26", gui + key)

    payload = (
        tlv("00", "01")
        + mai
        + tlv("52", "0000")
        + tlv("53", "986")
        + tlv("54", f"{valor:.2f}")
        + tlv("58", "BR")
        + tlv("59", nome[:25].upper())
        + tlv("60", cidade[:15].upper())
        + tlv("62", tlv("05", txid[:25]))
        + "6304"
    )
    return payload + crc16_ccitt(payload)


def gerar_declaracao_conteudo_html(ped: dict, fisc: dict) -> str:
    itens = ped.get("itens", [])
    fiscal_cli = itens[0].get("fiscal", {}) if itens else {}

    # Destinatário (Cliente)
    dest_nome = ped.get("cliente_nome", "Cliente")
    dest_doc = fiscal_cli.get("documento") or ped.get("cliente_cpf", "-")
    dest_end = ped.get("endereco_completo", "-")
    dest_cep = ped.get("cep", "-")
    dest_cid = fiscal_cli.get("cidade", "Manaus")
    dest_uf = fiscal_cli.get("uf", "AM")

    # Remetente (Tags Informática)
    rem_nome = fisc.get("razao_social", "Tags Informática")
    rem_cnpj = fisc.get("cnpj", "00.000.000/0001-00")
    rem_end = f"{fisc.get('rua_origem', 'Av. Djalma Batista')}, {fisc.get('numero_origem', '1000')} {fisc.get('complemento_origem', '')} - {fisc.get('bairro_origem', 'Chapada')}"
    rem_cid = fisc.get("cidade_origem", "Manaus")
    rem_uf = fisc.get("estado_origem", "AM")
    rem_cep = fisc.get("cep_origem", "69050-010")

    linhas_itens = ""
    for idx, it in enumerate(itens, 1):
        qtd = it.get("qtd", 1)
        tit = it.get("titulo", "Produto de Informática")
        val = float(it.get("preco_unit", 0)) * qtd
        linhas_itens += f"""
        <tr>
            <td style="border:1px solid #000; padding:5px; text-align:center;">{idx}</td>
            <td style="border:1px solid #000; padding:5px;">{tit}</td>
            <td style="border:1px solid #000; padding:5px; text-align:center;">{qtd}</td>
            <td style="border:1px solid #000; padding:5px; text-align:right;">R$ {val:.2f}</td>
        </tr>
        """
    total_val = float(ped.get("valor_total", 0))
    data_str = datetime.now().strftime("%d/%m/%Y")

    html = f"""
    <div style="background:#FFFFFF; color:#000000; padding:22px; border:2px solid #000000; font-family:Arial, Helvetica, sans-serif; font-size:12px; margin: 15px 0; border-radius:4px;">
        <div style="text-align:center; border-bottom:2px solid #000000; padding-bottom:8px; margin-bottom:12px;">
            <h3 style="margin:0; font-size:16px; font-weight:bold; letter-spacing:1px; color:#000;">DECLARAÇÃO DE CONTEÚDO</h3>
            <span style="font-size:10px; color:#444;">Exigência da Portaria nº 2.408 do Ministério da Fazenda / Correios e Transportadoras</span>
        </div>

        <table style="width:100%; border-collapse:collapse; margin-bottom:10px; border:1px solid #000; font-size:11px;">
            <tr style="background:#F1F5F9;"><th colspan="2" style="border:1px solid #000; padding:5px; text-align:left; color:#000;">1. REMETENTE (TAGS INFORMÁTICA)</th></tr>
            <tr><td style="border:1px solid #000; padding:5px; color:#000;"><b>Nome / Razão Social:</b> {rem_nome}</td><td style="border:1px solid #000; padding:5px; color:#000;"><b>CPF / CNPJ:</b> {rem_cnpj}</td></tr>
            <tr><td colspan="2" style="border:1px solid #000; padding:5px; color:#000;"><b>Endereço:</b> {rem_end}</td></tr>
            <tr><td style="border:1px solid #000; padding:5px; color:#000;"><b>Cidade / UF:</b> {rem_cid} / {rem_uf}</td><td style="border:1px solid #000; padding:5px; color:#000;"><b>CEP:</b> {rem_cep}</td></tr>
        </table>

        <table style="width:100%; border-collapse:collapse; margin-bottom:10px; border:1px solid #000; font-size:11px;">
            <tr style="background:#F1F5F9;"><th colspan="2" style="border:1px solid #000; padding:5px; text-align:left; color:#000;">2. DESTINATÁRIO (CLIENTE)</th></tr>
            <tr><td style="border:1px solid #000; padding:5px; color:#000;"><b>Nome / Razão Social:</b> {dest_nome}</td><td style="border:1px solid #000; padding:5px; color:#000;"><b>CPF / CNPJ:</b> {dest_doc}</td></tr>
            <tr><td colspan="2" style="border:1px solid #000; padding:5px; color:#000;"><b>Endereço de Entrega:</b> {dest_end}</td></tr>
            <tr><td style="border:1px solid #000; padding:5px; color:#000;"><b>Cidade / UF:</b> {dest_cid} / {dest_uf}</td><td style="border:1px solid #000; padding:5px; color:#000;"><b>CEP:</b> {dest_cep}</td></tr>
        </table>

        <table style="width:100%; border-collapse:collapse; margin-bottom:10px; border:1px solid #000; font-size:11px;">
            <tr style="background:#F1F5F9; color:#000;">
                <th style="border:1px solid #000; padding:5px; width:45px; text-align:center;">ITEM</th>
                <th style="border:1px solid #000; padding:5px; text-align:left;">CONTEÚDO / DISCRIMINAÇÃO</th>
                <th style="border:1px solid #000; padding:5px; width:60px; text-align:center;">QTD</th>
                <th style="border:1px solid #000; padding:5px; width:110px; text-align:right;">VALOR TOTAL</th>
            </tr>
            {linhas_itens}
            <tr style="font-weight:bold; background:#F8FAFC; color:#000;">
                <td colspan="3" style="border:1px solid #000; padding:6px; text-align:right;">TOTAL DECLARADO:</td>
                <td style="border:1px solid #000; padding:6px; text-align:right;">R$ {total_val:.2f}</td>
            </tr>
        </table>

        <div style="font-size:9.5px; border:1px solid #000; padding:6px; line-height:1.4; margin-bottom:14px; color:#222;">
            <b>DECLARAÇÃO DE RESPONSABILIDADE:</b> Declaro que não me enquadro no conceito de contribuinte previsto no art. 4º da Lei Complementar nº 87/1996, não realizando com habitualidade ou em volume que caracterize intuito comercial operações de circulação de mercadorias, a não ser as indicadas nesta declaração de conteúdo, estando dispensado da emissão de documento fiscal. Comprometo-me com a veracidade das informações sob as penas da lei.
        </div>

        <div style="display:flex; justify-content:space-between; align-items:flex-end; font-size:11px; margin-top:20px; padding:0 10px; color:#000;">
            <div>Local e Data: <b>{rem_cid}/{rem_uf}, {data_str}</b></div>
            <div style="text-align:center; border-top:1px solid #000; width:260px; padding-top:4px;">
                Assinatura do Declarante / Remetente
            </div>
        </div>
    </div>
    """
    return html


def gerar_danfe_recibo_html(ped: dict, fisc: dict) -> str:
    itens = ped.get("itens", [])
    fiscal_cli = itens[0].get("fiscal", {}) if itens else {}

    dest_nome = ped.get("cliente_nome", "Cliente")
    dest_doc = fiscal_cli.get("documento") or ped.get("cliente_cpf", "-")
    dest_end = ped.get("endereco_completo", "-")
    dest_cep = ped.get("cep", "-")
    dest_cid = fiscal_cli.get("cidade", "Manaus")
    dest_uf = fiscal_cli.get("uf", "AM")
    dest_email = fiscal_cli.get("email", "Não informado")
    dest_whats = ped.get("cliente_whatsapp", "-")

    rem_nome = fisc.get("razao_social", "Tags Informática")
    rem_cnpj = fisc.get("cnpj", "00.000.000/0001-00")
    rem_ie = fisc.get("inscricao_estadual", "Isento")
    rem_end = f"{fisc.get('rua_origem', 'Av. Djalma Batista')}, {fisc.get('numero_origem', '1000')} - {fisc.get('bairro_origem', 'Chapada')}"
    rem_cid = fisc.get("cidade_origem", "Manaus")
    rem_uf = fisc.get("estado_origem", "AM")
    rem_fone = fisc.get("telefone_fiscal", WHATSAPP_LOJA)
    nfe_serie = fisc.get("serie_nfe", "1")
    nfe_num = int(fisc.get("proxima_nfe", 1))

    linhas_danfe = ""
    subtotal_val = 0.0
    for it in itens:
        qtd = it.get("qtd", 1)
        tit = it.get("titulo", "Produto")
        p_unit = float(it.get("preco_unit", 0))
        t_it = p_unit * qtd
        subtotal_val += t_it
        ncm_it = it.get("fiscal", {}).get("ncm", fisc.get("ncm_padrao", "8471.60.52"))
        linhas_danfe += f"""
        <tr>
            <td style="border:1px solid #0F172A; padding:5px; text-align:center; color:#000;">{it.get('id', '01')}</td>
            <td style="border:1px solid #0F172A; padding:5px; color:#000;">{tit}</td>
            <td style="border:1px solid #0F172A; padding:5px; text-align:center; color:#000;">{ncm_it}</td>
            <td style="border:1px solid #0F172A; padding:5px; text-align:center; color:#000;">{qtd}</td>
            <td style="border:1px solid #0F172A; padding:5px; text-align:right; color:#000;">R$ {p_unit:.2f}</td>
            <td style="border:1px solid #0F172A; padding:5px; text-align:right; color:#000;">R$ {t_it:.2f}</td>
        </tr>
        """

    tot_val = float(ped.get("valor_total", 0))
    desc_val = max(0.0, subtotal_val - tot_val)
    data_str = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""
    <div style="background:#FFFFFF; color:#0F172A; padding:22px; border:2px solid #0F172A; font-family:Arial, sans-serif; font-size:12px; margin:15px 0; border-radius:4px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2px solid #0F172A; padding-bottom:10px; margin-bottom:10px;">
            <div>
                <h2 style="margin:0 0 4px 0; font-size:18px; font-weight:800; color:#0284C7;">{rem_nome}</h2>
                <div style="font-size:11px; color:#334155;"><b>CNPJ:</b> {rem_cnpj} &nbsp;|&nbsp; <b>Inscrição Estadual:</b> {rem_ie}</div>
                <div style="font-size:11px; color:#334155;"><b>Endereço:</b> {rem_end} - {rem_cid}/{rem_uf}</div>
                <div style="font-size:11px; color:#334155;"><b>Telefone / SAC:</b> {rem_fone}</div>
            </div>
            <div style="border:1px solid #0F172A; padding:8px 14px; text-align:right; background:#F8FAFC; border-radius:6px;">
                <div style="font-weight:bold; font-size:13px; color:#0F172A;">DANFE SIMPLIFICADA</div>
                <div style="font-size:11px;">PEDIDO: <b>#{ped.get('id', 'NOVO')}</b></div>
                <div style="font-size:11px;">SÉRIE: <b>{nfe_serie}</b> &nbsp;|&nbsp; NF-e: <b>{nfe_num:04d}</b></div>
                <div style="font-size:10px; color:#64748B;">EMISSÃO: {data_str}</div>
            </div>
        </div>

        <div style="margin-bottom:10px;">
            <div style="background:#0F172A; color:#FFFFFF; padding:4px 8px; font-weight:bold; font-size:11px;">DADOS DO DESTINATÁRIO / COMPRADOR</div>
            <div style="border:1px solid #0F172A; border-top:none; padding:8px; line-height:1.4; color:#000;">
                <div><b>Nome / Razão Social:</b> {dest_nome} &nbsp;&nbsp;|&nbsp;&nbsp; <b>CPF/CNPJ:</b> {dest_doc}</div>
                <div><b>Endereço Completo:</b> {dest_end}</div>
                <div><b>Município / UF:</b> {dest_cid} / {dest_uf} &nbsp;|&nbsp; <b>CEP:</b> {dest_cep} &nbsp;|&nbsp; <b>E-mail:</b> {dest_email} &nbsp;|&nbsp; <b>WhatsApp:</b> {dest_whats}</div>
            </div>
        </div>

        <div style="margin-bottom:10px;">
            <div style="background:#0F172A; color:#FFFFFF; padding:4px 8px; font-weight:bold; font-size:11px;">ITENS DA VENDA / PRESTAÇÃO DE SERVIÇO</div>
            <table style="width:100%; border-collapse:collapse; border:1px solid #0F172A; font-size:11px;">
                <tr style="background:#F1F5F9; color:#000;">
                    <th style="border:1px solid #0F172A; padding:4px; width:45px; text-align:center;">CÓD</th>
                    <th style="border:1px solid #0F172A; padding:4px; text-align:left;">DESCRIÇÃO DO PRODUTO / CURSO</th>
                    <th style="border:1px solid #0F172A; padding:4px; width:80px; text-align:center;">NCM</th>
                    <th style="border:1px solid #0F172A; padding:4px; width:50px; text-align:center;">QTD</th>
                    <th style="border:1px solid #0F172A; padding:4px; width:90px; text-align:right;">VALOR UNIT.</th>
                    <th style="border:1px solid #0F172A; padding:4px; width:100px; text-align:right;">TOTAL</th>
                </tr>
                {linhas_danfe}
            </table>
        </div>

        <table style="width:100%; border-collapse:collapse; border:1px solid #0F172A; margin-bottom:10px; font-size:11px; background:#F8FAFC; color:#000;">
            <tr>
                <td style="padding:6px; border:1px solid #0F172A;"><b>FORMA DE PAGAMENTO:</b> PIX BACEN (CONFIRMADO)</td>
                <td style="padding:6px; border:1px solid #0F172A;"><b>SUBTOTAL:</b> R$ {subtotal_val:.2f}</td>
                <td style="padding:6px; border:1px solid #0F172A;"><b>DESCONTO CUPOM:</b> R$ {desc_val:.2f}</td>
                <td style="padding:6px; border:1px solid #0F172A; font-weight:bold; font-size:12px; color:#16A34A; text-align:right;">TOTAL PAGO: R$ {tot_val:.2f}</td>
            </tr>
        </table>

        <div style="font-size:9.5px; border:1px solid #0F172A; padding:6px; color:#334155; line-height:1.4;">
            <b>INFORMAÇÕES FISCAIS:</b> Empresa optante pelo {fisc.get('regime_tributario', 'MEI - Microempreendedor Individual')}. Não gera direito a crédito fiscal de IPI ou ICMS. Operação acobertada nos termos da Legislação Tributária Vigente.
        </div>
    </div>
    """
    return html


CHAVE_PIX = st.secrets.get("CHAVE_PIX", "contato@tagsinfor.com")
NOME_BENEFICIARIO = st.secrets.get("NOME_BENEFICIARIO", "TAGSINFOR OFICIAL")
CIDADE_BENEFICIARIO = st.secrets.get("CIDADE_BENEFICIARIO", "SAO PAULO")
WHATSAPP_LOJA = st.secrets.get("WHATSAPP_LOJA", "11999999999")
MP_TOKEN = st.secrets.get("MP_ACCESS_TOKEN", "")
SENHA_ADMIN = st.secrets.get("SENHA_ADMIN", "admin123")

# Configurações dinâmicas de Layout, Cabeçalho e Rodapé da Loja
CONFIG_LOJA_PADRAO = {
    "nome_loja": "Tags Informática",
    "slogan_cabecalho": "Cursos, Mentorias & Tecnologia Oficial",
    "status_loja": "🟢 Aberto",
    "top_promo": "⚡ TAGS INFORMÁTICA | CURSOS, MENTORIAS E TECNOLOGIA | PAGAMENTO FÁCIL NO PIX",
    "localizacao_cabecalho": "📍 Manaus/AM • Envio p/ Todo Brasil",
    "exibir_barra_vantagens": True,
    "vantagem_1": "⚡ Pix com Aprovação Imediata",
    "vantagem_2": "🚚 Envio Rápido c/ Rastreio",
    "vantagem_3": "🛡️ Compra 100% Garantida",
    "vantagem_4": "🎓 Cursos com Certificado",
    "hero_title": "UPGRADE DO SEU SETUP E CARREIRA",
    "hero_subtitle": "Os melhores cursos de informática, mentorias individuais e equipamentos com pronta entrega.",
    "em_construcao": False,
    "logo_url": "",
    "rodape_sobre": "A Tags Informática é referência em cursos profissionalizantes, mentorias individuais VIP e equipamentos de tecnologia com pronta entrega, suporte dedicado e garantia oficial.",
    "rodape_horario": "Seg a Sex das 08h às 18h | Sáb das 08h às 13h",
    "rodape_email": "contato@tagsinfor.com",
    "rodape_whatsapp": WHATSAPP_LOJA,
    "rodape_endereco": "Av. Djalma Batista, 1000 - Chapada, Manaus/AM",
    "rodape_cnpj": "00.000.000/0001-00",
    "rodape_instagram": "https://instagram.com",
    "rodape_youtube": "https://youtube.com",
    "rodape_copyright": "© 2026 Tags Informática — Todos os direitos reservados.",
}
if "config_loja" not in st.session_state:
    st.session_state["config_loja"] = dict(CONFIG_LOJA_PADRAO)
else:
    for _k_cfg, _v_cfg in CONFIG_LOJA_PADRAO.items():
        st.session_state["config_loja"].setdefault(_k_cfg, _v_cfg)

# Cupons de Desconto ativos na loja
if "cupons" not in st.session_state:
    st.session_state["cupons"] = [
        {"codigo": "PRIMEIRACOMPRA", "tipo": "Porcentagem", "valor": 10.0, "ativo": True},
        {"codigo": "TAGS15", "tipo": "Porcentagem", "valor": 15.0, "ativo": True},
        {"codigo": "DESCONTO20", "tipo": "Valor fixo", "valor": 20.0, "ativo": True},
    ]
    try:
        res_cp = supabase.table("cupons").select("*").eq("ativo", True).execute()
        if res_cp.data:
            st.session_state["cupons"] = res_cp.data
    except Exception:
        pass

# Clientes cadastrados manualmente
if "clientes_extras" not in st.session_state:
    st.session_state["clientes_extras"] = []
    try:
        res_cl = supabase.table("clientes").select("*").execute()
        if res_cl.data:
            st.session_state["clientes_extras"] = [
                {
                    "nome": c.get("nome"),
                    "cpf": c.get("cpf_cnpj"),
                    "whatsapp": c.get("whatsapp"),
                    "email": c.get("email"),
                    "endereco": c.get("endereco_completo"),
                    "cep": c.get("cep"),
                    "tabela": c.get("tabela_preco", "Varejo"),
                    "total_pedidos": 0,
                }
                for c in res_cl.data
            ]
    except Exception:
        pass

# Dados Fiscais da Empresa e Centro de Distribuição (Nuvemshop)
if "dados_fiscais_loja" not in st.session_state:
    st.session_state["dados_fiscais_loja"] = {
        "razao_social": "Tags Informática",
        "nome_fantasia": "Tags Informática",
        "cnpj": "00.000.000/0001-00",
        "inscricao_estadual": "Isento",
        "telefone_fiscal": WHATSAPP_LOJA,
        "regime_tributario": "MEI - Microempreendedor Individual",
        "serie_nfe": "1",
        "proxima_nfe": 1,
        "ncm_padrao": "8471.60.52",
        "local_nome": "Depósito Principal Tags Informática",
        "pais": "Brasil",
        "cep_origem": "69050-010",
        "estado_origem": "AM",
        "cidade_origem": "Manaus",
        "bairro_origem": "Chapada",
        "rua_origem": "Av. Djalma Batista",
        "numero_origem": "1000",
        "complemento_origem": "Sala 102",
        "logo_danfe": "",
    }
    try:
        res_cd = supabase.table("centro_distribuicao").select("*").limit(1).execute()
        if res_cd.data:
            cd_db = res_cd.data[0]
            st.session_state["dados_fiscais_loja"].update({
                "local_nome": cd_db.get("nome_local", "Depósito Principal Tags Informática"),
                "razao_social": cd_db.get("razao_social", "Tags Informática LTDA"),
                "cnpj": cd_db.get("cnpj", "00.000.000/0001-00"),
                "inscricao_estadual": cd_db.get("inscricao_estadual", "Isento"),
                "telefone_fiscal": cd_db.get("telefone_fiscal", WHATSAPP_LOJA),
                "cep_origem": cd_db.get("cep", "69050-010"),
                "rua_origem": cd_db.get("logradouro", "Av. Djalma Batista"),
                "numero_origem": cd_db.get("numero", "1000"),
                "complemento_origem": cd_db.get("complemento", "Sala 102"),
                "bairro_origem": cd_db.get("bairro", "Chapada"),
                "cidade_origem": cd_db.get("cidade", "Manaus"),
                "estado_origem": cd_db.get("estado", "AM"),
                "regime_tributario": cd_db.get("regime_tributario", "MEI - Microempreendedor Individual"),
                "serie_nfe": str(cd_db.get("serie_nfe", "1")),
                "proxima_nfe": int(cd_db.get("proxima_nfe", 1)),
            })
    except Exception:
        pass

# =====================================================================
# ESTRUTURA MULTI-NICHO: DEPARTAMENTOS -> CATEGORIAS -> SUBCATEGORIAS
# =====================================================================
if "departamentos_fallback" not in st.session_state:
    st.session_state["departamentos_fallback"] = [
        {"id": 1, "nome": "Educação & Cursos", "icone": "🎓", "ordem": 1, "ativo": True},
        {"id": 2, "nome": "Informática & Tech", "icone": "💻", "ordem": 2, "ativo": True},
        {"id": 3, "nome": "Eletrônicos & Smart", "icone": "⌚", "ordem": 3, "ativo": True},
        {"id": 4, "nome": "Casa & Utilidades", "icone": "🏠", "ordem": 4, "ativo": True},
        {"id": 5, "nome": "Moda & Variedades", "icone": "🛍️", "ordem": 5, "ativo": True},
    ]
if "categorias_fallback" not in st.session_state:
    st.session_state["categorias_fallback"] = [
        {"id": 1, "departamento_id": 1, "nome": "Cursos Profissionalizantes", "ativo": True},
        {"id": 2, "departamento_id": 1, "nome": "Mentorias & Consultorias", "ativo": True},
        {"id": 3, "departamento_id": 1, "nome": "E-books & Apostilas", "ativo": True},
        {"id": 4, "departamento_id": 2, "nome": "Periféricos & Gamer", "ativo": True},
        {"id": 5, "departamento_id": 2, "nome": "Hardware & Peças", "ativo": True},
        {"id": 6, "departamento_id": 2, "nome": "Redes & Acessórios", "ativo": True},
        {"id": 7, "departamento_id": 3, "nome": "Áudio & Fones Bluetooth", "ativo": True},
        {"id": 8, "departamento_id": 3, "nome": "Smartwatches & Relógios", "ativo": True},
        {"id": 9, "departamento_id": 4, "nome": "Casa Inteligente & LED", "ativo": True},
        {"id": 10, "departamento_id": 4, "nome": "Ferramentas & Bricolagem", "ativo": True},
        {"id": 11, "departamento_id": 5, "nome": "Achadinhos & Ofertas", "ativo": True},
    ]
if "subcategorias_fallback" not in st.session_state:
    st.session_state["subcategorias_fallback"] = [
        {"id": 1, "categoria_id": 1, "nome": "Informática Básica & Office", "ncm_padrao": "8523.49.90", "ativo": True},
        {"id": 2, "categoria_id": 1, "nome": "Programação & Dados", "ncm_padrao": "8523.49.90", "ativo": True},
        {"id": 3, "categoria_id": 2, "nome": "Mentoria Individual VIP", "ncm_padrao": "8523.49.90", "ativo": True},
        {"id": 4, "categoria_id": 4, "nome": "Teclados Mecânicos & Office", "ncm_padrao": "8471.60.52", "ativo": True},
        {"id": 5, "categoria_id": 4, "nome": "Mouses Sem Fio & Gamer", "ncm_padrao": "8471.60.53", "ativo": True},
        {"id": 6, "categoria_id": 5, "nome": "SSD & Armazenamento", "ncm_padrao": "8471.70.40", "ativo": True},
        {"id": 7, "categoria_id": 7, "nome": "Fones TWS & Headsets", "ncm_padrao": "8518.30.00", "ativo": True},
        {"id": 8, "categoria_id": 8, "nome": "Relógios Inteligentes", "ncm_padrao": "8517.62.72", "ativo": True},
        {"id": 9, "categoria_id": 9, "nome": "Automação & Lâmpadas", "ncm_padrao": "8539.52.00", "ativo": True},
        {"id": 10, "categoria_id": 11, "nome": "Produtos Afiliados em Alta", "ncm_padrao": "8471.60.52", "ativo": True},
    ]
if "vinculos_produtos_local" not in st.session_state:
    st.session_state["vinculos_produtos_local"] = {}


def carregar_hierarquia_catalogo():
    """Carrega Departamentos, Categorias e Subcategorias do Supabase com fallback automático."""
    banco_ok = False
    try:
        r_dep = supabase.table("departamentos").select("*").order("ordem").order("id").execute()
        r_cat = supabase.table("categorias").select("*").order("id").execute()
        r_sub = supabase.table("subcategorias").select("*").order("id").execute()
        deps = r_dep.data or []
        cats = r_cat.data or []
        subs = r_sub.data or []
        banco_ok = True
        if not deps:
            deps = st.session_state["departamentos_fallback"]
            cats = st.session_state["categorias_fallback"]
            subs = st.session_state["subcategorias_fallback"]
    except Exception:
        deps = st.session_state["departamentos_fallback"]
        cats = st.session_state["categorias_fallback"]
        subs = st.session_state["subcategorias_fallback"]

    deps_map = {d["id"]: d for d in deps}
    cats_map = {c["id"]: c for c in cats}
    subs_map = {s["id"]: s for s in subs}
    return deps, cats, subs, deps_map, cats_map, subs_map, banco_ok


def obter_trilha_produto(prod: dict, deps_map: dict, cats_map: dict, subs_map: dict):
    """Resolve (departamento_id, categoria_id, subcategoria_id, texto_trilha) de qualquer produto."""
    pid = prod.get("id")
    vinc_local = st.session_state.get("vinculos_produtos_local", {}).get(pid, {})

    dep_id = prod.get("departamento_id") or vinc_local.get("departamento_id")
    cat_id = prod.get("categoria_id") or vinc_local.get("categoria_id")
    sub_id = prod.get("subcategoria_id") or vinc_local.get("subcategoria_id")

    # Inferência inteligente para produtos antigos caso ainda não tenham FK gravada
    if not dep_id and deps_map:
        tit_low = (prod.get("titulo") or "").lower()
        cat_txt = (prod.get("categoria") or "").lower()
        # Buscar pelos nomes padrão
        dep_por_nome = {d["nome"]: d["id"] for d in deps_map.values()}
        cat_por_nome = {c["nome"]: c["id"] for c in cats_map.values()}
        sub_por_nome = {s["nome"]: s["id"] for s in subs_map.values()}

        if "mentoria" in tit_low or cat_txt == "mentoria":
            dep_id = dep_por_nome.get("Educação & Cursos")
            cat_id = cat_por_nome.get("Mentorias & Consultorias")
            sub_id = sub_por_nome.get("Mentoria Individual VIP")
        elif "curso" in tit_low or cat_txt == "curso":
            dep_id = dep_por_nome.get("Educação & Cursos")
            cat_id = cat_por_nome.get("Cursos Profissionalizantes")
            sub_id = sub_por_nome.get("Informática Básica & Office")
        elif "fone" in tit_low or "headset" in tit_low:
            dep_id = dep_por_nome.get("Eletrônicos & Smart")
            cat_id = cat_por_nome.get("Áudio & Fones Bluetooth")
            sub_id = sub_por_nome.get("Fones TWS & Headsets")
        elif "mouse" in tit_low:
            dep_id = dep_por_nome.get("Informática & Tech")
            cat_id = cat_por_nome.get("Periféricos & Gamer")
            sub_id = sub_por_nome.get("Mouses Sem Fio & Gamer")
        else:
            dep_id = dep_por_nome.get("Informática & Tech")
            cat_id = cat_por_nome.get("Periféricos & Gamer")
            sub_id = sub_por_nome.get("Teclados Mecânicos & Office")

    dep_obj = deps_map.get(dep_id)
    cat_obj = cats_map.get(cat_id)
    sub_obj = subs_map.get(sub_id)

    partes = []
    if dep_obj:
        partes.append(f"{dep_obj.get('icone', '📦')} {dep_obj.get('nome')}")
    if cat_obj:
        partes.append(cat_obj.get("nome"))
    if sub_obj:
        partes.append(sub_obj.get("nome"))

    trilha_str = " › ".join(partes) if partes else "📦 Geral"
    return dep_id, cat_id, sub_id, trilha_str


# =====================================================================
# PERSISTÊNCIA DE SESSÃO POR NAVEGADOR (SID), CARRINHO E CONFIG_LOJA SUPABASE
# =====================================================================
ARQUIVO_SESSOES = ".sessoes_persistentes.json"


def obter_assinatura_dispositivo() -> str:
    """
    Gera uma assinatura curta exclusiva do navegador/aparelho atual (User-Agent).
    Assim, mesmo que alguém copie e envie o link com `?sid=...` do PC para um Celular,
    o Celular terá uma assinatura diferente e jamais entrará logado na conta do PC!
    """
    try:
        headers = st.context.headers or {}
        ua = str(headers.get("User-Agent") or headers.get("user-agent") or "unknown")
        sec_ch = str(headers.get("Sec-Ch-Ua-Platform") or headers.get("sec-ch-ua-platform") or "")
        sec_mob = str(headers.get("Sec-Ch-Ua-Mobile") or headers.get("sec-ch-ua-mobile") or "")
        raw_fp = f"{ua}|{sec_ch}|{sec_mob}"
        return hashlib.sha256(raw_fp.encode("utf-8")).hexdigest()[:8]
    except Exception:
        return "dev00000"


def obter_sid_navegador() -> str:
    """
    Garante um identificador de sessão individual e exclusivo por navegador + aparelho (`?sid=s_<fp>_<random>`).
    - Se você atualizar a página (F5) no mesmo aparelho, mantém o mesmo `sid` e continua logado na mesma tela.
    - Se você abrir o mesmo link em outro aparelho (ex: celular vs PC), a assinatura `_<fp>_` não bate e gera
      automaticamente um `sid` novo e deslogado!
    """
    fp_atual = obter_assinatura_dispositivo()
    prefixo_esperado = f"s_{fp_atual}_"

    sid_url = st.query_params.get("sid")
    if isinstance(sid_url, list):
        sid_url = sid_url[0] if sid_url else None

    # Só aceita o SID da URL se pertencer exatamente ao mesmo tipo de aparelho/navegador (prefixo_esperado)
    if sid_url and isinstance(sid_url, str) and sid_url.strip().startswith(prefixo_esperado):
        sid_limpo = sid_url.strip()
        st.session_state["_sid_navegador"] = sid_limpo
        return sid_limpo

    sid_mem = st.session_state.get("_sid_navegador")
    if sid_mem and isinstance(sid_mem, str) and sid_mem.startswith(prefixo_esperado):
        sid_limpo = sid_mem
    else:
        sid_limpo = f"{prefixo_esperado}{uuid.uuid4().hex[:10]}"
        st.session_state["_sid_navegador"] = sid_limpo

    try:
        st.query_params["sid"] = sid_limpo
    except Exception:
        pass
    return sid_limpo


def carregar_estado_persistente() -> dict:
    try:
        with open(ARQUIVO_SESSOES, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
    except Exception:
        return {}


def salvar_config_loja_supabase(cfg_dict: dict = None):
    """Salva o layout (Cabeçalho, Banner e Rodapé) na tabela public.config_loja do Supabase e no disco."""
    cfg_salvar = cfg_dict or st.session_state.get("config_loja", dict(CONFIG_LOJA_PADRAO))
    try:
        res_ck = supabase.table("config_loja").select("id").eq("chave", "principal").limit(1).execute()
        if res_ck.data:
            supabase.table("config_loja").update({
                "dados": cfg_salvar,
                "updated_at": datetime.now().isoformat(),
            }).eq("chave", "principal").execute()
        else:
            supabase.table("config_loja").insert({
                "chave": "principal",
                "dados": cfg_salvar,
            }).execute()
    except Exception:
        pass
    salvar_estado_persistente()


def salvar_estado_persistente():
    dados_atuais = carregar_estado_persistente()
    sid_atual = obter_sid_navegador()
    if st.query_params.get("sid") != sid_atual:
        try:
            st.query_params["sid"] = sid_atual
        except Exception:
            pass
    mapa_sids = dados_atuais.get("sessoes_por_sid")
    if not isinstance(mapa_sids, dict):
        mapa_sids = {}
    mapa_sids.pop("padrao_local", None)

    pacote_sessao_sid = {
        "cliente_logado": st.session_state.get("cliente_logado"),
        "carrinho_cliente": st.session_state.get("carrinho_cliente", []),
        "aba_loja_cliente": st.session_state.get("aba_loja_cliente", "vitrine"),
        "admin_logado": bool(st.session_state.get("admin_logado", False)),
        "auth_user": st.session_state.get("auth_user"),
        "menu_admin_nav": st.session_state.get("menu_admin_nav", "🏠 Início"),
        "sub_aba_cli": st.session_state.get("sub_aba_cli", "📋 Lista de clientes"),
        "sub_aba_cup": st.session_state.get("sub_aba_cup", "➕ Novo cupom"),
        "updated_at": datetime.now().isoformat(),
    }
    mapa_sids[sid_atual] = pacote_sessao_sid

    # Limpar chaves globais legadas para nunca vazar sessão entre dispositivos diferentes
    dados_atuais.pop("cliente_logado", None)
    dados_atuais.pop("carrinho_cliente", None)
    dados_atuais.pop("admin_logado", None)
    dados_atuais.pop("auth_user", None)

    dados_atuais.update({
        "sessoes_por_sid": mapa_sids,
        "contas_clientes_local": st.session_state.get("contas_clientes_local", {}),
        "chamados_suporte_local": st.session_state.get("chamados_suporte_local", []),
        "rastreios_pedidos_local": st.session_state.get("rastreios_pedidos_local", {}),
        "midia_produtos_local": st.session_state.get("midia_produtos_local", {}),
        "avaliacoes_produtos_local": st.session_state.get("avaliacoes_produtos_local", []),
        "config_loja": st.session_state.get("config_loja", dict(CONFIG_LOJA_PADRAO)),
    })
    try:
        with open(ARQUIVO_SESSOES, "w", encoding="utf-8") as f:
            json.dump(dados_atuais, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    # Persistir sessão individual também no Supabase (chave sessao_<sid>) para sobreviver no Streamlit Cloud
    try:
        chave_sup = f"sessao_{sid_atual}"
        res_s = supabase.table("config_loja").select("id").eq("chave", chave_sup).limit(1).execute()
        if res_s.data:
            supabase.table("config_loja").update({
                "dados": pacote_sessao_sid,
                "updated_at": datetime.now().isoformat(),
            }).eq("chave", chave_sup).execute()
        else:
            supabase.table("config_loja").insert({
                "chave": chave_sup,
                "dados": pacote_sessao_sid,
            }).execute()
    except Exception:
        pass


def hidratar_sessao_inicial():
    if not st.session_state.get("_sessao_hidratada"):
        persistido = carregar_estado_persistente()
        sid_atual = obter_sid_navegador()
        mapa_sids = persistido.get("sessoes_por_sid") if isinstance(persistido.get("sessoes_por_sid"), dict) else {}
        sessao_sid = mapa_sids.get(sid_atual)

        # Caso não encontre no disco local (ex: Streamlit Cloud após reboot), busca no Supabase pelo SID único
        if not isinstance(sessao_sid, dict):
            try:
                r_sup_sid = supabase.table("config_loja").select("dados").eq("chave", f"sessao_{sid_atual}").limit(1).execute()
                if r_sup_sid.data and isinstance(r_sup_sid.data[0].get("dados"), dict):
                    sessao_sid = r_sup_sid.data[0]["dados"]
            except Exception:
                pass

        if isinstance(sessao_sid, dict):
            st.session_state["cliente_logado"] = sessao_sid.get("cliente_logado")
            st.session_state["carrinho_cliente"] = sessao_sid.get("carrinho_cliente", [])
            st.session_state["aba_loja_cliente"] = sessao_sid.get("aba_loja_cliente", "vitrine")
            st.session_state["admin_logado"] = bool(sessao_sid.get("admin_logado", False))
            st.session_state["auth_user"] = sessao_sid.get("auth_user")
            st.session_state["menu_admin_nav"] = sessao_sid.get("menu_admin_nav", "🏠 Início")
            if sessao_sid.get("sub_aba_cli"):
                st.session_state["sub_aba_cli"] = sessao_sid.get("sub_aba_cli")
            if sessao_sid.get("sub_aba_cup"):
                st.session_state["sub_aba_cup"] = sessao_sid.get("sub_aba_cup")
        else:
            st.session_state["cliente_logado"] = None
            st.session_state["carrinho_cliente"] = []
            st.session_state["aba_loja_cliente"] = "vitrine"
            st.session_state["admin_logado"] = False
            st.session_state["auth_user"] = None
            st.session_state["menu_admin_nav"] = "🏠 Início"

        # Criptografar senhas legadas em texto puro nas contas locais
        contas_loc = persistido.get("contas_clientes_local", {})
        if isinstance(contas_loc, dict):
            for _k_c, _v_c in contas_loc.items():
                if isinstance(_v_c, dict) and _v_c.get("senha") and not str(_v_c["senha"]).startswith("sha256$"):
                    _v_c["senha"] = gerar_hash_senha(str(_v_c["senha"]))
        st.session_state["contas_clientes_local"] = contas_loc
        st.session_state["chamados_suporte_local"] = persistido.get("chamados_suporte_local", [])
        st.session_state["rastreios_pedidos_local"] = persistido.get("rastreios_pedidos_local", {})
        st.session_state["midia_produtos_local"] = persistido.get("midia_produtos_local", {})
        st.session_state["avaliacoes_produtos_local"] = persistido.get("avaliacoes_produtos_local", [])

        cfg_mesclada = dict(CONFIG_LOJA_PADRAO)
        if isinstance(persistido.get("config_loja"), dict):
            cfg_mesclada.update(persistido["config_loja"])
        # Tentar carregar config_loja direto do Supabase (tabela public.config_loja)
        try:
            res_cfg_db = supabase.table("config_loja").select("dados").eq("chave", "principal").limit(1).execute()
            if res_cfg_db.data and isinstance(res_cfg_db.data[0].get("dados"), dict):
                cfg_mesclada.update(res_cfg_db.data[0]["dados"])
        except Exception:
            pass
        st.session_state["config_loja"] = cfg_mesclada
        st.session_state["_sessao_hidratada"] = True


hidratar_sessao_inicial()


def parsear_texto_ficha_tecnica(texto: str) -> list:
    """Converte linhas 'Característica: Valor' em lista de dicts [{'nome': ..., 'valor': ...}]."""
    resultado = []
    for linha in (texto or "").splitlines():
        linha_s = linha.strip()
        if not linha_s:
            continue
        if ":" in linha_s:
            partes = linha_s.split(":", 1)
            resultado.append({"nome": partes[0].strip(), "valor": partes[1].strip()})
        else:
            resultado.append({"nome": "Especificação", "valor": linha_s})
    return resultado


def formatar_ficha_tecnica_texto(ficha: list) -> str:
    """Converte lista de dicts [{'nome': ..., 'valor': ...}] em linhas 'Característica: Valor' para edição."""
    if not ficha or not isinstance(ficha, list):
        return ""
    linhas = []
    for item in ficha:
        if isinstance(item, dict):
            linhas.append(f"{item.get('nome', 'Item')}: {item.get('valor', '')}")
        elif isinstance(item, str):
            linhas.append(item)
    return "\n".join(linhas)


def obter_midia_ficha_produto(prod: dict):
    """
    Retorna (galeria_completa, lista_extras, video_url, lista_ficha_tecnica) do produto,
    combinando dados do Supabase com fallback persistente local.
    """
    pid_str = str(prod.get("id", ""))
    local_info = st.session_state.get("midia_produtos_local", {}).get(pid_str, {})

    img_capa = prod.get("imagem_url") or "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600"

    gal_raw = prod.get("galeria_imagens")
    if isinstance(gal_raw, str):
        try:
            gal_raw = json.loads(gal_raw)
        except Exception:
            gal_raw = []
    if not isinstance(gal_raw, list) or not gal_raw:
        gal_raw = local_info.get("galeria_imagens", [])

    extras_limpas = [str(u).strip() for u in (gal_raw or []) if u and str(u).strip()]
    galeria_completa = [img_capa]
    for u_ex in extras_limpas:
        if u_ex not in galeria_completa:
            galeria_completa.append(u_ex)

    video_url = (prod.get("video_url") or local_info.get("video_url") or "").strip()

    ficha_raw = prod.get("ficha_tecnica")
    if isinstance(ficha_raw, str):
        try:
            ficha_raw = json.loads(ficha_raw)
        except Exception:
            ficha_raw = parsear_texto_ficha_tecnica(ficha_raw)
    if not isinstance(ficha_raw, list) or not ficha_raw:
        ficha_raw = local_info.get("ficha_tecnica", [])

    if not ficha_raw:
        tit_l = (prod.get("titulo") or "").lower()
        if "curso" in tit_l or prod.get("categoria") == "curso":
            ficha_raw = [
                {"nome": "Modalidade", "valor": "Presencial ou Online Ao Vivo / Gravado"},
                {"nome": "Certificado", "valor": "Incluso (Reconhecido em todo território nacional)"},
                {"nome": "Material Didático", "valor": "Apostilas digitais e exercícios práticos"},
                {"nome": "Suporte ao Aluno", "valor": "Tira-dúvidas direto via WhatsApp"},
            ]
        elif "mentoria" in tit_l or prod.get("categoria") == "mentoria":
            ficha_raw = [
                {"nome": "Formato", "valor": "Sessões Individuais VIP 1-a-1"},
                {"nome": "Acompanhamento", "valor": "Plano personalizado de carreira e tecnologia"},
                {"nome": "Suporte Direto", "valor": "Acesso prioritário via WhatsApp"},
            ]
        else:
            ficha_raw = [
                {"nome": "Condição do Item", "valor": "Novo e Lacrado"},
                {"nome": "Garantia", "valor": "Garantia Oficial com Nota / Declaração Fiscal"},
                {"nome": "Código Fiscal NCM", "valor": prod.get("ncm", "8471.60.52")},
                {"nome": "Envio", "valor": "Despacho rápido com Código de Rastreio"},
            ]

    return galeria_completa, extras_limpas, video_url, ficha_raw


def renderizar_player_video_produto(video_url: str):
    """Renderiza player de vídeo do YouTube, Shorts, Vimeo ou MP4 direto na página do produto."""
    url_v = (video_url or "").strip()
    if not url_v:
        return
    yt_id = None
    m_yt = re.search(r"(?:v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})", url_v)
    if m_yt:
        yt_id = m_yt.group(1)

    if yt_id:
        embed_url = f"https://www.youtube.com/embed/{yt_id}?rel=0"
        st.markdown(
            f"""
            <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; border:1px solid #334155; background:#000; margin-bottom:10px;">
                <iframe src="{embed_url}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif "vimeo.com/" in url_v:
        m_vm = re.search(r"vimeo\.com/(\d+)", url_v)
        if m_vm:
            vm_id = m_vm.group(1)
            st.markdown(
                f"""
                <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; border:1px solid #334155; background:#000; margin-bottom:10px;">
                    <iframe src="https://player.vimeo.com/video/{vm_id}" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allowfullscreen></iframe>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.video(url_v)
    else:
        try:
            st.video(url_v)
        except Exception:
            st.link_button("🎬 Assistir Vídeo Demonstrativo Externo ↗", url_v, width="stretch")


def carregar_mapa_avaliacoes_todos_produtos() -> dict:
    """
    Carrega todas as avaliações em uma ÚNICA consulta ao Supabase (eliminando o problema de N+1 queries na vitrine).
    Retorna dict {str(produto_id): (lista_avaliacoes, media_nota, qtd_total)}.
    """
    todas_db = []
    try:
        r_all = supabase.table("avaliacoes_produtos").select("*").order("id", desc=True).execute()
        todas_db = r_all.data or []
    except Exception:
        todas_db = []

    ids_db = {str(a.get("id")) for a in todas_db}
    for a_loc in reversed(st.session_state.get("avaliacoes_produtos_local", [])):
        if str(a_loc.get("id")) not in ids_db:
            todas_db.append(a_loc)

    agrupado = {}
    for a in todas_db:
        pid_k = str(a.get("produto_id"))
        agrupado.setdefault(pid_k, []).append(a)

    mapa_final = {}
    for pid_k, lista_a in agrupado.items():
        soma = sum(int(x.get("nota", 5)) for x in lista_a)
        media = round(soma / len(lista_a), 1)
        mapa_final[pid_k] = (lista_a, media, len(lista_a))
    return mapa_final


def carregar_avaliacoes_do_produto(produto_id: int, mapa_precarregado: dict = None):
    """Retorna (lista_avaliacoes, media_nota, qtd_total) de um produto específico (usando mapa em lote se disponível)."""
    if isinstance(mapa_precarregado, dict):
        return mapa_precarregado.get(str(produto_id), ([], 5.0, 0))

    aval_db = []
    try:
        r_av = supabase.table("avaliacoes_produtos").select("*").eq("produto_id", produto_id).order("id", desc=True).execute()
        aval_db = r_av.data or []
    except Exception:
        aval_db = []

    ids_db = {str(a.get("id")) for a in aval_db}
    for a_loc in reversed(st.session_state.get("avaliacoes_produtos_local", [])):
        if str(a_loc.get("produto_id")) == str(produto_id) and str(a_loc.get("id")) not in ids_db:
            aval_db.append(a_loc)

    if not aval_db:
        return [], 5.0, 0

    soma = sum(int(a.get("nota", 5)) for a in aval_db)
    media = round(soma / len(aval_db), 1)
    return aval_db, media, len(aval_db)


def sincronizar_carrinho_cliente():
    """Salva o carrinho atual tanto no disco (para não perder no F5) quanto na conta do cliente no Supabase."""
    carrinho_atual = st.session_state.get("carrinho_cliente", [])
    cli = st.session_state.get("cliente_logado")
    if cli:
        cli["carrinho"] = carrinho_atual
        chave_conta = (cli.get("email") or cli.get("cpf_cnpj") or "").strip().lower()
        if chave_conta:
            st.session_state.setdefault("contas_clientes_local", {})[chave_conta] = cli
        if cli.get("id"):
            try:
                supabase.table("clientes").update({"carrinho": carrinho_atual}).eq("id", cli["id"]).execute()
            except Exception:
                pass
    salvar_estado_persistente()


def obter_rastreio_pedido(ped: dict) -> str:
    """Retorna o código de rastreio salvo na coluna codigo_rastreio, no JSON de itens ou na memória persistente."""
    if not ped:
        return ""
    cod = ped.get("codigo_rastreio")
    if cod:
        return str(cod).strip()
    pid_str = str(ped.get("id", ""))
    cod_local = st.session_state.get("rastreios_pedidos_local", {}).get(pid_str)
    if cod_local:
        return str(cod_local).strip()
    itens = ped.get("itens") or []
    if itens and isinstance(itens, list) and isinstance(itens[0], dict):
        cod_it = itens[0].get("rastreio")
        if cod_it:
            return str(cod_it).strip()
    return ""


def devolver_estoque_se_cancelado(ped: dict, novo_status: str) -> bool:
    """
    Se o pedido mudou para 'cancelado' e ainda não teve o estoque devolvido,
    restaura automaticamente a quantidade dos produtos de estoque_proprio no Supabase.
    """
    status_anterior = (ped.get("status_pagamento") or "pendente").lower()
    itens_atuais = list(ped.get("itens") or [])
    ja_devolvido = bool(ped.get("estoque_devolvido", False))
    if not ja_devolvido and itens_atuais and isinstance(itens_atuais[0], dict):
        ja_devolvido = bool(itens_atuais[0].get("estoque_devolvido", False))

    if (novo_status or "").lower() == "cancelado" and status_anterior != "cancelado" and not ja_devolvido:
        for it in itens_atuais:
            if isinstance(it, dict) and it.get("id") and it.get("tipo_venda") == "estoque_proprio":
                qtd_dev = int(it.get("qtd", 1))
                try:
                    r_pr = supabase.table("produtos").select("estoque").eq("id", it["id"]).limit(1).execute()
                    if r_pr.data:
                        est_atual = int(r_pr.data[0].get("estoque") or 0)
                        supabase.table("produtos").update({"estoque": est_atual + qtd_dev}).eq("id", it["id"]).execute()
                except Exception:
                    pass
        return True
    return ja_devolvido


def salvar_rastreio_no_pedido(ped: dict, novo_rastreio: str, novo_status: str = None):
    """Salva o código de rastreio, devolve estoque se cancelado e atualiza status no Supabase."""
    pid = ped.get("id")
    rastreio_limpo = (novo_rastreio or "").strip().upper()
    st.session_state.setdefault("rastreios_pedidos_local", {})[str(pid)] = rastreio_limpo
    salvar_estado_persistente()

    foi_devolvido = devolver_estoque_se_cancelado(ped, novo_status) if novo_status else bool(ped.get("estoque_devolvido", False))

    itens_atuais = list(ped.get("itens") or [])
    if itens_atuais and isinstance(itens_atuais[0], dict):
        itens_atuais[0]["rastreio"] = rastreio_limpo
        if foi_devolvido:
            itens_atuais[0]["estoque_devolvido"] = True

    payload_up = {"itens": itens_atuais}
    if novo_status:
        payload_up["status_pagamento"] = novo_status

    try:
        payload_com_col = dict(payload_up)
        payload_com_col["codigo_rastreio"] = rastreio_limpo or None
        payload_com_col["estoque_devolvido"] = foi_devolvido
        supabase.table("pedidos").update(payload_com_col).eq("id", pid).execute()
    except Exception:
        supabase.table("pedidos").update(payload_up).eq("id", pid).execute()


# Detecta se é a página administrativa
query_params = st.query_params
modo_admin_ativo = "admin" in query_params

# =====================================================================
# ROTA 1: PAINEL DE ADMINISTRAÇÃO NUVEMSHOP (?admin=1)
# =====================================================================
if modo_admin_ativo:
    if "admin_logado" not in st.session_state:
        st.session_state["admin_logado"] = False
    if "auth_user" not in st.session_state:
        st.session_state["auth_user"] = None

    if not st.session_state["admin_logado"]:
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(
                """
                <div style="text-align:center; margin-top:40px; margin-bottom:20px;">
                    <div style="width:52px; height:52px; border-radius:14px; background:linear-gradient(135deg, #3B82F6, #1D4ED8); color:white; font-size:1.8rem; font-weight:800; display:inline-flex; align-items:center; justify-content:center; margin-bottom:12px; box-shadow:0 8px 20px rgba(37,99,235,0.35);">T</div>
                    <h2 style="color:#0F172A; font-weight:800; margin:0;">TagsInfor Gestão</h2>
                    <p style="color:#64748B; font-size:0.95rem; margin-top:4px;">Autenticação Oficial via Supabase</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.container(border=True):
                tab_login, tab_cad, tab_emerg = st.tabs(["🔑 Entrar com Supabase", "✨ Criar Conta Admin", "🔐 Senha Mestre"])

                with tab_login:
                    with st.form("form_login_supabase"):
                        email_sup = st.text_input("E-mail do Administrador", placeholder="admin@tagsinfor.com")
                        senha_sup = st.text_input("Senha", type="password", placeholder="••••••••")
                        btn_entrar = st.form_submit_button("Entrar no Painel", type="primary", use_container_width=True)
                        if btn_entrar:
                            if not email_sup or not senha_sup:
                                st.error("Preencha o e-mail e a senha.")
                            else:
                                try:
                                    res_auth = supabase.auth.sign_in_with_password({
                                        "email": email_sup.strip(),
                                        "password": senha_sup,
                                    })
                                    if res_auth and res_auth.user:
                                        st.session_state["admin_logado"] = True
                                        st.session_state["auth_user"] = {
                                            "id": res_auth.user.id,
                                            "email": res_auth.user.email,
                                            "nome": res_auth.user.user_metadata.get("nome", res_auth.user.email.split("@")[0].title()),
                                        }
                                        salvar_estado_persistente()
                                        st.success("✅ Autenticado com sucesso via Supabase!")
                                        st.rerun()
                                    else:
                                        st.error("Credenciais inválidas.")
                                except Exception as e_auth:
                                    st.error(f"Erro de autenticação no Supabase: {e_auth}")

                with tab_cad:
                    with st.form("form_signup_supabase"):
                        st.caption("Cadastre seu e-mail como administrador direto no Supabase Auth:")
                        nome_cad = st.text_input("Seu Nome Completo", placeholder="Ex: Gestor TagsInfor")
                        email_cad = st.text_input("E-mail para Cadastro", placeholder="admin@tagsinfor.com")
                        senha_cad = st.text_input("Definir Senha (mínimo 6 dígitos)", type="password")
                        btn_cad = st.form_submit_button("Cadastrar no Supabase", type="primary", use_container_width=True)
                        if btn_cad:
                            if not email_cad or not senha_cad:
                                st.error("Preencha todos os campos.")
                            elif len(senha_cad) < 6:
                                st.error("A senha deve ter pelo menos 6 caracteres.")
                            else:
                                try:
                                    res_cad = supabase.auth.sign_up({
                                        "email": email_cad.strip(),
                                        "password": senha_cad,
                                        "options": {"data": {"nome": nome_cad, "role": "admin"}},
                                    })
                                    if res_cad and res_cad.user:
                                        st.success("🎉 Conta criada com sucesso no Supabase! Agora vá na aba 'Entrar com Supabase' para logar.")
                                    else:
                                        st.info("Cadastro enviado para processamento.")
                                except Exception as e_cad:
                                    st.error(f"Erro ao criar conta no Supabase: {e_cad}")

                with tab_emerg:
                    with st.form("form_login_emergencia"):
                        st.caption("Acesso direto com a Senha Mestre de Emergência da Loja:")
                        senha_em = st.text_input("Senha Mestre:", type="password")
                        btn_em = st.form_submit_button("Entrar via Senha Mestre", use_container_width=True)
                        if btn_em:
                            if senha_em == SENHA_ADMIN:
                                st.session_state["admin_logado"] = True
                                st.session_state["auth_user"] = {
                                    "id": "admin_local",
                                    "email": "admin@tagsinfor.com.br",
                                    "nome": "Administrador Tags",
                                }
                                salvar_estado_persistente()
                                st.success("Acesso liberado!")
                                st.rerun()
                            else:
                                st.error("Senha mestre incorreta.")

            if st.button("← Voltar à Loja Online", use_container_width=True):
                sid_nav_keep = obter_sid_navegador()
                st.query_params.clear()
                st.query_params["sid"] = sid_nav_keep
                st.rerun()
        st.stop()

    # Callback instantâneo para navegação em 1 clique sem atraso de sessão
    def ir_para_aba_admin(destino: str):
        st.session_state["menu_admin_nav"] = destino
        salvar_estado_persistente()

    def ir_para_sub_aba(chave: str, valor: str):
        st.session_state[chave] = valor
        salvar_estado_persistente()

    opcoes_admin_nav = [
        "🏠 Início",
        "📦 Lista de produtos",
        "➕ Novo produto",
        "🗂️ Categorias & Nichos",
        "🛒 Vendas & Pedidos",
        "👥 Clientes",
        "🎨 Loja online (Layout)",
        "📄 Documentos fiscais (NF-e)",
        "🏢 Centro de distribuição",
        "🎟️ Criar cupom",
        "💳 Pagamento Pix",
    ]
    if "menu_admin_nav" not in st.session_state or st.session_state["menu_admin_nav"] not in opcoes_admin_nav:
        st.session_state["menu_admin_nav"] = "🏠 Início"

    # Layout Principal com Menu Lateral Estilo Figma (Imagem 2 - Botões Reais)
    col_nav, col_main = st.columns([1.3, 4.7])

    with col_nav:
        with st.container(border=True):
            # Header do Menu (Figma)
            st.markdown(
                """
                <div class="figma-sidebar-header">
                    <div class="figma-brand-icon">T</div>
                    <div>
                        <div class="figma-brand-title">TagsInfor</div>
                        <div class="figma-brand-badge">Painel Multi-Nicho</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Grupo 1: Gestão Principal
            st.markdown('<div class="figma-nav-section-label">PRINCIPAL</div>', unsafe_allow_html=True)
            menu_grupo_1 = [
                ("🏠 Início", "Início", ":material/dashboard:"),
                ("📦 Lista de produtos", "Produtos", ":material/inventory_2:"),
                ("➕ Novo produto", "Novo produto", ":material/add_box:"),
                ("🗂️ Categorias & Nichos", "Categorias & Nichos", ":material/category:"),
                ("🛒 Vendas & Pedidos", "Pedidos", ":material/shopping_bag:"),
                ("👥 Clientes", "Clientes", ":material/group:"),
                ("🎨 Loja online (Layout)", "Loja online", ":material/storefront:"),
            ]
            for idx_m, (aba_id, rotulo_curto, icone_mat) in enumerate(menu_grupo_1):
                ativo = (st.session_state["menu_admin_nav"] == aba_id)
                st.button(
                    rotulo_curto,
                    key=f"nav_item_g1_{idx_m}",
                    icon=icone_mat,
                    type="primary" if ativo else "tertiary",
                    use_container_width=True,
                    on_click=ir_para_aba_admin,
                    args=(aba_id,),
                )

            # Grupo 2: Fiscal, Marketing & Configurações
            st.markdown('<div class="figma-nav-section-label" style="margin-top:16px;">GESTÃO & FISCAL</div>', unsafe_allow_html=True)
            menu_grupo_2 = [
                ("📄 Documentos fiscais (NF-e)", "Notas fiscais", ":material/receipt_long:"),
                ("🏢 Centro de distribuição", "Centro distribuição", ":material/local_shipping:"),
                ("🎟️ Criar cupom", "Cupons", ":material/sell:"),
                ("💳 Pagamento Pix", "Pagamento Pix", ":material/qr_code_2:"),
            ]
            for idx_m2, (aba_id, rotulo_curto, icone_mat) in enumerate(menu_grupo_2):
                ativo = (st.session_state["menu_admin_nav"] == aba_id)
                st.button(
                    rotulo_curto,
                    key=f"nav_item_g2_{idx_m2}",
                    icon=icone_mat,
                    type="primary" if ativo else "tertiary",
                    use_container_width=True,
                    on_click=ir_para_aba_admin,
                    args=(aba_id,),
                )

            aba_admin = st.session_state["menu_admin_nav"]

            st.divider()

            # Atalho da Loja
            if st.button("Ver Loja Online ↗", icon=":material/open_in_new:", use_container_width=True):
                sid_nav_keep = obter_sid_navegador()
                st.query_params.clear()
                st.query_params["sid"] = sid_nav_keep
                st.rerun()

            # Bottom User Profile Card (Igual ao rodapé do Figma na Imagem 2)
            user_info = st.session_state.get("auth_user") or {
                "nome": "Admin Tags",
                "email": "admin@tagsinfor.com",
            }
            nome_u = user_info.get("nome", "Admin Tags")
            email_u = user_info.get("email", "admin@tagsinfor.com")
            inicial_u = (nome_u[0] if nome_u else "A").upper()

            st.markdown(
                f"""
                <div class="figma-user-profile">
                    <div class="figma-user-avatar">{inicial_u}</div>
                    <div class="figma-user-info">
                        <div class="figma-user-name">{nome_u}</div>
                        <div class="figma-user-role">● Supabase Auth</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("Sair do Painel", icon=":material/logout:", use_container_width=True):
                try:
                    supabase.auth.sign_out()
                except Exception:
                    pass
                st.session_state["admin_logado"] = False
                st.session_state["auth_user"] = None
                salvar_estado_persistente()
                sid_nav_keep = obter_sid_navegador()
                st.query_params.clear()
                st.query_params["sid"] = sid_nav_keep
                st.rerun()

    with col_main:
        cfg = st.session_state["config_loja"]

        # =================================================================
        # 1. ABA INÍCIO (CHECKLIST & PUBLICAR LOJA - IDÊNTICO AO SEU PRINT)
        # =================================================================
        if aba_admin == "🏠 Início":
            st.markdown('<h1 class="admin-page-title">Início</h1>', unsafe_allow_html=True)
            st.markdown("Confira os passos para deixar sua loja do seu jeito!")

            with st.container(border=True):
                # Passo 1: Validar conta (Já Concluído)
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; gap:14px; padding:10px 0;">
                        <span style="background:rgba(22, 163, 74, 0.2); color:#4ADE80; width:32px; height:32px; display:inline-flex; align-items:center; justify-content:center; border-radius:50%; font-weight:800; font-size:1.1rem;">✓</span>
                        <div>
                            <strong style="font-size:1.05rem; color:#F8FAFC;">Validar conta</strong><br>
                            <span style="color:#94A3B8; font-size:0.9rem;">Você já pode continuar trabalhando em sua loja.</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.divider()

                # Passo 2: Mostre seus produtos
                c_p1, c_p2 = st.columns([3.8, 1.4])
                with c_p1:
                    st.markdown(
                        """
                        <div style="display:flex; align-items:flex-start; gap:14px;">
                            <span style="background:rgba(59, 130, 246, 0.2); color:#60A5FA; width:32px; height:32px; display:inline-flex; align-items:center; justify-content:center; border-radius:8px; font-size:1.1rem;">🏷️</span>
                            <div>
                                <strong style="font-size:1.05rem; color:#F8FAFC;">Mostre seus produtos</strong><br>
                                <span style="color:#94A3B8; font-size:0.9rem;">Gere com IA, adicione um a um ou importe seu catálogo.</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c_p2:
                    st.button(
                        "Adicionar produto",
                        key="btn_step_add_prod",
                        type="primary",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("➕ Novo produto",),
                    )

                st.divider()

                # Passo 3: Personalize sua loja (Accordion Nuvemshop)
                with st.expander("🎨 Personalize sua loja", expanded=False):
                    st.write("Defina o banner principal, slogan promocional e o logotipo oficial da sua marca Tags Informática.")
                    st.button(
                        "Personalizar Layout da Loja",
                        key="btn_goto_layout",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("🎨 Loja online (Layout)",),
                    )

                st.divider()

                # Passo 4: Defina de onde saem seus pedidos
                with st.expander("📦 Defina de onde saem seus pedidos", expanded=False):
                    st.write("📍 **Origem do Envio:** Manaus - AM, Brasil.")
                    st.caption("Configurado para pronta entrega local e envio seguro de cursos e equipamentos para todo o Brasil.")
                    st.button(
                        "Configurar Centro de Distribuição",
                        key="btn_goto_cd",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("🏢 Centro de distribuição",),
                    )

                st.divider()

                # Passo 5: Revisar configurações do Nuvem Envio
                with st.expander("🚚 Revisar configurações do Nuvem Envio & Fiscal", expanded=False):
                    st.write("📦 **Formas de Envio:** Frete Grátis incluso para Cursos Online e Mentorias Digitais.")
                    st.caption("Para produtos físicos (mouses, teclados), o envio é despachado via Correios com Declaração de Conteúdo (DC-e) ou NF-e.")
                    st.button(
                        "Abrir Documentos Fiscais (NF-e / DC-e)",
                        key="btn_goto_nfe",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("📄 Documentos fiscais (NF-e)",),
                    )

                st.divider()

                # Passo 6: Revisar configurações do Nuvem Pago
                with st.expander("💳 Revisar configurações de Pagamento Pix", expanded=False):
                    st.write("⚡ **Pagamento Pix Direto BACEN:** Ativo com taxa zero e confirmação rápida.")
                    st.button(
                        "Revisar Chave Pix & Banco",
                        key="btn_goto_pix",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("💳 Pagamento Pix",),
                    )

            # Card inferior: Publicar Loja / Status da Loja
            with st.container(border=True):
                col_st1, col_st2, col_st3 = st.columns([3, 1, 1.3])
                with col_st1:
                    if cfg.get("em_construcao", False):
                        st.markdown(
                            """
                            <div style="display:flex; align-items:center; gap:16px;">
                                <div style="background:rgba(239, 68, 68, 0.2); border-radius:12px; width:52px; height:52px; display:flex; align-items:center; justify-content:center; font-size:1.6rem;">🔒</div>
                                <div>
                                    <strong style="font-size:1.15rem; color:#F8FAFC;">Sua loja está em construção</strong><br>
                                    <span style="color:#94A3B8; font-size:0.9rem;">Você já pode acessar <code>http://localhost:8501</code>. Seus clientes vão ver quando você publicar.</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            """
                            <div style="display:flex; align-items:center; gap:16px;">
                                <div style="background:rgba(34, 197, 94, 0.2); border-radius:12px; width:52px; height:52px; display:flex; align-items:center; justify-content:center; font-size:1.6rem;">🟢</div>
                                <div>
                                    <strong style="font-size:1.15rem; color:#F8FAFC;">Sua loja está publicada e online!</strong><br>
                                    <span style="color:#94A3B8; font-size:0.9rem;">Disponível publicamente em <code>http://localhost:8501</code> pronta para receber vendas no Pix.</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                with col_st2:
                    if st.button("👁️ Ver loja ↗", key="btn_ver_loja_bottom", use_container_width=True):
                        st.query_params.clear()
                        st.rerun()
                with col_st3:
                    if cfg.get("em_construcao", False):
                        if st.button("🚀 Publicar loja", key="btn_publicar_loja_bottom", type="primary", use_container_width=True):
                            st.session_state["config_loja"]["em_construcao"] = False
                            st.success("🎉 Loja publicada com sucesso! Clientes já podem comprar.")
                            st.rerun()
                    else:
                        if st.button("⏸️ Pausar loja", key="btn_pausar_loja_bottom", use_container_width=True):
                            st.session_state["config_loja"]["em_construcao"] = True
                            st.warning("Loja colocada em modo construção.")
                            st.rerun()

        # =================================================================
        # 2. ABA CATEGORIAS & NICHOS (DEPARTAMENTOS -> CATEGORIAS -> SUBCATEGORIAS)
        # =================================================================
        elif aba_admin == "🗂️ Categorias & Nichos":
            st.markdown('<h1 class="admin-page-title">Departamentos, Categorias e Subcategorias</h1>', unsafe_allow_html=True)
            st.markdown("Estruture sua loja para múltiplos nichos de mercado com liberdade ilimitada.")

            deps, cats, subs, deps_map, cats_map, subs_map, banco_ok = carregar_hierarquia_catalogo()

            if not banco_ok:
                with st.expander("⚠️ Ativar tabelas de Categorias no Supabase (Clique para ver o SQL)", expanded=False):
                    st.info("Suas alterações já funcionam na sessão atual! Para gravar permanentemente as 3 novas tabelas (`departamentos`, `categorias`, `subcategorias`) no Supabase sem perder nenhum produto, execute o arquivo `supabase_migracao_categorias.sql` no SQL Editor do Supabase.")

            opcoes_sub_cat = ["🏛️ 1. Departamentos (Nichos)", "📂 2. Categorias", "🏷️ 3. Subcategorias"]
            if "sub_aba_cat_tree" not in st.session_state or st.session_state["sub_aba_cat_tree"] not in opcoes_sub_cat:
                st.session_state["sub_aba_cat_tree"] = "🏛️ 1. Departamentos (Nichos)"

            c_tb1, c_tb2, c_tb3 = st.columns(3)
            for idx_tc, (col_tc, op_tc) in enumerate(zip([c_tb1, c_tb2, c_tb3], opcoes_sub_cat)):
                with col_tc:
                    st.button(
                        op_tc,
                        key=f"btn_sub_cat_tree_{idx_tc}",
                        type="primary" if st.session_state["sub_aba_cat_tree"] == op_tc else "secondary",
                        use_container_width=True,
                        on_click=ir_para_sub_aba,
                        args=("sub_aba_cat_tree", op_tc),
                    )

            aba_tree = st.session_state["sub_aba_cat_tree"]
            st.write("")

            # -------------------------------------------------------------
            # SUB-ABA 1: DEPARTAMENTOS (NICHOS)
            # -------------------------------------------------------------
            if aba_tree == "🏛️ 1. Departamentos (Nichos)":
                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">➕ Criar Novo Departamento (Nicho de Mercado)</div>', unsafe_allow_html=True)
                    with st.form("form_novo_departamento", clear_on_submit=True):
                        cd1, cd2, cd3, cd4 = st.columns([2.5, 1, 1, 1.2])
                        nome_dep_in = cd1.text_input("Nome do Departamento / Nicho *", placeholder="Ex: Games & Consoles, Perfumaria, Pet Shop, Ferramentas...")
                        icone_dep_in = cd2.selectbox("Ícone", ["📦", "🎓", "💻", "⌚", "🏠", "🛍️", "🎮", "📱", "👕", "💄", "🔧", "🐾", "📚", "🍔", "⚽", "🚗"])
                        ordem_dep_in = cd3.number_input("Ordem", min_value=1, value=len(deps) + 1, step=1)
                        with cd4:
                            st.write("")
                            st.write("")
                            btn_add_dep = st.form_submit_button("Criar Nicho", type="primary", use_container_width=True)

                        if btn_add_dep:
                            if not nome_dep_in.strip():
                                st.error("Digite o nome do departamento.")
                            else:
                                novo_dep = {
                                    "nome": nome_dep_in.strip(),
                                    "icone": icone_dep_in,
                                    "ordem": int(ordem_dep_in),
                                    "ativo": True,
                                }
                                try:
                                    supabase.table("departamentos").insert(novo_dep).execute()
                                except Exception:
                                    novo_id = max([d["id"] for d in st.session_state["departamentos_fallback"]] + [0]) + 1
                                    st.session_state["departamentos_fallback"].append({"id": novo_id, **novo_dep})
                                st.success(f"🎉 Departamento **{icone_dep_in} {nome_dep_in}** criado com sucesso!")
                                st.rerun()

                st.markdown(f"#### 📋 Departamentos Cadastrados ({len(deps)})")
                for d in deps:
                    qtd_cats_d = len([c for c in cats if c.get("departamento_id") == d["id"]])
                    with st.container(border=True):
                        c_d1, c_d2, c_d3, c_d4, c_d5 = st.columns([2.5, 1, 1, 1, 1.5])
                        ed_d_nome = c_d1.text_input("Nome", value=d["nome"], key=f"ed_dep_n_{d['id']}")
                        ed_d_ico = c_d2.text_input("Ícone", value=d.get("icone", "📦"), key=f"ed_dep_i_{d['id']}")
                        ed_d_ord = c_d3.number_input("Ordem", min_value=1, value=int(d.get("ordem", 1)), step=1, key=f"ed_dep_o_{d['id']}")
                        with c_d4:
                            st.write("")
                            ed_d_at = st.checkbox("Ativo", value=bool(d.get("ativo", True)), key=f"ed_dep_a_{d['id']}")
                            st.caption(f"📂 {qtd_cats_d} categoria(s)")
                        with c_d5:
                            if st.button("💾 Salvar", key=f"btn_sv_dep_{d['id']}", type="primary", use_container_width=True):
                                dados_up_d = {"nome": ed_d_nome, "icone": ed_d_ico, "ordem": int(ed_d_ord), "ativo": ed_d_at}
                                try:
                                    supabase.table("departamentos").update(dados_up_d).eq("id", d["id"]).execute()
                                except Exception:
                                    for df in st.session_state["departamentos_fallback"]:
                                        if df["id"] == d["id"]:
                                            df.update(dados_up_d)
                                st.success("Atualizado!")
                                st.rerun()
                            if st.button("🗑️ Excluir", key=f"btn_dl_dep_{d['id']}", use_container_width=True):
                                try:
                                    supabase.table("departamentos").delete().eq("id", d["id"]).execute()
                                except Exception:
                                    st.session_state["departamentos_fallback"] = [df for df in st.session_state["departamentos_fallback"] if df["id"] != d["id"]]
                                st.rerun()

            # -------------------------------------------------------------
            # SUB-ABA 2: CATEGORIAS
            # -------------------------------------------------------------
            elif aba_tree == "📂 2. Categorias":
                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">➕ Criar Nova Categoria dentro de um Departamento</div>', unsafe_allow_html=True)
                    if not deps:
                        st.warning("Crie pelo menos 1 Departamento primeiro.")
                    else:
                        with st.form("form_nova_categoria", clear_on_submit=True):
                            cc1, cc2, cc3 = st.columns([2, 2.5, 1.2])
                            dep_pai_sel = cc1.selectbox(
                                "Pertence ao Departamento (Nicho) *",
                                deps,
                                format_func=lambda x: f"{x.get('icone', '📦')} {x['nome']}",
                            )
                            nome_cat_in = cc2.text_input("Nome da Categoria *", placeholder="Ex: Periféricos, Cursos Livres, Perfumes Importados...")
                            with cc3:
                                st.write("")
                                st.write("")
                                btn_add_cat = st.form_submit_button("Criar Categoria", type="primary", use_container_width=True)

                            if btn_add_cat:
                                if not nome_cat_in.strip():
                                    st.error("Digite o nome da categoria.")
                                else:
                                    nova_cat = {
                                        "departamento_id": dep_pai_sel["id"],
                                        "nome": nome_cat_in.strip(),
                                        "ativo": True,
                                    }
                                    try:
                                        supabase.table("categorias").insert(nova_cat).execute()
                                    except Exception:
                                        novo_cid = max([c["id"] for c in st.session_state["categorias_fallback"]] + [0]) + 1
                                        st.session_state["categorias_fallback"].append({"id": novo_cid, **nova_cat})
                                    st.success(f"🎉 Categoria **{nome_cat_in}** adicionada em **{dep_pai_sel['nome']}**!")
                                    st.rerun()

                st.markdown(f"#### 📋 Categorias por Departamento ({len(cats)} no total)")
                for d in deps:
                    cats_do_dep = [c for c in cats if c.get("departamento_id") == d["id"]]
                    with st.expander(f"{d.get('icone', '📦')} {d['nome']} ({len(cats_do_dep)} categorias)", expanded=True):
                        if not cats_do_dep:
                            st.caption("Nenhuma categoria cadastrada neste departamento.")
                        for c in cats_do_dep:
                            qtd_subs_c = len([s for s in subs if s.get("categoria_id") == c["id"]])
                            col_c1, col_c2, col_c3 = st.columns([3.5, 1.5, 1])
                            col_c1.markdown(f"📂 **{c['nome']}**")
                            col_c2.caption(f"🏷️ {qtd_subs_c} subcategoria(s)")
                            if col_c3.button("🗑️ Remover", key=f"btn_del_cat_{c['id']}", use_container_width=True):
                                try:
                                    supabase.table("categorias").delete().eq("id", c["id"]).execute()
                                except Exception:
                                    st.session_state["categorias_fallback"] = [cf for cf in st.session_state["categorias_fallback"] if cf["id"] != c["id"]]
                                st.rerun()

            # -------------------------------------------------------------
            # SUB-ABA 3: SUBCATEGORIAS
            # -------------------------------------------------------------
            elif aba_tree == "🏷️ 3. Subcategorias":
                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">➕ Criar Nova Subcategoria (Filtro Específico)</div>', unsafe_allow_html=True)
                    if not cats:
                        st.warning("Crie pelo menos 1 Categoria primeiro.")
                    else:
                        cs1, cs2 = st.columns(2)
                        dep_filtro_sub = cs1.selectbox(
                            "1º Escolha o Departamento",
                            deps,
                            format_func=lambda x: f"{x.get('icone', '📦')} {x['nome']}",
                            key="sel_dep_para_sub",
                        )
                        cats_filtradas_sub = [c for c in cats if c.get("departamento_id") == dep_filtro_sub["id"]]
                        if not cats_filtradas_sub:
                            cs2.warning("Este departamento ainda não tem categorias. Crie uma na aba Categorias.")
                        else:
                            cat_pai_sel = cs2.selectbox(
                                "2º Escolha a Categoria *",
                                cats_filtradas_sub,
                                format_func=lambda x: f"📂 {x['nome']}",
                                key="sel_cat_para_sub",
                            )
                            with st.form("form_nova_subcategoria", clear_on_submit=True):
                                cs3, cs4, cs5 = st.columns([2.5, 1.5, 1.2])
                                nome_sub_in = cs3.text_input("3º Nome da Subcategoria *", placeholder="Ex: Mouses Sem Fio, Informática Básica, Smartwatches...")
                                ncm_sub_in = cs4.text_input("NCM Fiscal Padrão", value="8471.60.52")
                                with cs5:
                                    st.write("")
                                    st.write("")
                                    btn_add_sub = st.form_submit_button("Criar Subcategoria", type="primary", use_container_width=True)

                                if btn_add_sub:
                                    if not nome_sub_in.strip():
                                        st.error("Informe o nome da subcategoria.")
                                    else:
                                        nova_sub = {
                                            "categoria_id": cat_pai_sel["id"],
                                            "nome": nome_sub_in.strip(),
                                            "ncm_padrao": ncm_sub_in.strip() or "8471.60.52",
                                            "ativo": True,
                                        }
                                        try:
                                            supabase.table("subcategorias").insert(nova_sub).execute()
                                        except Exception:
                                            novo_sid = max([s["id"] for s in st.session_state["subcategorias_fallback"]] + [0]) + 1
                                            st.session_state["subcategorias_fallback"].append({"id": novo_sid, **nova_sub})
                                        st.success(f"🎉 Subcategoria **{nome_sub_in}** criada dentro de **{cat_pai_sel['nome']}**!")
                                        st.rerun()

                st.markdown(f"#### 📋 Todas as Subcategorias ({len(subs)})")
                for s in subs:
                    cat_o = cats_map.get(s.get("categoria_id"), {})
                    dep_o = deps_map.get(cat_o.get("departamento_id"), {})
                    with st.container(border=True):
                        sc1, sc2, sc3 = st.columns([3.5, 1.5, 1])
                        sc1.markdown(
                            f"<span style='color:#94A3B8; font-size:0.85rem;'>{dep_o.get('icone', '📦')} {dep_o.get('nome', '-')} › 📂 {cat_o.get('nome', '-')} ›</span> **🏷️ {s['nome']}**",
                            unsafe_allow_html=True,
                        )
                        sc2.caption(f"NCM: `{s.get('ncm_padrao', '8471.60.52')}`")
                        if sc3.button("🗑️ Excluir", key=f"btn_del_sub_{s['id']}", use_container_width=True):
                            try:
                                supabase.table("subcategorias").delete().eq("id", s["id"]).execute()
                            except Exception:
                                st.session_state["subcategorias_fallback"] = [sf for sf in st.session_state["subcategorias_fallback"] if sf["id"] != s["id"]]
                            st.rerun()

        # =================================================================
        # 2. ABA NOVO PRODUTO (COM SELEÇÃO EM CASCATA MULTI-NICHO)
        # =================================================================
        elif aba_admin == "➕ Novo produto":
            st.markdown('<h1 class="admin-page-title">Novo produto</h1>', unsafe_allow_html=True)

            deps, cats, subs, deps_map, cats_map, subs_map, _ = carregar_hierarquia_catalogo()

            # CARD 1: SELEÇÃO EM CASCATA (FORA DO FORM PARA ATUALIZAR AS OPÇÕES EM TEMPO REAL)
            with st.container(border=True):
                c_hdr1, c_hdr2 = st.columns([3.5, 1.5])
                with c_hdr1:
                    st.markdown('<div class="nuvem-card-title">🗂️ 1. Nicho, Categoria e Subcategoria</div>', unsafe_allow_html=True)
                with c_hdr2:
                    st.button(
                        "➕ Gerenciar Categorias",
                        key="btn_atalho_gerenciar_cats",
                        use_container_width=True,
                        on_click=ir_para_aba_admin,
                        args=("🗂️ Categorias & Nichos",),
                    )

                col_cas1, col_cas2, col_cas3 = st.columns(3)
                dep_escolhido = col_cas1.selectbox(
                    "Departamento (Nicho) *",
                    deps,
                    format_func=lambda x: f"{x.get('icone', '📦')} {x['nome']}",
                    key="np_sel_dep",
                )

                cats_do_dep_sel = [c for c in cats if dep_escolhido and c.get("departamento_id") == dep_escolhido["id"]]
                cat_escolhida = col_cas2.selectbox(
                    "Categoria *",
                    cats_do_dep_sel if cats_do_dep_sel else [{"id": None, "nome": "Sem categoria"}],
                    format_func=lambda x: f"📂 {x['nome']}",
                    key="np_sel_cat",
                )

                subs_da_cat_sel = [s for s in subs if cat_escolhida and cat_escolhida.get("id") and s.get("categoria_id") == cat_escolhida["id"]]
                sub_escolhida = col_cas3.selectbox(
                    "Subcategoria",
                    [{"id": None, "nome": "Geral (Todas)", "ncm_padrao": "8471.60.52"}] + subs_da_cat_sel,
                    format_func=lambda x: f"🏷️ {x['nome']}",
                    key="np_sel_sub",
                )

            ncm_sugerido_auto = (sub_escolhida.get("ncm_padrao") if sub_escolhida else None) or "8471.60.52"

            with st.form("form_nuvemshop_novo_produto", clear_on_submit=True):
                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">📝 2. Nome, Descrição e Características Técnicas</div>', unsafe_allow_html=True)
                    nome_prod = st.text_input("Nome do produto *", placeholder="Ex: Curso de Excel Avançado, Smartwatch Ultra, Teclado Mecânico...")
                    desc_prod = st.text_area("Descrição detalhada", placeholder="Descreva os benefícios, conteúdo completo, garantia ou módulos...", height=100)
                    ficha_prod_in = st.text_area(
                        "⚙️ Características Técnicas / Especificações (uma por linha no formato Característica: Valor)",
                        placeholder="Marca: TagsInfor\nModelo / Versão: 2026 Pro\nGarantia: 12 meses\nCarga Horária / Conteúdo: 40 horas com Certificado",
                        height=95,
                    )

                    c_mod1, c_mod2 = st.columns([2.5, 1.5])
                    modalidade_prod = c_mod1.selectbox(
                        "Modalidade de Operação / Entrega *",
                        [
                            ("estoque_proprio", "📦 Produto Físico (Estoque Próprio / Pronta Entrega)"),
                            ("direto", "🚚 Envio Direto / Fornecedor (Dropshipping)"),
                            ("curso", "🎓 Produto Digital / Curso Online (Sem Frete)"),
                            ("mentoria", "💼 Mentoria / Serviço Consultivo (Atendimento WhatsApp)"),
                            ("afiliado", "🔥 Link de Afiliado Externo (Shopee, Amazon, Mercado Livre, Hotmart)"),
                        ],
                        format_func=lambda x: x[1],
                    )
                    ncm_prod_in = c_mod2.text_input("Código Fiscal NCM", value=ncm_sugerido_auto)

                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">🖼️ 3. Imagem Principal, Galeria de Fotos Extras & Vídeo (YouTube / Outros)</div>', unsafe_allow_html=True)
                    st.markdown('<div class="dropzone-box">📂 Envie a Foto Principal (Capa), Fotos Secundárias da Galeria e Link de Vídeo</div>', unsafe_allow_html=True)
                    col_u1, col_u2 = st.columns(2)
                    arq_img = col_u1.file_uploader("📸 Upload da Foto Principal (Capa)", type=["png", "jpg", "jpeg", "webp"])
                    url_img = col_u2.text_input("Ou colar URL da Foto Principal", placeholder="https://exemplo.com/foto-capa.jpg")

                    st.divider()
                    col_g1, col_g2 = st.columns(2)
                    arqs_galeria = col_g1.file_uploader(
                        "🖼️ Upload de Mais Imagens (Galeria Secundária - selecione várias)",
                        type=["png", "jpg", "jpeg", "webp"],
                        accept_multiple_files=True,
                    )
                    urls_galeria_in = col_g2.text_area(
                        "Ou colar URLs de Mais Imagens (1 link por linha)",
                        placeholder="https://exemplo.com/angulo2.jpg\nhttps://exemplo.com/detalhe3.jpg",
                        height=85,
                    )

                    col_v_link1, col_v_link2 = st.columns(2)
                    video_url_in = col_v_link1.text_input(
                        "🎬 Link de Vídeo (YouTube, Shorts, Vimeo ou MP4)",
                        placeholder="https://www.youtube.com/watch?v=...",
                    )
                    link_af = col_v_link2.text_input("🔗 Link de afiliado externo (se aplicável)", placeholder="https://shopee.com.br/...")

                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">💰 4. Preço, Promoção ("De/Por"), Estoque e Destaque</div>', unsafe_allow_html=True)
                    col_p0, col_p1, col_p2, col_p3, col_p4 = st.columns([1.2, 1.2, 1.1, 1.0, 1.1])
                    preco_orig_in = col_p0.number_input("Preço De (R$ opcional)", min_value=0.0, value=0.0, step=1.0, help="Se preenchido maior que o preço de venda, exibe desconto automático (% OFF)")
                    preco_in = col_p1.number_input("Preço Por / Venda (R$) *", min_value=0.01, value=49.90, step=1.0)
                    estoque_in = col_p2.number_input("Estoque / Vagas", min_value=0, value=20, step=1)
                    destaque_in = col_p3.checkbox("⭐ Destaque no Topo", value=False)
                    visivel_in = col_p4.checkbox("Visível na loja", value=True)

                col_b1, col_b2 = st.columns([3.8, 1.2])
                if col_b2.form_submit_button("💾 Salvar produto", type="primary", width="stretch"):
                    if not nome_prod:
                        st.error("Informe o nome do produto.")
                    else:
                        img_final = converter_imagem_upload(arq_img) if arq_img else (url_img.strip() or None)
                        galeria_lista = []
                        if arqs_galeria:
                            for arq_g in arqs_galeria:
                                try:
                                    galeria_lista.append(converter_imagem_upload(arq_g))
                                except Exception:
                                    pass
                        if urls_galeria_in:
                            for l_u in urls_galeria_in.splitlines():
                                if l_u.strip():
                                    galeria_lista.append(l_u.strip())

                        ficha_lista = parsear_texto_ficha_tecnica(ficha_prod_in)
                        mod_key = modalidade_prod[0]
                        tipo_venda_db = "estoque_proprio" if mod_key in ["curso", "mentoria"] else mod_key
                        cat_slug = mod_key if mod_key in ["curso", "mentoria"] else (cat_escolhida["nome"].lower() if cat_escolhida else "geral")

                        dep_id_val = dep_escolhido["id"] if dep_escolhido else None
                        cat_id_val = cat_escolhida["id"] if (cat_escolhida and cat_escolhida.get("id")) else None
                        sub_id_val = sub_escolhida["id"] if (sub_escolhida and sub_escolhida.get("id")) else None
                        pr_orig_val = float(preco_orig_in) if float(preco_orig_in) > float(preco_in) else None

                        novo_p_completo = {
                            "titulo": nome_prod,
                            "descricao": desc_prod or None,
                            "preco_original": pr_orig_val,
                            "preco_venda": float(preco_in),
                            "destaque": bool(destaque_in),
                            "imagem_url": img_final,
                            "galeria_imagens": galeria_lista,
                            "video_url": video_url_in.strip() or None,
                            "ficha_tecnica": ficha_lista,
                            "tipo_venda": tipo_venda_db,
                            "categoria": cat_slug,
                            "departamento_id": dep_id_val,
                            "categoria_id": cat_id_val,
                            "subcategoria_id": sub_id_val,
                            "ncm": ncm_prod_in or "8471.60.52",
                            "estoque": int(estoque_in),
                            "link_afiliado": link_af or None,
                            "ativo": visivel_in,
                        }
                        try:
                            res_ins = supabase.table("produtos").insert(novo_p_completo).execute()
                            pid_novo = res_ins.data[0]["id"] if res_ins.data else None
                        except Exception:
                            # Fallback caso as novas colunas ainda não tenham sido rodadas no Supabase
                            novo_p_basico = {
                                "titulo": nome_prod,
                                "descricao": desc_prod or None,
                                "preco_venda": float(preco_in),
                                "imagem_url": img_final,
                                "tipo_venda": tipo_venda_db,
                                "estoque": int(estoque_in),
                                "link_afiliado": link_af or None,
                                "ativo": visivel_in,
                            }
                            res_ins = supabase.table("produtos").insert(novo_p_basico).execute()
                            pid_novo = res_ins.data[0]["id"] if res_ins.data else None
                            if pid_novo:
                                st.session_state["vinculos_produtos_local"][pid_novo] = {
                                    "departamento_id": dep_id_val,
                                    "categoria_id": cat_id_val,
                                    "subcategoria_id": sub_id_val,
                                }
                        if pid_novo:
                            st.session_state.setdefault("midia_produtos_local", {})[str(pid_novo)] = {
                                "galeria_imagens": galeria_lista,
                                "video_url": video_url_in.strip() or "",
                                "ficha_tecnica": ficha_lista,
                                "preco_original": pr_orig_val,
                                "destaque": bool(destaque_in),
                            }
                            salvar_estado_persistente()
                        st.success(f"✅ Produto **{nome_prod}** cadastrado com galeria e ficha técnica em **{dep_escolhido['nome']}**!")

        # =================================================================
        # 3. ABA LISTA DE PRODUTOS & ESTOQUE (COM EDIÇÃO DE FOTOS, VÍDEO E FICHA)
        # =================================================================
        elif aba_admin == "📦 Lista de produtos":
            st.markdown('<h1 class="admin-page-title">Lista de produtos, fotos, vídeos e estoque</h1>', unsafe_allow_html=True)
            deps, cats, subs, deps_map, cats_map, subs_map, _ = carregar_hierarquia_catalogo()

            res_prods = supabase.table("produtos").select("*").order("id", desc=True).execute()
            prods = res_prods.data or []
            mapa_avals_adm = carregar_mapa_avaliacoes_todos_produtos()

            # Barra de filtro por Departamento no Admin
            c_f_adm1, c_f_adm2 = st.columns([2, 3])
            opcoes_dep_filtro = [{"id": 0, "nome": "Todos os Departamentos (Nichos)", "icone": "🌟"}] + deps
            dep_adm_sel = c_f_adm1.selectbox(
                "Filtrar por Departamento",
                opcoes_dep_filtro,
                format_func=lambda x: f"{x.get('icone', '📦')} {x['nome']}",
            )
            busca_adm_prod = c_f_adm2.text_input("Buscar produto pelo nome", placeholder="Digite para filtrar...")

            for p in prods:
                dep_id_p, cat_id_p, sub_id_p, trilha_p = obter_trilha_produto(p, deps_map, cats_map, subs_map)
                if dep_adm_sel["id"] != 0 and dep_id_p != dep_adm_sel["id"]:
                    continue
                if busca_adm_prod and busca_adm_prod.lower() not in p.get("titulo", "").lower():
                    continue

                gal_p_all, extras_p_list, video_p_url, ficha_p_list = obter_midia_ficha_produto(p)
                avals_p_adm, media_p_adm, qtd_av_adm = carregar_avaliacoes_do_produto(p["id"], mapa_avals_adm)
                info_loc_p = st.session_state.get("midia_produtos_local", {}).get(str(p["id"]), {})
                pr_orig_atual = float(p.get("preco_original") or info_loc_p.get("preco_original") or 0.0)
                dest_atual = bool(p.get("destaque") if p.get("destaque") is not None else info_loc_p.get("destaque", False))

                with st.container(border=True):
                    c_img, c_info, c_pr, c_est, c_vis, c_act = st.columns([0.9, 2.7, 1.2, 1.0, 0.8, 1.6])
                    thumb = p.get("imagem_url") or "https://via.placeholder.com/150"
                    c_img.image(thumb, width=80)
                    badge_dest_adm = " &nbsp;<span style='background:#FEF3C7; color:#D97706; padding:2px 7px; border-radius:6px; font-size:0.72rem; font-weight:800;'>⭐ DESTAQUE</span>" if dest_atual else ""
                    c_info.markdown(
                        f"<span style='background:rgba(59,130,246,0.15); color:#60A5FA; padding:2px 8px; border-radius:6px; font-size:0.74rem; font-weight:700;'>{trilha_p}</span>{badge_dest_adm}",
                        unsafe_allow_html=True,
                    )
                    c_info.markdown(f"**#{p['id']} - {p['titulo']}**")
                    badge_vid = " • 🎬 Vídeo ativo" if video_p_url else ""
                    c_info.caption(f"🖼️ {len(gal_p_all)} foto(s){badge_vid} • ⭐ {media_p_adm:.1f} ({qtd_av_adm} aval.)")

                    np = c_pr.number_input("Preço (R$)", min_value=0.01, value=float(p["preco_venda"]), step=1.0, key=f"lp_pr_{p['id']}")
                    ne = c_est.number_input("Estoque", min_value=0, value=int(p.get("estoque") or 0), step=1, key=f"lp_est_{p['id']}")
                    nv = c_vis.checkbox("Ativo", value=bool(p.get("ativo", True)), key=f"lp_at_{p['id']}")

                    if c_act.button("Salvar Rápido", key=f"lp_save_{p['id']}", type="primary", width="stretch"):
                        supabase.table("produtos").update({"preco_venda": float(np), "estoque": int(ne), "ativo": nv}).eq("id", p["id"]).execute()
                        st.toast("✅ Preço e estoque atualizados!")
                        st.rerun()

                    if c_act.button("📸 Fotos & Vídeo", key=f"lp_midia_{p['id']}", width="stretch"):
                        st.session_state[f"abrir_ed_midia_{p['id']}"] = not st.session_state.get(f"abrir_ed_midia_{p['id']}", False)

                    if c_act.button("Excluir", key=f"lp_del_{p['id']}", width="stretch"):
                        supabase.table("produtos").delete().eq("id", p["id"]).execute()
                        st.rerun()

                    # EXPANDER COMPLETO PARA EDITAR FOTOS, GALERIA, VÍDEO, FICHA TÉCNICA E AVALIAÇÕES
                    with st.expander(
                        f"🖼️ Clique aqui para Editar Fotos, Galeria ({len(gal_p_all)}), Vídeo, Ficha Técnica e Avaliações — #{p['id']}",
                        expanded=st.session_state.get(f"abrir_ed_midia_{p['id']}", False),
                    ):
                        tab_ed_midia, tab_ed_ficha, tab_ed_aval = st.tabs([
                            "📸 Fotos & Vídeo (YouTube / Outros)",
                            "⚙️ Descrição, Categoria & Ficha Técnica",
                            f"⭐ Avaliações & Comentários ({qtd_av_adm})",
                        ])

                        with tab_ed_midia:
                            st.markdown("##### 1. Imagem Principal (Capa do Produto)")
                            cm_1, cm_2, cm_3 = st.columns([1, 2, 2])
                            with cm_1:
                                st.image(thumb, caption="Capa Atual", width=110)
                            with cm_2:
                                up_nova_capa = st.file_uploader(
                                    "Subir nova Foto Principal (substitui a atual)",
                                    type=["png", "jpg", "jpeg", "webp"],
                                    key=f"up_capa_p_{p['id']}",
                                )
                            with cm_3:
                                ed_img_p = st.text_input(
                                    "Ou editar URL da Foto Principal",
                                    value=p.get("imagem_url") or "",
                                    key=f"ed_p_img_{p['id']}",
                                )

                            st.divider()
                            st.markdown(f"##### 2. Galeria de Imagens Secundárias ({len(extras_p_list)} foto(s) extra(s))")
                            if extras_p_list:
                                cols_ex = st.columns(min(6, len(extras_p_list)))
                                for idx_ex, img_ex_u in enumerate(extras_p_list):
                                    with cols_ex[idx_ex % len(cols_ex)]:
                                        st.image(img_ex_u, width=85, caption=f"Extra #{idx_ex + 1}")
                                        if st.button("🗑️ Remover", key=f"btn_rem_img_ex_{p['id']}_{idx_ex}"):
                                            nova_lista_ex = [u for i_u, u in enumerate(extras_p_list) if i_u != idx_ex]
                                            st.session_state.setdefault("midia_produtos_local", {}).setdefault(str(p["id"]), {})["galeria_imagens"] = nova_lista_ex
                                            try:
                                                supabase.table("produtos").update({"galeria_imagens": nova_lista_ex}).eq("id", p["id"]).execute()
                                            except Exception:
                                                pass
                                            salvar_estado_persistente()
                                            st.rerun()

                            cg_ed1, cg_ed2 = st.columns(2)
                            with cg_ed1:
                                up_novas_extras = st.file_uploader(
                                    "➕ Subir mais fotos para a galeria (pode selecionar várias)",
                                    type=["png", "jpg", "jpeg", "webp"],
                                    accept_multiple_files=True,
                                    key=f"up_gal_ex_{p['id']}",
                                )
                            with cg_ed2:
                                urls_extras_txt = st.text_area(
                                    "URLs das fotos extras (1 link por linha)",
                                    value="\n".join([u for u in extras_p_list if not u.startswith("data:")]),
                                    placeholder="https://exemplo.com/foto2.jpg\nhttps://exemplo.com/foto3.jpg",
                                    height=85,
                                    key=f"ed_urls_ex_{p['id']}",
                                )

                            st.divider()
                            st.markdown("##### 3. Vídeo Demonstrativo (YouTube, Shorts, Vimeo ou MP4)")
                            ed_video_p = st.text_input(
                                "🎬 Link do Vídeo (cole o link do YouTube ou outra plataforma)",
                                value=video_p_url,
                                placeholder="https://www.youtube.com/watch?v=...",
                                key=f"ed_vid_p_{p['id']}",
                            )
                            if ed_video_p:
                                st.caption("Pré-visualização do vídeo:")
                                renderizar_player_video_produto(ed_video_p)

                        with tab_ed_ficha:
                            ed_tit_p = st.text_input("Título do Produto", value=p.get("titulo", ""), key=f"ed_p_tit_{p['id']}")
                            ed_desc_p = st.text_area("Descrição Completa", value=p.get("descricao") or "", key=f"ed_p_desc_{p['id']}", height=100)
                            ed_ficha_txt = st.text_area(
                                "⚙️ Características Técnicas (1 por linha no formato Característica: Valor)",
                                value=formatar_ficha_tecnica_texto(ficha_p_list),
                                height=110,
                                key=f"ed_ficha_p_{p['id']}",
                            )

                            c_cat_e1, c_cat_e2, c_cat_e3 = st.columns(3)
                            idx_dep_p = next((i for i, d in enumerate(deps) if d["id"] == dep_id_p), 0)
                            ed_dep_p = c_cat_e1.selectbox(
                                "Departamento (Nicho)",
                                deps,
                                index=idx_dep_p,
                                format_func=lambda x: f"{x.get('icone', '📦')} {x['nome']}",
                                key=f"ed_p_dep_{p['id']}",
                            )
                            cats_ed_p = [c for c in cats if ed_dep_p and c.get("departamento_id") == ed_dep_p["id"]]
                            idx_cat_p = next((i for i, c in enumerate(cats_ed_p) if c["id"] == cat_id_p), 0)
                            ed_cat_p = c_cat_e2.selectbox(
                                "Categoria",
                                cats_ed_p if cats_ed_p else [{"id": None, "nome": "Geral"}],
                                index=idx_cat_p,
                                format_func=lambda x: f"📂 {x['nome']}",
                                key=f"ed_p_cat_{p['id']}",
                            )
                            subs_ed_p = [s for s in subs if ed_cat_p and ed_cat_p.get("id") and s.get("categoria_id") == ed_cat_p["id"]]
                            opcoes_sub_ed = [{"id": None, "nome": "Geral (Todas)"}] + subs_ed_p
                            idx_sub_p = next((i for i, s in enumerate(opcoes_sub_ed) if s["id"] == sub_id_p), 0)
                            ed_sub_p = c_cat_e3.selectbox(
                                "Subcategoria",
                                opcoes_sub_ed,
                                index=idx_sub_p,
                                format_func=lambda x: f"🏷️ {x['nome']}",
                                key=f"ed_p_sub_{p['id']}",
                            )

                            c_m_l1, c_m_l2, c_m_l3, c_m_l4 = st.columns([1.3, 1.5, 1.2, 1.1])
                            mods_op = ["estoque_proprio", "direto", "afiliado"]
                            idx_mod_p = mods_op.index(p.get("tipo_venda", "estoque_proprio")) if p.get("tipo_venda") in mods_op else 0
                            ed_mod_p = c_m_l1.selectbox("Modalidade", mods_op, index=idx_mod_p, key=f"ed_p_mod_{p['id']}")
                            ed_link_p = c_m_l2.text_input("Link Afiliado", value=p.get("link_afiliado") or "", key=f"ed_p_lnk_{p['id']}")
                            ed_pr_orig_p = c_m_l3.number_input("Preço De (R$)", min_value=0.0, value=pr_orig_atual, step=1.0, key=f"ed_p_pro_{p['id']}")
                            ed_dest_p = c_m_l4.checkbox("⭐ Destaque", value=dest_atual, key=f"ed_p_dst_{p['id']}")

                        with tab_ed_aval:
                            st.caption("Gerencie os comentários e avaliações deste produto ou cadastre um depoimento verificado:")
                            if not avals_p_adm:
                                st.info("Ainda não há avaliações cadastradas para este produto.")
                            else:
                                for idx_av_a, av_a in enumerate(avals_p_adm):
                                    ca_1, ca_2 = st.columns([4, 1])
                                    ca_1.markdown(f"**{'⭐' * int(av_a.get('nota', 5))} {av_a.get('titulo_avaliacao') or ''}** — *{av_a.get('cliente_nome', 'Cliente')}*")
                                    ca_1.caption(av_a.get("comentario", ""))
                                    if ca_2.button("🗑️ Excluir", key=f"del_av_adm_{p['id']}_{av_a.get('id', idx_av_a)}"):
                                        try:
                                            supabase.table("avaliacoes_produtos").delete().eq("id", av_a.get("id")).execute()
                                        except Exception:
                                            pass
                                        st.session_state["avaliacoes_produtos_local"] = [
                                            x for x in st.session_state.get("avaliacoes_produtos_local", [])
                                            if str(x.get("id")) != str(av_a.get("id"))
                                        ]
                                        salvar_estado_persistente()
                                        st.rerun()

                        st.divider()
                        if st.button("💾 Salvar Todas as Alterações (Fotos, Galeria, Vídeo e Ficha Técnica)", key=f"btn_sv_full_p_{p['id']}", type="primary", width="stretch"):
                            nova_capa_final = converter_imagem_upload(up_nova_capa) if up_nova_capa else (ed_img_p.strip() or None)
                            b64_existentes = [u for u in extras_p_list if u.startswith("data:")]
                            urls_digitadas = [u.strip() for u in urls_extras_txt.splitlines() if u.strip()]
                            novos_b64_up = []
                            if up_novas_extras:
                                for arq_ne in up_novas_extras:
                                    try:
                                        novos_b64_up.append(converter_imagem_upload(arq_ne))
                                    except Exception:
                                        pass
                            galeria_atualizada = b64_existentes + urls_digitadas + novos_b64_up
                            ficha_atualizada = parsear_texto_ficha_tecnica(ed_ficha_txt)
                            pr_orig_up = float(ed_pr_orig_p) if float(ed_pr_orig_p) > float(np) else None

                            st.session_state.setdefault("midia_produtos_local", {})[str(p["id"])] = {
                                "galeria_imagens": galeria_atualizada,
                                "video_url": ed_video_p.strip(),
                                "ficha_tecnica": ficha_atualizada,
                                "preco_original": pr_orig_up,
                                "destaque": bool(ed_dest_p),
                            }
                            salvar_estado_persistente()

                            up_full = {
                                "titulo": ed_tit_p,
                                "descricao": ed_desc_p or None,
                                "preco_original": pr_orig_up,
                                "destaque": bool(ed_dest_p),
                                "tipo_venda": ed_mod_p,
                                "imagem_url": nova_capa_final,
                                "galeria_imagens": galeria_atualizada,
                                "video_url": ed_video_p.strip() or None,
                                "ficha_tecnica": ficha_atualizada,
                                "link_afiliado": ed_link_p or None,
                                "departamento_id": ed_dep_p["id"] if ed_dep_p else None,
                                "categoria_id": ed_cat_p["id"] if ed_cat_p else None,
                                "subcategoria_id": ed_sub_p["id"] if ed_sub_p else None,
                            }
                            try:
                                supabase.table("produtos").update(up_full).eq("id", p["id"]).execute()
                            except Exception:
                                supabase.table("produtos").update({
                                    "titulo": ed_tit_p,
                                    "descricao": ed_desc_p or None,
                                    "tipo_venda": ed_mod_p,
                                    "imagem_url": nova_capa_final,
                                    "link_afiliado": ed_link_p or None,
                                }).eq("id", p["id"]).execute()
                                st.session_state["vinculos_produtos_local"][p["id"]] = {
                                    "departamento_id": ed_dep_p["id"] if ed_dep_p else None,
                                    "categoria_id": ed_cat_p["id"] if ed_cat_p else None,
                                    "subcategoria_id": ed_sub_p["id"] if ed_sub_p else None,
                                }
                            st.success("✅ Fotos, galeria, vídeo e ficha técnica atualizados com sucesso!")
                            st.rerun()

        # =================================================================
        # 4. ABA LOJA ONLINE (LAYOUT, CABEÇALHO E RODAPÉ)
        # =================================================================
        elif aba_admin == "🎨 Loja online (Layout)":
            st.markdown('<h1 class="admin-page-title">Layout, Cabeçalho & Rodapé da Loja</h1>', unsafe_allow_html=True)
            st.caption("Personalize o cabeçalho, barra de vantagens, banner principal e o rodapé institucional do seu site (salvo no Supabase + Disco):")

            # Pré-visualização ao vivo do Cabeçalho + Banner + Rodapé
            with st.container(border=True):
                st.markdown('<div class="nuvem-card-title">🖥️ Pré-visualização ao vivo (Cabeçalho & Rodapé)</div>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style="background:#0F172A; border:1px solid #334155; border-radius:12px; padding:14px 18px; margin-bottom:10px;">
                        <div style="background:#F59E0B; color:#0F172A; font-weight:800; font-size:0.75rem; padding:4px 12px; border-radius:6px; display:flex; justify-content:space-between; margin-bottom:10px;">
                            <span>{cfg.get('top_promo', '')[:65]}</span>
                            <span>{cfg.get('localizacao_cabecalho', '📍 Manaus/AM')} &nbsp;|&nbsp; 🔒 Compra Segura</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                            <div>
                                <div style="font-size:1.35rem; font-weight:800; color:#F8FAFC;">{cfg.get('nome_loja', 'Tags Informática')} <span style="font-size:0.72rem; background:rgba(34,197,94,0.18); color:#4ADE80; padding:2px 8px; border-radius:12px;">{cfg.get('status_loja', '🟢 Aberto')}</span></div>
                                <div style="font-size:0.78rem; color:#94A3B8;">{cfg.get('slogan_cabecalho', 'Cursos, Mentorias & Tecnologia Oficial')}</div>
                            </div>
                            <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:6px 16px; color:#94A3B8; font-size:0.78rem; min-width:220px;">🔍 Buscar produtos, cursos...</div>
                            <div style="font-size:0.78rem; color:#60A5FA; font-weight:700;">👤 Minha Conta &nbsp;|&nbsp; 🛒 Meu Carrinho</div>
                        </div>
                    </div>
                    <div style="background:#090D16; border:1px solid #1E293B; border-radius:12px; padding:12px 18px; color:#94A3B8; font-size:0.78rem; display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px;">
                        <div><strong style="color:#F8FAFC;">🔻 Rodapé: {cfg.get('nome_loja', 'Tags Informática')}</strong> — {cfg.get('rodape_sobre', '')[:70]}...</div>
                        <div>📱 {cfg.get('rodape_whatsapp', WHATSAPP_LOJA)} &nbsp;|&nbsp; ✉️ {cfg.get('rodape_email', '')} &nbsp;|&nbsp; CNPJ: {cfg.get('rodape_cnpj', '')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            tab_lay_cab, tab_lay_ban, tab_lay_rod = st.tabs([
                "🔝 1. Cabeçalho & Logotipo",
                "🎯 2. Banner Principal & Faixa de Vantagens",
                "🔻 3. Rodapé Institucional & Redes Sociais",
            ])

            with tab_lay_cab:
                col_l1, col_l2 = st.columns([3, 2])
                with col_l1:
                    with st.form("form_layout_cabecalho"):
                        st.markdown('<div class="nuvem-card-title">🔝 Dados do Cabeçalho (Header)</div>', unsafe_allow_html=True)
                        c_cb1, c_cb2 = st.columns([2, 1])
                        nn = c_cb1.text_input("Nome da Loja *", value=cfg.get("nome_loja", "Tags Informática"))
                        st_loja_opcoes = ["🟢 Aberto", "🟡 Atendimento Online", "🔴 Fechado"]
                        st_atual_lj = cfg.get("status_loja", "🟢 Aberto")
                        idx_st_lj = st_loja_opcoes.index(st_atual_lj) if st_atual_lj in st_loja_opcoes else 0
                        n_status_lj = c_cb2.selectbox("Status no Cabeçalho", st_loja_opcoes, index=idx_st_lj)

                        n_slogan = st.text_input("Slogan abaixo do Nome/Logo", value=cfg.get("slogan_cabecalho", "Cursos, Mentorias & Tecnologia Oficial"))
                        np_txt = st.text_input("Texto da Barra Promocional do Topo", value=cfg.get("top_promo", ""))
                        n_loc_top = st.text_input("Selo de Localização / Envio no Topo", value=cfg.get("localizacao_cabecalho", "📍 Manaus/AM • Envio p/ Todo Brasil"))

                        if st.form_submit_button("💾 Salvar Cabeçalho no Supabase", type="primary", width="stretch"):
                            st.session_state["config_loja"]["nome_loja"] = nn.strip() or "Tags Informática"
                            st.session_state["config_loja"]["status_loja"] = n_status_lj
                            st.session_state["config_loja"]["slogan_cabecalho"] = n_slogan.strip()
                            st.session_state["config_loja"]["top_promo"] = np_txt.strip()
                            st.session_state["config_loja"]["localizacao_cabecalho"] = n_loc_top.strip()
                            salvar_config_loja_supabase()
                            st.success("✅ Cabeçalho salvo no Supabase com sucesso!")
                            st.rerun()

                with col_l2:
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">🏷️ Logotipo da Marca</div>', unsafe_allow_html=True)
                        if cfg.get("logo_url"):
                            st.image(cfg["logo_url"], width=150, alt="Logotipo da loja")
                        up_l = st.file_uploader("Subir logotipo (PNG/JPG/WEBP)", type=["png", "jpg", "jpeg", "webp"], key="up_logo_l")
                        url_l = st.text_input("Ou link da logo (URL)", value=cfg.get("logo_url", ""))
                        c_lg1, c_lg2 = st.columns(2)
                        if c_lg1.button("💾 Salvar Logo", type="primary", width="stretch"):
                            if up_l:
                                st.session_state["config_loja"]["logo_url"] = converter_imagem_upload(up_l)
                            else:
                                st.session_state["config_loja"]["logo_url"] = url_l.strip()
                            salvar_config_loja_supabase()
                            st.success("Logo atualizado!")
                            st.rerun()
                        if cfg.get("logo_url") and c_lg2.button("🗑️ Usar Texto", width="stretch"):
                            st.session_state["config_loja"]["logo_url"] = ""
                            salvar_config_loja_supabase()
                            st.rerun()

            with tab_lay_ban:
                with st.form("form_layout_banner_vantagens"):
                    st.markdown('<div class="nuvem-card-title">🎯 Banner Principal & Faixa de Vantagens do Cabeçalho</div>', unsafe_allow_html=True)
                    nh_t = st.text_input("Título do Banner Principal", value=cfg.get("hero_title", ""))
                    nh_s = st.text_area("Subtítulo do Banner", value=cfg.get("hero_subtitle", ""), height=70)
                    ex_vant = st.checkbox("Exibir Faixa de 4 Vantagens abaixo do cabeçalho", value=bool(cfg.get("exibir_barra_vantagens", True)))
                    cv1, cv2, cv3, cv4 = st.columns(4)
                    v1_in = cv1.text_input("Vantagem 1", value=cfg.get("vantagem_1", "⚡ Pix com Aprovação Imediata"))
                    v2_in = cv2.text_input("Vantagem 2", value=cfg.get("vantagem_2", "🚚 Envio Rápido c/ Rastreio"))
                    v3_in = cv3.text_input("Vantagem 3", value=cfg.get("vantagem_3", "🛡️ Compra 100% Garantida"))
                    v4_in = cv4.text_input("Vantagem 4", value=cfg.get("vantagem_4", "🎓 Cursos com Certificado"))

                    if st.form_submit_button("💾 Salvar Banner e Vantagens no Supabase", type="primary", width="stretch"):
                        st.session_state["config_loja"]["hero_title"] = nh_t.strip()
                        st.session_state["config_loja"]["hero_subtitle"] = nh_s.strip()
                        st.session_state["config_loja"]["exibir_barra_vantagens"] = bool(ex_vant)
                        st.session_state["config_loja"]["vantagem_1"] = v1_in.strip()
                        st.session_state["config_loja"]["vantagem_2"] = v2_in.strip()
                        st.session_state["config_loja"]["vantagem_3"] = v3_in.strip()
                        st.session_state["config_loja"]["vantagem_4"] = v4_in.strip()
                        salvar_config_loja_supabase()
                        st.success("✅ Banner e faixa de vantagens salvos no Supabase!")
                        st.rerun()

            with tab_lay_rod:
                with st.form("form_layout_rodape"):
                    st.markdown('<div class="nuvem-card-title">🔻 Configuração Completa do Rodapé (Footer)</div>', unsafe_allow_html=True)
                    r_sobre = st.text_area("Texto 'Sobre a Loja' no Rodapé", value=cfg.get("rodape_sobre", ""), height=80)

                    cr1, cr2, cr3 = st.columns(3)
                    r_whats = cr1.text_input("WhatsApp de Atendimento", value=cfg.get("rodape_whatsapp", WHATSAPP_LOJA))
                    r_email = cr2.text_input("E-mail de Atendimento", value=cfg.get("rodape_email", "contato@tagsinfor.com"))
                    r_cnpj = cr3.text_input("CNPJ exibido no Rodapé", value=cfg.get("rodape_cnpj", "00.000.000/0001-00"))

                    cr4, cr5 = st.columns(2)
                    r_end = cr4.text_input("Endereço / Cidade no Rodapé", value=cfg.get("rodape_endereco", "Av. Djalma Batista, 1000 - Chapada, Manaus/AM"))
                    r_hor = cr5.text_input("Horário de Atendimento", value=cfg.get("rodape_horario", "Seg a Sex das 08h às 18h | Sáb das 08h às 13h"))

                    cr6, cr7 = st.columns(2)
                    r_insta = cr6.text_input("Link do Instagram", value=cfg.get("rodape_instagram", "https://instagram.com"))
                    r_yt = cr7.text_input("Link do YouTube", value=cfg.get("rodape_youtube", "https://youtube.com"))

                    r_copy = st.text_input("Texto de Direitos Autorais (Copyright)", value=cfg.get("rodape_copyright", "© 2026 Tags Informática — Todos os direitos reservados."))

                    if st.form_submit_button("💾 Salvar Configurações do Rodapé no Supabase", type="primary", width="stretch"):
                        st.session_state["config_loja"]["rodape_sobre"] = r_sobre.strip()
                        st.session_state["config_loja"]["rodape_whatsapp"] = r_whats.strip()
                        st.session_state["config_loja"]["rodape_email"] = r_email.strip()
                        st.session_state["config_loja"]["rodape_cnpj"] = r_cnpj.strip()
                        st.session_state["config_loja"]["rodape_endereco"] = r_end.strip()
                        st.session_state["config_loja"]["rodape_horario"] = r_hor.strip()
                        st.session_state["config_loja"]["rodape_instagram"] = r_insta.strip()
                        st.session_state["config_loja"]["rodape_youtube"] = r_yt.strip()
                        st.session_state["config_loja"]["rodape_copyright"] = r_copy.strip()
                        salvar_config_loja_supabase()
                        st.success("✅ Rodapé salvo no Supabase com sucesso!")
                        st.rerun()

        # =================================================================
        # 5. ABA CLIENTES & SUPORTE (LISTA, ADICIONAR, SENHAS E CHAMADOS)
        # =================================================================
        elif aba_admin == "👥 Clientes":
            opcoes_cli = ["📋 Lista de clientes", "➕ Adicionar cliente", "🔑 Alterar Senha de Usuários", "🎧 Chamados de Suporte"]
            if "sub_aba_cli" not in st.session_state or st.session_state["sub_aba_cli"] not in opcoes_cli:
                st.session_state["sub_aba_cli"] = "📋 Lista de clientes"

            st.markdown('<h1 class="admin-page-title">Clientes & Atendimento</h1>', unsafe_allow_html=True)

            col_cl_b1, col_cl_b2, col_cl_b3, col_cl_b4 = st.columns([1.3, 1.3, 1.6, 1.4])
            with col_cl_b1:
                st.button(
                    "📋 Lista de clientes",
                    key="btn_tab_cli_list",
                    type="primary" if st.session_state["sub_aba_cli"] == "📋 Lista de clientes" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cli", "📋 Lista de clientes"),
                )
            with col_cl_b2:
                st.button(
                    "➕ Adicionar cliente",
                    key="btn_tab_cli_add",
                    type="primary" if st.session_state["sub_aba_cli"] == "➕ Adicionar cliente" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cli", "➕ Adicionar cliente"),
                )
            with col_cl_b3:
                st.button(
                    "🔑 Alterar Senhas",
                    key="btn_tab_cli_pwd",
                    type="primary" if st.session_state["sub_aba_cli"] == "🔑 Alterar Senha de Usuários" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cli", "🔑 Alterar Senha de Usuários"),
                )
            with col_cl_b4:
                st.button(
                    "🎧 Chamados de Suporte",
                    key="btn_tab_cli_sup",
                    type="primary" if st.session_state["sub_aba_cli"] == "🎧 Chamados de Suporte" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cli", "🎧 Chamados de Suporte"),
                )

            sub_aba_cli = st.session_state["sub_aba_cli"]

            if sub_aba_cli == "📋 Lista de clientes":
                # Carrega clientes cadastrados diretamente na tabela clientes do Supabase
                clientes_map = {}
                try:
                    res_cls = supabase.table("clientes").select("*").order("id", desc=True).execute()
                    for c in (res_cls.data or []):
                        chave = c.get("cpf_cnpj") or c.get("email") or f"id_{c.get('id')}"
                        clientes_map[chave] = {
                            "id": c.get("id"),
                            "auth_uid": c.get("auth_uid"),
                            "nome": c.get("nome") or "Cliente",
                            "cpf": c.get("cpf_cnpj") or "Não informado",
                            "whatsapp": c.get("whatsapp") or "Não informado",
                            "email": c.get("email") or "Não informado",
                            "endereco": c.get("endereco_completo") or "Não informado",
                            "cep": c.get("cep") or "Não informado",
                            "tabela": c.get("tabela_preco", "Varejo"),
                            "tem_senha": bool(c.get("senha")),
                            "total_pedidos": 0,
                        }
                except Exception:
                    pass

                # Carrega pedidos para somar histórico de compras
                try:
                    res_peds = supabase.table("pedidos").select("*").execute()
                    peds_data = res_peds.data or []
                except Exception:
                    peds_data = []

                for ped in peds_data:
                    cpf = ped.get("cliente_cpf")
                    if cpf and cpf not in clientes_map:
                        clientes_map[cpf] = {
                            "id": ped.get("cliente_id"),
                            "nome": ped.get("cliente_nome", "Cliente Sem Nome"),
                            "cpf": cpf,
                            "whatsapp": ped.get("cliente_whatsapp", ""),
                            "email": ped.get("cliente_email", ""),
                            "endereco": ped.get("endereco_completo", "Não informado"),
                            "cep": ped.get("cep", ""),
                            "tabela": "Varejo",
                            "tem_senha": False,
                            "total_pedidos": 1,
                        }
                    elif cpf in clientes_map:
                        clientes_map[cpf]["total_pedidos"] += 1

                # Junta com os clientes da sessão
                for c_extra in st.session_state.get("clientes_extras", []):
                    cpf_e = c_extra.get("cpf")
                    if cpf_e and cpf_e not in clientes_map:
                        clientes_map[cpf_e] = c_extra

                if not clientes_map:
                    # Tela idêntica ao print do usuário (Nuvemshop: "Seu primeiro cliente vem aí!")
                    st.markdown(
                        """
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:48px 24px; text-align:center; max-width:680px; margin:20px auto;">
                            <div style="font-size:3.5rem; margin-bottom:12px;">👥</div>
                            <span style="font-size:0.75rem; font-weight:800; color:#64748B; letter-spacing:0.1em; text-transform:uppercase;">CLIENTES</span>
                            <h2 style="font-size:1.6rem; font-weight:800; color:#0F172A; margin:8px 0 12px 0;">Seu primeiro cliente vem aí!</h2>
                            <p style="color:#64748B; font-size:0.95rem; line-height:1.5; max-width:480px; margin:0 auto 24px auto;">
                                Aqui você vai encontrar os dados de seus clientes. Enquanto isso, você pode adicionar informação de pessoas que já realizaram alguma compra antes.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    c_btn1, c_btn2, c_btn3 = st.columns([1, 1.2, 1.2])
                    with c_btn2:
                        if st.button("Adicionar cliente", key="btn_empty_add_cli", type="primary", use_container_width=True):
                            st.session_state["sub_aba_cli"] = "➕ Adicionar cliente"
                            st.rerun()
                    with c_btn3:
                        if st.button("📥 Importar Exemplo", key="btn_importar_exemplo_cli", use_container_width=True):
                            st.session_state["clientes_extras"].append({
                                "nome": "Lucas Martins Silva",
                                "cpf": "123.456.789-00",
                                "whatsapp": "92981234567",
                                "email": "lucas.martins@exemplo.com",
                                "endereco": "Av. Djalma Batista, 1000, Chapada, Manaus/AM",
                                "cep": "69050-010",
                                "total_pedidos": 2,
                            })
                            st.success("Cliente de teste adicionado!")
                            st.rerun()

                    st.markdown(
                        """
                        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:18px 20px; display:flex; align-items:center; gap:16px; margin-top:24px;">
                            <div style="background:#0284C7; color:white; border-radius:8px; width:42px; height:42px; display:flex; align-items:center; justify-content:center; font-size:1.2rem; font-weight:800;">NM</div>
                            <div>
                                <strong style="color:#0F172A; font-size:0.95rem;">Tags Marketing & Relacionamento</strong><br>
                                <span style="color:#64748B; font-size:0.85rem;">Mantenha contato direto via WhatsApp com cada cliente para fidelização e envio de certificados dos cursos.</span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    busca_cli = st.text_input("🔍 Buscar cliente por Nome, E-mail ou CPF:", placeholder="Digite o nome, e-mail ou CPF...")
                    st.caption(f"Total de {len(clientes_map)} cliente(s) cadastrado(s)")

                    for idx_c_list, (chave_c, cli) in enumerate(clientes_map.items()):
                        if busca_cli:
                            termo = busca_cli.lower()
                            if (
                                termo not in str(cli.get("nome", "")).lower()
                                and termo not in str(cli.get("cpf", "")).lower()
                                and termo not in str(cli.get("email", "")).lower()
                            ):
                                continue

                        with st.container(border=True):
                            c_c1, c_c2, c_c3 = st.columns([2.8, 2.7, 2.3])
                            with c_c1:
                                st.markdown(f"**👤 {cli['nome']}**")
                                st.write(f"CPF: `{cli.get('cpf', '-')}` | E-mail: `{cli.get('email', 'Não informado')}`")
                            with c_c2:
                                st.write(f"📱 WhatsApp: `{cli.get('whatsapp', '-')}`")
                                st.caption(f"📍 {cli.get('endereco', 'Endereço')} (CEP: {cli.get('cep', '-')})")
                            with c_c3:
                                num_w = re.sub(r"\D", "", str(cli.get("whatsapp", "")))
                                if num_w:
                                    st.markdown(f"[💬 Falar no WhatsApp](https://wa.me/55{num_w})")
                                st.caption(f"🛒 Compras: {cli.get('total_pedidos', 0)} pedido(s)")

                                with st.popover("🔑 Alterar Senha", use_container_width=True):
                                    st.markdown(f"**🔑 Redefinir Senha de {cli['nome']}**")
                                    nova_s_pop = st.text_input(
                                        "Nova senha (mín. 6 caracteres)",
                                        type="password",
                                        key=f"pop_pw1_{idx_c_list}",
                                        placeholder="Digite a nova senha",
                                    )
                                    conf_s_pop = st.text_input(
                                        "Confirmar nova senha",
                                        type="password",
                                        key=f"pop_pw2_{idx_c_list}",
                                        placeholder="Repita a nova senha",
                                    )
                                    if st.button("💾 Salvar Nova Senha", key=f"btn_pop_pw_{idx_c_list}", type="primary", use_container_width=True):
                                        if not nova_s_pop or len(nova_s_pop.strip()) < 4:
                                            st.error("Informe uma senha válida (mínimo 4 caracteres).")
                                        elif nova_s_pop != conf_s_pop:
                                            st.error("As senhas não conferem.")
                                        else:
                                            hash_novo = gerar_hash_senha(nova_s_pop.strip())
                                            atualizou_db = False
                                            try:
                                                if cli.get("id"):
                                                    supabase.table("clientes").update({"senha": hash_novo}).eq("id", cli["id"]).execute()
                                                    atualizou_db = True
                                                elif cli.get("cpf") and cli.get("cpf") != "Não informado":
                                                    r_up = supabase.table("clientes").update({"senha": hash_novo}).eq("cpf_cnpj", cli["cpf"]).execute()
                                                    if r_up.data:
                                                        atualizou_db = True
                                                if not atualizou_db and cli.get("email") and "@" in str(cli.get("email")):
                                                    r_up2 = supabase.table("clientes").update({"senha": hash_novo}).ilike("email", cli["email"].strip()).execute()
                                                    if r_up2.data:
                                                        atualizou_db = True
                                                if not atualizou_db:
                                                    supabase.table("clientes").insert({
                                                        "nome": cli["nome"],
                                                        "cpf_cnpj": cli.get("cpf") if cli.get("cpf") != "Não informado" else None,
                                                        "email": cli.get("email") if cli.get("email") != "Não informado" else None,
                                                        "whatsapp": cli.get("whatsapp") if cli.get("whatsapp") != "Não informado" else None,
                                                        "endereco_completo": cli.get("endereco"),
                                                        "cep": cli.get("cep"),
                                                        "senha": hash_novo,
                                                    }).execute()
                                            except Exception:
                                                pass

                                            # Atualizar também no Supabase Auth caso SERVICE_ROLE_KEY esteja configurada
                                            srv_key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_SERVICE_ROLE")
                                            if srv_key and cli.get("auth_uid"):
                                                try:
                                                    sup_adm = create_client(st.secrets["SUPABASE_URL"], srv_key)
                                                    sup_adm.auth.admin.update_user_by_id(cli["auth_uid"], {"password": nova_s_pop.strip()})
                                                except Exception:
                                                    pass

                                            # Atualizar cache local de contas
                                            contas_loc = st.session_state.setdefault("contas_clientes_local", {})
                                            em_k = (cli.get("email") or "").strip().lower()
                                            cpf_k = re.sub(r"\D", "", str(cli.get("cpf") or ""))
                                            if em_k and em_k in contas_loc:
                                                contas_loc[em_k]["senha"] = hash_novo
                                            if cpf_k and cpf_k in contas_loc:
                                                contas_loc[cpf_k]["senha"] = hash_novo
                                            salvar_estado_persistente()
                                            st.success(f"✅ Senha de **{cli['nome']}** alterada com sucesso!")

            elif sub_aba_cli == "➕ Adicionar cliente":
                # Formulário idêntico ao print do usuário (Nuvemshop: "Adicionar cliente")
                st.markdown("### Adicionar cliente")

                with st.form("form_adicionar_cliente_nuvem", clear_on_submit=False):
                    # CARD 1: DADOS PESSOAIS
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Dados pessoais</div>', unsafe_allow_html=True)
                        nome_cli_in = st.text_input("Nome e sobrenome *", placeholder="Ex: Lucas Silva")
                        email_cli_in = st.text_input("E-mail", placeholder="ex: cliente@exemplo.com")

                        col_dp1, col_dp2 = st.columns(2)
                        with col_dp1:
                            tel_cli_in = st.text_input("Telefone (opcional)", placeholder="Ex: 92981234567")
                        with col_dp2:
                            cpf_cli_in = st.text_input("CPF ou CNPJ (opcional)", placeholder="Ex: 000.000.000-00")

                        senha_cli_in = st.text_input(
                            "🔑 Senha de acesso do cliente na loja (opcional)",
                            type="password",
                            placeholder="Defina uma senha para o cliente logar na loja (mínimo 6 caracteres)",
                        )

                    # CARD 2: DADOS DE ENTREGA
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Dados de entrega</div>', unsafe_allow_html=True)
                        col_de1, col_de2 = st.columns([1, 2.5])
                        with col_de1:
                            cep_cli_in = st.text_input("CEP", placeholder="69000-000")
                        with col_de2:
                            end_cli_in = st.text_input("Endereço completo", placeholder="Rua, Número, Bairro, Cidade/UF")

                    # CARD 3: TABELAS DE PREÇOS
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Tabelas de preços</div>', unsafe_allow_html=True)
                        st.caption("Selecione uma tabela para dar acesso aos novos preços de atacado para esse cliente.")
                        tabela_cli_in = st.selectbox(
                            "Tabela vinculada",
                            ["Tabela Padrão (Varejo)", "Tabela Aluno / Cursos VIP", "Tabela Atacado Tags"],
                        )

                    c_btn_c1, c_btn_c2 = st.columns([4, 1.2])
                    submit_cli = c_btn_c2.form_submit_button("Adicionar", type="primary", use_container_width=True)

                c_canc1, c_canc2 = st.columns([4, 1.2])
                with c_canc2:
                    if st.button("Cancelar", key="btn_cancelar_add_cli", use_container_width=True):
                        st.session_state["sub_aba_cli"] = "📋 Lista de clientes"
                        st.rerun()

                if submit_cli:
                    if not nome_cli_in:
                        st.error("Informe o Nome e sobrenome do cliente.")
                    else:
                        hash_s_add = gerar_hash_senha(senha_cli_in.strip()) if senha_cli_in and senha_cli_in.strip() else None
                        try:
                            payload_new_cli = {
                                "nome": nome_cli_in,
                                "cpf_cnpj": cpf_cli_in or None,
                                "whatsapp": tel_cli_in or None,
                                "email": email_cli_in.strip().lower() if email_cli_in else None,
                                "endereco_completo": end_cli_in or None,
                                "cep": cep_cli_in or None,
                                "tabela_preco": tabela_cli_in,
                            }
                            if hash_s_add:
                                payload_new_cli["senha"] = hash_s_add
                            supabase.table("clientes").insert(payload_new_cli).execute()
                        except Exception:
                            pass
                        st.session_state["clientes_extras"].append({
                            "nome": nome_cli_in,
                            "cpf": cpf_cli_in or "Não informado",
                            "whatsapp": tel_cli_in or "Não informado",
                            "email": email_cli_in or "Não informado",
                            "endereco": end_cli_in or "Não informado",
                            "cep": cep_cli_in or "Não informado",
                            "tabela": tabela_cli_in,
                            "total_pedidos": 0,
                        })
                        st.success(f"🎉 Cliente **{nome_cli_in}** adicionado com sucesso!")
                        st.session_state["sub_aba_cli"] = "📋 Lista de clientes"
                        st.rerun()

            elif sub_aba_cli == "🔑 Alterar Senha de Usuários":
                st.markdown("### 🔑 Central de Controle de Senhas (Clientes & Administrador)")
                st.caption("Altere imediatamente a senha de acesso de qualquer cliente cadastrado ou gerencie sua própria senha de administrador.")

                col_pw_cli, col_pw_adm = st.columns([1.45, 1.15])

                with col_pw_cli:
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">👤 Redefinir Senha de Cliente da Loja</div>', unsafe_allow_html=True)
                        st.caption("Selecione um cliente da lista ou digite o E-mail / CPF para definir uma nova senha na hora:")

                        lista_clientes_db = []
                        try:
                            r_cl_pw = supabase.table("clientes").select("*").order("nome").execute()
                            lista_clientes_db = r_cl_pw.data or []
                        except Exception:
                            lista_clientes_db = []

                        opcoes_sel_cli = ["-- Digitar E-mail ou CPF manualmente --"]
                        mapa_sel_cli = {}
                        for c_item_pw in lista_clientes_db:
                            rotulo_c = f"{c_item_pw.get('nome', 'Cliente')} | E-mail: {c_item_pw.get('email') or '-'} | CPF: {c_item_pw.get('cpf_cnpj') or '-'}"
                            opcoes_sel_cli.append(rotulo_c)
                            mapa_sel_cli[rotulo_c] = c_item_pw

                        escolha_cli_pw = st.selectbox("Selecionar cliente cadastrado:", opcoes_sel_cli, key="sel_cli_reset_pw")
                        cli_selecionado_obj = mapa_sel_cli.get(escolha_cli_pw)

                        with st.form("form_admin_reset_senha_cliente"):
                            ident_manual_pw = st.text_input(
                                "Ou informe o E-mail / CPF do cliente (caso não esteja na lista acima):",
                                value=(cli_selecionado_obj.get("email") or cli_selecionado_obj.get("cpf_cnpj") or "") if cli_selecionado_obj else "",
                                placeholder="cliente@email.com ou 000.000.000-00",
                            )
                            c_np1, c_np2 = st.columns(2)
                            nova_senha_u = c_np1.text_input("Nova Senha do Usuário *", type="password", placeholder="Mínimo 6 caracteres")
                            conf_senha_u = c_np2.text_input("Confirmar Nova Senha *", type="password", placeholder="Repita a senha")

                            btn_salvar_pw_u = st.form_submit_button("💾 Alterar Senha do Cliente Agora", type="primary", use_container_width=True)

                            if btn_salvar_pw_u:
                                ident_alvo = ident_manual_pw.strip()
                                if not cli_selecionado_obj and not ident_alvo:
                                    st.error("Selecione um cliente na lista ou digite o E-mail / CPF.")
                                elif not nova_senha_u or len(nova_senha_u.strip()) < 4:
                                    st.error("A nova senha deve ter pelo menos 4 caracteres (recomendado 6+).")
                                elif nova_senha_u != conf_senha_u:
                                    st.error("As senhas digitadas não conferem.")
                                else:
                                    hash_pw_novo = gerar_hash_senha(nova_senha_u.strip())
                                    sucesso_up = False
                                    nome_exib = cli_selecionado_obj.get("nome") if cli_selecionado_obj else ident_alvo
                                    auth_uid_alvo = cli_selecionado_obj.get("auth_uid") if cli_selecionado_obj else None

                                    try:
                                        if cli_selecionado_obj and cli_selecionado_obj.get("id"):
                                            supabase.table("clientes").update({"senha": hash_pw_novo}).eq("id", cli_selecionado_obj["id"]).execute()
                                            sucesso_up = True
                                        elif "@" in ident_alvo:
                                            r_u_em = supabase.table("clientes").update({"senha": hash_pw_novo}).ilike("email", ident_alvo.lower()).execute()
                                            if r_u_em.data:
                                                sucesso_up = True
                                                nome_exib = r_u_em.data[0].get("nome", ident_alvo)
                                                auth_uid_alvo = r_u_em.data[0].get("auth_uid")
                                        if not sucesso_up and ident_alvo:
                                            r_u_cpf = supabase.table("clientes").update({"senha": hash_pw_novo}).eq("cpf_cnpj", ident_alvo).execute()
                                            if r_u_cpf.data:
                                                sucesso_up = True
                                                nome_exib = r_u_cpf.data[0].get("nome", ident_alvo)
                                                auth_uid_alvo = r_u_cpf.data[0].get("auth_uid")
                                        if not sucesso_up and ident_alvo:
                                            # Criar registro se ainda não existia na tabela clientes
                                            eh_email = "@" in ident_alvo
                                            supabase.table("clientes").insert({
                                                "nome": ident_alvo.split("@")[0].title() if eh_email else f"Cliente {ident_alvo}",
                                                "email": ident_alvo.lower() if eh_email else None,
                                                "cpf_cnpj": None if eh_email else ident_alvo,
                                                "senha": hash_pw_novo,
                                                "tabela_preco": "Varejo",
                                            }).execute()
                                            sucesso_up = True
                                    except Exception as e_db_pw:
                                        st.warning(f"Aviso ao atualizar tabela: {e_db_pw}")

                                    # Também sincroniza com Supabase Auth Admin se houver chave service_role
                                    srv_key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_SERVICE_ROLE")
                                    if srv_key and auth_uid_alvo:
                                        try:
                                            sup_adm = create_client(st.secrets["SUPABASE_URL"], srv_key)
                                            sup_adm.auth.admin.update_user_by_id(auth_uid_alvo, {"password": nova_senha_u.strip()})
                                        except Exception:
                                            pass

                                    # Atualiza cache local persistente
                                    contas_loc = st.session_state.setdefault("contas_clientes_local", {})
                                    if ident_alvo:
                                        k_l = ident_alvo.lower()
                                        if k_l in contas_loc:
                                            contas_loc[k_l]["senha"] = hash_pw_novo
                                        k_num = re.sub(r"\D", "", ident_alvo)
                                        if k_num and k_num in contas_loc:
                                            contas_loc[k_num]["senha"] = hash_pw_novo
                                    salvar_estado_persistente()
                                    st.success(f"✅ Senha de **{nome_exib}** redefinida com sucesso! O cliente já pode entrar usando a nova senha.")

                with col_pw_adm:
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">🛡️ Alterar Minha Senha de Administrador</div>', unsafe_allow_html=True)
                        st.caption("Atualize a senha da sua conta de Administrador no Supabase Auth:")
                        with st.form("form_admin_mudar_propria_senha"):
                            nova_s_adm = st.text_input("Nova Senha do Admin (mín. 6 dígitos) *", type="password")
                            conf_s_adm = st.text_input("Confirmar Nova Senha *", type="password")
                            btn_up_adm_pw = st.form_submit_button("🔐 Atualizar Senha do Admin", use_container_width=True)
                            if btn_up_adm_pw:
                                if not nova_s_adm or len(nova_s_adm) < 6:
                                    st.error("A senha do Supabase Auth deve ter no mínimo 6 caracteres.")
                                elif nova_s_adm != conf_s_adm:
                                    st.error("As senhas não conferem.")
                                else:
                                    try:
                                        supabase.auth.update_user({"password": nova_s_adm})
                                        st.success("✅ Senha de Administrador atualizada no Supabase Auth!")
                                    except Exception as e_adm_pw:
                                        st.error(f"Para alterar a senha do Admin no Supabase Auth, entre usando a aba 'Entrar com Supabase'. Detalhe: {e_adm_pw}")

                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">📧 Enviar E-mail de Recuperação</div>', unsafe_allow_html=True)
                        st.caption("Prefere que o próprio usuário escolha a senha por e-mail?")
                        email_envio_rec = st.text_input("E-mail do usuário:", placeholder="usuario@email.com", key="adm_inp_email_rec")
                        if st.button("📨 Disparar Link de Redefinição (Supabase)", use_container_width=True):
                            if not email_envio_rec or "@" not in email_envio_rec:
                                st.warning("Digite um e-mail válido.")
                            else:
                                try:
                                    supabase.auth.reset_password_for_email(email_envio_rec.strip().lower())
                                    st.success(f"✅ Link enviado para **{email_envio_rec}**!")
                                except Exception as e_rec_adm:
                                    st.error(f"Erro ao enviar e-mail: {e_rec_adm}")

            elif sub_aba_cli == "🎧 Chamados de Suporte":
                st.markdown("### 🎧 Central de Atendimento & Chamados de Clientes")
                st.caption("Acompanhe e responda aos chamados abertos pelos clientes na Loja Online.")

                chamados_lista = []
                try:
                    res_ch = supabase.table("chamados_suporte").select("*").order("id", desc=True).execute()
                    chamados_lista = res_ch.data or []
                except Exception:
                    chamados_lista = []

                ids_ch_db = {str(ch.get("id")) for ch in chamados_lista}
                for ch_loc in reversed(st.session_state.get("chamados_suporte_local", [])):
                    if str(ch_loc.get("id")) not in ids_ch_db:
                        chamados_lista.append(ch_loc)

                if not chamados_lista:
                    st.info("Nenhum chamado de suporte aberto pelos clientes no momento.")
                else:
                    for idx_ch, ch in enumerate(chamados_lista):
                        st_ch = ch.get("status", "aberto")
                        cor_ch = {"aberto": "#F59E0B", "em_atendimento": "#3B82F6", "resolvido": "#10B981"}.get(st_ch, "#64748B")
                        with st.container(border=True):
                            c_ch1, c_ch2 = st.columns([3.2, 1.8])
                            with c_ch1:
                                ped_ref = f" • Pedido #{ch['pedido_id']}" if ch.get("pedido_id") else ""
                                st.markdown(
                                    f"**Chamado #{ch.get('id', idx_ch + 1)} — {ch.get('assunto', 'Atendimento')}**{ped_ref} "
                                    f"<span style='background:{cor_ch}22; color:{cor_ch}; border:1px solid {cor_ch}55; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700; text-transform:uppercase;'>{st_ch}</span>",
                                    unsafe_allow_html=True,
                                )
                                st.caption(f"👤 Cliente: **{ch.get('cliente_nome', 'Cliente')}** | 📱 WhatsApp: `{ch.get('cliente_whatsapp', '-')}` | ✉️ E-mail: `{ch.get('cliente_email', '-')}`")
                                st.markdown(f"💬 **Mensagem do Cliente:**\n> {ch.get('mensagem', '')}")
                                resp_atual = ch.get("resposta_admin") or ""
                                nova_resp = st.text_area(
                                    "Sua resposta oficial (visível na conta do cliente):",
                                    value=resp_atual,
                                    placeholder="Digite a orientação, código de rastreio ou solução para o cliente...",
                                    key=f"adm_resp_ch_{ch.get('id', idx_ch)}",
                                    height=75,
                                )
                            with c_ch2:
                                ops_st_ch = ["aberto", "em_atendimento", "resolvido"]
                                idx_st_ch = ops_st_ch.index(st_ch) if st_ch in ops_st_ch else 0
                                novo_st_ch = st.selectbox("Status do Chamado", ops_st_ch, index=idx_st_ch, key=f"adm_st_ch_{ch.get('id', idx_ch)}")
                                if st.button("💾 Salvar Resposta / Status", key=f"btn_sv_ch_{ch.get('id', idx_ch)}", type="primary", use_container_width=True):
                                    try:
                                        supabase.table("chamados_suporte").update({
                                            "status": novo_st_ch,
                                            "resposta_admin": nova_resp,
                                        }).eq("id", ch.get("id")).execute()
                                    except Exception:
                                        pass
                                    for c_l in st.session_state.get("chamados_suporte_local", []):
                                        if str(c_l.get("id")) == str(ch.get("id")):
                                            c_l["status"] = novo_st_ch
                                            c_l["resposta_admin"] = nova_resp
                                    salvar_estado_persistente()
                                    st.success("Chamado atualizado!")
                                    st.rerun()

                                num_w_ch = re.sub(r"\D", "", str(ch.get("cliente_whatsapp", "")))
                                if num_w_ch:
                                    msg_w_sup = f"Olá {ch.get('cliente_nome')}! Sobre seu chamado ({ch.get('assunto')}) na TagsInfor: {nova_resp or 'Como podemos ajudar?'}"
                                    st.link_button(
                                        "💬 Responder no WhatsApp",
                                        f"https://wa.me/55{num_w_ch}?text={urllib.parse.quote(msg_w_sup)}",
                                        use_container_width=True,
                                    )

        # =================================================================
        # 6. ABA CRIAR CUPOM (DESCONTOS - IDÊNTICO AO SEU PRINT)
        # =================================================================
        elif aba_admin == "🎟️ Criar cupom":
            opcoes_cup = ["➕ Novo cupom", "📋 Cupons ativos"]
            if "sub_aba_cup" not in st.session_state or st.session_state["sub_aba_cup"] not in opcoes_cup:
                st.session_state["sub_aba_cup"] = "➕ Novo cupom"

            st.markdown('<h1 class="admin-page-title">Criar cupom de desconto</h1>', unsafe_allow_html=True)

            col_cp_b1, col_cp_b2, _ = st.columns([1.4, 1.4, 3])
            with col_cp_b1:
                st.button(
                    "➕ Novo cupom",
                    key="btn_tab_cup_new",
                    type="primary" if st.session_state["sub_aba_cup"] == "➕ Novo cupom" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cup", "➕ Novo cupom"),
                )
            with col_cp_b2:
                st.button(
                    "📋 Cupons ativos",
                    key="btn_tab_cup_list",
                    type="primary" if st.session_state["sub_aba_cup"] == "📋 Cupons ativos" else "secondary",
                    use_container_width=True,
                    on_click=ir_para_sub_aba,
                    args=("sub_aba_cup", "📋 Cupons ativos"),
                )

            sub_aba_cup = st.session_state["sub_aba_cup"]

            if sub_aba_cup == "➕ Novo cupom":
                with st.form("form_criar_cupom_nuvem", clear_on_submit=True):
                    # CARD 1: CÓDIGO DO CUPOM
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Código do cupom</div>', unsafe_allow_html=True)
                        cod_cupom_in = st.text_input("Código promocional *", placeholder="Ex: PRIMEIRACOMPRA, TAGS10 ou PROMOPIX").strip().upper()
                        st.caption("Este é o código que seu cliente deverá inserir no momento da compra para receber o desconto.")

                    # CARD 2: TIPO DE DESCONTO
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Tipo de desconto</div>', unsafe_allow_html=True)
                        tipo_desc_in = st.radio("Modalidade", ["Porcentagem (%)", "Valor fixo (R$)", "Frete grátis"], horizontal=True)
                        val_desc_in = st.number_input("Valor do desconto *", min_value=0.0, value=10.0, step=1.0)

                    # CARD 3: LIMITES DE USO
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">Limites de uso</div>', unsafe_allow_html=True)
                        min_carrinho_in = st.number_input("Valor mínimo do pedido para aplicar o cupom (R$)", min_value=0.0, value=0.0, step=10.0)
                        limite_usos = st.number_input("Quantidade máxima de utilizações (0 = Ilimitado)", min_value=0, value=100, step=10)
                        uso_unico = st.checkbox("Limitar a 1 uso por cliente", value=True)

                    col_cp1, col_cp2 = st.columns([3.8, 1.2])
                    if col_cp2.form_submit_button("Criar cupom", type="primary", use_container_width=True):
                        if not cod_cupom_in:
                            st.error("Digite o código do cupom.")
                        else:
                            tipo_cup = "Porcentagem" if "Porcentagem" in tipo_desc_in else ("Valor fixo" if "fixo" in tipo_desc_in else "Frete grátis")
                            novo_cp_dict = {
                                "codigo": cod_cupom_in,
                                "tipo": tipo_cup,
                                "valor": float(val_desc_in),
                                "min_carrinho": float(min_carrinho_in),
                                "limite_usos": int(limite_usos),
                                "ativo": True,
                            }
                            try:
                                supabase.table("cupons").insert(novo_cp_dict).execute()
                            except Exception:
                                pass
                            st.session_state["cupons"].append(novo_cp_dict)
                            st.success(f"🎉 Cupom **{cod_cupom_in}** criado com sucesso! Já pode ser usado pelos clientes.")
                            st.session_state["sub_aba_cup"] = "📋 Cupons ativos"
                            st.rerun()

            elif sub_aba_cup == "📋 Cupons ativos":
                st.caption(f"Total de {len(st.session_state['cupons'])} cupons configurados")
                for i, c_item in enumerate(st.session_state["cupons"]):
                    with st.container(border=True):
                        c_cp1, c_cp2, c_cp3 = st.columns([3, 3, 2])
                        with c_cp1:
                            tipo_s = c_item.get("tipo", "Porcentagem")
                            if tipo_s == "Porcentagem":
                                val_s = f"{c_item['valor']:.0f}% OFF"
                            elif tipo_s == "Valor fixo":
                                val_s = f"R$ {c_item['valor']:.2f} OFF"
                            else:
                                val_s = "Frete Grátis"
                            st.markdown(f"🏷️ **Cupom:** <span style='background:#DCFCE7; color:#15803D; font-weight:800; padding:4px 8px; border-radius:6px;'>{c_item['codigo']}</span> — **{val_s}**", unsafe_allow_html=True)
                        with c_cp2:
                            min_val = c_item.get("min_carrinho", 0)
                            if min_val > 0:
                                st.write(f"Válido para pedidos a partir de R$ {min_val:.2f}")
                            else:
                                st.write("Válido para qualquer valor de pedido")
                        with c_cp3:
                            if st.button("🗑️ Excluir Cupom", key=f"del_cup_{i}", use_container_width=True):
                                try:
                                    supabase.table("cupons").delete().eq("codigo", c_item.get("codigo")).execute()
                                except Exception:
                                    pass
                                st.session_state["cupons"].pop(i)
                                st.success("Cupom removido!")
                                st.rerun()

        # =================================================================
        # 7. ABA VENDAS & PEDIDOS
        # =================================================================
        elif aba_admin == "🛒 Vendas & Pedidos":
            st.markdown('<h1 class="admin-page-title">Vendas & Pedidos</h1>', unsafe_allow_html=True)
            res_ped = supabase.table("pedidos").select("*").order("id", desc=True).execute()
            lista_ped = res_ped.data or []

            if not lista_ped:
                st.info("Nenhuma venda registrada até o momento.")
            else:
                m1, m2, m3 = st.columns(3)
                fat = sum(float(p["valor_total"]) for p in lista_ped)
                m1.metric("Faturamento", f"R$ {fat:.2f}")
                m2.metric("Total de Pedidos", len(lista_ped))
                m3.metric("Aguardando Pix", len([p for p in lista_ped if p.get("status_pagamento") == "pendente"]))
                st.divider()

                for ped in lista_ped:
                    with st.container(border=True):
                        c1, c2, c3 = st.columns([3.2, 2.8, 2.2])
                        
                        st_atual = ped.get("status_pagamento", "pendente")
                        rastreio_atual = obter_rastreio_pedido(ped)
                        badge_color = {
                            "pago": "#16A34A",
                            "enviado": "#2563EB",
                            "entregue": "#059669",
                            "cancelado": "#DC2626",
                            "pendente": "#D97706",
                        }.get(st_atual, "#64748B")

                        c1.markdown(f"### Pedido #{ped['id']} — {ped['cliente_nome']}")
                        rastreio_badge = (
                            f"&nbsp;<span style='background:#1E293B; color:#38BDF8; border:1px solid #0284C7; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.78rem;'>🚚 Rastreio: {rastreio_atual}</span>"
                            if rastreio_atual
                            else ""
                        )
                        c1.markdown(
                            f"<span style='background:{badge_color}22; color:{badge_color}; border:1px solid {badge_color}55; padding:3px 10px; border-radius:12px; font-weight:700; font-size:0.8rem; text-transform:uppercase;'>Status: {st_atual}</span>{rastreio_badge}",
                            unsafe_allow_html=True,
                        )
                        c1.write(f"📱 WhatsApp: `{ped['cliente_whatsapp']}` | 📄 CPF: `{ped['cliente_cpf']}`")
                        c1.write(f"📍 Endereço: {ped['endereco_completo']} (CEP: {ped['cep']})")

                        c2.markdown(f"💰 **Total: R$ {float(ped['valor_total']):.2f}**")
                        c2.caption(f"Produtos: R$ {float(ped.get('valor_produtos', ped['valor_total'])):.2f} | Frete: R$ {float(ped.get('valor_frete', 0)):.2f} | Desconto: R$ {float(ped.get('valor_desconto', 0)):.2f}")
                        for it in ped.get("itens", []):
                            c2.caption(f"• {it.get('qtd', 1)}x {it.get('titulo', 'Item')}")

                        status_opcoes = ["pendente", "pago", "enviado", "entregue", "cancelado"]
                        idx_st = status_opcoes.index(st_atual) if st_atual in status_opcoes else 0
                        novo_st = c3.selectbox("Mudar Status Rápido", status_opcoes, index=idx_st, key=f"adm_v_st_{ped['id']}")
                        novo_rast = c3.text_input(
                            "Código de Rastreio",
                            value=rastreio_atual,
                            placeholder="Ex: AA123456789BR",
                            key=f"adm_v_rast_{ped['id']}",
                        )
                        if c3.button("💾 Salvar Status & Rastreio", key=f"btn_v_st_{ped['id']}", type="primary", use_container_width=True):
                            salvar_rastreio_no_pedido(ped, novo_rast, novo_status=novo_st)
                            st.success("Status e rastreio atualizados!")
                            st.rerun()

                        # Botões de Ação Completa (Editar Dados, WhatsApp, Excluir)
                        col_ac1, col_ac2, col_ac3 = st.columns([1.4, 1.2, 1.2])

                        with col_ac1:
                            with st.popover("✏️ Editar Pedido Completo", use_container_width=True):
                                st.markdown(f"#### ✏️ Editar Pedido #{ped['id']}")
                                st.caption("Altere dados do cliente, endereço, código de rastreio, valores ou status diretamente no Supabase:")

                                with st.form(f"form_editar_pedido_{ped['id']}"):
                                    c_st_r1, c_st_r2 = st.columns(2)
                                    ed_status = c_st_r1.selectbox("Status Geral", status_opcoes, index=idx_st)
                                    ed_rastreio = c_st_r2.text_input("Código de Rastreio", value=rastreio_atual, placeholder="Ex: AA123456789BR")
                                    
                                    col_ed1, col_ed2 = st.columns(2)
                                    ed_nome = col_ed1.text_input("Nome do Cliente", value=ped.get("cliente_nome", ""))
                                    ed_whats = col_ed2.text_input("WhatsApp", value=ped.get("cliente_whatsapp", ""))

                                    col_ed3, col_ed4 = st.columns(2)
                                    ed_cpf = col_ed3.text_input("CPF / CNPJ", value=ped.get("cliente_cpf", ""))
                                    ed_email = col_ed4.text_input("E-mail", value=ped.get("cliente_email", ""))

                                    col_ed5, col_ed6 = st.columns([1, 2])
                                    ed_cep = col_ed5.text_input("CEP", value=ped.get("cep", ""))
                                    ed_end = col_ed6.text_input("Endereço Completo", value=ped.get("endereco_completo", ""))

                                    col_v1, col_v2, col_v3 = st.columns(3)
                                    ed_prods = col_v1.number_input("Produtos (R$)", value=float(ped.get("valor_produtos", ped["valor_total"])), step=10.0)
                                    ed_frete = col_v2.number_input("Frete (R$)", value=float(ped.get("valor_frete", 0.0)), step=5.0)
                                    ed_desc = col_v3.number_input("Desconto (R$)", value=float(ped.get("valor_desconto", 0.0)), step=5.0)

                                    ed_total = max(0.0, float(ed_prods) + float(ed_frete) - float(ed_desc))
                                    st.write(f"💵 **Novo Valor Total Calculado: R$ {ed_total:.2f}**")

                                    btn_salvar_ed = st.form_submit_button("💾 Salvar Alterações no Supabase", type="primary", use_container_width=True)
                                    if btn_salvar_ed:
                                        try:
                                            salvar_rastreio_no_pedido(ped, ed_rastreio, novo_status=ed_status)
                                            supabase.table("pedidos").update({
                                                "status_pagamento": ed_status,
                                                "cliente_nome": ed_nome,
                                                "cliente_whatsapp": ed_whats,
                                                "cliente_cpf": ed_cpf,
                                                "cliente_email": ed_email,
                                                "cep": ed_cep,
                                                "endereco_completo": ed_end,
                                                "valor_produtos": float(ed_prods),
                                                "valor_frete": float(ed_frete),
                                                "valor_desconto": float(ed_desc),
                                                "valor_total": float(ed_total),
                                            }).eq("id", ped["id"]).execute()
                                            st.success("✅ Pedido atualizado com sucesso no Supabase!")
                                            st.rerun()
                                        except Exception as e_up_ped:
                                            st.error(f"Erro ao salvar pedido: {e_up_ped}")

                        with col_ac2:
                            num_cli = re.sub(r"\D", "", ped.get("cliente_whatsapp", ""))
                            rastreio_msg = f" Código de rastreio: {rastreio_atual}." if rastreio_atual else ""
                            msg_cli = f"Olá {ped.get('cliente_nome')}! Sou da TagsInfor sobre o seu Pedido #{ped['id']} (Status: {st_atual.upper()}).{rastreio_msg}"
                            url_cli = f"https://wa.me/55{num_cli}?text={urllib.parse.quote(msg_cli)}"
                            st.link_button("💬 WhatsApp", url_cli, use_container_width=True)

                        with col_ac3:
                            with st.popover("🗑️ Excluir Pedido", use_container_width=True):
                                st.warning(f"Excluir definitivamente o Pedido #{ped['id']} do banco?")
                                if st.button(f"Confirmar Exclusão #{ped['id']}", key=f"btn_del_ped_{ped['id']}", type="primary", use_container_width=True):
                                    try:
                                        supabase.table("pedidos").delete().eq("id", ped["id"]).execute()
                                        st.success(f"Pedido #{ped['id']} excluído com sucesso!")
                                        st.rerun()
                                    except Exception as e_del_ped:
                                        st.error(f"Erro ao excluir pedido: {e_del_ped}")

        # =================================================================
        # 8. ABA DOCUMENTOS FISCAIS (NF-E & DC-E - NUVEMSHOP)
        # =================================================================
        elif aba_admin == "📄 Documentos fiscais (NF-e)":
            st.markdown('<h1 class="admin-page-title">Documentos Fiscais (NF-e & DC-e)</h1>', unsafe_allow_html=True)

            fisc = st.session_state["dados_fiscais_loja"]

            opcoes_sub_fisc = ["📋 Pedidos & Emissão Fiscal", "⚙️ Configurar Notas Fiscais", "📊 Relatório para Contabilidade (CSV)"]
            if "sub_aba_fisc" not in st.session_state or st.session_state["sub_aba_fisc"] not in opcoes_sub_fisc:
                st.session_state["sub_aba_fisc"] = "📋 Pedidos & Emissão Fiscal"

            col_fb1, col_fb2, col_fb3 = st.columns(3)
            for idx_fb, (col_f, op_f) in enumerate(zip([col_fb1, col_fb2, col_fb3], opcoes_sub_fisc)):
                with col_f:
                    st.button(
                        op_f,
                        key=f"btn_tab_fisc_{idx_fb}",
                        type="primary" if st.session_state["sub_aba_fisc"] == op_f else "secondary",
                        use_container_width=True,
                        on_click=ir_para_sub_aba,
                        args=("sub_aba_fisc", op_f),
                    )

            sub_aba_fisc = st.session_state["sub_aba_fisc"]

            if sub_aba_fisc == "📋 Pedidos & Emissão Fiscal":
                res_ped = supabase.table("pedidos").select("*").order("id", desc=True).execute()
                lista_ped = res_ped.data or []

                if not lista_ped:
                    st.markdown(
                        """
                        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:36px; text-align:center;">
                            <div style="font-size:3rem; margin-bottom:10px;">📄</div>
                            <h3 style="color:#0F172A;">Nenhum pedido aguardando documento fiscal</h3>
                            <p style="color:#64748B; font-size:0.95rem;">Assim que um cliente realizar um pedido na sua loja, os dados fiscais completos aparecerão aqui prontos para você gerar a Declaração de Conteúdo (DC-e) ou DANFE em 1 clique.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.caption(f"Exibindo {len(lista_ped)} pedido(s) com dados fiscais disponíveis:")

                    for ped in lista_ped:
                        with st.container(border=True):
                            c_f1, c_f2, c_f3 = st.columns([3.2, 3, 2])
                            
                            itens_ped = ped.get("itens", [])
                            fiscal_ped = itens_ped[0].get("fiscal", {}) if itens_ped else {}
                            doc_val = fiscal_ped.get("documento") or ped.get("cliente_cpf", "-")
                            email_val = fiscal_ped.get("email") or "Não informado"

                            with c_f1:
                                st.markdown(f"**Pedido #{ped['id']}** — **{ped['cliente_nome']}**")
                                st.write(f"📄 **CPF/CNPJ:** `{doc_val}`")
                                st.write(f"✉️ **E-mail:** `{email_val}` | 📱 **WhatsApp:** `{ped.get('cliente_whatsapp', '-')}`")

                            with c_f2:
                                st.markdown(f"📍 **Endereço Fiscal:**")
                                st.caption(f"{ped.get('endereco_completo', '-')}")
                                st.write(f"💰 **Total:** :green[R$ {float(ped.get('valor_total', 0)):.2f}]")

                            with c_f3:
                                st.caption(f"Status: **{ped.get('status_pagamento', 'pendente').upper()}**")

                            # Ações Fiscais em Popovers
                            col_b1, col_b2, col_b3 = st.columns(3)
                            
                            with col_b1:
                                with st.popover("🖨️ Declaração Correios (DC-e)", use_container_width=True):
                                    st.caption("Modelo oficial exigido pelos Correios / Transportadoras:")
                                    dc_html = gerar_declaracao_conteudo_html(ped, fisc)
                                    st.markdown(dc_html, unsafe_allow_html=True)
                                    st.download_button(
                                        "📥 Baixar Declaração (.html)",
                                        data=dc_html,
                                        file_name=f"declaracao_conteudo_pedido_{ped['id']}.html",
                                        mime="text/html",
                                        key=f"dl_dc_{ped['id']}",
                                        use_container_width=True,
                                    )

                            with col_b2:
                                with st.popover("🧾 Ver DANFE / Recibo", use_container_width=True):
                                    st.caption("Espelho fiscal para impressão ou envio ao cliente:")
                                    danfe_html = gerar_danfe_recibo_html(ped, fisc)
                                    st.markdown(danfe_html, unsafe_allow_html=True)
                                    st.download_button(
                                        "📥 Baixar DANFE (.html)",
                                        data=danfe_html,
                                        file_name=f"danfe_pedido_{ped['id']}.html",
                                        mime="text/html",
                                        key=f"dl_danfe_{ped['id']}",
                                        use_container_width=True,
                                    )

                            with col_b3:
                                export_dados = {
                                    "pedido_id": ped["id"],
                                    "data": ped.get("created_at"),
                                    "emitente": {
                                        "razao_social": fisc.get("razao_social"),
                                        "cnpj": fisc.get("cnpj"),
                                        "ie": fisc.get("inscricao_estadual"),
                                        "endereco": f"{fisc.get('rua_origem')}, {fisc.get('numero_origem')}",
                                        "cidade": fisc.get("cidade_origem"),
                                        "uf": fisc.get("estado_origem"),
                                        "cep": fisc.get("cep_origem"),
                                    },
                                    "destinatario": {
                                        "nome": ped.get("cliente_nome"),
                                        "cpf_cnpj": doc_val,
                                        "email": email_val,
                                        "whatsapp": ped.get("cliente_whatsapp"),
                                        "endereco": ped.get("endereco_completo"),
                                        "cep": ped.get("cep"),
                                    },
                                    "itens": itens_ped,
                                    "valor_total": float(ped.get("valor_total", 0)),
                                    "meio_pagamento": "PIX",
                                }
                                json_export = json.dumps(export_dados, indent=2, ensure_ascii=False)
                                st.download_button(
                                    "📥 Exportar SEFAZ/Bling (.json)",
                                    data=json_export,
                                    file_name=f"fiscal_pedido_{ped['id']}.json",
                                    mime="application/json",
                                    key=f"dl_json_{ped['id']}",
                                    use_container_width=True,
                                )

            elif sub_aba_fisc == "⚙️ Configurar Notas Fiscais":
                st.markdown(
                    """
                    <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:14px; padding:24px; margin-bottom:20px;">
                        <h3 style="color:#15803D; margin-top:0;">Emita notas fiscais sem complicação</h3>
                        <p style="color:#166534; font-size:0.95rem; margin-bottom:12px;">
                            Configuração completa para emissão B2C de produtos físicos, cursos digitais e mentorias.
                            Suporte para <b>MEI (Microempreendedor Individual)</b> e <b>Simples Nacional</b>.
                        </p>
                        <div style="display:flex; gap:16px; flex-wrap:wrap;">
                            <span style="background:white; border:1px solid #BBF7D0; padding:6px 14px; border-radius:20px; font-size:0.85rem; color:#15803D; font-weight:700;">✓ Fácil e Integrado</span>
                            <span style="background:white; border:1px solid #BBF7D0; padding:6px 14px; border-radius:20px; font-size:0.85rem; color:#15803D; font-weight:700;">✓ Rápido e Sem Burocracia</span>
                            <span style="background:white; border:1px solid #BBF7D0; padding:6px 14px; border-radius:20px; font-size:0.85rem; color:#15803D; font-weight:700;">✓ Declaração Correios Automática</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                with st.form("form_config_fiscal_nuvem"):
                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">1. Dados da empresa</div>', unsafe_allow_html=True)
                        rs_in = st.text_input("Razão Social *", value=fisc.get("razao_social", "Tags Informática"), placeholder="Ex: Tags Informática LTDA")
                        nf_in = st.text_input("Nome Fantasia", value=fisc.get("nome_fantasia", "Tags Informática"), placeholder="Ex: Tags Informática")
                        c_cnpj1, c_cnpj2 = st.columns(2)
                        cnpj_in = c_cnpj1.text_input("CNPJ *", value=fisc.get("cnpj", "00.000.000/0001-00"), placeholder="00.000.000/0001-00")
                        ie_in = c_cnpj2.text_input("Inscrição Estadual (ou Isento)", value=fisc.get("inscricao_estadual", "Isento"), placeholder="Ex: Isento ou 000.000.000")

                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">2. Telefone de contato</div>', unsafe_allow_html=True)
                        st.caption("Esse telefone aparece no cabeçalho da nota fiscal e da DANFE da sua loja.")
                        tel_fisc_in = st.text_input("Telefone Fiscal", value=fisc.get("telefone_fiscal", WHATSAPP_LOJA), placeholder="Ex: 92981234567")

                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">3. Certificado digital A1 & Emissão</div>', unsafe_allow_html=True)
                        st.info("ℹ️ Para lojas MEI ou em fase inicial, o sistema gera a **Declaração de Conteúdo (DC-e)** oficial para envio nos Correios e o **Comprovante de Venda Fiscal**. Para emissão direta via SEFAZ com certificado digital A1 (.pfx/.p12), você pode exportar o arquivo pronto em 1 clique para o Bling, Tiny ou Focus NFe.")
                        cert_up = st.file_uploader("Certificado digital A1 (opcional)", type=["pfx", "p12"])
                        if cert_up:
                            st.success(f"Certificado {cert_up.name} anexado para emissão.")

                    with st.container(border=True):
                        st.markdown('<div class="nuvem-card-title">4. Informações fiscais & Numeração</div>', unsafe_allow_html=True)
                        regimes = ["MEI - Microempreendedor Individual", "Simples Nacional", "Lucro Presumido", "Autônomo / Pessoa Física"]
                        idx_reg = regimes.index(fisc.get("regime_tributario", regimes[0])) if fisc.get("regime_tributario") in regimes else 0
                        regime_in = st.selectbox("Regime Tributário *", regimes, index=idx_reg)

                        c_num1, c_num2, c_num3 = st.columns(3)
                        serie_in = c_num1.text_input("Série da NF-e", value=str(fisc.get("serie_nfe", "1")))
                        prox_in = c_num2.number_input("Próxima NF-e", min_value=1, value=int(fisc.get("proxima_nfe", 1)), step=1)
                        ncm_in = c_num3.text_input("NCM Padrão", value=fisc.get("ncm_padrao", "8471.60.52"), placeholder="8471.60.52")

                    c_btn_f1, c_btn_f2 = st.columns([4, 1.2])
                    if c_btn_f2.form_submit_button("Salvar configurações", type="primary", use_container_width=True):
                        fisc["razao_social"] = rs_in
                        fisc["nome_fantasia"] = nf_in
                        fisc["cnpj"] = cnpj_in
                        fisc["inscricao_estadual"] = ie_in
                        fisc["telefone_fiscal"] = tel_fisc_in
                        fisc["regime_tributario"] = regime_in
                        fisc["serie_nfe"] = serie_in
                        fisc["proxima_nfe"] = int(prox_in)
                        fisc["ncm_padrao"] = ncm_in
                        st.success("✅ Configurações fiscais salvas com sucesso!")
                        st.rerun()

            elif sub_aba_fisc == "📊 Relatório para Contabilidade (CSV)":
                st.markdown("### Relatório Mensal de Vendas & Documentos Fiscais")
                st.markdown("Exporte a planilha completa com todos os dados fiscais e cadastrais exigidos pelo seu Contador / Contabilidade.")

                res_ped = supabase.table("pedidos").select("*").order("id", desc=True).execute()
                lista_ped = res_ped.data or []

                if not lista_ped:
                    st.info("Nenhuma venda registrada até o momento.")
                else:
                    csv_linhas = ["Pedido_ID;Data;Cliente;Documento_CPF_CNPJ;Email;WhatsApp;Endereco_Completo;CEP;Itens;Valor_Total;Status_Pagamento"]
                    for p in lista_ped:
                        its = p.get("itens", [])
                        f_cli = its[0].get("fiscal", {}) if its else {}
                        doc_c = f_cli.get("documento") or p.get("cliente_cpf", "")
                        email_c = f_cli.get("email") or ""
                        whats_c = p.get("cliente_whatsapp", "")
                        end_c = p.get("endereco_completo", "").replace(";", " ")
                        cep_c = p.get("cep", "")
                        tit_its = " + ".join([f"{it.get('qtd', 1)}x {it.get('titulo', '')}" for it in its]).replace(";", " ")
                        val_c = f"{float(p.get('valor_total', 0)):.2f}"
                        dt_c = p.get("created_at", "")[:10]
                        st_c = p.get("status_pagamento", "pendente")
                        csv_linhas.append(f"{p['id']};{dt_c};{p.get('cliente_nome', '')};{doc_c};{email_c};{whats_c};{end_c};{cep_c};{tit_its};{val_c};{st_c}")

                    csv_conteudo = "\ufeff" + "\n".join(csv_linhas)
                    
                    st.dataframe(
                        [
                            {
                                "Pedido": p["id"],
                                "Cliente": p.get("cliente_nome"),
                                "CPF/CNPJ": (p.get("itens", [{}])[0].get("fiscal", {}).get("documento") or p.get("cliente_cpf")),
                                "Valor Total": f"R$ {float(p.get('valor_total', 0)):.2f}",
                                "Status": p.get("status_pagamento"),
                            }
                            for p in lista_ped
                        ],
                        use_container_width=True,
                    )

                    st.download_button(
                        "📥 Baixar Planilha para o Contador (.csv)",
                        data=csv_conteudo.encode("utf-8-sig"),
                        file_name=f"relatorio_fiscal_tagsinfor_{datetime.now().strftime('%Y_%m')}.csv",
                        mime="text/csv",
                        type="primary",
                        use_container_width=True,
                    )

        # =================================================================
        # 9. ABA CENTRO DE DISTRIBUIÇÃO (NUVEMSHOP - PRINT 1)
        # =================================================================
        elif aba_admin == "🏢 Centro de distribuição":
            st.markdown('<h1 class="admin-page-title">Definir centro de distribuição principal</h1>', unsafe_allow_html=True)
            st.markdown("Será usado como o principal local de envio ou armazenamento dos produtos da loja.")

            fisc = st.session_state["dados_fiscais_loja"]

            with st.form("form_centro_distribuicao"):
                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">Nome do local</div>', unsafe_allow_html=True)
                    loc_nome = st.text_input("Identificação do Centro *", value=fisc.get("local_nome", "Depósito Principal Tags Informática"), placeholder="Ex: Depósito Principal Tags Informática")

                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">Endereço de Origem do Envio</div>', unsafe_allow_html=True)
                    st.selectbox("País", ["Brasil"], disabled=True)
                    
                    c_cd1, c_cd2 = st.columns(2)
                    cep_orig = c_cd1.text_input("CEP *", value=fisc.get("cep_origem", "69050-010"), placeholder="69000-000")
                    uf_orig = c_cd2.text_input("Estado (UF) *", value=fisc.get("estado_origem", "AM"), max_chars=2)

                    c_cd3, c_cd4 = st.columns(2)
                    cid_orig = c_cd3.text_input("Cidade *", value=fisc.get("cidade_origem", "Manaus"))
                    bair_orig = c_cd4.text_input("Bairro *", value=fisc.get("bairro_origem", "Chapada"))

                    rua_orig = st.text_input("Rua / Logradouro *", value=fisc.get("rua_origem", "Av. Djalma Batista"))
                    
                    c_cd5, c_cd6 = st.columns(2)
                    num_orig = c_cd5.text_input("Número *", value=fisc.get("numero_origem", "1000"))
                    comp_orig = c_cd6.text_input("Complemento (opcional)", value=fisc.get("complemento_origem", "Sala 102"))

                with st.container(border=True):
                    st.markdown('<div class="nuvem-card-title">Estoque e Logística</div>', unsafe_allow_html=True)
                    st.caption("Este centro é o remetente oficial preenchido automaticamente nas Declarações de Conteúdo (DC-e) dos Correios e nas Notas Fiscais Eletrônicas (NF-e).")

                c_salv1, c_salv2 = st.columns([4, 1.2])
                if c_salv2.form_submit_button("Salvar centro de distribuição", type="primary", use_container_width=True):
                    fisc["local_nome"] = loc_nome
                    fisc["cep_origem"] = cep_orig
                    fisc["estado_origem"] = uf_orig.upper()
                    fisc["cidade_origem"] = cid_orig
                    fisc["bairro_origem"] = bair_orig
                    fisc["rua_origem"] = rua_orig
                    fisc["numero_origem"] = num_orig
                    fisc["complemento_origem"] = comp_orig
                    try:
                        res_cd_check = supabase.table("centro_distribuicao").select("id").limit(1).execute()
                        dados_up = {
                            "nome_local": loc_nome,
                            "cep": cep_orig,
                            "estado": uf_orig.upper(),
                            "cidade": cid_orig,
                            "bairro": bair_orig,
                            "logradouro": rua_orig,
                            "numero": num_orig,
                            "complemento": comp_orig,
                        }
                        if res_cd_check.data:
                            supabase.table("centro_distribuicao").update(dados_up).eq("id", res_cd_check.data[0]["id"]).execute()
                        else:
                            supabase.table("centro_distribuicao").insert(dados_up).execute()
                    except Exception:
                        pass
                    st.success("✅ Centro de distribuição atualizado com sucesso no Supabase!")
                    st.rerun()

        # =================================================================
        # 8. ABA PAGAMENTO PIX
        # =================================================================
        elif aba_admin == "💳 Pagamento Pix":
            st.markdown('<h1 class="admin-page-title">Configurações de Pagamento e Loja</h1>', unsafe_allow_html=True)
            with st.container(border=True):
                st.markdown('<div class="nuvem-card-title">🔑 Dados da sua Chave Pix</div>', unsafe_allow_html=True)
                st.write(f"• **Chave Pix Ativa:** `{CHAVE_PIX}`")
                st.write(f"• **Nome do Recebedor:** `{NOME_BENEFICIARIO}`")
                st.write(f"• **WhatsApp da Loja:** `{WHATSAPP_LOJA}`")
                st.write(f"• **Mercado Pago Automático:** `{'Ativo' if MP_TOKEN and not MP_TOKEN.startswith('APP_USR-seu') else 'Pix Direto Oficial BACEN'}`")
                st.info("💡 Para alterar estes dados da sua conta, edite o arquivo `.streamlit/secrets.toml`.")

    st.stop()


# =====================================================================
# ROTA 2: A LOJA OFICIAL (CLIENTES) - LOGIN, CARRINHO, RASTREIO E SUPORTE
# =====================================================================
cfg_loja = st.session_state.get("config_loja", {})
whats_num_clean = re.sub(r"\D", "", WHATSAPP_LOJA)

if cfg_loja.get("em_construcao", False):
    st.markdown(
        f"""
        <div style="text-align:center; padding: 80px 20px;">
            <h1 style="font-size:2.8rem; font-weight:800; color:#FFFFFF;">🚧 Estamos em Manutenção</h1>
            <p style="font-size:1.15rem; color:#94A3B8; max-width:600px; margin: 15px auto;">
                Nossa loja online está passando por melhorias no momento. Para atendimento imediato, clique no botão abaixo.
            </p>
            <a href="https://wa.me/55{whats_num_clean}?text=Ol%C3%A1,%20gostaria%20de%20atendimento" target="_blank" class="btn-whats-pay" style="max-width:320px; margin:20px auto; display:block;">
                💬 Falar no WhatsApp da Loja
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()


# Funções de Navegação, Carrinho e Autenticação do Cliente
def ir_para_aba_loja(destino: str):
    st.session_state["aba_loja_cliente"] = destino
    salvar_estado_persistente()


def adicionar_item_carrinho(prod: dict, ir_para_checkout: bool = False):
    carrinho = list(st.session_state.get("carrinho_cliente", []))
    pid = prod.get("id")
    max_est = int(prod.get("estoque") or 99) if prod.get("tipo_venda") == "estoque_proprio" else 99
    encontrado = False
    for item in carrinho:
        if item.get("id") == pid:
            item["qtd"] = min(max_est, int(item.get("qtd", 1)) + 1)
            item["preco_venda"] = float(prod.get("preco_venda", item.get("preco_venda", 0)))
            encontrado = True
            break
    if not encontrado:
        carrinho.append({
            "id": pid,
            "titulo": prod.get("titulo", "Produto"),
            "preco_venda": float(prod.get("preco_venda", 0)),
            "imagem_url": prod.get("imagem_url"),
            "tipo_venda": prod.get("tipo_venda", "direto"),
            "estoque": max_est,
            "ncm": prod.get("ncm", "8471.60.52"),
            "qtd": 1,
        })
    st.session_state["carrinho_cliente"] = carrinho
    sincronizar_carrinho_cliente()
    if ir_para_checkout:
        st.session_state["aba_loja_cliente"] = "carrinho"
        st.session_state["pedido_concluido"] = False
        salvar_estado_persistente()


def mesclar_carrinhos(carrinho_atual: list, carrinho_salvo: list) -> list:
    mapa = {}
    for it in (carrinho_salvo or []):
        if isinstance(it, dict) and it.get("id") is not None:
            mapa[it["id"]] = dict(it)
    for it in (carrinho_atual or []):
        if isinstance(it, dict) and it.get("id") is not None:
            pid = it["id"]
            if pid in mapa:
                mapa[pid]["qtd"] = int(mapa[pid].get("qtd", 1)) + int(it.get("qtd", 1))
            else:
                mapa[pid] = dict(it)
    return list(mapa.values())


def autenticar_cliente_loja(identificador: str, senha_digitada: str):
    """
    Autenticação Híbrida Oficial (Supabase Auth + public.clientes com Hash SHA-256 e filtro indexado):
    1. Aceita E-mail ou CPF/CNPJ (busca indexada em public.clientes).
    2. Valida no Supabase Auth (supabase.auth.sign_in_with_password).
    3. Caso o cliente já existisse na tabela public.clientes (compra anterior), migra/sincroniza automaticamente para o Supabase Auth.
    4. Restaura o carrinho salvo na conta do cliente.
    """
    ident_limpo = identificador.strip().lower()
    ident_num = re.sub(r"\D", "", ident_limpo)

    conta_achada = None
    # 1. Busca indexada rápida na tabela public.clientes do Supabase (evita baixar a tabela inteira)
    try:
        if "@" in ident_limpo:
            r_em = supabase.table("clientes").select("*").ilike("email", ident_limpo).limit(1).execute()
            if r_em.data:
                conta_achada = dict(r_em.data[0])
        if not conta_achada:
            r_cpf = supabase.table("clientes").select("*").eq("cpf_cnpj", identificador.strip()).limit(1).execute()
            if r_cpf.data:
                conta_achada = dict(r_cpf.data[0])
        if not conta_achada and ident_num and len(ident_num) >= 11:
            res_cl_all = supabase.table("clientes").select("*").execute()
            for c in (res_cl_all.data or []):
                cpf_num = re.sub(r"\D", "", str(c.get("cpf_cnpj") or ""))
                if ident_num == cpf_num:
                    conta_achada = dict(c)
                    break
    except Exception:
        pass

    # 2. Complementar com cache local persistente
    contas_loc = st.session_state.get("contas_clientes_local", {})
    conta_loc = contas_loc.get(ident_limpo) or (contas_loc.get(ident_num) if ident_num else None)
    if not conta_loc:
        for _, v_l in contas_loc.items():
            em_l = (v_l.get("email") or "").strip().lower()
            cpf_l = re.sub(r"\D", "", str(v_l.get("cpf_cnpj") or ""))
            if (ident_limpo and ident_limpo == em_l) or (ident_num and len(ident_num) >= 11 and ident_num == cpf_l):
                conta_loc = v_l
                break

    if conta_achada and conta_loc:
        if not conta_achada.get("senha") and conta_loc.get("senha"):
            conta_achada["senha"] = conta_loc["senha"]
        if not conta_achada.get("carrinho") and conta_loc.get("carrinho"):
            conta_achada["carrinho"] = conta_loc["carrinho"]
    elif not conta_achada and conta_loc:
        conta_achada = dict(conta_loc)

    # Descobrir o e-mail para autenticar no Supabase Auth
    email_auth = ident_limpo if "@" in ident_limpo else ((conta_achada.get("email") or "").strip().lower() if conta_achada else "")

    autenticado_supabase_auth = False
    auth_user_obj = None

    # 2.5 Priorizar validação da senha da tabela public.clientes (permite que o Admin altere a senha do cliente imediatamente)
    autenticado_pelo_banco = False
    if conta_achada and conta_achada.get("senha"):
        if verificar_senha_cliente(senha_digitada, conta_achada.get("senha")):
            autenticado_pelo_banco = True

    # 3. Tentar autenticação oficial no Supabase Auth (auth.users)
    if email_auth and "@" in email_auth:
        try:
            res_auth_cli = supabase.auth.sign_in_with_password({
                "email": email_auth,
                "password": senha_digitada,
            })
            if res_auth_cli and res_auth_cli.user:
                autenticado_supabase_auth = True
                auth_user_obj = res_auth_cli.user
        except Exception as e_sup_login:
            msg_err_sup = str(e_sup_login).lower()
            # Se o cliente já estava em public.clientes e a senha confere, sincroniza/cria no Supabase Auth
            if conta_achada and autenticado_pelo_banco:
                if len(senha_digitada) >= 6 and "email not confirmed" not in msg_err_sup:
                    try:
                        res_mig = supabase.auth.sign_up({
                            "email": email_auth,
                            "password": senha_digitada,
                            "options": {
                                "data": {
                                    "nome": conta_achada.get("nome", "Cliente"),
                                    "cpf_cnpj": conta_achada.get("cpf_cnpj", ""),
                                    "role": "cliente",
                                }
                            },
                        })
                        if res_mig and res_mig.user:
                            autenticado_supabase_auth = True
                            auth_user_obj = res_mig.user
                    except Exception:
                        pass

    # Se a senha conferiu pela tabela public.clientes (ex: redefinida pelo Admin), considera autenticado
    if autenticado_pelo_banco:
        autenticado_supabase_auth = True

    # Se autenticou via Supabase Auth mas ainda não tinha linha em public.clientes, cria agora
    if autenticado_supabase_auth and not conta_achada and auth_user_obj:
        meta_u = auth_user_obj.user_metadata or {}
        conta_achada = {
            "auth_uid": auth_user_obj.id,
            "nome": meta_u.get("nome") or email_auth.split("@")[0].title(),
            "cpf_cnpj": meta_u.get("cpf_cnpj") or "",
            "email": email_auth,
            "whatsapp": meta_u.get("whatsapp") or "",
            "cep": meta_u.get("cep") or "",
            "endereco_completo": meta_u.get("endereco_completo") or "",
            "tabela_preco": "Varejo",
            "carrinho": [],
        }
        try:
            r_ins_sync = supabase.table("clientes").insert({
                "nome": conta_achada["nome"],
                "cpf_cnpj": conta_achada["cpf_cnpj"] or None,
                "email": email_auth,
                "whatsapp": conta_achada["whatsapp"] or None,
                "tabela_preco": "Varejo",
            }).execute()
            if r_ins_sync.data:
                conta_achada["id"] = r_ins_sync.data[0].get("id")
        except Exception:
            pass

    if not conta_achada:
        return False, "Conta não encontrada com este E-mail ou CPF/CNPJ. Crie sua conta rápida ao lado!"

    senha_hash_segura = gerar_hash_senha(senha_digitada)

    # Validar senha caso ainda não tenha validado pelo Supabase Auth
    if not autenticado_supabase_auth:
        senha_cadastrada = conta_achada.get("senha")
        if senha_cadastrada and not verificar_senha_cliente(senha_digitada, senha_cadastrada):
            return False, "Senha incorreta. Verifique sua senha ou use 'Esqueci minha senha' abaixo."

    # Garantir que a senha na ficha use hash SHA-256 (nunca texto puro)
    conta_achada["senha"] = senha_hash_segura
    if auth_user_obj:
        conta_achada["auth_uid"] = auth_user_obj.id
    if conta_achada.get("id"):
        try:
            up_sec = {"senha": senha_hash_segura}
            if conta_achada.get("auth_uid"):
                up_sec["auth_uid"] = conta_achada["auth_uid"]
            supabase.table("clientes").update(up_sec).eq("id", conta_achada["id"]).execute()
        except Exception:
            try:
                supabase.table("clientes").update({"senha": senha_hash_segura}).eq("id", conta_achada["id"]).execute()
            except Exception:
                pass
    conta_achada["autenticado_supabase"] = True

    carrinho_conta = conta_achada.get("carrinho")
    if isinstance(carrinho_conta, str):
        try:
            carrinho_conta = json.loads(carrinho_conta)
        except Exception:
            carrinho_conta = []
    elif not isinstance(carrinho_conta, list):
        carrinho_conta = []

    carrinho_final = mesclar_carrinhos(st.session_state.get("carrinho_cliente", []), carrinho_conta)
    conta_achada["carrinho"] = carrinho_final

    st.session_state["cliente_logado"] = conta_achada
    st.session_state["carrinho_cliente"] = carrinho_final
    if conta_achada.get("email"):
        st.session_state.setdefault("contas_clientes_local", {})[conta_achada["email"].strip().lower()] = conta_achada
    if conta_achada.get("cpf_cnpj"):
        cpf_k = re.sub(r"\D", "", str(conta_achada["cpf_cnpj"]))
        if cpf_k:
            st.session_state.setdefault("contas_clientes_local", {})[cpf_k] = conta_achada
    sincronizar_carrinho_cliente()
    return True, f"✅ Autenticado com sucesso via Supabase! Bem-vindo(a), {conta_achada.get('nome', 'Cliente')}!"


# =====================================================================
# CABEÇALHO OFICIAL DO SITE (TOP BAR + HEADER PRINCIPAL + NAVEGAÇÃO + FAIXA DE VANTAGENS)
# =====================================================================
texto_promo_topo = cfg_loja.get("top_promo") or "⚡ TAGS INFORMÁTICA | CURSOS, MENTORIAS E TECNOLOGIA | PAGAMENTO FÁCIL NO PIX"
local_topo = cfg_loja.get("localizacao_cabecalho") or "📍 Manaus/AM • Envio p/ Todo Brasil"
slogan_topo = cfg_loja.get("slogan_cabecalho") or "Cursos, Mentorias & Tecnologia Oficial"

st.markdown(
    f'<div class="top-promo-bar">'
    f'<div class="top-promo-text">{texto_promo_topo}</div>'
    f'<div class="top-links">'
    f'<span>{local_topo}</span>'
    f'<a href="https://wa.me/55{whats_num_clean}?text=Ol%C3%A1,%20gostaria%20de%20informa%C3%A7%C3%B5es%20sobre%20os%20cursos%20e%20produtos!" target="_blank">💬 CENTRAL WHATSAPP</a>'
    f'<span>🔒 COMPRA 100% SEGURA</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# 2. Cabeçalho Principal: Identidade Visual + Busca Inteligente + Central do Cliente e Carrinho
cliente_atual = st.session_state.get("cliente_logado")
carrinho_atual = st.session_state.get("carrinho_cliente", [])
qtd_itens_carrinho = sum(int(i.get("qtd", 1)) for i in carrinho_atual)
subtotal_carrinho_topo = sum(float(i.get("preco_venda", 0)) * int(i.get("qtd", 1)) for i in carrinho_atual)

with st.container(border=True):
    col_logo, col_search, col_actions = st.columns([2.2, 2.6, 1.9], vertical_alignment="center")

    with col_logo:
        logo_custom = cfg_loja.get("logo_url")
        if logo_custom:
            st.image(logo_custom, width=165, alt=cfg_loja.get("nome_loja", "Logo da Loja"))
            st.caption(f"{slogan_topo} • {cfg_loja.get('status_loja', '🟢 Aberto')}")
        else:
            st.markdown(
                f'<div class="header-brand-wrap">'
                f'<div class="header-brand-row">'
                f'<div class="brand-logo">{cfg_loja.get("nome_loja", "Tags Informática")}<span class="brand-dot"></span></div>'
                f'<span class="header-status-badge">{cfg_loja.get("status_loja", "🟢 Aberto")}</span>'
                f'</div>'
                f'<div class="header-slogan-text">{slogan_topo}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with col_search:
        termo_busca = st.text_input(
            "Buscar produtos na loja",
            placeholder="🔍 Buscar cursos, mentorias, informática...",
            label_visibility="collapsed",
        )

    with col_actions:
        if cliente_atual:
            primeiro_nome_cli = (cliente_atual.get("nome") or "Cliente").split()[0]
            st.markdown(
                f'<div class="header-actions-wrap">'
                f'<span class="header-action-pill" style="background:rgba(59, 130, 246, 0.16); color:#60A5FA; border:1px solid rgba(59, 130, 246, 0.35);">👤 Olá, {primeiro_nome_cli}</span>'
                f'<span class="header-action-pill" style="background:rgba(16, 185, 129, 0.16); color:#34D399; border:1px solid rgba(16, 185, 129, 0.35);">🛒 {qtd_itens_carrinho} item(ns) • R$ {subtotal_carrinho_topo:.2f}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="header-actions-wrap">'
                f'<a href="https://wa.me/55{whats_num_clean}" target="_blank" class="header-action-pill" style="background:rgba(34,197,94,0.14); color:#4ADE80; border:1px solid rgba(34,197,94,0.3);">💬 Suporte WhatsApp</a>'
                f'<span class="header-action-pill" style="background:rgba(255,255,255,0.07); color:#F8FAFC; border:1px solid rgba(255,255,255,0.15);">🛒 Carrinho ({qtd_itens_carrinho}) • R$ {subtotal_carrinho_topo:.2f}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

# 3. Barra de Navegação do Cliente (Vitrine | Meu Carrinho | Meus Pedidos & Rastreio | Suporte | Minha Conta)
aba_loja = st.session_state.get("aba_loja_cliente", "vitrine")
if aba_loja not in ("vitrine", "carrinho", "pedidos", "suporte", "conta"):
    aba_loja = "vitrine"
    st.session_state["aba_loja_cliente"] = "vitrine"

c_nav1, c_nav2, c_nav3, c_nav4, c_nav5 = st.columns([1.3, 1.35, 1.5, 1.25, 1.4])
with c_nav1:
    st.button(
        "🛍️ Vitrine & Ofertas",
        key="btn_loja_nav_vitrine",
        type="primary" if aba_loja == "vitrine" else "secondary",
        width="stretch",
        on_click=ir_para_aba_loja,
        args=("vitrine",),
    )
with c_nav2:
    rotulo_carrinho_btn = f"🛒 Meu Carrinho ({qtd_itens_carrinho})" if qtd_itens_carrinho > 0 else "🛒 Meu Carrinho"
    st.button(
        rotulo_carrinho_btn,
        key="btn_loja_nav_carrinho",
        type="primary" if aba_loja == "carrinho" else "secondary",
        width="stretch",
        on_click=ir_para_aba_loja,
        args=("carrinho",),
    )
with c_nav3:
    st.button(
        "📦 Meus Pedidos & Rastreio",
        key="btn_loja_nav_pedidos",
        type="primary" if aba_loja == "pedidos" else "secondary",
        width="stretch",
        on_click=ir_para_aba_loja,
        args=("pedidos",),
    )
with c_nav4:
    st.button(
        "🎧 Suporte & Ajuda",
        key="btn_loja_nav_suporte",
        type="primary" if aba_loja == "suporte" else "secondary",
        width="stretch",
        on_click=ir_para_aba_loja,
        args=("suporte",),
    )
with c_nav5:
    rotulo_conta_btn = (
        f"👤 Minha Conta ({(cliente_atual.get('nome') or 'Cliente').split()[0]})"
        if cliente_atual
        else "🔐 Entrar / Criar Conta"
    )
    st.button(
        rotulo_conta_btn,
        key="btn_loja_nav_conta",
        type="primary" if aba_loja == "conta" else "secondary",
        width="stretch",
        on_click=ir_para_aba_loja,
        args=("conta",),
    )

# 4. Faixa de Vantagens e Confiança abaixo do Cabeçalho
if cfg_loja.get("exibir_barra_vantagens", True):
    v1_t = cfg_loja.get("vantagem_1") or "⚡ Pix com Aprovação Imediata"
    v2_t = cfg_loja.get("vantagem_2") or "🚚 Envio Rápido c/ Rastreio"
    v3_t = cfg_loja.get("vantagem_3") or "🛡️ Compra 100% Garantida"
    v4_t = cfg_loja.get("vantagem_4") or "🎓 Cursos com Certificado"
    st.markdown(
        f'<div class="benefits-bar-grid">'
        f'<div class="benefits-bar-item">{v1_t}</div>'
        f'<div class="benefits-bar-item">{v2_t}</div>'
        f'<div class="benefits-bar-item">{v3_t}</div>'
        f'<div class="benefits-bar-item">{v4_t}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

# =====================================================================
# VISÃO A: ÁREA DO CLIENTE (LOGIN, CADASTRO E DADOS DA CONTA)
# =====================================================================
if aba_loja == "conta":
    if not cliente_atual:
        st.markdown('<div class="section-title">🔐 Área do Cliente — Autenticação Oficial Supabase</div>', unsafe_allow_html=True)
        st.caption("Entre na sua conta protegida pelo Supabase Auth para salvar produtos no carrinho, acompanhar o status e rastrear seus pedidos.")

        col_auth1, col_auth2 = st.columns([1, 1.25])

        with col_auth1:
            with st.container(border=True):
                st.markdown("#### 🔑 Já sou cliente")
                st.markdown(
                    "<span style='background:rgba(16,185,129,0.15); color:#34D399; border:1px solid rgba(16,185,129,0.35); padding:2px 9px; border-radius:12px; font-size:0.74rem; font-weight:700;'>🔒 Protegido com Supabase Auth + CPF/E-mail</span>",
                    unsafe_allow_html=True,
                )
                st.caption("Acesse digitando seu E-mail ou seu CPF/CNPJ e senha:")
                with st.form("form_login_cliente_loja"):
                    id_login_in = st.text_input("E-mail ou CPF/CNPJ *", placeholder="cliente@email.com ou 000.000.000-00")
                    senha_login_in = st.text_input("Sua Senha *", type="password", placeholder="••••••••")
                    btn_entrar_cli = st.form_submit_button("Entrar na Minha Conta", type="primary", use_container_width=True)
                    if btn_entrar_cli:
                        if not id_login_in or not senha_login_in:
                            st.error("Informe seu E-mail/CPF e sua senha.")
                        else:
                            ok_l, msg_l = autenticar_cliente_loja(id_login_in, senha_login_in)
                            if ok_l:
                                st.success(msg_l)
                                st.rerun()
                            else:
                                st.error(msg_l)

                with st.expander("🔄 Esqueci minha senha (Recuperar por E-mail)"):
                    st.caption("O Supabase enviará um link seguro de redefinição de senha para o seu e-mail cadastrado:")
                    id_rec_in = st.text_input("Digite seu E-mail ou CPF cadastrado:", key="inp_rec_senha_cli", placeholder="cliente@email.com ou CPF")
                    if st.button("📧 Enviar Link de Recuperação", key="btn_rec_senha_cli", use_container_width=True):
                        if not id_rec_in.strip():
                            st.warning("Informe seu E-mail ou CPF.")
                        else:
                            email_rec = id_rec_in.strip().lower()
                            if "@" not in email_rec:
                                cpf_rec_num = re.sub(r"\D", "", email_rec)
                                try:
                                    r_all_c = supabase.table("clientes").select("email, cpf_cnpj").execute()
                                    for c_r in (r_all_c.data or []):
                                        if cpf_rec_num and cpf_rec_num == re.sub(r"\D", "", str(c_r.get("cpf_cnpj") or "")):
                                            email_rec = (c_r.get("email") or "").strip().lower()
                                            break
                                except Exception:
                                    pass
                            if "@" not in email_rec:
                                st.error("Não localizamos um e-mail vinculado a este CPF. Digite seu e-mail diretamente.")
                            else:
                                try:
                                    supabase.auth.reset_password_for_email(email_rec)
                                    st.success(f"✅ E-mail de recuperação enviado pelo Supabase para **{email_rec}**! Verifique sua caixa de entrada e spam.")
                                except Exception as e_reset:
                                    st.error(f"Não foi possível enviar o e-mail de recuperação agora: {e_reset}")

        with col_auth2:
            with st.container(border=True):
                st.markdown("#### ✨ Criar minha conta rápida (Supabase Auth)")
                st.caption("Cadastre-se uma única vez para compras em 1 clique, carrinho salvo e acompanhamento de entregas:")

                col_cep_cad1, col_cep_cad2 = st.columns([2.5, 1.3])
                with col_cep_cad1:
                    cep_cad_busca = st.text_input("📍 Buscar endereço pelo CEP:", placeholder="Ex: 69050-010", key="cep_busca_cadastro_cli")
                with col_cep_cad2:
                    st.write("")
                    if st.button("⚡ Preencher CEP", key="btn_cep_cadastro_cli", use_container_width=True):
                        c_limpo = re.sub(r"\D", "", cep_cad_busca)
                        if len(c_limpo) == 8:
                            try:
                                r_v = requests.get(f"https://viacep.com.br/ws/{c_limpo}/json/", timeout=3)
                                if r_v.status_code == 200 and "erro" not in r_v.json():
                                    dv = r_v.json()
                                    st.session_state["cad_cli_cep"] = cep_cad_busca
                                    st.session_state["cad_cli_rua"] = dv.get("logradouro", "")
                                    st.session_state["cad_cli_bairro"] = dv.get("bairro", "")
                                    st.session_state["cad_cli_cidade"] = dv.get("localidade", "")
                                    st.session_state["cad_cli_uf"] = dv.get("uf", "AM")
                                    st.success("Endereço localizado!")
                                    st.rerun()
                            except Exception:
                                pass

                with st.form("form_cadastro_cliente_loja"):
                    c_cd1, c_cd2 = st.columns(2)
                    nome_cad_cli = c_cd1.text_input("Nome Completo *", placeholder="Ex: Maria Oliveira")
                    cpf_cad_cli = c_cd2.text_input("CPF ou CNPJ *", placeholder="000.000.000-00")

                    c_cd3, c_cd4 = st.columns(2)
                    email_cad_cli = c_cd3.text_input("E-mail *", placeholder="maria@email.com")
                    whats_cad_cli = c_cd4.text_input("WhatsApp com DDD *", placeholder="92981234567")

                    c_cd5, c_cd6 = st.columns(2)
                    senha_cad_cli = c_cd5.text_input("Criar Senha (mín. 6 dígitos) *", type="password", placeholder="Mínimo 6 caracteres")
                    conf_senha_cli = c_cd6.text_input("Confirmar Senha *", type="password", placeholder="Repita a senha")

                    st.markdown("##### 📍 Endereço Padrão de Entrega")
                    c_ce1, c_ce2, c_ce3 = st.columns([1.2, 2.2, 0.9])
                    cep_cad_f = c_ce1.text_input("CEP *", value=st.session_state.get("cad_cli_cep", ""), placeholder="69050-010")
                    rua_cad_f = c_ce2.text_input("Rua / Logradouro *", value=st.session_state.get("cad_cli_rua", ""), placeholder="Av. Djalma Batista")
                    num_cad_f = c_ce3.text_input("Número *", placeholder="1000")

                    c_ce4, c_ce5, c_ce6 = st.columns([1.4, 1.4, 0.8])
                    bairro_cad_f = c_ce4.text_input("Bairro *", value=st.session_state.get("cad_cli_bairro", ""), placeholder="Chapada")
                    cid_cad_f = c_ce5.text_input("Cidade *", value=st.session_state.get("cad_cli_cidade", ""), placeholder="Manaus")
                    uf_cad_f = c_ce6.text_input("UF *", value=st.session_state.get("cad_cli_uf", "AM"), max_chars=2)

                    btn_criar_conta_cli = st.form_submit_button("✨ Criar Conta no Supabase e Entrar", type="primary", use_container_width=True)
                    if btn_criar_conta_cli:
                        if not (nome_cad_cli and cpf_cad_cli and email_cad_cli and whats_cad_cli and senha_cad_cli):
                            st.error("Preencha Nome, CPF/CNPJ, E-mail, WhatsApp e Senha.")
                        elif len(senha_cad_cli) < 6:
                            st.error("A senha deve ter pelo menos 6 caracteres (padrão de segurança do Supabase Auth).")
                        elif senha_cad_cli != conf_senha_cli:
                            st.error("As senhas digitadas não conferem.")
                        else:
                            end_comp_cad = (
                                f"{rua_cad_f}, {num_cad_f}, {bairro_cad_f}, {cid_cad_f}/{uf_cad_f.upper()} - CEP {cep_cad_f}"
                                if rua_cad_f
                                else "Não informado"
                            )
                            carrinho_inicial = st.session_state.get("carrinho_cliente", [])
                            email_limpo_cad = email_cad_cli.strip().lower()

                            # 1. Registrar oficialmente no Supabase Auth (auth.users)
                            auth_uid_novo = None
                            try:
                                res_sup_up = supabase.auth.sign_up({
                                    "email": email_limpo_cad,
                                    "password": senha_cad_cli,
                                    "options": {
                                        "data": {
                                            "nome": nome_cad_cli.strip(),
                                            "cpf_cnpj": cpf_cad_cli.strip(),
                                            "whatsapp": whats_cad_cli.strip(),
                                            "cep": cep_cad_f.strip(),
                                            "endereco_completo": end_comp_cad,
                                            "role": "cliente",
                                        }
                                    },
                                })
                                if res_sup_up and res_sup_up.user:
                                    auth_uid_novo = res_sup_up.user.id
                            except Exception:
                                pass

                            senha_hash_cad = gerar_hash_senha(senha_cad_cli)
                            novo_cli_obj = {
                                "auth_uid": auth_uid_novo,
                                "autenticado_supabase": True,
                                "nome": nome_cad_cli.strip(),
                                "cpf_cnpj": cpf_cad_cli.strip(),
                                "email": email_limpo_cad,
                                "whatsapp": whats_cad_cli.strip(),
                                "senha": senha_hash_cad,
                                "cep": cep_cad_f.strip(),
                                "endereco_completo": end_comp_cad,
                                "rua": rua_cad_f.strip(),
                                "numero": num_cad_f.strip(),
                                "bairro": bairro_cad_f.strip(),
                                "cidade": cid_cad_f.strip(),
                                "estado": uf_cad_f.strip().upper(),
                                "tabela_preco": "Varejo",
                                "carrinho": carrinho_inicial,
                            }
                            # 2. Salvar ou atualizar ficha completa na tabela public.clientes do Supabase
                            try:
                                r_ex = supabase.table("clientes").select("id").eq("cpf_cnpj", novo_cli_obj["cpf_cnpj"]).execute()
                                if r_ex.data:
                                    cid_db = r_ex.data[0]["id"]
                                    novo_cli_obj["id"] = cid_db
                                    try:
                                        supabase.table("clientes").update({
                                            "auth_uid": auth_uid_novo,
                                            "nome": novo_cli_obj["nome"],
                                            "email": novo_cli_obj["email"],
                                            "whatsapp": novo_cli_obj["whatsapp"],
                                            "senha": senha_hash_cad,
                                            "cep": novo_cli_obj["cep"],
                                            "endereco_completo": novo_cli_obj["endereco_completo"],
                                            "bairro": novo_cli_obj["bairro"],
                                            "cidade": novo_cli_obj["cidade"],
                                            "estado": novo_cli_obj["estado"],
                                            "carrinho": carrinho_inicial,
                                        }).eq("id", cid_db).execute()
                                    except Exception:
                                        supabase.table("clientes").update({
                                            "nome": novo_cli_obj["nome"],
                                            "email": novo_cli_obj["email"],
                                            "whatsapp": novo_cli_obj["whatsapp"],
                                            "cep": novo_cli_obj["cep"],
                                            "endereco_completo": novo_cli_obj["endereco_completo"],
                                        }).eq("id", cid_db).execute()
                                else:
                                    try:
                                        r_ins = supabase.table("clientes").insert({
                                            "auth_uid": auth_uid_novo,
                                            "nome": novo_cli_obj["nome"],
                                            "cpf_cnpj": novo_cli_obj["cpf_cnpj"],
                                            "email": novo_cli_obj["email"],
                                            "whatsapp": novo_cli_obj["whatsapp"],
                                            "senha": senha_hash_cad,
                                            "cep": novo_cli_obj["cep"],
                                            "endereco_completo": novo_cli_obj["endereco_completo"],
                                            "bairro": novo_cli_obj["bairro"],
                                            "cidade": novo_cli_obj["cidade"],
                                            "estado": novo_cli_obj["estado"],
                                            "tabela_preco": "Varejo",
                                            "carrinho": carrinho_inicial,
                                        }).execute()
                                    except Exception:
                                        r_ins = supabase.table("clientes").insert({
                                            "nome": novo_cli_obj["nome"],
                                            "cpf_cnpj": novo_cli_obj["cpf_cnpj"],
                                            "email": novo_cli_obj["email"],
                                            "whatsapp": novo_cli_obj["whatsapp"],
                                            "cep": novo_cli_obj["cep"],
                                            "endereco_completo": novo_cli_obj["endereco_completo"],
                                            "bairro": novo_cli_obj["bairro"],
                                            "cidade": novo_cli_obj["cidade"],
                                            "estado": novo_cli_obj["estado"],
                                            "tabela_preco": "Varejo",
                                        }).execute()
                                    if r_ins.data:
                                        novo_cli_obj["id"] = r_ins.data[0].get("id")
                            except Exception:
                                pass

                            st.session_state["cliente_logado"] = novo_cli_obj
                            st.session_state.setdefault("contas_clientes_local", {})[novo_cli_obj["email"]] = novo_cli_obj
                            cpf_num_k = re.sub(r"\D", "", novo_cli_obj["cpf_cnpj"])
                            if cpf_num_k:
                                st.session_state["contas_clientes_local"][cpf_num_k] = novo_cli_obj
                            sincronizar_carrinho_cliente()
                            st.success(f"🎉 Conta criada no Supabase Auth com sucesso! Bem-vindo(a), **{novo_cli_obj['nome']}**!")
                            st.rerun()
    else:
        st.markdown(f'<div class="section-title">👤 Minha Conta — {cliente_atual.get("nome")}</div>', unsafe_allow_html=True)
        col_pf1, col_pf2 = st.columns([1.5, 1.5])
        with col_pf1:
            with st.container(border=True):
                st.markdown("#### 📋 Meus Dados Cadastrados")
                st.markdown(
                    "<span style='background:rgba(16,185,129,0.15); color:#34D399; border:1px solid rgba(16,185,129,0.35); padding:3px 10px; border-radius:12px; font-size:0.76rem; font-weight:700;'>● Autenticado via Supabase Auth + Perfil Relacional</span>",
                    unsafe_allow_html=True,
                )
                st.write("")
                st.write(f"**Nome:** {cliente_atual.get('nome')}")
                st.write(f"**CPF/CNPJ:** `{cliente_atual.get('cpf_cnpj', '-')}`")
                st.write(f"**E-mail:** `{cliente_atual.get('email', '-')}`")
                st.write(f"**WhatsApp:** `{cliente_atual.get('whatsapp', '-')}`")
                st.write(f"**Endereço Salvo:** {cliente_atual.get('endereco_completo', '-')}")
                st.caption("🔒 Sua sessão permanece ativa mesmo se você atualizar a página (F5).")
                st.divider()
                c_ac_p1, c_ac_p2 = st.columns(2)
                with c_ac_p1:
                    st.button(
                        f"🛒 Meu Carrinho ({qtd_itens_carrinho})",
                        key="btn_conta_ir_carr",
                        type="primary",
                        use_container_width=True,
                        on_click=ir_para_aba_loja,
                        args=("carrinho",),
                    )
                with c_ac_p2:
                    st.button(
                        "📦 Meus Pedidos & Rastreio",
                        key="btn_conta_ir_peds",
                        use_container_width=True,
                        on_click=ir_para_aba_loja,
                        args=("pedidos",),
                    )
                if st.button("🚪 Sair da Minha Conta (Logout)", key="btn_logout_cliente_loja", use_container_width=True):
                    sincronizar_carrinho_cliente()
                    try:
                        supabase.auth.sign_out()
                    except Exception:
                        pass
                    st.session_state["cliente_logado"] = None
                    salvar_estado_persistente()
                    st.rerun()

        with col_pf2:
            with st.container(border=True):
                st.markdown("#### ✏️ Atualizar Meus Dados & Endereço")
                with st.form("form_atualizar_perfil_cli"):
                    up_nome = st.text_input("Nome Completo", value=cliente_atual.get("nome", ""))
                    up_whats = st.text_input("WhatsApp", value=cliente_atual.get("whatsapp", ""))
                    up_cep = st.text_input("CEP", value=cliente_atual.get("cep", ""))
                    up_end = st.text_input("Endereço Completo", value=cliente_atual.get("endereco_completo", ""))
                    if st.form_submit_button("💾 Salvar Meus Dados", type="primary", use_container_width=True):
                        cliente_atual["nome"] = up_nome
                        cliente_atual["whatsapp"] = up_whats
                        cliente_atual["cep"] = up_cep
                        cliente_atual["endereco_completo"] = up_end
                        if cliente_atual.get("id"):
                            try:
                                supabase.table("clientes").update({
                                    "nome": up_nome,
                                    "whatsapp": up_whats,
                                    "cep": up_cep,
                                    "endereco_completo": up_end,
                                }).eq("id", cliente_atual["id"]).execute()
                            except Exception:
                                pass
                        sincronizar_carrinho_cliente()
                        st.success("✅ Dados atualizados com sucesso!")
                        st.rerun()


# =====================================================================
# VISÃO B: MEU CARRINHO & CHECKOUT MULTI-PRODUTOS
# =====================================================================
elif aba_loja == "carrinho":
    st.markdown('<div class="section-title">🛒 Meu Carrinho de Compras</div>', unsafe_allow_html=True)

    if not carrinho_atual and not st.session_state.get("pedido_concluido"):
        with st.container(border=True):
            st.markdown(
                """
                <div style="text-align:center; padding: 36px 20px;">
                    <div style="font-size: 3.2rem; margin-bottom: 10px;">🛒</div>
                    <h3 style="color:#F8FAFC; margin:0 0 8px 0;">Seu carrinho está vazio no momento</h3>
                    <p style="color:#94A3B8; margin-bottom:20px;">Adicione cursos, mentorias ou produtos da vitrine para finalizar sua compra com Pix.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c_v1, c_v2, c_v3 = st.columns([1.5, 2, 1.5])
            with c_v2:
                st.button(
                    "🛍️ Explorar Produtos na Vitrine",
                    type="primary",
                    use_container_width=True,
                    on_click=ir_para_aba_loja,
                    args=("vitrine",),
                )
    else:
        if carrinho_atual:
            col_car_lista, col_car_resumo = st.columns([1.65, 1.35])

            with col_car_lista:
                with st.container(border=True):
                    c_top_c1, c_top_c2 = st.columns([3, 1.4])
                    c_top_c1.markdown(f"#### 📦 Itens salvos no carrinho ({qtd_itens_carrinho})")
                    if c_top_c2.button("🗑️ Limpar tudo", key="btn_limpar_carrinho_todo", use_container_width=True):
                        st.session_state["carrinho_cliente"] = []
                        sincronizar_carrinho_cliente()
                        st.rerun()

                    for idx_c, item_c in enumerate(list(carrinho_atual)):
                        st.divider()
                        img_it_c = item_c.get("imagem_url") or "https://via.placeholder.com/120"
                        pv_it_c = float(item_c.get("preco_venda", 0))
                        qtd_it_c = int(item_c.get("qtd", 1))
                        sub_it = pv_it_c * qtd_it_c
                        st.markdown(
                            f'<div style="display:flex; align-items:center; gap:12px; background:rgba(15,23,42,0.55); border:1px solid #334155; border-radius:12px; padding:10px 12px; margin-bottom:8px;">'
                            f'<img src="{img_it_c}" style="width:62px; height:62px; border-radius:8px; object-fit:cover; flex-shrink:0; background:#0F172A;">'
                            f'<div style="flex:1; min-width:0;">'
                            f'<div style="font-weight:700; color:#F8FAFC; font-size:0.94rem; line-height:1.3; margin-bottom:4px;">{item_c.get("titulo")}</div>'
                            f'<div style="font-size:0.8rem; color:#94A3B8;">Qtd: <b style="color:#F8FAFC;">{qtd_it_c}</b> &nbsp;•&nbsp; Unitário: R$ {pv_it_c:.2f}</div>'
                            f'</div>'
                            f'<div style="text-align:right; flex-shrink:0;">'
                            f'<div style="font-size:0.7rem; color:#94A3B8;">Subtotal</div>'
                            f'<div style="font-weight:800; color:#10B981; font-size:1.05rem;">R$ {sub_it:.2f}</div>'
                            f'</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        b_m1, b_m2, b_m3 = st.columns([1, 1, 1.2])
                        if b_m1.button("➖ Diminuir", key=f"car_dec_{item_c['id']}_{idx_c}", width="stretch"):
                            if qtd_it_c > 1:
                                item_c["qtd"] = qtd_it_c - 1
                            else:
                                carrinho_atual.pop(idx_c)
                            st.session_state["carrinho_cliente"] = carrinho_atual
                            sincronizar_carrinho_cliente()
                            st.rerun()
                        if b_m2.button("➕ Mais", key=f"car_inc_{item_c['id']}_{idx_c}", width="stretch"):
                            max_e = int(item_c.get("estoque") or 99)
                            item_c["qtd"] = min(max_e, qtd_it_c + 1)
                            st.session_state["carrinho_cliente"] = carrinho_atual
                            sincronizar_carrinho_cliente()
                            st.rerun()
                        if b_m3.button("🗑️ Remover", key=f"car_rem_{item_c['id']}_{idx_c}", width="stretch"):
                            carrinho_atual.pop(idx_c)
                            st.session_state["carrinho_cliente"] = carrinho_atual
                            sincronizar_carrinho_cliente()
                            st.rerun()

                    st.divider()
                    st.button(
                        "← Continuar Comprando na Vitrine",
                        key="btn_voltar_vitrine_car",
                        on_click=ir_para_aba_loja,
                        args=("vitrine",),
                    )

            with col_car_resumo:
                with st.container(border=True):
                    st.markdown("#### 🎟️ Cupom & Resumo do Pedido")
                    cupom_digitado = st.text_input("Cupom promocional:", placeholder="Ex: PRIMEIRACOMPRA ou TAGS15", key="input_cupom_carrinho").strip().upper()

                    subtotal_calc = sum(float(i.get("preco_venda", 0)) * int(i.get("qtd", 1)) for i in carrinho_atual)
                    desconto_valor = 0.0
                    cupom_encontrado = None

                    if cupom_digitado:
                        cupom_encontrado = next((c for c in st.session_state["cupons"] if c["codigo"] == cupom_digitado and c.get("ativo", True)), None)
                        if cupom_encontrado:
                            lim_u = int(cupom_encontrado.get("limite_usos") or 0)
                            atu_u = int(cupom_encontrado.get("usos_atuais") or 0)
                            if lim_u > 0 and atu_u >= lim_u:
                                st.error("Este cupom já atingiu o limite máximo de utilizações.")
                                cupom_encontrado = None
                            elif subtotal_calc >= cupom_encontrado.get("min_carrinho", 0):
                                if cupom_encontrado["tipo"] == "Porcentagem":
                                    desconto_valor = subtotal_calc * (cupom_encontrado["valor"] / 100.0)
                                elif cupom_encontrado["tipo"] == "Valor fixo":
                                    desconto_valor = min(subtotal_calc, float(cupom_encontrado["valor"]))
                                st.success(f"✅ Cupom **{cupom_digitado}** aplicado! (-R$ {desconto_valor:.2f})")
                            else:
                                st.warning(f"Válido para pedidos acima de R$ {cupom_encontrado.get('min_carrinho', 0):.2f}")
                        else:
                            st.error("Cupom inválido ou expirado.")

                    frete_valor = 0.0
                    total_calc = max(0.01, subtotal_calc - desconto_valor + frete_valor)

                    st.markdown(f"**Subtotal ({qtd_itens_carrinho} itens):** R$ {subtotal_calc:.2f}")
                    if desconto_valor > 0:
                        st.markdown(f"**Desconto Cupom:** :green[-R$ {desconto_valor:.2f}]")
                    st.markdown("**Frete:** :green[Grátis]")
                    st.markdown(f"### **Total no Pix:** :green[R$ {total_calc:.2f}]")

            st.write("")
            with st.container(border=True):
                st.markdown("#### 📋 Dados de Entrega & Faturamento Fiscal")
                if not cliente_atual:
                    c_av1, c_av2 = st.columns([3, 1.2])
                    c_av1.info("💡 **Já possui cadastro?** Faça login para preencher todo o seu endereço automaticamente e salvar o pedido na sua conta.")
                    with c_av2:
                        st.write("")
                        st.button(
                            "🔐 Fazer Login Agora",
                            key="btn_checkout_ir_login",
                            use_container_width=True,
                            on_click=ir_para_aba_loja,
                            args=("conta",),
                        )

                # Busca rápida de CEP via ViaCEP
                col_vcep1, col_vcep2 = st.columns([2.8, 1.2])
                with col_vcep1:
                    cep_auto_in = st.text_input(
                        "📍 Preenchimento Automático por CEP:",
                        value=st.session_state.get("checkout_cep") or (cliente_atual.get("cep", "") if cliente_atual else ""),
                        placeholder="Digite seu CEP (Ex: 69050-010)",
                        key="busca_rapida_cep",
                    )
                with col_vcep2:
                    st.write("")
                    if st.button("⚡ Buscar CEP", key="btn_exec_viacep", use_container_width=True):
                        cep_limpo = re.sub(r"\D", "", cep_auto_in)
                        if len(cep_limpo) == 8:
                            try:
                                r_cep = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=3)
                                if r_cep.status_code == 200:
                                    d_cep = r_cep.json()
                                    if "erro" not in d_cep:
                                        st.session_state["checkout_cep"] = cep_auto_in
                                        st.session_state["checkout_rua"] = d_cep.get("logradouro", "")
                                        st.session_state["checkout_bairro"] = d_cep.get("bairro", "")
                                        st.session_state["checkout_cidade"] = d_cep.get("localidade", "")
                                        st.session_state["checkout_uf"] = d_cep.get("uf", "AM")
                                        st.success("✅ Endereço preenchido!")
                                        st.rerun()
                                    else:
                                        st.warning("CEP não localizado.")
                            except Exception:
                                st.warning("Serviço de CEP indisponível. Preencha manualmente abaixo.")
                        else:
                            st.error("Informe um CEP válido com 8 números.")

                def_nome = cliente_atual.get("nome", "") if cliente_atual else ""
                def_doc = cliente_atual.get("cpf_cnpj", "") if cliente_atual else ""
                def_email = cliente_atual.get("email", "") if cliente_atual else ""
                def_whats = cliente_atual.get("whatsapp", "") if cliente_atual else ""
                def_cep = st.session_state.get("checkout_cep") or (cliente_atual.get("cep", "") if cliente_atual else "")
                def_rua = st.session_state.get("checkout_rua") or (cliente_atual.get("rua", "") or cliente_atual.get("endereco_completo", "") if cliente_atual else "")
                def_num = cliente_atual.get("numero", "S/N") if cliente_atual else ""
                def_bairro = st.session_state.get("checkout_bairro") or (cliente_atual.get("bairro", "Centro") if cliente_atual else "")
                def_cid = st.session_state.get("checkout_cidade") or (cliente_atual.get("cidade", "Manaus") if cliente_atual else "")
                def_uf = st.session_state.get("checkout_uf") or (cliente_atual.get("estado", "AM") if cliente_atual else "AM")

                with st.form("form_checkout_carrinho_multi"):
                    c_doc_t1, c_doc_t2 = st.columns([1.1, 2])
                    with c_doc_t1:
                        tipo_doc_c = st.radio("Documento:", ["CPF", "CNPJ"], horizontal=True)
                    with c_doc_t2:
                        doc_c = st.text_input(f"{tipo_doc_c} *", value=def_doc, placeholder="000.000.000-00")

                    col_nf1, col_nf2 = st.columns(2)
                    nome_c = col_nf1.text_input("Nome Completo ou Razão Social *", value=def_nome, placeholder="Ex: Lucas Silva")
                    email_c = col_nf2.text_input("E-mail para Nota Fiscal e Rastreio *", value=def_email, placeholder="cliente@exemplo.com")

                    c_w1, c_w2 = st.columns(2)
                    whats_c = c_w1.text_input("WhatsApp com DDD *", value=def_whats, placeholder="Ex: 92981234567")
                    cep_c = c_w2.text_input("CEP *", value=def_cep, placeholder="69050-010")

                    c_end1, c_end2 = st.columns([3, 1])
                    rua_c = c_end1.text_input("Logradouro / Endereço *", value=def_rua, placeholder="Ex: Av. Djalma Batista")
                    num_c = c_end2.text_input("Número *", value=def_num, placeholder="Ex: 1000")

                    c_end3, c_end4, c_end5 = st.columns([1.5, 1.5, 1])
                    bairro_c = c_end3.text_input("Bairro *", value=def_bairro, placeholder="Ex: Chapada")
                    cid_c = c_end4.text_input("Cidade *", value=def_cid, placeholder="Ex: Manaus")
                    uf_c = c_end5.text_input("UF *", value=def_uf, max_chars=2)

                    comp_c = st.text_input("Complemento (opcional)", placeholder="Ex: Apto 102, Bloco B")

                    senha_checkout_nova = ""
                    if not cliente_atual:
                        senha_checkout_nova = st.text_input(
                            "🔑 Criar uma senha para acompanhar e rastrear este pedido depois (opcional):",
                            type="password",
                            placeholder="Digite uma senha para criar sua conta automaticamente",
                        )

                    submit_pedido = st.form_submit_button("🔒 Confirmar Pedido e Gerar QR Code Pix", type="primary", use_container_width=True)

                if submit_pedido:
                    if not (nome_c and doc_c and email_c and whats_c and cep_c and rua_c and num_c and bairro_c and cid_c and uf_c):
                        st.error("Preencha todos os campos obrigatórios (*) para emissão fiscal e entrega.")
                    else:
                        endereco_c = f"{rua_c}, {num_c}{(' - ' + comp_c) if comp_c else ''}, {bairro_c}, {cid_c}/{uf_c.upper()} - CEP {cep_c}"

                        # 1. Vincular ou criar cliente relacional
                        cliente_id = cliente_atual.get("id") if cliente_atual else None
                        try:
                            res_cl_exist = supabase.table("clientes").select("id").eq("cpf_cnpj", doc_c).execute()
                            if res_cl_exist.data:
                                cliente_id = res_cl_exist.data[0]["id"]
                            elif not cliente_id:
                                dados_ins_cli = {
                                    "nome": nome_c,
                                    "cpf_cnpj": doc_c,
                                    "email": email_c.strip().lower(),
                                    "whatsapp": whats_c,
                                    "cep": cep_c,
                                    "endereco_completo": endereco_c,
                                    "bairro": bairro_c,
                                    "cidade": cid_c,
                                    "estado": uf_c.upper(),
                                    "tabela_preco": "Varejo",
                                }
                                res_ins_cl = supabase.table("clientes").insert(dados_ins_cli).execute()
                                if res_ins_cl.data:
                                    cliente_id = res_ins_cl.data[0]["id"]
                        except Exception:
                            pass

                        # Se o visitante informou senha no checkout, registra no Supabase Auth e já loga automaticamente
                        if not cliente_atual and senha_checkout_nova:
                            auth_uid_chk = None
                            senha_hash_chk = gerar_hash_senha(senha_checkout_nova)
                            if len(senha_checkout_nova) >= 6:
                                try:
                                    r_sup_chk = supabase.auth.sign_up({
                                        "email": email_c.strip().lower(),
                                        "password": senha_checkout_nova,
                                        "options": {
                                            "data": {
                                                "nome": nome_c,
                                                "cpf_cnpj": doc_c,
                                                "whatsapp": whats_c,
                                                "cep": cep_c,
                                                "endereco_completo": endereco_c,
                                                "role": "cliente",
                                            }
                                        },
                                    })
                                    if r_sup_chk and r_sup_chk.user:
                                        auth_uid_chk = r_sup_chk.user.id
                                except Exception:
                                    pass
                            if cliente_id:
                                try:
                                    supabase.table("clientes").update({"senha": senha_hash_chk, "auth_uid": auth_uid_chk}).eq("id", cliente_id).execute()
                                except Exception:
                                    try:
                                        supabase.table("clientes").update({"senha": senha_hash_chk}).eq("id", cliente_id).execute()
                                    except Exception:
                                        pass
                            novo_cli_auto = {
                                "id": cliente_id,
                                "auth_uid": auth_uid_chk,
                                "autenticado_supabase": True,
                                "nome": nome_c,
                                "cpf_cnpj": doc_c,
                                "email": email_c.strip().lower(),
                                "whatsapp": whats_c,
                                "senha": senha_hash_chk,
                                "cep": cep_c,
                                "endereco_completo": endereco_c,
                                "rua": rua_c,
                                "numero": num_c,
                                "bairro": bairro_c,
                                "cidade": cid_c,
                                "estado": uf_c.upper(),
                                "carrinho": [],
                            }
                            st.session_state["cliente_logado"] = novo_cli_auto
                            st.session_state.setdefault("contas_clientes_local", {})[email_c.strip().lower()] = novo_cli_auto

                        # 2. Vincular cupom relacional e incrementar contador de usos (usos_atuais)
                        cupom_id = None
                        if cupom_encontrado and cupom_encontrado.get("codigo"):
                            novo_uso_c = int(cupom_encontrado.get("usos_atuais") or 0) + 1
                            cupom_encontrado["usos_atuais"] = novo_uso_c
                            try:
                                res_cup = supabase.table("cupons").select("id, usos_atuais").eq("codigo", cupom_encontrado["codigo"]).execute()
                                if res_cup.data:
                                    cupom_id = res_cup.data[0]["id"]
                                    usos_db = int(res_cup.data[0].get("usos_atuais") or 0) + 1
                                    try:
                                        supabase.table("cupons").update({"usos_atuais": usos_db}).eq("id", cupom_id).execute()
                                    except Exception:
                                        pass
                            except Exception:
                                pass

                        itens_pedido_json = []
                        for it_c in carrinho_atual:
                            itens_pedido_json.append({
                                "id": it_c["id"],
                                "titulo": it_c["titulo"],
                                "qtd": int(it_c.get("qtd", 1)),
                                "tipo_venda": it_c.get("tipo_venda", "direto"),
                                "preco_unit": float(it_c.get("preco_venda", 0)),
                                "cupom": cupom_digitado if desconto_valor > 0 else None,
                                "fiscal": {
                                    "tipo_doc": tipo_doc_c,
                                    "documento": doc_c,
                                    "email": email_c,
                                    "rua": rua_c,
                                    "numero": num_c,
                                    "complemento": comp_c,
                                    "bairro": bairro_c,
                                    "cidade": cid_c,
                                    "uf": uf_c.upper(),
                                    "cep": cep_c,
                                    "ncm": it_c.get("ncm", "8471.60.52"),
                                },
                            })

                        pedido_novo = {
                            "cliente_id": cliente_id,
                            "cupom_id": cupom_id,
                            "cliente_nome": nome_c,
                            "cliente_cpf": doc_c,
                            "cliente_whatsapp": whats_c,
                            "cliente_email": email_c,
                            "cep": cep_c,
                            "endereco_completo": endereco_c,
                            "valor_produtos": subtotal_calc,
                            "valor_desconto": desconto_valor,
                            "valor_frete": frete_valor,
                            "valor_total": total_calc,
                            "itens": itens_pedido_json,
                            "status_pagamento": "pendente",
                        }
                        res_p = supabase.table("pedidos").insert(pedido_novo).execute()
                        id_ped = res_p.data[0]["id"] if res_p.data else "NOVO"

                        # 3. Inserir itens relacionais na tabela pedido_itens e atualizar estoque
                        for it_c in carrinho_atual:
                            if res_p.data and "id" in res_p.data[0]:
                                try:
                                    supabase.table("pedido_itens").insert({
                                        "pedido_id": id_ped,
                                        "produto_id": it_c.get("id"),
                                        "titulo": it_c.get("titulo", ""),
                                        "quantidade": int(it_c.get("qtd", 1)),
                                        "preco_unitario": float(it_c.get("preco_venda", 0)),
                                        "subtotal": float(it_c.get("preco_venda", 0)) * int(it_c.get("qtd", 1)),
                                    }).execute()
                                except Exception:
                                    pass
                            if it_c.get("tipo_venda") == "estoque_proprio" and it_c.get("estoque"):
                                novo_est = max(0, int(it_c["estoque"]) - int(it_c.get("qtd", 1)))
                                try:
                                    supabase.table("produtos").update({"estoque": novo_est}).eq("id", it_c["id"]).execute()
                                except Exception:
                                    pass

                        resumo_titulos = ", ".join(f"{i.get('qtd', 1)}x {i.get('titulo')}" for i in carrinho_atual)
                        st.session_state["carrinho_cliente"] = []
                        sincronizar_carrinho_cliente()

                        st.session_state["pedido_concluido"] = True
                        st.session_state["detalhes_pedido"] = {
                            "id": id_ped,
                            "total": total_calc,
                            "cliente_nome": nome_c,
                            "whatsapp": whats_c,
                            "titulo": resumo_titulos,
                            "qtd": qtd_itens_carrinho,
                        }
                        st.rerun()

        # ÁREA DE PAGAMENTO PIX APÓS CONFIRMAÇÃO
        if st.session_state.get("pedido_concluido") and "detalhes_pedido" in st.session_state:
            det = st.session_state["detalhes_pedido"]
            st.success(f"🎉 **Pedido #{det['id']} Confirmado com Sucesso!**")

            with st.container(border=True):
                st.markdown("### ⚡ Pague via Pix para Liberação e Envio Imediato")
                col_px1, col_px2 = st.columns([1, 1.6])

                pix_code = gerar_pix_bacen(
                    chave=CHAVE_PIX,
                    nome=NOME_BENEFICIARIO,
                    cidade=CIDADE_BENEFICIARIO,
                    valor=det["total"],
                    txid=f"PED{det['id']}",
                )
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=260x260&data={urllib.parse.quote(pix_code)}"

                with col_px1:
                    st.image(qr_url, caption="Escaneie o código com o app do seu banco", width=250)

                with col_px2:
                    st.markdown(f"**Valor a Pagar:** :green[**R$ {det['total']:.2f}**]")
                    st.markdown(f"**Itens:** {det['titulo']}")
                    st.markdown(f"**Recebedor Oficial:** `{NOME_BENEFICIARIO}`")
                    st.markdown("---")
                    st.markdown("**📋 Código Pix Copia e Cola (clique no botão ao lado para copiar):**")
                    st.code(pix_code, language="text")

                    msg_w = (
                        f"Olá! Acabei de fazer o Pedido #{det['id']} na TagsInfor.\n"
                        f"Itens: {det['titulo']}\n"
                        f"Total: R$ {det['total']:.2f}\n"
                        f"Cliente: {det['cliente_nome']}\n"
                        f"Seguem dados para confirmação!"
                    )
                    url_w = f"https://wa.me/55{whats_num_clean}?text={urllib.parse.quote(msg_w)}"
                    st.markdown(
                        f"""
                        <a href="{url_w}" target="_blank" class="btn-whats-pay">
                            💬 Enviar Comprovante no WhatsApp da Loja
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write("")
                    c_pos1, c_pos2 = st.columns(2)
                    with c_pos1:
                        if st.button("📦 Acompanhar Status & Rastreio", key="btn_pos_ir_pedidos", type="primary", use_container_width=True):
                            st.session_state["pedido_concluido"] = False
                            ir_para_aba_loja("pedidos")
                            st.rerun()
                    with c_pos2:
                        if st.button("🛍️ Voltar para a Vitrine", key="btn_voltar_catalogo", use_container_width=True):
                            st.session_state["pedido_concluido"] = False
                            ir_para_aba_loja("vitrine")
                            st.rerun()


# =====================================================================
# VISÃO C: MEUS PEDIDOS, ACOMPANHAMENTO DE STATUS E RASTREIO DE ENTREGA
# =====================================================================
elif aba_loja == "pedidos":
    st.markdown('<div class="section-title">📦 Meus Pedidos, Status & Rastreamento</div>', unsafe_allow_html=True)

    col_busca_p1, col_busca_p2 = st.columns([3, 1.2])
    with col_busca_p1:
        termo_rastreio_in = st.text_input(
            "🔍 Consultar pedido por CPF/CNPJ, E-mail ou Número do Pedido (#):",
            value=(cliente_atual.get("cpf_cnpj") or cliente_atual.get("email") or "") if cliente_atual else "",
            placeholder="Digite seu CPF, E-mail ou Nº do Pedido (Ex: 12)...",
        )
    with col_busca_p2:
        st.write("")
        st.button("🔄 Atualizar Status", key="btn_refresh_meus_pedidos", type="primary", use_container_width=True)

    try:
        res_todos_peds = supabase.table("pedidos").select("*").order("id", desc=True).execute()
        todos_peds_db = res_todos_peds.data or []
    except Exception:
        todos_peds_db = []

    meus_pedidos = []
    termo_r_clean = termo_rastreio_in.strip().lower()
    termo_r_num = re.sub(r"\D", "", termo_r_clean)

    for p_item in todos_peds_db:
        match_ped = False
        # Se cliente está logado, traz todos os pedidos vinculados a ele
        if cliente_atual:
            cid_log = cliente_atual.get("id")
            cpf_log = re.sub(r"\D", "", str(cliente_atual.get("cpf_cnpj") or ""))
            em_log = (cliente_atual.get("email") or "").strip().lower()

            cpf_p = re.sub(r"\D", "", str(p_item.get("cliente_cpf") or ""))
            em_p = (p_item.get("cliente_email") or "").strip().lower()

            if (cid_log and p_item.get("cliente_id") == cid_log) or (cpf_log and cpf_log == cpf_p) or (em_log and em_log == em_p):
                match_ped = True

        # Se digitou busca manual por CPF, E-mail ou Número do Pedido
        if termo_r_clean:
            id_str = str(p_item.get("id", "")).lower()
            cpf_p_raw = (p_item.get("cliente_cpf") or "").lower()
            cpf_p_num = re.sub(r"\D", "", cpf_p_raw)
            em_p_raw = (p_item.get("cliente_email") or "").lower()
            cod_rast_p = obter_rastreio_pedido(p_item).lower()

            if (
                termo_r_clean == id_str
                or termo_r_clean == f"#{id_str}"
                or termo_r_clean in cpf_p_raw
                or (termo_r_num and len(termo_r_num) >= 11 and termo_r_num == cpf_p_num)
                or (termo_r_clean in em_p_raw and len(termo_r_clean) > 3)
                or (cod_rast_p and termo_r_clean == cod_rast_p)
            ):
                match_ped = True

        if match_ped:
            meus_pedidos.append(p_item)

    if not meus_pedidos:
        with st.container(border=True):
            st.info("Nenhum pedido localizado para os dados informados. Faça login na sua conta ou digite o CPF utilizado na compra acima.")
    else:
        st.caption(f"Mostrando **{len(meus_pedidos)}** pedido(s) localizado(s):")
        for ped_c in meus_pedidos:
            st_p = (ped_c.get("status_pagamento") or "pendente").lower()
            cod_rastreio_c = obter_rastreio_pedido(ped_c)

            # Definir estágio da linha do tempo (1 a 4)
            mapa_etapa = {"pendente": 1, "pago": 2, "enviado": 3, "entregue": 4, "cancelado": 0}
            etapa_atual = mapa_etapa.get(st_p, 1)

            with st.container(border=True):
                c_hd1, c_hd2 = st.columns([3, 1.5])
                with c_hd1:
                    st.markdown(f"### 🛍️ Pedido #{ped_c['id']} — {ped_c.get('cliente_nome')}")
                    st.caption(f"📍 Entrega: {ped_c.get('endereco_completo')} (CEP: {ped_c.get('cep')})")
                with c_hd2:
                    st.markdown(
                        f"<div style='text-align:right;'><span style='font-size:1.35rem; font-weight:800; color:#10B981;'>R$ {float(ped_c.get('valor_total', 0)):.2f}</span></div>",
                        unsafe_allow_html=True,
                    )

                # LINHA DO TEMPO VISUAL DE 4 ETAPAS
                if st_p == "cancelado":
                    st.error("❌ Este pedido foi cancelado. Entre em contato com o suporte caso precise de ajuda.")
                else:
                    etapas_info = [
                        (1, "🕒 Pedido Recebido", "Aguardando Pix"),
                        (2, "✅ Pago & Separado", "Nota e preparação"),
                        (3, "🚚 Em Transporte", "Enviado à transportadora"),
                        (4, "🎉 Pedido Entregue", "Concluído com sucesso"),
                    ]
                    cols_tl = st.columns(4)
                    for idx_tl, (num_e, tit_e, sub_e) in enumerate(etapas_info):
                        concluido_tl = etapa_atual >= num_e
                        cor_borda = "#10B981" if concluido_tl else "#334155"
                        cor_bg = "rgba(16, 185, 129, 0.14)" if concluido_tl else "rgba(30, 41, 59, 0.5)"
                        cor_txt = "#34D399" if concluido_tl else "#64748B"
                        with cols_tl[idx_tl]:
                            st.markdown(
                                f"""
                                <div style="border:2px solid {cor_borda}; background:{cor_bg}; border-radius:10px; padding:10px 12px; text-align:center; margin-bottom:10px;">
                                    <div style="font-weight:800; font-size:0.88rem; color:{cor_txt};">{tit_e}</div>
                                    <div style="font-size:0.74rem; color:#94A3B8; margin-top:2px;">{sub_e}</div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                # BLOCO DE RASTREAMENTO DA ENTREGA
                with st.container(border=True):
                    cr_1, cr_2 = st.columns([2.8, 1.4])
                    with cr_1:
                        if cod_rastreio_c:
                            st.markdown(f"🚚 **Código de Rastreio Oficial:** `{cod_rastreio_c}`")
                            st.caption("Copie o código acima ou clique ao lado para acompanhar a movimentação da sua encomenda.")
                        elif st_p == "pendente":
                            st.markdown("⏳ **Status do Rastreio:** Aguardando confirmação do pagamento Pix para iniciar a separação e envio.")
                        elif st_p == "pago":
                            st.markdown("📦 **Status do Rastreio:** Pagamento confirmado! Seu pedido está sendo embalado no Centro de Distribuição e o código de rastreio será exibido aqui assim que despachado.")
                        else:
                            st.markdown("🚚 **Status do Rastreio:** Pedido em rota de entrega.")
                    with cr_2:
                        if cod_rastreio_c:
                            st.link_button(
                                "🔍 Rastrear nos Correios / Transp.",
                                f"https://rastreamento.correios.com.br/app/index.php?objetos={urllib.parse.quote(cod_rastreio_c)}",
                                type="primary",
                                use_container_width=True,
                            )

                # ITENS DO PEDIDO E AÇÕES DO CLIENTE (2ª VIA PIX, DANFE, SUPORTE)
                st.markdown("**Itens do Pedido:**")
                for it_p in (ped_c.get("itens") or []):
                    st.write(f"• **{it_p.get('qtd', 1)}x {it_p.get('titulo', 'Produto')}** — R$ {float(it_p.get('preco_unit', 0)):.2f}/un")

                ca_p1, ca_p2, ca_p3 = st.columns(3)
                with ca_p1:
                    if st_p == "pendente":
                        with st.popover("💳 Pagar / 2ª Via QR Code Pix", use_container_width=True):
                            pix_2via = gerar_pix_bacen(
                                chave=CHAVE_PIX,
                                nome=NOME_BENEFICIARIO,
                                cidade=CIDADE_BENEFICIARIO,
                                valor=float(ped_c.get("valor_total", 0)),
                                txid=f"PED{ped_c['id']}",
                            )
                            qr_2via = f"https://api.qrserver.com/v1/create-qr-code/?size=240x240&data={urllib.parse.quote(pix_2via)}"
                            st.image(qr_2via, width=220)
                            st.caption("Pix Copia e Cola:")
                            st.code(pix_2via, language="text")
                with ca_p2:
                    with st.popover("📄 Ver Nota / Recibo DANFE", use_container_width=True):
                        html_danfe_cli = gerar_danfe_recibo_html(ped_c, st.session_state["dados_fiscais_loja"])
                        st.components.v1.html(html_danfe_cli, height=520, scrolling=True)
                with ca_p3:
                    if st.button(f"🎧 Suporte para Pedido #{ped_c['id']}", key=f"btn_sup_ped_{ped_c['id']}", use_container_width=True):
                        st.session_state["pedido_suporte_selecionado"] = ped_c["id"]
                        ir_para_aba_loja("suporte")
                        st.rerun()


# =====================================================================
# VISÃO D: CENTRAL DE SUPORTE E ATENDIMENTO AO CLIENTE
# =====================================================================
elif aba_loja == "suporte":
    st.markdown('<div class="section-title">🎧 Central de Suporte & Atendimento ao Cliente</div>', unsafe_allow_html=True)

    col_sup1, col_sup2 = st.columns([1.4, 1.6])

    with col_sup1:
        with st.container(border=True):
            st.markdown("#### 💬 Atendimento Rápido via WhatsApp")
            st.write("Precisa falar imediatamente com nossa equipe sobre cursos, mentorias, pagamentos ou entregas?")
            st.markdown(
                f"""
                <a href="https://wa.me/55{whats_num_clean}?text=Ol%C3%A1!%20Preciso%20de%20suporte%20na%20loja%20TagsInfor." target="_blank" class="btn-whats-pay" style="margin: 14px 0;">
                    💬 Iniciar Conversa no WhatsApp Agora
                </a>
                """,
                unsafe_allow_html=True,
            )
            st.divider()
            st.markdown("#### 🏢 Dados Oficiais de Atendimento")
            fisc_info = st.session_state.get("dados_fiscais_loja", {})
            st.write(f"• **Empresa:** {fisc_info.get('razao_social', 'Tags Informática')}")
            st.write(f"• **WhatsApp / SAC:** `{WHATSAPP_LOJA}`")
            st.write(f"• **Localização:** {fisc_info.get('cidade_origem', 'Manaus')}/{fisc_info.get('estado_origem', 'AM')}")

        # Histórico de Chamados do Cliente
        st.write("")
        with st.container(border=True):
            st.markdown("#### 📋 Meus Chamados Abertos & Respostas")
            chamados_cli = []
            try:
                r_ch_cli = supabase.table("chamados_suporte").select("*").order("id", desc=True).execute()
                todos_ch = r_ch_cli.data or []
            except Exception:
                todos_ch = []

            ids_vistos = {str(c.get("id")) for c in todos_ch}
            for c_loc in reversed(st.session_state.get("chamados_suporte_local", [])):
                if str(c_loc.get("id")) not in ids_vistos:
                    todos_ch.append(c_loc)

            for ch_item in todos_ch:
                if cliente_atual:
                    em_log = (cliente_atual.get("email") or "").strip().lower()
                    w_log = re.sub(r"\D", "", str(cliente_atual.get("whatsapp") or ""))
                    em_ch = (ch_item.get("cliente_email") or "").strip().lower()
                    w_ch = re.sub(r"\D", "", str(ch_item.get("cliente_whatsapp") or ""))
                    if (em_log and em_log == em_ch) or (w_log and w_log == w_ch) or (cliente_atual.get("id") and ch_item.get("cliente_id") == cliente_atual.get("id")):
                        chamados_cli.append(ch_item)
                else:
                    chamados_cli.append(ch_item)

            if not chamados_cli:
                st.caption("Você ainda não possui chamados abertos.")
            else:
                for ch_c in chamados_cli[:8]:
                    st_c = ch_c.get("status", "aberto")
                    cor_c = {"aberto": "#F59E0B", "em_atendimento": "#3B82F6", "resolvido": "#10B981"}.get(st_c, "#64748B")
                    with st.container(border=True):
                        ped_txt = f" (Pedido #{ch_c['pedido_id']})" if ch_c.get("pedido_id") else ""
                        st.markdown(
                            f"**#{ch_c.get('id', 'NOVO')} - {ch_c.get('assunto')}**{ped_txt} "
                            f"<span style='background:{cor_c}22; color:{cor_c}; padding:2px 8px; border-radius:8px; font-size:0.74rem; font-weight:700; text-transform:uppercase;'>{st_c}</span>",
                            unsafe_allow_html=True,
                        )
                        st.caption(f"Sua mensagem: {ch_c.get('mensagem')}")
                        if ch_c.get("resposta_admin"):
                            st.success(f"💬 **Resposta da Loja:** {ch_c['resposta_admin']}")
                        else:
                            st.caption("⏳ Nossa equipe recebeu seu chamado e responderá em breve.")

    with col_sup2:
        with st.container(border=True):
            st.markdown("#### 📝 Abrir Novo Chamado de Suporte")
            st.caption("Envie sua solicitação diretamente para o painel da loja e acompanhe a resposta por aqui ou pelo WhatsApp:")

            ped_pre = st.session_state.get("pedido_suporte_selecionado", "")
            with st.form("form_abrir_chamado_suporte", clear_on_submit=True):
                sup_nome = st.text_input("Seu Nome *", value=cliente_atual.get("nome", "") if cliente_atual else "")
                c_sp1, c_sp2 = st.columns(2)
                sup_whats = c_sp1.text_input("Seu WhatsApp *", value=cliente_atual.get("whatsapp", "") if cliente_atual else "", placeholder="92981234567")
                sup_email = c_sp2.text_input("Seu E-mail", value=cliente_atual.get("email", "") if cliente_atual else "", placeholder="cliente@email.com")

                c_sp3, c_sp4 = st.columns([1.2, 2])
                sup_ped_id = c_sp3.text_input("Nº do Pedido (opcional)", value=str(ped_pre) if ped_pre else "", placeholder="Ex: 15")
                sup_assunto = c_sp4.selectbox(
                    "Motivo do Contato *",
                    [
                        "🚚 Dúvida sobre Rastreio / Prazo de Entrega",
                        "💳 Confirmação de Pagamento Pix",
                        "🎓 Acesso ao Curso / Emissão de Certificado",
                        "🔄 Troca, Garantia ou Suporte Técnico",
                        "💬 Outras Dúvidas ou Solicitações",
                    ],
                )
                sup_msg = st.text_area("Descreva como podemos ajudar você *", height=120, placeholder="Informe os detalhes da sua solicitação...")

                if st.form_submit_button("🚀 Enviar Chamado para o Suporte", type="primary", use_container_width=True):
                    if not (sup_nome and sup_whats and sup_msg):
                        st.error("Preencha seu Nome, WhatsApp e a Mensagem.")
                    else:
                        ped_id_int = int(re.sub(r"\D", "", sup_ped_id)) if re.sub(r"\D", "", sup_ped_id) else None
                        novo_chamado = {
                            "id": int(datetime.now().timestamp()),
                            "cliente_id": cliente_atual.get("id") if cliente_atual else None,
                            "pedido_id": ped_id_int,
                            "cliente_nome": sup_nome.strip(),
                            "cliente_whatsapp": sup_whats.strip(),
                            "cliente_email": sup_email.strip().lower(),
                            "assunto": sup_assunto,
                            "mensagem": sup_msg.strip(),
                            "status": "aberto",
                            "resposta_admin": None,
                        }
                        try:
                             payload_db_ch = dict(novo_chamado)
                             payload_db_ch.pop("id", None)
                             r_ch_ins = supabase.table("chamados_suporte").insert(payload_db_ch).execute()
                             if r_ch_ins.data and r_ch_ins.data[0].get("id"):
                                 novo_chamado["id"] = r_ch_ins.data[0]["id"]
                        except Exception:
                            pass

                        st.session_state.setdefault("chamados_suporte_local", []).append(novo_chamado)
                        salvar_estado_persistente()
                        st.success("✅ Chamado registrado com sucesso! Nossa equipe já recebeu sua mensagem.")
                        st.rerun()


# =====================================================================
# VISÃO E: VITRINE MULTI-NICHO (CATÁLOGO DE PRODUTOS)
# =====================================================================
else:
    # Barra Dinâmica Multi-Nicho: Departamentos -> Categorias -> Subcategorias
    deps_loja, cats_loja, subs_loja, deps_map_loja, cats_map_loja, subs_map_loja, _ = carregar_hierarquia_catalogo()
    deps_ativos_loja = [d for d in deps_loja if d.get("ativo", True)]

    ids_dep_vitrine = [0] + [d["id"] for d in deps_ativos_loja]
    dep_id_sel = st.pills(
        "Departamentos",
        ids_dep_vitrine,
        default=0,
        format_func=lambda did: "🌟 Todos os Departamentos" if did == 0 else f"{deps_map_loja[did].get('icone', '📦')} {deps_map_loja[did]['nome']}",
        label_visibility="collapsed",
        key="pills_dep_vitrine_id",
    )
    dep_id_ativo = dep_id_sel if dep_id_sel is not None else 0

    cat_id_ativa = 0
    sub_id_ativa = 0

    if dep_id_ativo != 0:
        cats_do_dep_vitrine = [c for c in cats_loja if c.get("departamento_id") == dep_id_ativo and c.get("ativo", True)]
        if cats_do_dep_vitrine:
            ids_cat_vitrine = [0] + [c["id"] for c in cats_do_dep_vitrine]
            cat_id_sel = st.pills(
                "Categorias do Departamento",
                ids_cat_vitrine,
                default=0,
                format_func=lambda cid: "📂 Todas as Categorias" if cid == 0 else f"📂 {cats_map_loja[cid]['nome']}",
                label_visibility="collapsed",
                key=f"pills_cat_vitrine_id_{dep_id_ativo}",
            )
            cat_id_ativa = cat_id_sel if cat_id_sel is not None else 0

            if cat_id_ativa != 0:
                subs_da_cat_vitrine = [s for s in subs_loja if s.get("categoria_id") == cat_id_ativa and s.get("ativo", True)]
                if subs_da_cat_vitrine:
                    ids_sub_vitrine = [0] + [s["id"] for s in subs_da_cat_vitrine]
                    sub_id_sel = st.pills(
                        "Subcategorias",
                        ids_sub_vitrine,
                        default=0,
                        format_func=lambda sid: "🏷️ Todas" if sid == 0 else f"🏷️ {subs_map_loja[sid]['nome']}",
                        label_visibility="collapsed",
                        key=f"pills_sub_vitrine_id_{cat_id_ativa}",
                    )
                    sub_id_ativa = sub_id_sel if sub_id_sel is not None else 0

    # Mini-barra de resumo se houver itens no carrinho
    if qtd_itens_carrinho > 0:
        with st.container(border=True):
            c_bar_c1, c_bar_c2 = st.columns([3.5, 1.3])
            c_bar_c1.markdown(
                f"🛒 **Você tem {qtd_itens_carrinho} produto(s) salvo(s) no seu carrinho** — Subtotal: :green[**R$ {subtotal_carrinho_topo:.2f}**]"
            )
            c_bar_c2.button(
                "Ir para o Carrinho →",
                key="btn_banner_ir_carrinho",
                type="primary",
                use_container_width=True,
                on_click=ir_para_aba_loja,
                args=("carrinho",),
            )

    # Hero Banner
    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-text">
                <h1>{cfg_loja.get('hero_title', 'UPGRADE DO SEU SETUP E CARREIRA')}</h1>
                <p>{cfg_loja.get('hero_subtitle', 'Cursos de informática, mentorias e equipamentos com pronta entrega.')}</p>
                <div class="hero-badges">
                    <span class="hero-badge-item">⚡ Desconto no Pix à Vista</span>
                    <span class="hero-badge-item">🚀 Rastreio de Entrega em Tempo Real</span>
                    <span class="hero-badge-item">🛒 Carrinho Salvo na Sua Conta</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Buscar e Filtrar Produtos por Departamento, Categoria, Subcategoria e Busca
    try:
        res = supabase.table("produtos").select("*").eq("ativo", True).order("id", desc=True).execute()
        todos_produtos_vitrine = res.data or []
    except Exception:
        todos_produtos_vitrine = []

    # Ordena priorizando produtos em Destaque no topo da vitrine
    todos_produtos_vitrine.sort(key=lambda item_p: (1 if item_p.get("destaque") else 0, int(item_p.get("id") or 0)), reverse=True)

    # Pré-carrega todas as avaliações em uma única query (elimina gargalo N+1 na vitrine)
    mapa_avals_vitrine = carregar_mapa_avaliacoes_todos_produtos()

    for p_all in todos_produtos_vitrine:
        _, _, _, trilha_t = obter_trilha_produto(p_all, deps_map_loja, cats_map_loja, subs_map_loja)
        p_all["_trilha_exibicao"] = trilha_t

    # =================================================================
    # MODAL POPUP DE DETALHES DO PRODUTO (ABRE NA FRENTE DA PÁGINA!)
    # =================================================================
    @st.dialog("🛍️ Detalhes Completos do Produto", width="large")
    def abrir_modal_detalhes_produto(prod_expandido: dict):
        gal_exp, extras_exp, video_exp, ficha_exp = obter_midia_ficha_produto(prod_expandido)
        avals_exp, media_exp, qtd_av_exp = carregar_avaliacoes_do_produto(prod_expandido["id"])

        st.markdown(
            f"<div style='color:#60A5FA; font-size:0.82rem; font-weight:700; margin-bottom:8px;'>{prod_expandido.get('_trilha_exibicao', '📦 Catálogo')}</div>",
            unsafe_allow_html=True,
        )

        col_det_midia, col_det_compra = st.columns([1.25, 1.35])

        with col_det_midia:
            pid_g = prod_expandido["id"]
            regras_css_gal = [
                ".gal-rad-in { display:none !important; }",
                ".gal-slides-wrap { width:100%; margin-bottom:10px; }",
                ".gal-slide-box { display:none; width:100%; height:300px; border-radius:14px; overflow:hidden; background:#0F172A; border:1px solid #334155; align-items:center; justify-content:center; }",
                ".gal-slide-box img { max-width:100%; max-height:100%; object-fit:contain; }",
                ".gal-pills-wrap { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:8px; }",
                ".gal-pill-btn { cursor:pointer; padding:6px 12px; border-radius:20px; font-size:0.78rem; font-weight:700; background:#1E293B; color:#CBD5E1; border:1px solid #334155; user-select:none; transition:all 0.15s ease; }",
                ".gal-thumbs-wrap { display:flex; gap:8px; overflow-x:auto; padding:4px 2px 8px 2px; margin-bottom:6px; }",
                ".gal-thumb-btn { cursor:pointer; width:64px; height:64px; flex-shrink:0; border-radius:10px; overflow:hidden; border:2px solid #334155; background:#0F172A; opacity:0.65; transition:all 0.15s ease; display:block; }",
                ".gal-thumb-btn img { width:100%; height:100%; object-fit:cover; display:block; pointer-events:none; }",
            ]
            radios_html = ""
            pills_html = ""
            slides_html = ""
            thumbs_html = ""

            for idx_g, url_g in enumerate(gal_exp):
                chk_str = "checked" if idx_g == 0 else ""
                rotulo_p = "📸 Foto Principal" if idx_g == 0 else f"📸 Foto {idx_g + 1}"
                radios_html += f'<input type="radio" name="gal_grp_{pid_g}" id="gal_rad_{pid_g}_{idx_g}" class="gal-rad-in" {chk_str}>'
                pills_html += f'<label for="gal_rad_{pid_g}_{idx_g}" class="gal-pill-btn">{rotulo_p}</label>'
                slides_html += f'<div id="gal_slide_{pid_g}_{idx_g}" class="gal-slide-box"><img src="{url_g}" alt="Foto {idx_g + 1}"></div>'
                thumbs_html += f'<label for="gal_rad_{pid_g}_{idx_g}" class="gal-thumb-btn" title="Toque para ver {rotulo_p}"><img src="{url_g}" alt="Thumb {idx_g + 1}"></label>'
                regras_css_gal.append(f'#gal_rad_{pid_g}_{idx_g}:checked ~ .gal-slides-wrap #gal_slide_{pid_g}_{idx_g} {{ display:flex !important; }}')
                regras_css_gal.append(f'#gal_rad_{pid_g}_{idx_g}:checked ~ .gal-thumbs-wrap label[for="gal_rad_{pid_g}_{idx_g}"] {{ border:2px solid #3B82F6 !important; opacity:1 !important; transform:scale(1.05); box-shadow:0 0 10px rgba(59,130,246,0.45); }}')
                regras_css_gal.append(f'#gal_rad_{pid_g}_{idx_g}:checked ~ .gal-pills-wrap label[for="gal_rad_{pid_g}_{idx_g}"] {{ background:#2563EB !important; color:#FFFFFF !important; border-color:#3B82F6 !important; }}')

            bloco_pills_top = f'<div class="gal-pills-wrap">{pills_html}</div>' if len(gal_exp) > 1 else ""
            bloco_thumbs_bot = (
                f'<div style="font-size:0.74rem; color:#94A3B8; margin-bottom:2px;">👆 Toque nas miniaturas ou botões acima para trocar a foto ({len(gal_exp)} fotos):</div>'
                f'<div class="gal-thumbs-wrap">{thumbs_html}</div>'
                if len(gal_exp) > 1
                else ""
            )
            galeria_interativa_html = (
                f'<style>{"".join(regras_css_gal)}</style>'
                f'<div class="gal- interactive-container">'
                f'{radios_html}'
                f'{bloco_pills_top}'
                f'<div class="gal-slides-wrap">{slides_html}</div>'
                f'{bloco_thumbs_bot}'
                f'</div>'
            )
            st.markdown(galeria_interativa_html, unsafe_allow_html=True)

            if video_exp:
                with st.expander("🎬 Assistir Vídeo Demonstrativo do Produto", expanded=False):
                    renderizar_player_video_produto(video_exp)

        with col_det_compra:
            st.markdown(
                f"<h3 style='margin:0 0 6px 0; color:#F8FAFC; font-weight:800; line-height:1.3;'>{prod_expandido['titulo']}</h3>",
                unsafe_allow_html=True,
            )
            estrelas_vis = "⭐" * int(round(media_exp))
            txt_av_resumo = (
                f"{estrelas_vis} **{media_exp:.1f}/5.0** ({qtd_av_exp} avaliação(ões))"
                if qtd_av_exp > 0
                else "⭐⭐⭐⭐⭐ **5.0** (Produto em Destaque • Seja o primeiro a avaliar!)"
            )
            st.markdown(txt_av_resumo)

            tipo_exp = prod_expandido.get("tipo_venda", "direto")
            est_exp = int(prod_expandido.get("estoque") or 0)
            badge_destaque_exp = (
                '<span style="background:rgba(245, 158, 11, 0.2); color:#FBBF24; border:1px solid rgba(245, 158, 11, 0.45); padding:4px 10px; border-radius:20px; font-size:0.74rem; font-weight:800; margin-right:6px;">⭐ DESTAQUE</span>'
                if prod_expandido.get("destaque")
                else ""
            )
            if tipo_exp == "estoque_proprio":
                if est_exp > 0:
                    st.markdown(f'{badge_destaque_exp}<span class="badge-status status-estoque">📦 Em Estoque ({est_exp} disponíveis)</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'{badge_destaque_exp}<span class="badge-status status-esgotado">❌ Esgotado</span>', unsafe_allow_html=True)
            elif tipo_exp == "afiliado":
                st.markdown(f'{badge_destaque_exp}<span class="badge-status status-afiliado">⭐ Oferta de Loja Parceira</span>', unsafe_allow_html=True)
            else:
                st.markdown(f'{badge_destaque_exp}<span class="badge-status status-direto">🚚 Envio Direto com Rastreio</span>', unsafe_allow_html=True)

            pv_exp = float(prod_expandido.get("preco_venda") or 0.0)
            po_exp = float(prod_expandido.get("preco_original") or 0.0)
            bloco_de_por_exp = ""
            if po_exp > pv_exp and pv_exp > 0:
                pct_off_exp = int(round(((po_exp - pv_exp) / po_exp) * 100))
                bloco_de_por_exp = (
                    f'<div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">'
                    f'<span style="text-decoration:line-through; color:#94A3B8; font-size:0.95rem;">De R$ {po_exp:.2f}</span>'
                    f'<span style="background:#EF4444; color:#FFFFFF; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:800;">🔥 -{pct_off_exp}% OFF</span>'
                    f'</div>'
                )

            st.markdown(
                f'<div style="background:rgba(16, 185, 129, 0.12); border:1px solid rgba(16, 185, 129, 0.3); border-radius:12px; padding:12px 16px; margin:10px 0;">'
                f'<div style="font-size:0.78rem; color:#94A3B8; font-weight:600;">PREÇO ESPECIAL À VISTA NO PIX</div>'
                f'{bloco_de_por_exp}'
                f'<div style="font-size:1.95rem; font-weight:800; color:#10B981;">R$ {pv_exp:.2f}</div>'
                f'<div style="font-size:0.78rem; color:#34D399;">⚡ Aprovação imediata • Use cupom de desconto no carrinho</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            resumo_desc_exp = prod_expandido.get("descricao") or "Produto oficial Tags Informática com garantia e suporte dedicado."
            st.write(resumo_desc_exp[:220] + ("..." if len(resumo_desc_exp) > 220 else ""))

            if tipo_exp == "afiliado" and prod_expandido.get("link_afiliado"):
                st.link_button("🔥 Acessar Oferta na Loja Parceira ↗", prod_expandido["link_afiliado"], type="primary", width="stretch")
            elif tipo_exp == "estoque_proprio" and est_exp <= 0:
                st.button("❌ Produto Indisponível no Momento", disabled=True, width="stretch")
            else:
                c_act_exp1, c_act_exp2 = st.columns(2)
                with c_act_exp1:
                    if st.button("🛒 + Carrinho", key=f"btn_exp_add_{prod_expandido['id']}", width="stretch"):
                        adicionar_item_carrinho(prod_expandido, ir_para_checkout=False)
                        st.session_state[f"_adicionado_modal_{prod_expandido['id']}"] = True
                with c_act_exp2:
                    if st.button("⚡ Comprar no Pix", key=f"btn_exp_buy_{prod_expandido['id']}", type="primary", width="stretch"):
                        adicionar_item_carrinho(prod_expandido, ir_para_checkout=True)
                        st.rerun()

                if st.session_state.get(f"_adicionado_modal_{prod_expandido['id']}"):
                    st.success("✅ Produto salvo no seu carrinho!")
                    if st.button("🛍️ Ir para o Carrinho e Finalizar →", key=f"btn_ir_car_modal_{prod_expandido['id']}", type="primary", width="stretch"):
                        st.session_state[f"_adicionado_modal_{prod_expandido['id']}"] = False
                        ir_para_aba_loja("carrinho")
                        st.rerun()

        st.divider()
        # ABAS COMPLETAS DENTRO DO MODAL: DESCRIÇÃO + FICHA TÉCNICA + AVALIAÇÕES
        tab_det_desc, tab_det_ficha, tab_det_aval = st.tabs([
            "📝 Descrição & Vídeo",
            "⚙️ Ficha Técnica",
            f"⭐ Avaliações ({qtd_av_exp})",
        ])

        with tab_det_desc:
            st.markdown(f"#### 📖 Sobre **{prod_expandido['titulo']}**")
            st.write(prod_expandido.get("descricao") or "Descrição detalhada disponível com nosso atendimento.")
            if video_exp:
                st.markdown("#### 🎬 Vídeo Demonstrativo")
                renderizar_player_video_produto(video_exp)

        with tab_det_ficha:
            st.markdown("#### ⚙️ Especificações e Características Técnicas")
            linhas_ficha_html = ""
            for idx_f, item_f in enumerate(ficha_exp):
                bg_f = "rgba(30, 41, 59, 0.7)" if idx_f % 2 == 0 else "rgba(15, 23, 42, 0.7)"
                linhas_ficha_html += (
                    f'<tr style="background:{bg_f};">'
                    f'<td style="padding:10px 14px; border:1px solid #334155; font-weight:700; color:#93C5FD; width:38%;">{item_f.get("nome", "Característica")}</td>'
                    f'<td style="padding:10px 14px; border:1px solid #334155; color:#F8FAFC;">{item_f.get("valor", "-")}</td>'
                    f'</tr>'
                )
            st.markdown(
                f'<table style="width:100%; border-collapse:collapse; border-radius:10px; overflow:hidden; margin-top:8px;">{linhas_ficha_html}</table>',
                unsafe_allow_html=True,
            )

        with tab_det_aval:
            st.markdown(f"#### 💬 O que os clientes dizem ({qtd_av_exp})")
            if not avals_exp:
                st.info("Este produto ainda não possui comentários. Seja o primeiro a avaliar abaixo!")
            else:
                for av_item in avals_exp:
                    nota_int = max(1, min(5, int(av_item.get("nota", 5))))
                    estrelas_str = "⭐" * nota_int
                    with st.container(border=True):
                        st.markdown(
                            f"**{estrelas_str} {av_item.get('titulo_avaliacao') or 'Excelente produto!'}** "
                            f"<span style='background:rgba(16,185,129,0.15); color:#34D399; padding:2px 7px; border-radius:8px; font-size:0.7rem; font-weight:700;'>✔ Avaliação Verificada</span>",
                            unsafe_allow_html=True,
                        )
                        st.write(av_item.get("comentario", ""))
                        st.caption(f"👤 Por **{av_item.get('cliente_nome', 'Cliente')}**")

            st.write("")
            with st.container(border=True):
                st.markdown("#### ✍️ Avaliar este Produto")
                with st.form(f"form_avaliar_prod_modal_{prod_expandido['id']}", clear_on_submit=True):
                    av_nome_in = st.text_input(
                        "Seu Nome *",
                        value=cliente_atual.get("nome", "") if cliente_atual else "",
                        placeholder="Ex: Carlos Eduardo",
                    )
                    av_nota_in = st.selectbox(
                        "Sua Nota (Estrelas) *",
                        [
                            (5, "⭐⭐⭐⭐⭐ (5/5) — Excelente / Recomendo muito"),
                            (4, "⭐⭐⭐⭐ (4/5) — Muito Bom"),
                            (3, "⭐⭐⭐ (3/5) — Bom / Regular"),
                            (2, "⭐⭐ (2/5) — Abaixo do esperado"),
                            (1, "⭐ (1/5) — Insatisfeito"),
                        ],
                        format_func=lambda x: x[1],
                    )
                    av_tit_in = st.text_input("Título do Comentário", placeholder="Ex: Ótimo custo-benefício e entrega rápida!")
                    av_com_in = st.text_area("Seu Comentário ou Avaliação *", height=85, placeholder="Conte o que achou da qualidade, atendimento ou conteúdo...")
                    if st.form_submit_button("🌟 Publicar Avaliação", type="primary", width="stretch"):
                        if not (av_nome_in.strip() and av_com_in.strip()):
                            st.error("Preencha seu nome e seu comentário.")
                        else:
                            nova_av_obj = {
                                "id": int(datetime.now().timestamp()),
                                "produto_id": prod_expandido["id"],
                                "cliente_id": cliente_atual.get("id") if cliente_atual else None,
                                "cliente_nome": av_nome_in.strip(),
                                "nota": int(av_nota_in[0]),
                                "titulo_avaliacao": av_tit_in.strip() or "Recomendo!",
                                "comentario": av_com_in.strip(),
                                "compra_verificada": True,
                            }
                            try:
                                payload_av_db = dict(nova_av_obj)
                                payload_av_db.pop("id", None)
                                r_av_ins = supabase.table("avaliacoes_produtos").insert(payload_av_db).execute()
                                if r_av_ins.data and r_av_ins.data[0].get("id"):
                                    nova_av_obj["id"] = r_av_ins.data[0]["id"]
                            except Exception:
                                pass
                            st.session_state.setdefault("avaliacoes_produtos_local", []).append(nova_av_obj)
                            salvar_estado_persistente()
                            st.success("🎉 Obrigado! Sua avaliação foi publicada com sucesso!")

        st.write("")
        if st.button("← Fechar Detalhes e Continuar na Vitrine", key=f"btn_fechar_modal_{prod_expandido['id']}", width="stretch"):
            st.session_state["produto_expandido_id"] = None
            st.rerun()

    produtos_vitrine = []
    for p in todos_produtos_vitrine:
        d_id, c_id, s_id, trilha_txt = obter_trilha_produto(p, deps_map_loja, cats_map_loja, subs_map_loja)
        p["_trilha_exibicao"] = trilha_txt
        if dep_id_ativo != 0 and d_id != dep_id_ativo:
            continue
        if cat_id_ativa != 0 and c_id != cat_id_ativa:
            continue
        if sub_id_ativa != 0 and s_id != sub_id_ativa:
            continue
        if termo_busca:
            termo_low = termo_busca.lower()
            if (
                termo_low not in p.get("titulo", "").lower()
                and termo_low not in (p.get("descricao") or "").lower()
                and termo_low not in trilha_txt.lower()
            ):
                continue
        produtos_vitrine.append(p)

    dep_obj_ativo = deps_map_loja.get(dep_id_ativo)
    titulo_secao = (
        f"{dep_obj_ativo.get('icone', '⚡')} {dep_obj_ativo['nome']}"
        if dep_id_ativo != 0 and dep_obj_ativo
        else "⚡ Catálogo Oficial — Todos os Departamentos"
    )
    st.markdown(f'<div class="section-title">{titulo_secao}</div>', unsafe_allow_html=True)

    # Grid de Produtos
    if not produtos_vitrine:
        st.info("Nenhum produto encontrado neste departamento/categoria.")
    else:
        cols = st.columns(4)
        for i, p in enumerate(produtos_vitrine):
            with cols[i % 4]:
                with st.container(border=True):
                    gal_card, _, vid_card, _ = obter_midia_ficha_produto(p)
                    _, media_card, qtd_av_card = mapa_avals_vitrine.get(p["id"], ([], 5.0, 0))

                    img_url = p.get("imagem_url") or "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600"
                    st.markdown(f'<div class="img-box"><img src="{img_url}" alt="{p["titulo"]}"></div>', unsafe_allow_html=True)

                    tipo = p.get("tipo_venda", "direto")
                    est = p.get("estoque", 0)
                    badge_dest_card = (
                        '<span style="background:rgba(245, 158, 11, 0.2); color:#FBBF24; border:1px solid rgba(245, 158, 11, 0.45); padding:3px 8px; border-radius:20px; font-size:0.68rem; font-weight:800; margin-right:4px;">⭐ DESTAQUE</span>'
                        if p.get("destaque")
                        else ""
                    )

                    if tipo == "estoque_proprio":
                        if est > 0:
                            st.markdown(f'{badge_dest_card}<span class="badge-status status-estoque">📦 Pronta Entrega ({est} un.)</span>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'{badge_dest_card}<span class="badge-status status-esgotado">❌ Esgotado</span>', unsafe_allow_html=True)
                    elif tipo == "afiliado":
                        st.markdown(f'{badge_dest_card}<span class="badge-status status-afiliado">⭐ Loja Parceira</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'{badge_dest_card}<span class="badge-status status-direto">🚚 Envio Direto</span>', unsafe_allow_html=True)

                    st.markdown(
                        f'<div style="color:#60A5FA; font-size:0.72rem; font-weight:700; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{p.get("_trilha_exibicao", "📦 Geral")}</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f'<div class="prod-title">{p["titulo"]}</div>', unsafe_allow_html=True)
                    info_midia_card = f"⭐ {media_card:.1f} ({qtd_av_card})" if qtd_av_card > 0 else "⭐⭐⭐⭐⭐ 5.0"
                    if len(gal_card) > 1:
                        info_midia_card += f" • 🖼️ {len(gal_card)} fotos"
                    if vid_card:
                        info_midia_card += " • 🎬 Vídeo"
                    st.caption(info_midia_card)

                    desc_curta = (p.get("descricao") or "")[:65] + "..." if len(p.get("descricao") or "") > 65 else (p.get("descricao") or "")
                    st.markdown(f'<div class="prod-desc">{desc_curta}</div>', unsafe_allow_html=True)

                    pv_card = float(p.get("preco_venda") or 0.0)
                    po_card = float(p.get("preco_original") or 0.0)
                    if po_card > pv_card and pv_card > 0:
                        pct_off_card = int(round(((po_card - pv_card) / po_card) * 100))
                        st.markdown(
                            f'<div style="display:flex; align-items:center; gap:6px; margin-bottom:-4px;">'
                            f'<span style="text-decoration:line-through; color:#94A3B8; font-size:0.78rem;">De R$ {po_card:.2f}</span>'
                            f'<span style="background:#EF4444; color:#FFFFFF; padding:1px 6px; border-radius:5px; font-size:0.68rem; font-weight:800;">-{pct_off_card}% OFF</span>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(f'<div class="prod-price">R$ {pv_card:.2f} <small>no Pix</small></div>', unsafe_allow_html=True)

                    if st.button("🔍 Ver Detalhes / Fotos & Vídeo", key=f"btn_ver_det_{p['id']}", width="stretch"):
                        st.session_state["produto_expandido_id"] = p["id"]
                        abrir_modal_detalhes_produto(p)

                    if tipo == "afiliado" and p.get("link_afiliado"):
                        st.link_button("Ver Oferta na Loja", p["link_afiliado"], width="stretch")
                    elif tipo == "estoque_proprio" and est <= 0:
                        st.button("Indisponível", key=f"btn_esgot_{p['id']}", disabled=True, width="stretch")
                    else:
                        cb_add, cb_buy = st.columns(2)
                        with cb_add:
                            if st.button("🛒 + Carrinho", key=f"btn_add_car_{p['id']}", width="stretch"):
                                adicionar_item_carrinho(p, ir_para_checkout=False)
                                st.toast(f"✅ {p['titulo']} salvo no seu carrinho!")
                                st.rerun()
                        with cb_buy:
                            if st.button("⚡ Comprar", key=f"btn_buy_{p['id']}", type="primary", width="stretch"):
                                adicionar_item_carrinho(p, ir_para_checkout=True)
                                st.rerun()

# =====================================================================
# RODAPÉ OFICIAL DO SITE (FOOTER INSTITUCIONAL + NAVEGAÇÃO RÁPIDA + SELOS DE SEGURANÇA)
# =====================================================================
st.write("")
st.divider()

deps_rodape, _, _, _, _, _, _ = carregar_hierarquia_catalogo()
deps_nomes_rodape = [f"{d.get('icone', '📦')} {d.get('nome')}" for d in deps_rodape if d.get("ativo", True)][:6]
deps_html_lista = "".join(
    [f"<li style='margin-bottom:6px; color:#CBD5E1; font-size:0.84rem;'>{dn}</li>" for dn in deps_nomes_rodape]
) or "<li style='color:#CBD5E1; font-size:0.84rem;'>🎓 Cursos & Mentorias</li><li style='color:#CBD5E1; font-size:0.84rem;'>💻 Informática & Tech</li>"

rod_nome_loja = cfg_loja.get("nome_loja") or "Tags Informática"
rod_sobre = cfg_loja.get("rodape_sobre") or (
    "A Tags Informática é referência em cursos profissionalizantes, mentorias individuais VIP e equipamentos de tecnologia com pronta entrega, suporte dedicado e garantia oficial."
)
rod_whats_raw = cfg_loja.get("rodape_whatsapp") or WHATSAPP_LOJA
rod_whats_num = re.sub(r"\D", "", str(rod_whats_raw)) or whats_num_clean
rod_email = cfg_loja.get("rodape_email") or "contato@tagsinfor.com"
rod_endereco = cfg_loja.get("rodape_endereco") or "Av. Djalma Batista, 1000 - Chapada, Manaus/AM"
rod_horario = cfg_loja.get("rodape_horario") or "Seg a Sex das 08h às 18h | Sáb das 08h às 13h"
rod_cnpj = cfg_loja.get("rodape_cnpj") or st.session_state.get("dados_fiscais_loja", {}).get("cnpj", "00.000.000/0001-00")
rod_insta = cfg_loja.get("rodape_instagram") or "https://instagram.com"
rod_yt = cfg_loja.get("rodape_youtube") or "https://youtube.com"
rod_copy = cfg_loja.get("rodape_copyright") or f"© {datetime.now().year} {rod_nome_loja} — Todos os direitos reservados."

# Barra de Atalhos Rápidos do Rodapé
c_ft_nav1, c_ft_nav2, c_ft_nav3, c_ft_nav4, c_ft_nav5 = st.columns(5)
with c_ft_nav1:
    st.button("🛍️ Ir para a Vitrine", key="btn_ft_vitrine", width="stretch", on_click=ir_para_aba_loja, args=("vitrine",))
with c_ft_nav2:
    st.button(f"🛒 Meu Carrinho ({qtd_itens_carrinho})", key="btn_ft_carrinho", width="stretch", on_click=ir_para_aba_loja, args=("carrinho",))
with c_ft_nav3:
    st.button("📦 Rastrear Meu Pedido", key="btn_ft_pedidos", width="stretch", on_click=ir_para_aba_loja, args=("pedidos",))
with c_ft_nav4:
    st.button("🎧 Central de Suporte", key="btn_ft_suporte", width="stretch", on_click=ir_para_aba_loja, args=("suporte",))
with c_ft_nav5:
    st.button("👤 Área do Cliente", key="btn_ft_conta", width="stretch", on_click=ir_para_aba_loja, args=("conta",))

rodape_html_oficial = (
    f'<div style="background:linear-gradient(180deg, #0F172A 0%, #090D16 100%); border:1px solid #1E293B; border-radius:16px; padding:32px 28px 20px 28px; margin-top:12px; color:#E2E8F0;">'
    f'<div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:28px; padding-bottom:24px; border-bottom:1px solid rgba(255,255,255,0.08);">'
    f'<div>'
    f'<div style="font-size:1.45rem; font-weight:800; color:#FFFFFF; margin-bottom:8px; display:flex; align-items:center; gap:6px;">'
    f'{rod_nome_loja}<span style="width:8px; height:8px; background:#F59E0B; border-radius:50%; display:inline-block;"></span>'
    f'</div>'
    f'<p style="color:#94A3B8; font-size:0.84rem; line-height:1.55; margin:0 0 14px 0;">{rod_sobre}</p>'
    f'<div style="display:flex; gap:8px; flex-wrap:wrap;">'
    f'<a href="https://wa.me/55{rod_whats_num}" target="_blank" style="text-decoration:none; background:#16A34A22; color:#4ADE80; border:1px solid #16A34A55; padding:5px 11px; border-radius:8px; font-size:0.76rem; font-weight:700;">💬 WhatsApp</a>'
    f'<a href="{rod_insta}" target="_blank" style="text-decoration:none; background:#E1306C22; color:#F472B6; border:1px solid #E1306C55; padding:5px 11px; border-radius:8px; font-size:0.76rem; font-weight:700;">📸 Instagram</a>'
    f'<a href="{rod_yt}" target="_blank" style="text-decoration:none; background:#EF444422; color:#F87171; border:1px solid #EF444455; padding:5px 11px; border-radius:8px; font-size:0.76rem; font-weight:700;">▶️ YouTube</a>'
    f'</div>'
    f'</div>'
    f'<div>'
    f'<div style="font-size:0.92rem; font-weight:800; color:#F8FAFC; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:12px;">📂 Nossos Departamentos</div>'
    f'<ul style="list-style:none; padding:0; margin:0;">{deps_html_lista}</ul>'
    f'</div>'
    f'<div>'
    f'<div style="font-size:0.92rem; font-weight:800; color:#F8FAFC; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:12px;">🎧 Atendimento ao Cliente</div>'
    f'<div style="color:#CBD5E1; font-size:0.84rem; line-height:1.65;">'
    f'<div>📱 <b>WhatsApp SAC:</b> <a href="https://wa.me/55{rod_whats_num}" target="_blank" style="color:#4ADE80; text-decoration:none; font-weight:700;">{rod_whats_raw}</a></div>'
    f'<div>✉️ <b>E-mail:</b> {rod_email}</div>'
    f'<div>🕒 <b>Horário:</b> {rod_horario}</div>'
    f'<div style="margin-top:6px; color:#94A3B8; font-size:0.8rem;">📍 {rod_endereco}</div>'
    f'</div>'
    f'</div>'
    f'<div>'
    f'<div style="font-size:0.92rem; font-weight:800; color:#F8FAFC; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:12px;">💳 Pagamento & Segurança</div>'
    f'<div style="display:flex; flex-wrap:wrap; gap:6px; margin-bottom:12px;">'
    f'<span style="background:#064E3B; color:#34D399; border:1px solid #059669; padding:5px 10px; border-radius:8px; font-size:0.75rem; font-weight:800;">💠 PIX OFICIAL BACEN</span>'
    f'<span style="background:#1E3A8A; color:#93C5FD; border:1px solid #2563EB; padding:5px 10px; border-radius:8px; font-size:0.75rem; font-weight:800;">🤝 MERCADO PAGO</span>'
    f'<span style="background:#1E293B; color:#E2E8F0; border:1px solid #334155; padding:5px 10px; border-radius:8px; font-size:0.75rem; font-weight:700;">⚡ Aprovação Imediata</span>'
    f'</div>'
    f'<div style="background:rgba(15, 23, 42, 0.9); border:1px solid #334155; border-radius:10px; padding:10px 12px; font-size:0.76rem; color:#94A3B8;">'
    f'<div style="color:#4ADE80; font-weight:800; margin-bottom:2px;">🔒 Ambiente 100% Criptografado (SSL)</div>'
    f'Autenticação oficial via <b>Supabase Auth</b> + emissão de comprovante e rastreio Correios.'
    f'</div>'
    f'</div>'
    f'</div>'
    f'<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; padding-top:16px; font-size:0.78rem; color:#64748B;">'
    f'<div>{rod_copy} &nbsp;|&nbsp; <b>CNPJ:</b> {rod_cnpj}</div>'
    f'<div>Desenvolvido com tecnologia <b>{rod_nome_loja} E-Commerce</b> • Todos os pedidos com código de rastreio</div>'
    f'</div>'
    f'</div>'
)
st.markdown(rodape_html_oficial, unsafe_allow_html=True)

# Botão Flutuante do WhatsApp (posicionado acima da barra inferior do Streamlit Cloud / iOS Safe Area)
st.markdown(
    f'<a href="https://wa.me/55{whats_num_clean}?text=Ol%C3%A1!%20Vim%20pelo%20site%20da%20Tags%20Inform%C3%A1tica" target="_blank" class="whatsapp-float-btn" title="Atendimento WhatsApp">💬</a>',
    unsafe_allow_html=True,
)
