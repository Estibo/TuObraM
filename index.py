from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='tuobra'
mysql =MySQL(app)

app.secret_key='TuObra'


@app.route('/')
def inicio():
    return render_template('inicio.html')
    
@app.route('/editari/<id>')
def editari(id):
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM items WHERE id= %s',[id])
    data=cur.fetchall()
    return render_template('editari.html', item=data[0])

@app.route('/editarp/<id>')
def editarp(id):
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM `proyectos` WHERE `proyectos`.`id` = %s;", [id])
    data=cur.fetchall()
    return render_template('editarp.html', proyecto=data[0])
    
@app.route('/eliminari/<idi>')
def eliminari(idi):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM `items` WHERE `items`.`id` = %s;", [idi])
    mysql.connection.commit()
    return redirect(url_for('items'))

@app.route('/eliminarp/<idp>')
def eliminarp(idp):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM `proyectos` WHERE `proyectos`.`id`= %s;", [idp])
    mysql.connection.commit()
    return redirect(url_for('proyectos'))

@app.route('/proyectos')
def proyectos():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM proyectos')
    data=cur.fetchall()
    return render_template('proyectos.html', proyectos=data)

@app.route('/addp',methods=['POST'])
def addProyectos():
    if request.method == 'POST':
        codigoP=request.form['idp']
        nombreP=request.form['nombrep'] 
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO proyectos (idp, nombrep) VALUES (%s, %s)', (codigoP, nombreP))
        mysql.connection.commit()
        flash('Proyect added successfully')
        return redirect(url_for('proyectos'))

@app.route('/addi',methods=['POST'])
def addItems():
    if request.method == 'POST':
        codigoI=request.form['idi']
        nombreI=request.form['nombrei'] 
        titulo=request.form['titulo'] 
        unidad=request.form['unidad'] 
        valoru=request.form['valoru'] 
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO items (idi, nombrei, titulo, unidad, valoru) VALUES (%s, %s, %s, %s, %s)', (codigoI, nombreI,titulo,unidad,valoru))
        mysql.connection.commit()
        flash('Item added successfully')
        return redirect(url_for('items'))

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html')

@app.route('/db')
def db():
    return render_template('db.html')

@app.route('/items')
def items():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM items')
    data=cur.fetchall()
    return render_template('items.html', items=data)



if __name__=='__main__':
    app.run(debug=True)