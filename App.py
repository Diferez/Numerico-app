import matplotlib.pyplot as plt
import numpy as np
import libs

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


#Inicializacion de la App
app = Flask(__name__, template_folder='templates',static_folder='statics')
CORS(app)



@app.route('/biseccion',methods =['GET'])
def biseccion():
    return render_template('biseccion.html', title = 'Bisección')


@app.route('/biseccion',methods =['POST'])
def biseccion_post():
    Xi = float(request.form.get('Xi'))
    Xs = float(request.form.get('Xs'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    #Captura de datos del formulario
    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]

    return redirect(url_for('biseccion_show', title = 'Bisección',datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/biseccion/show',methods =['GET'])
def biseccion_show():
    datos = request.args.getlist('datos', None)  
    #Traer los datos que se enviaron previamente
    Xi =float(datos[0])
    Xs = float(datos[1])
    Tol = float(datos[2])
    Ite = float(datos[3])
    Fo = parse_expr(datos[4].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    #Formateo de los datos
    r,lista = libs.biseccion(F,Xi,Xs,Ite,Tol)
    #Ejecucion del metodo
    for item in lista:
        xx = np.linspace(Xi, Xs, 1000)
        yy = F(xx)
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[3]),F(float(item[3])),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        plt.savefig('statics/temp/{0}.png'.format(item[0]))
        plt.clf()
        #Creacion de las imagenes para la animacion de la grafica

    return render_template('biseccion_show.html', title = 'Biseccion Run', lista = lista, tam = len(lista),Tol = Tol, r = r)

@app.route('/busquedas',methods =['GET'])
def busquedas():
    #Completar
    pass

@app.route('/busquedas',methods =['POST'])
def busquedas_post():
    #Completar
    pass

@app.route('/busquedas/show',methods =['GET'])
def busquedas_show():
    #Completar
    pass

#Ruta Raiz
@app.route('/numerico',methods =['GET'])
def numerico():
    return render_template('numerico.html', title = 'Numérico')

app.run(host= '0.0.0.0')