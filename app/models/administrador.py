from .db import get_connection

mydb = get_connection()

class Category:

    def __init__(self, ID_Administrador, Nombre, Usuario, Contraseña, CorreoElectronico, FechaRegistro=None):
        self.ID_Administrador = ID_Administrador
        self.Nombre = Nombre
        self.Usuario = Usuario
        self.Contraseña = Contraseña
        self.CorreoElectronico = CorreoElectronico 
        self.FechaRegistro = FechaRegistro
        
    def save(self):
        # Create a New Object in DB
        if self.ID_Administrador is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO administrador(Nombre, Usuario, Contraseña, CorreoElectronico, FechaRegistro) VALUES(%s, %s, %s, %s, %s)"
                val = (self.Nombre, self.Usuario, self.Contraseña, self.CorreoElectronico, self.FechaRegistro)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.ID_Administrador
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE administrador SET Nombre = %s, Usuario = %s , Contraseña = %s , CorreoElectronico = %s , FechaRegistro WHERE ID_Administrador = %s"
                val = (self.Nombre, self.Usuario, self.Contraseña, self.CorreoElectronico, self.FechaRegistro)
                cursor.execute(sql, val)
                mydb.commit()
                return self.ID_Administrador
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM administrador WHERE ID_Administrador = { self.ID_Administrador }"
            cursor.execute(sql)
            mydb.commit()
            return self.ID_Administrador