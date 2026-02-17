import os

path = r'd:\SalaJuntasCC\templates\informes\informe_usuario.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscamos el bloque exacto que vimos en el view_file
bad_block = '{% if usuario_seleccionado and usuario_seleccionado.id==u.id %}'
good_block = '{% if usuario_seleccionado and usuario_seleccionado.id == u.id %}'

if bad_block in content:
    new_content = content.replace(bad_block, good_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Informe Usuario corregido.")
else:
    # Intento con variaciones de espacios
    import re
    # Buscamos cualquier instancia de id==u.id dentro de tags de django
    new_content = re.sub(r'usuario_seleccionado\.id\s*==\s*u\.id', 'usuario_seleccionado.id == u.id', content)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("SUCCESS: Informe Usuario corregido vía Regex.")
    else:
        print("ERROR: No se encontró el bloque en Informe Usuario.")
