# 🖐️ IA Vision Studio | NLW Operador (Trilha Python)

O **IA Vision Studio** é uma plataforma de visão computacional em tempo real que une o poder do **Python** com modelos avançados de Deep Learning. Este projeto foi desenvolvido durante a trilha Python do evento **NLW Operador** da Rocketseat, explorando o potencial de fluxos inteligentes, automação e arquitetura de IA.

---

## ⚡ Desenvolvimento Low Code & IA Assistida

Este projeto foi construído utilizando uma abordagem moderna de desenvolvimento acelerado por Inteligência Artificial, focada em produtividade e resolução de problemas complexos:

* **Prompt Engineering:** Uso estratégico de LLMs para arquitetura de código, lógica de negócio e correção de bugs.
* **Antigravity:** Utilização do ambiente Antigravity para prototipagem rápida e testes de fluxos.
* **VS Code:** Ambiente de desenvolvimento principal para refinamento, integração de sistemas e versionamento.

---

## 🚀 Deploy & Infraestrutura (Hugging Face)

Um dos grandes marcos deste projeto foi o **Deploy no Hugging Face Spaces**. O aplicativo está rodando em um container **Docker**, garantindo que todas as dependências (como OpenCV e MediaPipe) funcionem perfeitamente na nuvem, assim como funcionam localmente.

* **Ambiente:** Hugging Face Spaces (SDK Docker)
* **Processamento:** Otimização de CPU para execução de modelos YOLOv8 e MediaPipe.
* **Acesse o projeto ao vivo:** 👉 [IA Vision Studio no Hugging Face](https://huggingface.co/spaces/tissiany-delmiro/IA-Vision-Studio)

---

## 🧠 Funcionalidades Principais

* **Reconhecimento de Gestos:** Identificação precisa de sinais (coração, joinha, paz, etc.) utilizando **MediaPipe** e um classificador customizado treinado via **Scikit-Learn**.
* **Detecção de Objetos:** Implementação do modelo **YOLOv8** (Ultralytics) para rastreamento de elementos em tempo real.
* **Interface Interativa:** Painel dinâmico desenvolvido com **FastHTML** e **JavaScript** que permite ativar/desativar camadas de IA e monitorar o FPS.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.11
* **Visão Computacional:** OpenCV, MediaPipe, Ultralytics (YOLOv8)
* **Machine Learning:** Scikit-Learn, Joblib
* **Web Framework:** FastHTML
* **Infraestrutura:** Docker, Hugging Face Spaces, GitHub

---

## 💻 Como Rodar Localmente

Siga o passo a passo abaixo para clonar o repositório e rodar o projeto na sua máquina:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/tissiany-delmiro/ia-vision-studio.git](https://github.com/tissiany-delmiro/ia-vision-studio.git)
    ```

2.  **Entre na pasta do projeto:**
    ```bash
    cd ia-vision-studio
    ```

3.  **Crie e ative seu ambiente virtual:**
    ```bash
    python -m venv .venv

    # No Windows:
    .venv\Scripts\activate

    # No Linux/Mac:
    source .venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    Após rodar, abra o navegador no endereço indicado (geralmente `http://localhost:5001`).

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais durante o NLW Operador. Sinta-se à vontade para explorar, contribuir e aprender com ele!

---
> **Dica Extra:** Não esqueça de adicionar o link do seu Hugging Face no campo **"Website"** na lateral direita do repositório no GitHub para facilitar o acesso de quem visita seu perfil!
