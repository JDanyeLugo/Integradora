from .db import get_connection

mydb = get_connection()

class Category:

    def __init__(self, ID_Reporte, ID_Cliente, Tipo, Descripcion, Fecha_Generacion=None):
        self.ID_Reporte = ID_Reporte
        self.ID_Cliente = ID_Cliente
        self.Tipo = Tipo
        self.Descripcion = Descripcion
        self.Fecha_Generacion = Fecha_Generacion 
        
    def save(self):
        # Create a New Object in DB
        if self.ID_Reporte is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO reportes(Tipo, Descripcion, Fecha_Generacion) VALUES(%s, %s, %s)"
                val = (self.Tipo, self.Descripcion, self.Fecha_Generacion)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Reporte
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE reportes SET Tipo = %s, Descripcion = %s , Fecha_Genenracion = %s WHERE ID_Reportes = %s"
                val = (self.Tipo, self.Descripcion, self.Fecha_Generacion)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Reporte
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM reportes WHERE ID_Reporte = { self.ID_Reporte }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Reporte