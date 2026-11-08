"""Conexão com o banco de dados.

- Se as variáveis TURSO_DATABASE_URL e TURSO_AUTH_TOKEN estiverem definidas,
  conecta no banco remoto (Turso, persistente). É o modo usado no deploy.
- Caso contrário, usa o SQLite local em ./database/ (modo desenvolvimento).

A interface é a mesma do sqlite3 padrão (execute/commit/fetchall/close),
portanto o restante do código não precisa saber quem está por trás.
"""
import os

try:
    from dotenv import load_dotenv

    # Procura o .env subindo as pastas (funciona tanto da raiz quanto de src/)
    load_dotenv()
except Exception:
    pass


def connect_db(db_path: str):
    """Abre conexão: remoto (Turso) quando configurado, senão local."""
    turso_url = os.getenv("TURSO_DATABASE_URL")
    turso_token = os.getenv("TURSO_AUTH_TOKEN")

    if turso_url:
        import turso_serverless

        return turso_serverless.connect(turso_url, auth_token=turso_token)

    import sqlite3

    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(db_path)
