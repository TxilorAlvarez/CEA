import os
import subprocess

def install_dependencies():
    try:
        # Verificar si pip está instalado
        subprocess.check_call([os.sys.executable, "-m", "pip", "--version"])

        # Instalar dependencias desde requirements.txt
        print("Instalando dependencias...")
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Todas las dependencias se instalaron correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la instalación de dependencias: {e}")
    except FileNotFoundError:
        print("No se encontró el archivo 'requirements.txt'. Por favor, asegúrate de que exista.")

if __name__ == "__main__":
    install_dependencies()