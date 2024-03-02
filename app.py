from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        clave = request.form['clave']
        # Verificar el DNI y la clave en un archivo CSV
        with open('usuarios.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['dni'] == dni and row['clave'] == clave:
                    return redirect(url_for('votacion', dni=dni))  # Pasar el DNI en la redirección
        return "Credenciales inválidas. Inténtalo de nuevo."
    return render_template('login.html')

# Ruta de votación
@app.route('/votacion', methods=['GET', 'POST'])
def votacion():
    if request.method == 'POST':
        opcion = request.form['opcion']
        dni = request.form['dni']
        # Guardar la opción y el DNI en un archivo CSV
        with open('votos.csv', 'a', newline='') as csvfile:
            fieldnames = ['dni', 'opcion']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'dni': dni, 'opcion': opcion})
        return "¡Gracias por votar!"
    # Obtener el DNI de la solicitud (request) o establecerlo como None si no está disponible
    dni = request.args.get('dni', None)
    return render_template('votacion.html', dni=dni)

if __name__ == '__main__':
    app.run(debug=True)
