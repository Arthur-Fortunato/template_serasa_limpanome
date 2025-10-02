import requests
from ..dbacess import DbCON

def inclusao_limpa_nome():
    url             = "URL DE INCLUSAO EM PRODUÇÃO DO SERASA LIMPA NOME"
    db              = DbCON()
    resultado_query = db.pega_dados_para_incluir()
    apikey          = "SUA APIKEY DISPONIBILIZADA PELO SERASA LIMPA NOME"
    
    header = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type" : "application/json"
    }    
    
    resp = requests.post(url=url, headers=header, json=resultado_query)
    print(f"status_code: {resp.status_code}")
    print("Resposta bruta:", resp.text)
    
def exclusao_limpa_nome():
    url             = "URL DE EXCLUSAO EM PRODUÇÃO DO SERASA LIMPA NOME"
    db              = DbCON()
    resultado_query = db.pega_dados_para_excluir()
    apikey          = "SUA APIKEY DISPONIBILIZADA PELO SERASA LIMPA NOME"
    
    header = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type" : "application/json"
    }    
    
    resp = requests.post(url=url, headers=header, json=resultado_query)
    print(f"status_code: {resp.status_code}")
    print("Resposta bruta:", resp.text)  