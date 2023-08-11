from .db import get_connection

mydb = get_connection()

class Category:

    def __init__(self, ID_Mensualidad, ID_Prestamo, NumeroMensualidad, Monto, FechaVencimiento, Estado=None):
        self.ID_Mensualidad = ID_Mensualidad
        self.ID_Prestamo = ID_Prestamo
        self.NumeroMensualidad = NumeroMensualidad
        self.Monto = Monto
        self.FechaVencimiento = FechaVencimiento
        self.Estado = Estado
        
    def save(self):
        # Create a New Object in DB
        if self.ID_Mensualidad is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO mensualidades(NumeroMensualidad, Monto, FechaVencimiento, Estado) VALUES(%s, %s, %s, %s)"
                val = (self.NumeroMensualidad, self.Monto, self.FechaVencimiento, self.Estado)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Mensualidad
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE mensualidades SET NumeroMensualidad = %s, Monto = %s , FechaVencimiento = %s , Estado = %s WHERE ID_Mensualidad = %s"
                val = (self.NumeroMensualidad, self.Monto, self.FechaVencimiento, self.Estado, self.ID_Mensualidad)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Mensualidad
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM mensualidades WHERE ID_Mensualidad = { self.ID_Mensualidad }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Mensualidad
        
