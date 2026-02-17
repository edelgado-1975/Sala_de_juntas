import os

path = r'd:\SalaJuntasCC\templates\reservas\dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscamos el bloque problematico con espacios flexibles
bad_block = """                var currentUserId = {{ request.user.id
        }};
    var isStaff = {{ request.user.is_staff| yesno: "true,false" }};"""

good_block = """                var currentUserId = {{ request.user.id }};
                var isStaff = {{ request.user.is_staff|yesno:"true,false" }};"""

if bad_block in content:
    new_content = content.replace(bad_block, good_block)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("SUCCESS: Bloque reemplazado.")
else:
    # Intento 2: Sin saltos de linea especificos
    import re
    pattern = r'var currentUserId = \{\{ request\.user\.id\s+\}\};\s+var isStaff = \{\{ request\.user\.is_staff\| yesno: "true,false" \}\};'
    # Intentemos algo mas simple basado en lo que vimos
    pattern = r'var currentUserId = \{\{ request\.user\.id\n\s+\}\};\n\s+var isStaff = \{\{ request\.user\.is_staff\| yesno: "true,false" \}\};'
    
    # Simplemente buscaremos la linea 383 y la arreglaremos
    lines = content.splitlines()
    found = False
    for i, line in enumerate(lines):
        if 'request.user.is_staff| yesno: "true,false"' in line:
            lines[i] = '                var isStaff = {{ request.user.is_staff|yesno:"true,false" }};'
            # Tambien arreglar la linea anterior que tiene el id roto
            if i > 0 and 'request.user.id' in lines[i-1]:
                lines[i-1] = '                var currentUserId = {{ request.user.id }};'
            # Y la linea del medio que solo tiene }};
            if i > 0 and lines[i-1].strip() == '}};':
                 # Borrar esa linea si existe
                 pass
            found = True
            break
    
    if found:
        # Re-limpiar lineas vacias o rotas
        final_lines = []
        for line in lines:
            if line.strip() == '}};': # Esta es la linea 382 rota
                continue
            final_lines.append(line)
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(final_lines))
        print("SUCCESS: Lineas corregidas individualmente.")
    else:
        print("ERROR: No se encontró el bloque problemático.")
