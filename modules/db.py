import sqlite3

def conectar_db():
  conexion = sqlite3.connect('database.db')
  return conexion
  
def obtener_db():
  conexion = conectar_db()
  return conexion
  
def cerrar_db(conexion):
  conexion.close()
  
def obtener_cursor(conexion):
  cursor = conexion.cursor()
  return cursor
  
def cerrar_cursor(cursor):
  cursor.close()
  
def ejecutar_sentencia(cursor, sentencia):
  cursor.execute(sentencia)

def ejecturar_sentencia_y_commit(conexion,cursor,sentencia):
  cursor.execute(sentencia)
  conexion.commit()
  
def ejecutar_sentencias(cursor, sentencias):
  for sentencia in sentencias:
    ejecutar_sentencia(cursor, sentencia)
    
def ejecutar_sentencias_con_parametros(cursor, sentencias, parametros):
  for sentencia in sentencias:
    cursor.execute(sentencia, parametros)
    
def ejecutar_sentencias_con_parametros_y_commit(conexion, cursor, sentencias, parametros=None):
  try:
      for sentencia in sentencias:
          if parametros is not None:
              cursor.execute(sentencia, parametros)
          else:
              cursor.execute(sentencia)
      conexion.commit()
  except sqlite3.Error as e:
      conexion.rollback()
      raise e
    
def ejecutar_sentencias_con_parametros_y_commit_con_retorno(cursor, sentencias, parametros):
  ejecutar_sentencias_con_parametros(cursor, sentencias, parametros)
  return cursor.lastrowid
  
def create_table():
    conexion = obtener_db()
    cursor = obtener_cursor(conexion)
    ejecutar_sentencias_con_parametros_y_commit(conexion, cursor, ['''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )'''], [])
    cerrar_cursor(cursor)
    cerrar_db(conexion)