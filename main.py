from flask import Flask, render_template, jsonify, request
#importar mysql
from flask_mysqldb import MySQL


#cuando usamos __(doble guion bajo al inicio y final de una variable) es porque sera de ambito global
#la variable name, hace referencia al modulo que estamos ejecutando
#anotación->aplicar funcionalidad extra
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='system'
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/customers/<int:id>')
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customers WHERE id='+str(id)+';')
    data = cur.fetchall();
    content = {}
    for row in data:
        content = {"id": row[0], "firsname": row[1], "lastname": row[2], "email": row[3], "phone": row[4],
                   "addres": row[5]}
    return jsonify(content)

@app.route('/customers')
def getAllCustomer():
    #JSON con los datos
    #funcioón jsonfy, para convertir los datos que vienen de la base de datos a aun formato JSON
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customers')
    data = cur.fetchall();
    resultado = []
    for row in data:
        content = {"id":row[0], "firstname":row[1],"lastname":row[2],"email":row[3],"phone":row[4],"addres":row[5]}
        resultado.append(content)
    return jsonify(resultado)

@app.route('/customers', methods=['POST'])
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `customers`( `firtname`, `lastname`, `email`, `phone`, `addres`) VALUES (%s,%s,%s,%s,%s)",(request.json['firstname'], request.json['lastname'], request.json['email'],request.json['phone'],request.json['addres']))
    mysql.connection.commit() #realizar la última parte de la consulta, empaquetar y enviar a la base de datos
    return "Cliente Guardado";

@app.route('/customers', methods=['PUT'])
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firtname`=%s,`lastname`=%s,`email`=%s,`phone`=%s,`addres`=%s WHERE `id`=%s",(request.json['firstname'], request.json['lastname'], request.json['email'],request.json['phone'],request.json['addres'], request.json['id']))
    mysql.connection.commit() #realizar la última parte de la consulta, empaquetar y enviar a la base de datos
    return "Cliente Actualizado";

@app.route('/customers/<int:id>', methods=['DELETE'])
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM customers WHERE id ="+str(id)+";")
    mysql.connection.commit()  # realizar la última parte de la consulta, empaquetar y enviar a la base de datos
    return "Cliente eliminado";





if __name__ == '__main__':
    app.run(None, 3000, True)
