from functools import wraps

import pymongo
from pymongo.errors import OperationFailure

from src.clases import usuario
from src.clases.grupo import Grupo
from src.clases.usuario import Usuario

class GestorUsuarios():
        def __init__(self, host=None, user="", password="", port="27017"):
            self.MONGO_USER = user
            self.MONGO_PASSWORD = password
            self.MONGO_HOST = host if host else "localhost"
            self.MONGO_PORT = 27017
            self.MONGO_URI = None
            self.MONGO_CLIENT = None
            self.MONGO_CURSOR = None

        def conectar_mongodb(self):
            try:
                if self.MONGO_HOST == "localhost":
                    self.MONGO_URI = "mongodb://localhost:27017"
                else:
                    self.MONGO_URI = f"mongodb+srv://hugorojas:admin1234@itj-desarrollo.yi09p.mongodb.net/?retryWrites=true&w=majority&appName=ITJ-DESARROLLO"
                self.MONGO_CLIENT = pymongo.MongoClient(self.MONGO_URI)
                try:
                    print(self.MONGO_CLIENT.host)
                except OperationFailure as e:
                    return "Error en la conexión " + str(e)
            except pymongo.errors.ServerSelectionTimeoutError as e_tiempo:
                return "Tiempo excedido " + str(e_tiempo)

        def registrar_usuario(self, usuario, db="ITJ-DESARROLLO", coleccion="usuarios_grupos"):
            self.conectar_mongodb()
            if self.MONGO_CLIENT[db][coleccion].find_one({"email": usuario.email}):
                self.cerrar_conexion_mongodb()
                return {"Mensaje": f"El usuario {usuario.email} ya existe..."}, 409
            #Insertar en la BD
            self.MONGO_CLIENT[db][coleccion].insert_one(usuario.to_dict())
            self.cerrar_conexion_mongodb()
            return {"Mensaje": f"Usuario {usuario.email} registrado correctamente"}, 201

        def reset_password(self, usuario, nuevo_password, db="ITJ-DESARROLLO", coleccion="users"):
            self.conectar_mongodb()
            usuario.hashed_password = nuevo_password
            self.MONGO_CLIENT[db][coleccion].update_one({"email": usuario.email},{"$set":{"password": usuario.hashed_password}})
            self.cerrar_conexion_mongodb()
            return {"mensaje":f"El usuario {usuario.email} cambio su contraseña con exito"}, 201

        def obtener_usuario_email(self, email, db="ITJ-DESARROLLO", coleccion="usuarios_grupos"):
            self.conectar_mongodb()
            usr = self.MONGO_CLIENT[db][coleccion].find_one({"email": email})
            if usr:
                self.cerrar_conexion_mongodb()
                return Usuario(usr["id_grupo"],usr["nombre"],usr["email"],usr["password"])
            self.cerrar_conexion_mongodb()
            return None

        def regresa_conexion_mongodb(self):
            return self.MONGO_CLIENT

        def cerrar_conexion_mongodb(self):
            try:
                if self.MONGO_CLIENT:
                    self.MONGO_CLIENT.close()
            except Exception as e:
                return "No hay conexiones activas a la BD " + str(e)

        def buscar_grupo_por_id(self, id_grupo, db="ITJ-DESARROLLO", coleccion="grupos"):
            self.conectar_mongodb()
            #print(id_grupo)
            grupo_data = self.MONGO_CLIENT[db][coleccion].find_one({"grupo": id_grupo})
            self.cerrar_conexion_mongodb()
            if grupo_data:
                return Grupo(grupo_data["grupo"],grupo_data["nombre"],grupo_data["permisos"])
            return None

        def requerir_cliente(func):
            def wrapper(self, usuario, *args, **kwargs):
                grupo = self.buscar_grupo_por_id(int(usuario.id_grupo))  # Obtener el grupo del usuario
                if grupo and grupo.nombre == "Clientes":  # Verificar si el grupo es "Clientes"
                    return func(self, usuario, *args, **kwargs)
                return "Acceso denegado: el usuario no pertenece al grupo de clientes."

            return wrapper


        @requerir_cliente
        def ver_carrito(self, usuario):
            return "Eres cliente, puedes ver el carrito"

objUsuario = Usuario("200", "Hugo Rojas", "hugo@email.com", "1234")
objMongo = GestorUsuarios("nube", "hugorojas", "admin1234")
#objMongo.registrar_usuario(objUsuario)
#print(objMongo.buscar_grupo_por_id(objUsuario.id_grupo))
#print(objUsuario.id_grupo)
#print(objMongo.obtener_usuario_email("hugo@email.com"))
print(objMongo.ver_carrito(objUsuario))

"""
grupo = objMongo.buscar_grupo_por_id(100)
if grupo:
    print(grupo.tiene_permiso("Ver-Productos"))   
    print(grupo.tiene_permiso("Editar-Producto"))
"""
