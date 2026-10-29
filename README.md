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
├── assets/
|   ├── logo.png
|   └── styles.css
├── dashboard/
|   ├── __init__.py
|   ├── analysis.py
|   ├── history.py
|   ├── history_ui.py
|   ├── layout.py
|   ├── media.py
|   ├── reports.py
|   ├── results.py
|   └── settings.py
├── treinamento/
|   ├── organize.py
|   └── train.py
├── .env.example
├── .gitignore
├── api.py
├── app.py
├── LICENSE
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## ⚙️ Como executar o projeto

### Pré-requisitos

- Python 3.11, 3.12 ou 3.13
- Git
- `uv`

No Windows, instale o `uv` pelo WinGet:

```bash
winget install --id=astral-sh.uv -e
```

Outras opções estão na [documentação oficial de instalação do uv](https://docs.astral.sh/uv/getting-started/installation/).

### 1. Baixar o projeto e instalar as dependências

```bash
git clone https://github.com/CW-Mobo/ai.git
cd ai
uv python install 3.11
uv sync
```

O `uv sync` cria o ambiente virtual `.venv` e instala as versões fixadas em `uv.lock`.

### 2. Obter e preparar o dataset

O repositório não inclui o dataset. Obtenha as imagens e anotações usadas pela equipe e coloque-as em `treinamento/dataset`, com esta estrutura:

```text
treinamento/dataset/
├── train/
│   ├── images/
│   └── labels/
├── val/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

As anotações devem estar no formato YOLO usado pelo projeto: classe `0` corresponde a `nao_madura`, classe `2` corresponde a `madura`; a classe `1` é ignorada. Os nomes-base do arquivo `.txt` e da imagem correspondente devem ser iguais.

Converta as imagens anotadas para as pastas de classes que o treinamento espera:

```bash
uv run python treinamento/organize.py
```

Esse comando cria `madura/` e `nao_madura/` dentro de cada divisão. Se o dataset já estiver nesse formato, pule a conversão e confirme que existem imagens nas duas pastas em `train`, `val` e `test`. O treinamento usa lotes de 32 imagens; mantenha pelo menos 32 imagens em `train` e em `val`.

### 3. Gerar ou instalar o modelo Keras

Para gerar o modelo a partir do dataset preparado, execute:

```bash
uv run python treinamento/train.py
```

Ao terminar sem erros, o arquivo será criado em:

```text
treinamento/modelo_lichia.keras
```

Confira se ele existe antes de iniciar a API:

```powershell
Test-Path treinamento\modelo_lichia.keras
```

O resultado deve ser `True`. O GitHub não fornece esse arquivo: modelos `.keras` são ignorados pelo `.gitignore`. Se a equipe já tiver um modelo treinado, copie-o para `treinamento/modelo_lichia.keras` e pule o treinamento.

### 4. Configurar o MongoDB Atlas

Crie um arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
notepad .env
```

Abra `.env` e substitua o valor de `MONGO_URI` pela connection string do seu cluster no MongoDB Atlas. Use o usuário e a senha do banco, autorize o IP da máquina no Atlas e mantenha a linha neste formato:

```dotenv
MONGO_URI=mongodb+srv://USUARIO:SENHA@SEU-CLUSTER.mongodb.net/?retryWrites=true&w=majority&appName=mobo
```

Se a senha tiver caracteres especiais, faça a codificação URL desses caracteres antes de colocá-la na connection string. Não publique o `.env` nem coloque credenciais diretamente no código. A API grava as análises no banco `mobo`, coleção `analises`.

### 5. Iniciar a API

Em um terminal aberto na pasta `ai`, execute:

```bash
uv run uvicorn api:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`. Confira `http://127.0.0.1:8000/health`; o campo `mongodb_atlas` deve indicar `conectado`.

### 6. Iniciar o painel

Em outro terminal, também na pasta `ai`, execute:

```bash
uv run streamlit run app.py
```

O Streamlit exibirá o endereço local do painel. O painel e a API carregam o mesmo arquivo `treinamento/modelo_lichia.keras`.

### Ordem resumida

1. Obter o dataset e colocá-lo em `treinamento/dataset`.
2. Preparar as classes, se os dados estiverem no formato YOLO.
3. Treinar o modelo ou copiar o modelo já treinado para `treinamento/modelo_lichia.keras`.
4. Configurar o MongoDB no `.env`.
5. Iniciar a API e o painel em terminais separados.

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

Os dados são armazenados em: `mobo` -> `analises`

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

* ✅ API e painel implementados
* ✅ Integração com MongoDB Atlas
* ℹ️ Dataset e modelo `.keras` não são incluídos no GitHub; siga as etapas acima para obter ou gerar o modelo localmente.
* 🔜 Integração com IoT (futuro)

---

## 📄 Licença

Projeto acadêmico de uso educacional.
