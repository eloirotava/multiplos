import sqlite3
import os

DB_DIR = "dbs"
os.makedirs(DB_DIR, exist_ok=True)

# Dados para o Restaurante 1
db1_path = os.path.join(DB_DIR, "restaurante1.db")
conn1 = sqlite3.connect(db1_path)
cursor1 = conn1.cursor()
cursor1.execute("DROP TABLE IF EXISTS menu")
cursor1.execute("CREATE TABLE menu (id INTEGER PRIMARY KEY, item TEXT, preco REAL)")
cursor1.execute("INSERT INTO menu (item, preco) VALUES ('Bife Ancho', 55.00)")
cursor1.execute("INSERT INTO menu (item, preco) VALUES ('Salmão Grelhado', 48.00)")
conn1.commit()
conn1.close()
print(f"Banco de dados '{db1_path}' criado com sucesso.")

# Dados para o Restaurante 2
db2_path = os.path.join(DB_DIR, "restaurante2.db")
conn2 = sqlite3.connect(db2_path)
cursor2 = conn2.cursor()
cursor2.execute("DROP TABLE IF EXISTS menu")
cursor2.execute("CREATE TABLE menu (id INTEGER PRIMARY KEY, item TEXT, preco REAL)")
cursor2.execute("INSERT INTO menu (item, preco) VALUES ('Pizza Calabresa', 35.00)")
cursor2.execute("INSERT INTO menu (item, preco) VALUES ('Refrigerante', 8.00)")
conn2.commit()
conn2.close()
print(f"Banco de dados '{db2_path}' criado com sucesso.")