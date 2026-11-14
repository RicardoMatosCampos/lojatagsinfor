# 🛒 TagsInfor — E-Commerce de Grande Escala & ERP Comercial (Streamlit + Supabase)

Plataforma completa de **E-Commerce Multi-Nicho, Checkout Híbrido (Pix + Ton + Mercado Pago) e Inteligência Comercial (BI/ERP)** desenvolvida para a **Tags Informática**, utilizando **Streamlit** (com tema claro de alto contraste) e **Supabase** (PostgreSQL + Supabase Auth + Supabase Storage).

---

## ✨ Principais Funcionalidades

### 🛍️ 1. Loja Online — Vitrine de Grande Escala (Experiência do Cliente)
- **Visual Claro, Moderno e Confiável (Light UI):** Tema claro suave (`#F8FAFC` / `#FFFFFF`) projetado para máxima leitura e conversão em Desktop, Android e iOS.
- **Carrossel de Propagandas & Banners Animados:** Slides rotativos abaixo do cabeçalho totalmente gerenciáveis pelo painel administrativo.
- **Ordenação Comercial & Paginação Rápida:**
  - Ordenação por **⭐ Destaques & Relevância**, **🔥 Mais Vendidos** (calculado sobre vendas reais), **💰 Menor Preço**, **💎 Maior Preço**, **🏷️ Maior Desconto (%)** e **🆕 Lançamentos**.
  - Paginação rápida (`12`, `24`, `48` ou `96` itens por página) e filtro instantâneo **`⚡ Só disponível / estoque`**.
- **Gatilhos de Conversão (Escassez & Prova Social):**
  - Alertas automáticos de **`🚨 ÚLTIMA UNIDADE EM ESTOQUE!`** e **`⏳ Últimas X unidades — Alta procura!`** quando o estoque está baixo (`1 a 5` unidades).
  - Selo dinâmico **`🔥 +X vendidos`** nos produtos com histórico de pedidos.
- **Modal de Detalhes Interativo (`@st.dialog`):** Galeria de fotos sem recarregar a página, vídeo demonstrativo (YouTube, Shorts, Vimeo ou MP4), simulador de frete por CEP, ficha técnica e avaliações verificadas.
- **Checkout Transparente com 3 Formas de Pagamento Simultâneas:**
  1. **💠 Pix Oficial (Padrão Bacen):** QR Code imediato + código Pix Copia e Cola.
  2. **💚 Link de Pagamento Ton (Stone):** Redireciona o cliente para o link do produto (ou link global da loja) para parcelar no cartão em até 12x.
  3. **💙 Mercado Pago:** Suporta Link Direto por produto, Link Global ou geração automática via API (`MP_ACCESS_TOKEN`).
- **Integração Direta com WhatsApp:** Ao finalizar o pedido (inclusive via Link da Ton ou Mercado Pago), o sistema gera o protocolo do pedido e abre uma mensagem pronta para o WhatsApp da loja para **separação imediata do produto**.
- **Políticas Oficiais no Rodapé:** Modais interativos de **🔒 Privacidade e LGPD (Lei nº 13.709/2018)**, **🔄 Trocas, Devoluções e Garantia (CDC - 7 dias)** e **🚚 Política de Frete & Rastreio**.

---

### 🛠️ 2. Painel Administrativo & BI Comercial (`?admin=1`)
- **📊 Painel "Saber o que Vendo" (Inteligência Comercial & Lucro Real):**
  - Filtro por período (**Hoje**, **Últimos 7 dias**, **Últimos 30 dias**, **Este Mês** ou **Todo o Histórico**) e por status (**Todos** vs **Apenas Pagos/Entregues**).
  - **KPIs Financeiros em Tempo Real:** Faturamento Bruto, **Lucro Líquido Real (R$ e Margem %)** descontando o preço de custo, Ticket Médio, Unidades Vendidas e Capital Parado em Estoque.
  - **Gráficos e Rankings:** Receita por Forma de Pagamento (Pix, Ton, Mercado Pago), **Curva ABC dos Produtos Mais Vendidos** e Vendas por Departamento.
  - **Exportação 1-Clique:** Download de planilhas **CSV/Excel** de *Produtos Mais Vendidos (Curva ABC)* e *Relatório Completo de Pedidos*.
- **📦 Gestão Rápida de Produtos, Custos e Links Ton/MP:**
  - Edição rápida na própria lista de produtos: **Custo (R$)**, **Venda (R$)**, **Estoque**, **Links Individuais da Ton e Mercado Pago** e **Selo de Lucro Unitário (`📈 Lucro: R$ X/un (Y%)`)**.
  - **Ativação / Inativação Instantânea:** Marcar ou desmarcar a caixinha **`[x] Ativo`** oculta ou exibe o produto na vitrine imediatamente, sem precisar clicar em botões extras.
  - Upload de fotos otimizadas em WebP direto para o bucket público `produtos-midia` do **Supabase Storage**.
- **🚚 Configuração de Frete & Logística:**
  - Configuração de **Frete Grátis acima de R$ X**, **Motoboy / Entrega Expressa Local**, **Correios PAC**, **Correios SEDEX** e **Retirada no Centro de Distribuição**.
- **🔔 Notificações Automáticas de Status (WhatsApp + E-mail):**
  - Ao alterar o status de um pedido (`pendente`, `pago`, `enviado`, `entregue`, `cancelado`) ou informar o código de rastreio, o sistema envia e-mail automático (se SMTP configurado) e gera o botão de 1 clique para avisar o cliente no WhatsApp.
- **🧾 Documentos Fiscais:** Emissão pronta para impressão de **DANFE Simplificada (NF-e)** e **Declaração de Conteúdo dos Correios**.

---

## 🗄️ O que Alterar no Banco de Dados (Supabase SQL Editor)

### Opção A — Você JÁ TEM o banco criado com produtos e pedidos (Recomendado)
Para **não apagar nenhum produto ou pedido existente**, abra o **SQL Editor** no painel do Supabase, cole apenas o comando abaixo e clique em **Run**:

```sql
-- Adiciona Preço de Custo, Links Individuais (Ton e Mercado Pago) e Frete Grátis em Produtos
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS preco_custo NUMERIC(10, 2) DEFAULT 0.00;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS link_pagamento_ton TEXT;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS link_pagamento_mp TEXT;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS frete_gratis_produto BOOLEAN DEFAULT FALSE;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS preco_original NUMERIC(10, 2);
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS destaque BOOLEAN DEFAULT FALSE;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS galeria_imagens JSONB DEFAULT '[]'::jsonb;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS video_url TEXT;
ALTER TABLE public.produtos ADD COLUMN IF NOT EXISTS ficha_tecnica JSONB DEFAULT '[]'::jsonb;

-- Adiciona Método de Pagamento (Pix, Ton, MP), Modalidade de Frete e Rastreio em Pedidos
ALTER TABLE public.pedidos ADD COLUMN IF NOT EXISTS metodo_pagamento TEXT DEFAULT 'pix';
ALTER TABLE public.pedidos ADD COLUMN IF NOT EXISTS modalidade_frete TEXT DEFAULT 'Entrega Padrão';
ALTER TABLE public.pedidos ADD COLUMN IF NOT EXISTS codigo_rastreio TEXT;
ALTER TABLE public.pedidos ADD COLUMN IF NOT EXISTS estoque_devolvido BOOLEAN DEFAULT FALSE;

-- Garante a tabela de configurações globais da loja (Banners, Cabeçalho, Frete, Políticas LGPD)
CREATE TABLE IF NOT EXISTS public.config_loja (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    chave TEXT UNIQUE NOT NULL DEFAULT 'principal',
    dados JSONB NOT NULL DEFAULT '{}'::jsonb
);
ALTER TABLE public.config_loja DISABLE ROW LEVEL SECURITY;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated, service_role;

-- Recarrega o cache da API do Supabase imediatamente
NOTIFY pgrst, 'reload schema';
```

### Opção B — Criar um banco de dados novo do zero
Se estiver configurando um projeto Supabase novo do zero, execute o conteúdo completo do arquivo [`supabase_schema.sql`](supabase_schema.sql) no SQL Editor.

---

## 📁 Organização das Pastas: O que vai para o GitHub?

A pasta do projeto está organizada para que **somente os 7 arquivos essenciais e seguros** subam para o GitHub:

```text
Lojatagsinfor/
├── .streamlit/
│   └── config.toml                   # ✅ VAI PARA O GITHUB (Tema claro oficial da loja)
├── .gitignore                        # ✅ VAI PARA O GITHUB (Bloqueia senhas, venv e caches)
├── README.md                         # ✅ VAI PARA O GITHUB (Documentação completa e SQL)
├── requirements.txt                  # ✅ VAI PARA O GITHUB (Dependências do Streamlit Cloud)
├── app.py                            # ✅ VAI PARA O GITHUB (Código principal da Loja + Admin)
├── supabase_schema.sql               # ✅ VAI PARA O GITHUB (Estrutura completa de 13 tabelas)
└── supabase_migracao_categorias.sql  # ✅ VAI PARA O GITHUB (Script de atualização sem perda de dados)
```

### 🔒 O que fica APENAS no seu computador (Bloqueado pelo `.gitignore`)
Estes arquivos/pastas **nunca** devem ir para o GitHub (o `.gitignore` já os protege automaticamente):
- ❌ `.streamlit/secrets.toml` *(suas chaves secretas do Supabase, Pix e senha Admin)*
- ❌ `Senha Banco.txt` *(anotação pessoal de senha)*
- ❌ `.sessoes_persistentes.json` *(cache local de sessões)*
- ❌ `.venv/` e `__pycache__/` *(ambiente Python local)*
- ❌ `.agents/` *(configurações locais do assistente)*

---

## 🚀 Como Enviar para o GitHub e Publicar no Streamlit Cloud

### 1. Subindo para o GitHub
No terminal dentro da pasta do projeto (`c:\Users\USUARIO\Documents\Pasta casa\Lojatagsinfor`), execute:

```powershell
git init
git add .gitignore .streamlit/config.toml README.md requirements.txt app.py supabase_schema.sql supabase_migracao_categorias.sql
git commit -m "Atualizacao completa: Vitrine Grande Escala, BI Saber o que Vendo, Ton/MP e Tema Claro"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### 2. Configurando os Secrets no Streamlit Cloud
No painel do **Streamlit Cloud** (`share.streamlit.io`), acesse **Settings** › **Secrets** do seu aplicativo e cole:

```toml
SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_CHAVE_ANON_OU_SERVICE_ROLE"
CHAVE_PIX = "sua_chave_pix_aqui"
NOME_BENEFICIARIO = "TAGS INFORMATICA"
CIDADE_BENEFICIARIO = "MANAUS"
WHATSAPP_LOJA = "92981234567"
SENHA_ADMIN = "sua_senha_mestre_admin"
```

---

## 💻 Como Executar Localmente no seu Computador

```powershell
# 1. Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar/atualizar dependências
pip install -r requirements.txt

# 3. Iniciar a loja e o painel administrativo
streamlit run app.py
```

- **Acesso à Vitrine da Loja:** `http://localhost:8501`
- **Acesso direto ao Painel Admin:** `http://localhost:8501/?admin=1`
