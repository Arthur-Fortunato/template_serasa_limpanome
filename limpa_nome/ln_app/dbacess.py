import mysql.connector

class DbCON:
    def __init__(self):
        self.host_db    = 'SEU HOST DO BANCO',
        self.senha_db   = 'SUA SENHA DO BANCO',
        self.user_db    = 'SEU USUARIO DO BANCO',
        self.db         = 'SEU BANCO DE DADOS'
        
    def conecta_db(self):
        try:
            conn = mysql.connector.connect(
                host_db     = self.host_db,
                senha_db    = self.senha_db,
                user_db     = self.user_db,
                db          = self.db
            )
            return conn
        except:
            print("Falha ao conectar no banco")
            return None
    
    def pega_dados_para_incluir(self): 
        conn   = self.conecta_db()
        cursor = conn.cursor()
        query  = """
            SUA QUERY PRA PEGAR OS DADOS DO BANCO
        """
        cursor.execute(query)
        ressultado_query  = cursor.fetchall()
        lista_para_envio  = []
        for resp in ressultado_query:
            # ESTOU FAZENDO DESSE JEITO COMO SE FOSSE PEGAR NESSA MESMA ORDEM, MAS VOCÊ DECIDE COMO VAI FICAR
            payload = {
                "contractNumber": resp[0],
                "document"      : resp[1],
                "wallet"        : resp[2],
                "occurrenceDate": resp[3], 
                "debtType"      : resp[4],
                "debtValue"     : resp[5],
                "offer": 
                { 
                    "value"                   : resp[6], 
                    "dueDaysFirstInstallment" : resp[7],
                    "maxInstallments"         : resp[8],
                },
                "debtOrigin": 
                {
                    "name"      : resp[9],
                    "document"  : resp[10]
                }
            }
            lista_para_envio.append(payload)
        return lista_para_envio
    
    
    def pega_dados_para_excluir(self): 
        conn   = self.conecta_db()
        cursor = conn.cursor()
        query  = """
            SUA QUERY PRA PEGAR OS DADOS DO BANCO
        """
        cursor.execute(query)
        ressultado_query  = cursor.fetchall()
        lista_para_envio  = []
        for resp in ressultado_query:
            # AQUI É O DEBT_ID
            payload = {
                "id": resp[0]
            }
            lista_para_envio.append(payload)
        return lista_para_envio