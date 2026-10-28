# IA

## 📋 Sobre

Sistema de **Inteligência Artificial** capaz de analisar imagens de lichias e classificar seu estado de maturação, integrado a uma **API em FastAPI** e persistência de dados no **MongoDB Atlas**.

---

## 🚀 Funcionalidades

* 📷 Upload de imagem via API
* 🧠 Classificação com modelo de IA (TensorFlow/Keras)
* 📊 Retorno da classe prevista + confiança
* ☁️ Armazenamento dos resultados no MongoDB Atlas
* 🔗 API REST para integração com web/mobile

---

## 🧠 Tecnologias utilizadas

* **Python 3.11**
* **FastAPI**
* **TensorFlow / Keras**
* **NumPy**
* **Pillow (PIL)**
* **MongoDB Atlas**
* **PyMongo**
* **Uvicorn**

---

## 📂 Estrutura do projeto

```text
ai/
├── ia_lichia/
|   ├── organize.py
|   └── train.py           
├── .env.example
├── .gitignore      
├── api.py       
├── app.py
├── LICENSE
├── logo.png
├── pyproject.toml
├── README.md
├── uv.lock
└── styles.css
```

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/CW-Mobo/ai.git
cd ai
```

### 2. Instalar dependências

```bash
uv sync
```

O `uv` cria o ambiente virtual em `.venv` e instala as versões registradas em `uv.lock`.

### 4. Configurar MongoDB Atlas

No código, configure sua string de conexão:

```python
MongoClient("mongodb+srv://USUARIO:SENHA@cluster.mongodb.net/")
```

> ⚠️ **Importante:** Nunca exponha sua senha em produção. Use variáveis de ambiente (`.env`).

### 5. Rodar a API

```bash
uv run uvicorn api:app --reload
```

Para iniciar a interface Streamlit:

```bash
uv run streamlit run app.py
```

---

## 📡 Endpoint principal

### 🔍 `POST /predict`

Envia uma imagem para análise.

**Exemplo via cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@imagem.jpg"
```

### 📥 Resposta

```json
{
  "classe_prevista": "madura",
  "confianca": 96.7,
  "nome_arquivo": "imagem.jpg",
  "mensagem": "Análise salva no MongoDB Atlas com sucesso"
}
```

---

## 🗄️ Banco de Dados (MongoDB)

Os dados são armazenados em: `ia_lichia_db` -> `analises`

**Exemplo de documento:**

```json
{
  "nome_arquivo": "imagem.jpg",
  "classe_prevista": "madura",
  "confianca": 96.7,
  "data_analise": "2026-04-23T15:55:34Z"
}
```

---

## 📌 Status do projeto

* ✅ API funcionando
* ✅ Integração com MongoDB Atlas
* ✅ Modelo de IA treinado
* 🔜 Integração com IoT (futuro)

---

## 📄 Licença

Projeto acadêmico de uso educacional.
