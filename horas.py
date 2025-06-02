"""
Autor: Sebastian Pérez
Este módulo contiene la función `normalizaHoras` que busca expresiones horarias
en un fichero de texto y las reemplaza por su forma normalizada HH:MM.
"""

import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText y escribe en ficNorm las mismas líneas pero
    con las expresiones horarias en formato normalizado HH:MM.

    Sólo se normalizan las expresiones correctas. Las incorrectas se dejan igual.
    """
    def reemplaza(match):
        # Casos estándar tipo 08:30 o 8:05
        if match.group('hora_std'):
            h = int(match.group('hora_std'))
            m = int(match.group('min_std'))
            return f'{h:02}:{m:02}'

        # Casos tipo 7h45m, 7h o 7h00m
        elif match.group('hora_h'):
            h = int(match.group('hora_h'))
            m = match.group('min_h')
            m = int(m) if m else 0
            if 0 <= h <= 23 and 0 <= m <= 59:
                return f'{h:02}:{m:02}'
            return match.group(0)  # Expresión incorrecta

        # Casos en lenguaje natural (hora, expresión, periodo)
        elif match.group('hora_nat'):
            h = int(match.group('hora_nat'))
            tipo = match.group('tipo') or ''
            periodo = match.group('periodo') or ''
            m = 0
            if tipo.strip() == 'y cuarto':
                m = 15
            elif tipo.strip() == 'y media':
                m = 30
            elif tipo.strip() == 'menos cuarto':
                h = (h - 1) if h > 1 else 12
                m = 45
            elif tipo.strip() == 'en punto' or tipo.strip() == '':
                m = 0
            else:
                return match.group(0)  # Expresión no válida

            # Convertimos la hora de 12h a 24h
            if 'mañana' in periodo:
                if h == 12:
                    h = 0
            elif 'mediodía' in periodo:
                if 1 <= h <= 3:
                    h += 12
                else:
                    return match.group(0)
            elif 'tarde' in periodo:
                if 1 <= h <= 8:
                    h += 12
                else:
                    return match.group(0)
            elif 'noche' in periodo:
                if 8 <= h <= 11:
                    h += 12
                elif h == 12:
                    h = 0
                elif 1 <= h <= 4:
                    h += 12
                else:
                    return match.group(0)
            elif 'madrugada' in periodo:
                if 1 <= h <= 6:
                    h = h
                else:
                    return match.group(0)
            return f'{h:02}:{m:02}'

        return match.group(0)  # por si acaso

    # Patrón general con grupos nombrados
    patron = re.compile(r'''
        (?P<hora_std>\d{1,2}):(?P<min_std>\d{2})                          | # 8:05 o 18:30
        (?P<hora_h>\d{1,2})h(?:\s*(?P<min_h>\d{1,2})m)?                  | # 8h o 8h45m
        (?P<hora_nat>\d{1,2})\s*
        (?P<tipo>en\s+punto|y\s+cuarto|y\s+media|menos\s+cuarto)?\s*
        (de\s+la\s+(?P<periodo>mañana|tarde|noche|madrugada)|del\s+mediodía)?
    ''', re.IGNORECASE | re.VERBOSE)

    with open(ficText, encoding='utf-8') as f_in, open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            nueva = patron.sub(reemplaza, linea)
            f_out.write(nueva)


if __name__ == "__main__":
    normalizaHoras('horas.txt', 'horas-normalizadas.txt')
    print("Fichero normalizado guardado en 'horas-normalizadas.txt'")
