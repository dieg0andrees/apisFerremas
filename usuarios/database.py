import oracledb

def get_conexion():
    conexion = oracledb.connect(
        user="entregaferramas",
        password="entregaferramas",
        dsn="localhost:1521/orcl"
    )
    return conexion

#Puede que no funcione correctamente porque falta algo despues del puerto en el dsn