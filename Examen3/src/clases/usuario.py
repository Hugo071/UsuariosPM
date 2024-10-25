from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id_grupo, nombre, email, password=None, hashed_password=None):
        self.__id_grupo = id_grupo
        self.__nombre = nombre
        self.__email = email
        self.__hashed_password = self.__hash_password(password) if password else hashed_password

    def __str__(self):
        return f'Nombre: {self.__nombre}, email: {self.__email},  Password: {self.__hashed_password}, ID Grupo {self.__id_grupo}'

    @property
    def hashed_password(self):
        return self.__hashed_password

    @property
    def nombre(self):
        return self.__nombre

    @property
    def id_grupo(self):
        return self.__id_grupo

    @property
    def email(self):
        return self.__email

    @hashed_password.setter
    def hashed_password(self, password):
        self.__hashed_password = generate_password_hash(password)

    def __hash_password(self, password):
        if password:
            return generate_password_hash(password, method='pbkdf2:sha256')

    def verificar_password(self, password):
        return check_password_hash(self.__hashed_password, password)

    def to_dict(self):
        return {
            'nombre': self.__nombre,
            'email': self.__email,
            'password': self.__hashed_password,
            'id_grupo': self.__id_grupo
        }