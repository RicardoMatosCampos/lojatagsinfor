# 🛒 TagsInfor — E-Commerce & Painel Multi-Nicho (Streamlit + Supabase)

Sistema completo de **E-commerce, Catálogo Multi-Nicho e Gestão Comercial (ERP/Admin)** desenvolvido para a **Tags Informática**, utilizando **Streamlit** no frontend/backend e **Supabase** (PostgreSQL + Supabase Auth + Supabase Storage) para persistência relacional em nuvem.

---

## ✨ Principais Funcionalidades

### 🛍️ Loja Online (Experiência do Cliente)
- **Vitrine Responsiva (Desktop, Android e iOS):** Grade adaptativa com busca inteligente e filtros por **Departamento › Categoria › Subcategoria**.
- **Modal de Detalhes Interativo (`@st.dialog`):** Abre na frente da tela com galeria de fotos interativa, player de vídeo demonstrativo (YouTube, Shorts, Vimeo ou MP4), ficha técnica e avaliações reais de clientes.
- **Sessão e Login Individual por Usuário:** Cada visitante recebe seu próprio identificador de sessão (`sid`), isolando carrinhos e contas logadas entre dispositivos diferentes.
- **Autenticação Híbrida Oficial:** Cadastro e login por **E-mail ou CPF/CNPJ** integrados ao **Supabase Auth** e à tabela relacional `public.clientes` (com senhas protegidas por hash `SHA-256`).
- **Checkout Transparente com Pix (Padrão Bacen):** Cálculo automático de cupons de desconto, preenchimento automático de endereço via **ViaCEP** e geração instantânea de QR Code Pix Copia e Cola.
- **Área do Cliente & Rastreio:** Histórico de pedidos em tempo real, código de rastreio e abertura de chamados de suporte.

### 🛠️ Painel Administrativo (`?admin=1`)
- **Gestão Completa de Produtos & Mídia:** Cadastro e edição rápida de preços, estoque, múltiplas fotos (salvas automaticamente no bucket público `produtos-midia` do Supabase Storage) e vídeo.
- **Gestão de Clientes & Controle de Senhas:**
  - Lista completa de clientes com atalho direto para WhatsApp.
  - **Redefinição imediata de senha de qualquer usuário/cliente** pelo Administrador (tanto pelo botão `🔑 Alterar Senha` na lista de clientes quanto pela aba dedicada `🔑 Alterar Senhas`).
  - Alteração da própria senha de Administrador e disparo de link de recuperação por e-mail.
- **Vendas, Pedidos e Estoque Inteligente:** Atualização de status, inserção de código de rastreio e devolução automática de estoque caso o pedido seja cancelado.
- **Emissão de Documentos Fiscais:** Geração pronta para impressão de **DANFE Simplificada (NF-e)** e **Declaração de Conteúdo dos Correios**.
- **Personalização da Loja Online:** Edição em tempo real do cabeçalho, barra promocional, banner principal e rodapé institucional.

---

## 📁 Estrutura de Arquivos do Repositório (O que vai para o GitHub)

Mantenha no GitHub **apenas** os arquivos essenciais de código, banco de dados e dependências:

```text
Lojatagsinfor/
├── .gitignore                        # Protege credenciais, venv e caches locais
├── README.md                         # Documentação oficial do projeto
├── requirements.txt                  # Dependências Python para o Streamlit Cloud
├── app.py                            # Aplicação principal (Loja + Painel Admin)
├── supabase_schema.sql               # Script SQL completo (13 tabelas relacionais)
└── supabase_migracao_categorias.sql  # Script SQL de migração/seed de categorias
```

### 🚫 Pastas e Arquivos Ignorados pelo `.gitignore` (NÃO vão para o GitHub)
- `.venv/` e `__pycache__/` (ambiente virtual Python e cache de execução)
- `.streamlit/` (contém `secrets.toml` com suas chaves privadas do Supabase)
- `Senha Banco.txt` (arquivo local de senha)
- `.sessoes_persistentes.json` (cache local temporário de sessões)
- `.agents/` (arquivos auxiliares locais do editor)

---

## 🚀 Como Implantar no Streamlit Cloud

1. Suba os arquivos listados acima para o seu repositório no GitHub (`main`).
2. No painel do **Streamlit Cloud** (`share.streamlit.io`), clique em **Create app**:
   - **Repository:** `RicardoMatosCampos/lojatagsinfor`
   - **Branch:** `main`
   - **Main file path:** `app.py` *(atenção: digite exatamente `app.py`)*
3. Clique em **Advanced settings...** › **Secrets** e cole suas chaves do Supabase:

```toml
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_ANON_OU_SERVICE_ROLE"
CHAVE_PIX = "sua_chave_pix_aqui"
NOME_BENEFICIARIO = "TAGS INFORMATICA"
CIDADE_BENEFICIARIO = "MANAUS"
WHATSAPP_LOJA = "92981234567"
SENHA_ADMIN = "sua_senha_mestre_admin"
```

4. Clique em **Deploy!**.

---

## 💻 Como Executar Localmente

```powershell
# 1. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Iniciar a aplicação
streamlit run app.py
```

- **Acesso à Loja:** `http://localhost:8501`
- **Acesso ao Painel Admin:** `http://localhost:8501/?admin=1`
