from .db import get_connection

mydb = get_connection()

class Category:

    def __init__(self, ID_Prestamo, ID_Cliente, Monto, TasaInteres, FechaInicio, FechaVencimiento, Estado=None):
        self.ID_Prestamo = ID_Prestamo
        self.ID_Cliente = ID_Cliente
        self.Monto =  Monto
        self.TasaInteres = TasaInteres
        self.FechaInicio = FechaInicio
        self.FechaVencimiento = FechaVencimiento
        self.Estado = Estado
        
    def save(self):
        # Create a New Object in DB
        if self.ID_Prestamo is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO prestamos(Monto, TasaInteres, FechaInicio, FechaVencimiento, Estado) VALUES(%s, %s, %s, %s, %s)"
                val = (self.Monto, self.TasaInteres, self.FechaInicio, self.FechaVencimiento, self.Estado)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Prestamo
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE prestamos SET Monto = %s, TasaInteres = %s , FechaInicio = %s , FechaVencimiento = %s , Estado = %s WHERE ID_Pago = %s"
                val = (self.Monto, self.TasaInteres, self.FechaInicio, self.FechaVencimiento, self.Estado)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Prestamo
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM prestamos WHERE ID_Prestamo = { self.ID_Prestamo }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Prestamo