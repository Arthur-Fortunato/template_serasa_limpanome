# Integração Serasa - Limpa Nome

**Template de integração com o Serasa (Pefin), desenvolvido de acordo com o manual oficial.**

## 📌 O que faz
- Envia requests para o Serasa  
- Recebe e processa os webhooks de retorno  
- Salva e atualiza os dados no banco de dados

## 💻 Tecnologias
- Python  
- Django  
- MySQL (utilizado para incluir e remover dados do Serasa)

## ⚙️ Configuração
Antes de rodar o projeto, **atualize as configurações do banco de dados** no arquivo `settings.py`.  
> ⚠️ Não altere apenas as views ou scripts, pois o sistema pode falhar se as configurações do banco não estiverem corretas.  
> Se preferir, utilize variáveis de ambiente — este é apenas um código base simplificado.

## 🧑‍💻 Como usar os scripts
Exemplo de execução no shell do Django:

```bash
1° - cd limpa_nome  # ou o nome da pasta principal
2° - python manage.py shell
3° - from limpa_nome_app.scripts.scripts import nome_da_função
4° - nome_da_função()
