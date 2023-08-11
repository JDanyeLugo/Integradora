from .db import get_connection

mydb = get_connection()

class Category:

    def __init__(self, ID_Pago, ID_Prestamo, FechaPago, Monto, Estado=None):
        self.ID_Pago = ID_Pago
        self.ID_Prestamo = ID_Prestamo
        self.FechaPago = FechaPago
        self.Monto =  Monto
        self.Estado = Estado
        
    def save(self):
        # Create a New Object in DB
        if self.ID_Pago is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO pagos(FechaPago, Monto, Estado) VALUES(%s, %s, %s)"
                val = (self.FechaPago, self.Monto, self.Estado)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Pago
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE pagos SET FechaPago = %s, Monto = %s , Estado = %s WHERE ID_Pago = %s"
                val = (self.FechaPago, self.Monto, self.Estado)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Pago
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM pagos WHERE ID_Pago = { self.ID_Pago }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Pago