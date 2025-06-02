"""
Autor: Sebastian Pérez
Este módulo contiene la clase Alumno y la función leeAlumnos para procesar
ficheros de texto con los datos y calificaciones de alumnos.
"""

import re
import doctest

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Lee un fichero con datos de alumnos y devuelve un diccionario cuya clave
    es el nombre completo y el valor un objeto Alumno.

    Cada línea contiene el ID, el nombre completo (puede tener espacios) y una
    lista de notas separadas por espacios o tabuladores.

    El análisis se realiza con expresiones regulares.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    ...
    171\tBlanca Agirrebarrenetse\t9.5
    23\tCarles Balcell de Lara\t4.9
    68\tDavid Garcia Fuster\t7.0
    """
    resultado = {}
    patron = re.compile(r'^\s*(\d+)\s+(.+?)\s+((?:\d+(?:\.\d+)?[\t ]*)+)$')

    with open(ficAlum, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            m = patron.match(linea)
            if m:
                numIden = int(m.group(1))
                nombre = m.group(2).strip()
                notas_str = m.group(3).strip().split()
                notas = list(map(float, notas_str))
                resultado[nombre] = Alumno(nombre, numIden, notas)

    return resultado


if __name__ == "__main__":
    import doctest
    print("Ejecutando doctest desde main...\n")
    doctest.testmod(verbose=True, optionflags=doctest.NORMALIZE_WHITESPACE)

