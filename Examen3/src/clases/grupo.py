
class Grupo:
    def __init__(self, id_grupo="", nombre="", permisos=""):
        self.id_grupo = id_grupo
        self.nombre = nombre
        self.permisos = permisos

    def __str__(self):
        return f'ID Grupo: {self.id_grupo}, Nombre: {self.nombre}, Permisos: {self.permisos}'

    def tiene_permiso(self, permiso):
        return permiso in self.permisos