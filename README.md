# TagsInfor – e‑Commerce Streamlit + Supabase

**TagsInfor** is a lightweight e‑commerce storefront built with **Streamlit** for the UI and **Supabase** as the backend (database, authentication and storage).  The application lets customers browse products, view a responsive product‑detail modal with an image‑gallery/ video player, add items to a cart and checkout.  Admin users can manage products, upload media to Supabase storage, and edit pricing.

---

## ✨ Features
- Responsive UI for desktop and mobile (auto‑layout, custom CSS).  
- Product gallery modal with image thumbnails and video support (uses `st.radio` + thumbnails).  
- Supabase integration: tables for departments, categories, sub‑categories, products, orders, coupons, customers, etc.  
- Media upload (images/video) stored in a public Supabase bucket (`produtos‑midia`).  
- Cart persisted per user (via Supabase Auth UID).  
- Admin panel (adds/edits products, uploads media).  
- Simple pricing logic with discount percentages and Pix‑payment badge.  
- Test suite with `pytest` for core services.  
- CI pipeline (GitHub Actions) for linting, type‑checking and tests.

---

## 📁 Repository layout
```
Lojatagsinfor/
│   .gitignore           # excludes env, caches, secrets, etc.
│   README.md            # ⬆️ this file
│   requirements.txt     # Python dependencies
│
├── lojatagsinfor/       # Python package (core code)
│   ├── __init__.py
│   ├── main.py          # `streamlit run lojatagsinfor/main.py`
│   ├── config.py        # Settings & secret loading
│   ├── client/
│   │   └── supabase_client.py
│   ├── services/
│   │   ├── product_service.py
│   │   └── media_service.py
│   ├── ui/
│   │   ├── header.py
│   │   ├── hero.py
│   │   ├── product_card.py
│   │   ├── modal.py      # gallery & video modal
│   │   └── footer.py
│   ├── utils/
│   │   └── helpers.py
│   └── assets/
│       └── custom.css   # all CSS (was embedded in app.py)
│
├── sql/                 # Supabase schema & migration scripts
│   ├── supabase_schema.sql
│   └── supabase_migracao_categorias.sql
│
├── tests/               # Pytest suite
│   ├── __init__.py
│   └── test_product_service.py
│
└── .github/            # CI workflow (optional)
    └── workflows/ci.yml
```

---

## 🛠️ Setup (local development)
1. **Clone the repo**
   ```bash
   git clone https://github.com/<your‑user>/Lojatagsinfor.git
   cd Lojatagsinfor
   ```
2. **Create a virtual environment** (requires Python 3.10+)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # PowerShell: .venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Supabase credentials**
   - In the project root create a file `.streamlit/secrets.toml` (it is ignored by git). Example:
   ```toml
   SUPABASE_URL = "https://<your‑project>.supabase.co"
   SUPABASE_KEY = "public‑anon‑key"
   ```
   - Alternatively, export the variables in your shell:
   ```bash
   export SUPABASE_URL=...
   export SUPABASE_KEY=...
   ```
5. **Run the app**
   ```bash
   streamlit run lojatagsinfor/main.py
   ```
   The UI will be available at `http://localhost:8501`.

---

## 📚 Database schema
The full schema lives in `sql/supabase_schema.sql`.  It defines 13 tables:
- `departamentos`, `categorias`, `subcategorias`
- `clientes` (Supabase Auth UID + cart JSONB)
- `produtos` – includes `galeria_imagens` (JSONB), `video_url`, `ficha_tecnica`
- `pedidos`, `pedido_itens`
- `cupons`, `avaliacoes_produtos`, `chamados_suporte`, etc.

Run the script on your Supabase project (via the Supabase dashboard → SQL editor) to create the tables.  The migration script `supabase_migracao_categorias.sql` adds sample data for categories.

---

## ✅ Testing
```bash
pytest tests
```
The test suite covers:
- CRUD operations on products (`product_service`).
- Media upload logic (`media_service`).
- Helper utilities.

A CI workflow (`.github/workflows/ci.yml`) runs lint (`ruff`), type checking (`mypy`) and the test suite on each push.

---

## 🤝 Contributing
Contributions are welcome!  Typical workflow:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/awesome‑thing`).
3. Make your changes, add/extend tests.
4. Ensure the CI passes locally:
   ```bash
   ruff check .
   mypy lojatagsinfor
   pytest
   ```
5. Open a Pull Request with a clear description of the change.

Please keep the **`.gitignore`** up‑to‑date if you add new temporary files or secrets.

---

## 📄 License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## 🎉 Enjoy!
Feel free to open an issue if you find bugs or have feature ideas.  Happy coding!
