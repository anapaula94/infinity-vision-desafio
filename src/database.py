import psycopg2
from psycopg2.extras import RealDictCursor

class DatabaseManager:
    """
    Gerencia a persistência de dados no PostgreSQL.
    Aqui fazemos o uso da biblioteca psycopg2 para realizar a
    integração Python-PostgreSQL.
    """

    def __init__(self, db_config: dict):
        self.conn = psycopg2.connect(**db_config)

    def save_result(self, img1, img2, img_res, dist, is_same):
        #Função para salvar as imagens e o resultado.
        query = """
            INSERT INTO resultados_comparacao 
            (img_1_origem, img_2_origem, img_final_resultado, distancia_calculada, foi_aprovado)
            VALUES (%s, %s, %s, %s, %s)
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (str(img1), str(img2), str(img_res), dist, is_same))
            self.conn.commit()

    def list_all_history(self):
        #Função para ler o banco e listar imagens salvas.
        query = "SELECT * FROM resultados_comparacao ORDER BY data_execucao DESC"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def close(self):
        self.conn.close()
