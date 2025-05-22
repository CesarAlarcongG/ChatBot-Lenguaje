#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import nltk


def main():
    # Solo descargar datos si es el proceso principal
    if os.environ.get('RUN_MAIN') != 'true':
        descargar_nltk_datos()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
"---------------------------------------------------------------"
#Código para las dependencias de nltk

def descargar_nltk_datos():
    import os
    import zipfile
    import shutil

    # Convertimos a ruta absoluta basada en la ubicación del script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir, 'venv', 'nltk_data')
    os.makedirs(ruta, exist_ok=True)

    # Forzar a NLTK a usar solo nuestra ruta (limpiando paths existentes)
    nltk.data.path = [ruta]

    # Lista de recursos necesarios
    recursos = [
        ('tokenizers/punkt', 'punkt'),
        ('corpora/stopwords', 'stopwords'),
        ('corpora/', 'wordnet')
    ]

    # Verificar y descargar cada recurso
    for recurso, paquete in recursos:
        try:
            path = nltk.data.find(recurso)
            if path.startswith(ruta):
                print(f"✅ Recurso {recurso} ya está disponible en {path}")
                continue
            else:
                print(f"⚠️ Recurso {recurso} está en ubicación no esperada: {path}")
                # Eliminar versión existente para reinstalar en la ruta correcta
                if os.path.exists(os.path.join(ruta, paquete)):
                    shutil.rmtree(os.path.join(ruta, paquete))
        except LookupError:
            pass

        print(f"⬇️ Descargando {paquete}...")
        nltk.download(paquete, download_dir=ruta)

        # Manejar archivos ZIP
        zip_path = os.path.join(ruta, f'{paquete}.zip')
        if os.path.exists(zip_path):
            print(f"📦 Descomprimiendo {paquete}.zip...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(ruta)
            os.remove(zip_path)  # Eliminar el zip después de descomprimir

        # Verificar instalación
        try:
            installed_path = nltk.data.find(recurso)
            print(f"✔️ {recurso} instalado en: {installed_path}")
        except LookupError:
            print(f"❌ Error: {recurso} no se instaló correctamente")

    # Verificación final
    print("\n🔍 Verificación final:")
    for recurso, _ in recursos:
        try:
            path = nltk.data.find(recurso)
            status = "✅" if path.startswith(ruta) else "⚠️"
            print(f"{status} {recurso}: {path}")
        except LookupError:
            print(f"❌ {recurso}: NO ENCONTRADO")


if __name__ == '__main__':
    main()
