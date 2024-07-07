#--------------------------------------------------------------------
# Instalar con pip install Flask
from flask import Flask, request, jsonify, render_template
#from flask import request

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time
#--------------------------------------------------------------------



app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

#--------------------------------------------------------------------
class Catalogo:
    #----------------------------------------------------------------
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS vehiculos (
                                codigo INT AUTO_INCREMENT PRIMARY KEY,
                                marca VARCHAR(255) NOT NULL,
                                modelo VARCHAR(255) NOT NULL,
                                transmision VARCHAR(255),
                                kilometros INT(7) NOT NULL,
                                año INT(4) NOT NULL,
                                precio DECIMAL(15, 2) NOT NULL,
                                imagen_url VARCHAR(255))''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    #----------------------------------------------------------------
    def agregar_vehiculo(self, marca, modelo, precio, imagen, año, kilometros, transmision ):
               
        sql = "INSERT INTO vehiculos (marca, modelo, precio, imagen_url, año, kilometros, transmision) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valores = (marca, modelo, precio, imagen, año, kilometros, transmision)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.lastrowid

    #----------------------------------------------------------------
    def consultar_vehiculo(self, codigo):
        # Consultamos un vehiculo a partir de su código
        self.cursor.execute(f"SELECT * FROM vehiculos WHERE codigo = {codigo}")
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_vehiculo(self, codigo, nueva_marca, nuevo_modelo, nuevo_precio, nueva_imagen, nuevo_año, nuevo_kilometros, nueva_transmision):
        sql = "UPDATE vehiculos SET marca = %s, modelo = %s, precio = %s, imagen_url = %s, año = %s, kilometros= %s, transmision=%s WHERE codigo = %s"
        valores = (nueva_marca, nuevo_modelo, nuevo_precio, nueva_imagen, nuevo_año, nuevo_kilometros, nueva_transmision, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def listar_vehiculos(self):
        self.cursor.execute("SELECT * FROM vehiculos")
        vehiculos = self.cursor.fetchall()
        return vehiculos

    #----------------------------------------------------------------
    def eliminar_vehiculo(self, codigo):
        # Eliminamos un vehiculo de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM vehiculos WHERE codigo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------
    def mostrar_vehiculo(self, codigo):
        # Mostramos los datos de un vehiculo a partir de su código
        vehiculo = self.consultar_vehiculo(codigo)
        if vehiculo:
            print("-" * 40)
            print(f"Código.....: {vehiculo['codigo']}")
            print(f"Marca......: {vehiculo['marca']}")
            print(f"Modelo.....: {vehiculo['modelo']}")
            print(f"Precio.....: {vehiculo['precio']}")
            print(f"Imagen.....: {vehiculo['imagen_url']}")
            print(f"Año........: {vehiculo['año']}")
            print(f"Kilometros.: {vehiculo['kilometros']}")
            print(f"Transmision: {vehiculo['transmision']}")
            print("-" * 40)
        else:
            print("Vehiculo no encontrado.")


#--------------------------------------------------------------------
# Cuerpo del programa
#--------------------------------------------------------------------
# Crear una instancia de la clase Catalogo
#catalogo = Catalogo(host='localhost', user='root', password='', database='miapp')
catalogo = Catalogo(host='GimenezCristian.mysql.pythonanywhere-services.com', user='GimenezCristian', password='root2024', database='GimenezCristian$miapp')


# Carpeta para guardar las imagenes.
#RUTA_DESTINO = './static/imagenes/'

#Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
RUTA_DESTINO = '/home/GimenezCristian/mysite/static/imagenes'


#--------------------------------------------------------------------
# Listar todos los productos
#--------------------------------------------------------------------
#La ruta Flask /productos con el método HTTP GET está diseñada para proporcionar los detalles de todos los productos almacenados en la base de datos.
#El método devuelve una lista con todos los productos en formato JSON.
@app.route("/vehiculos", methods=["GET"])
def listar_vehiculos():
    vehiculos = catalogo.listar_vehiculos()
    return jsonify(vehiculos)


#--------------------------------------------------------------------
# Mostrar un sólo vehiculo según su código
#--------------------------------------------------------------------
#La ruta Flask /vehiculos/<int:codigo> con el método HTTP GET está diseñada para proporcionar los detalles de un vehiculo específico basado en su código.
#El método busca en la base de datos el vehiculo con el código especificado y devuelve un JSON con los detalles del vehiculo si lo encuentra, o None si no lo encuentra.
@app.route("/vehiculos/<int:codigo>", methods=["GET"])
def mostrar_vehiculo(codigo):
    vehiculo = catalogo.consultar_vehiculo(codigo)
    if vehiculo:
        return jsonify(vehiculo), 201
    else:
        return "vehiculo no encontrado", 404


#--------------------------------------------------------------------
# Agregar un vehiculo
#--------------------------------------------------------------------
@app.route("/vehiculos", methods=["POST"])
#La ruta Flask `/vehiculos` con el método HTTP POST está diseñada para permitir la adición de un nuevo vehiculo a la base de datos.
#La función agregar_vehiculo se asocia con esta URL y es llamada cuando se hace una solicitud POST a /vehiculos.
def agregar_vehiculo():
    #Recojo los datos del form
    marca = request.form['marca']
    modelo = request.form['modelo']
    precio = request.form['precio']
    imagen = request.files['imagen']
    año = request.form['año']
    kilometros = request.form['kilometros']
    transmision = request.form['transmision']  
    nombre_imagen=""

    # Genero el nombre de la imagen
    nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
    nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

    nuevo_codigo = catalogo.agregar_vehiculo(marca, modelo, precio, nombre_imagen, año, kilometros, transmision)
    if nuevo_codigo:    
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))

        #Si el vehiculo se agrega con éxito, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "vehiculo agregado correctamente.", "codigo": nuevo_codigo, "imagen": nombre_imagen}), 201
    else:
        #Si el vehiculo no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el vehiculo."}), 500
    

#--------------------------------------------------------------------
# Modificar un vehiculo según su código
#--------------------------------------------------------------------
@app.route("/vehiculos/<int:codigo>", methods=["PUT"])
#La ruta Flask /vehiculos/<int:codigo> con el método HTTP PUT está diseñada para actualizar la información de un vehiculo existente en la base de datos, identificado por su código.
#La función modificar_vehiculo se asocia con esta URL y es invocada cuando se realiza una solicitud PUT a /vehiculos/ seguido de un número (el código del vehiculo).
def modificar_vehiculo(codigo):
    #Se recuperan los nuevos datos del formulario
    nueva_marca = request.form.get("marca")
    nuevo_modelo = request.form.get("modelo")
    nuevo_precio = request.form.get("precio")
    nuevo_año = request.form.get("año")
    nuevo_kilometros = request.form.get("kilometros")
    nueva_transmision = request.form.get("transmision")
    
    
    # Verifica si se proporcionó una nueva imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        # Procesamiento de la imagen
        nombre_imagen = secure_filename(imagen.filename) #Chequea el nombre del archivo de la imagen, asegurándose de que sea seguro para guardar en el sistema de archivos
        nombre_base, extension = os.path.splitext(nombre_imagen) #Separa el nombre del archivo de su extensión.
        nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}" #Genera un nuevo nombre para la imagen usando un timestamp, para evitar sobreescrituras y conflictos de nombres.

        # Guardar la imagen en el servidor
        imagen.save(os.path.join(RUTA_DESTINO, nombre_imagen))
        
        # Busco el vehiculo guardado
        vehiculo = catalogo.consultar_vehiculo(codigo)
        if vehiculo: # Si existe el vehiculo...
            imagen_vieja = vehiculo["imagen_url"]
            # Armo la ruta a la imagen
            ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

            # Y si existe la borro.
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)
    
    else:
        # Si no se proporciona una nueva imagen, simplemente usa la imagen existente del vehiculo
        vehiculo = catalogo.consultar_vehiculo(codigo)
        if vehiculo:
            nombre_imagen = vehiculo["imagen_url"]


    # Se llama al método modificar_vehiculo pasando el codigo del vehiculo y los nuevos datos.
    if catalogo.modificar_vehiculo(codigo, nueva_marca, nuevo_modelo, nuevo_precio, nombre_imagen, nuevo_año, nuevo_kilometros, nueva_transmision):
        
        #Si la actualización es exitosa, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
        return jsonify({"mensaje": "vehiculo modificado"}), 200
    else:
        #Si el vehiculo no se encuentra (por ejemplo, si no hay ningún vehiculo con el código dado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "vehiculo no encontrado"}), 403



#--------------------------------------------------------------------
# Eliminar un vehiculo según su código
#--------------------------------------------------------------------
@app.route("/vehiculos/<int:codigo>", methods=["DELETE"])
#La ruta Flask /vehiculos/<int:codigo> con el método HTTP DELETE está diseñada para eliminar un vehiculo específico de la base de datos, utilizando su código como identificador.
#La función eliminar_vehiculo se asocia con esta URL y es llamada cuando se realiza una solicitud DELETE a /vehiculos/ seguido de un número (el código del vehiculo).
def eliminar_vehiculo(codigo):
    # Busco el vehiculo en la base de datos
    vehiculo = catalogo.consultar_vehiculo(codigo)
    if vehiculo: # Si el vehiculo existe, verifica si hay una imagen asociada en el servidor.
        imagen_vieja = vehiculo["imagen_url"]
        # Armo la ruta a la imagen
        ruta_imagen = os.path.join(RUTA_DESTINO, imagen_vieja)

        # Y si existe, la elimina del sistema de archivos.
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

        # Luego, elimina el vehiculo del catálogo
        if catalogo.eliminar_vehiculo(codigo):
            #Si el vehiculo se elimina correctamente, se devuelve una respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "vehiculo eliminado"}), 200
        else:
            #Si ocurre un error durante la eliminación (por ejemplo, si el vehiculo no se puede eliminar de la base de datos por alguna razón), se devuelve un mensaje de error con un código de estado HTTP 500 (Error Interno del Servidor).
            return jsonify({"mensaje": "Error al eliminar el vehiculo"}), 500
    else:
        #Si el vehiculo no se encuentra (por ejemplo, si no existe un vehiculo con el codigo proporcionado), se devuelve un mensaje de error con un código de estado HTTP 404 (No Encontrado). 
        return jsonify({"mensaje": "vehiculo no encontrado"}), 404

#--------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)