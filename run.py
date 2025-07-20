# Punto de entrada de la aplicación.

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Servidor Flask iniciando...")
    app.run(debug=True) 
    