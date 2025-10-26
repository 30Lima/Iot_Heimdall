import sys
import os

# Adiciona a pasta raiz ao 'path' do Python
# Isto permite-nos importar módulos de dentro da pasta 'app'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Importa o 'init_db' de dentro de 'app/database.py'
from app.database import init_db, db_session

if __name__ == "__main__":
    print("\nTentando conectar ao Oracle e criar tabelas...")
    print("(Isto pode demorar alguns segundos...)")
    
    try:
        # Esta é a função que importámos do app/database.py
        init_db()
        
    except Exception as e:
        print("\n❌ Ocorreu um ERRO ao tentar criar as tabelas.")
        print("--------------------------------------------------")
        print(f"Detalhes: {e}")
        print("--------------------------------------------------")
        print("Possíveis causas:")
        print("1. O Oracle Instant Client não está instalado ou configurado no PATH do sistema.")
        print("2. As credenciais no arquivo .env (USER, PASSWORD, HOST) estão incorretas.")
        print("3. O servidor Oracle está offline ou a porta 1521 está bloqueada.")
        
    finally:
        # É importante fechar a sessão após o uso
        db_session.remove()
        print("Processo de inicialização do banco de dados concluído.")