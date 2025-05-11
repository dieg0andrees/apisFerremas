import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="entregaferramas",
        password="entregaferramas",
        dsn="localhost:1521"
    )
    return conexion