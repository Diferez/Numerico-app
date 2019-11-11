import matplotlib.pyplot as plt
import numpy as np
import libs

from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from sympy import *
from sympy.parsing.sympy_parser import parse_expr


lang = 'En'
#Inicializacion de la App
app = Flask(__name__, template_folder='templates',static_folder='statics')
CORS(app)



@app.route('/biseccion',methods =['GET'])
def biseccion():
    title = traduccion('biseccion')
    tolerancia = traduccion('tolerancia')
    correr = traduccion('correr')
    iteraciones = traduccion('iteraciones')
    funcion = traduccion('funcion')
    return render_template('biseccion.html', title = title, correr = correr, tolerancia = tolerancia, iteraciones = iteraciones,funcion = funcion)


@app.route('/biseccion',methods =['POST'])
def biseccion_post():
    title = traduccion('biseccion')
    Xi = float(request.form.get('Xi'))
    Xs = float(request.form.get('Xs'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    #Captura de datos del formulario
    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]

    return redirect(url_for('biseccion_show', title = title,datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/biseccion/show',methods =['GET'])
def biseccion_show():
    title = traduccion('biseccion')
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

    return render_template('biseccion_show.html', title = title, lista = lista, tam = len(lista),Tol = Tol, r = r)

@app.route('/busquedas',methods =['GET'])
def busquedas():
    return render_template('busquedas.html', title = 'Búsquedas Incrementales')
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
    title = traduccion('title')
    biseccion = traduccion('biseccion')
    busquedas = traduccion('busquedas')

    return render_template('numerico.html', title = title, biseccion = biseccion, busquedas = busquedas)

def traduccion(key):
    Es = {'title':"Análisis numérico",'correr':'Correr', 'biseccion':"Bisección", 'busquedas':"Búsquedas Incrementales", 'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerancia', 'iteraciones':'Iteraciones','funcion':'Función'}
    En = {'title':"Numerical analysis",'correr':'Run', 'biseccion':"Bisection", 'busquedas':"Incremental search", 'Xi:':'Xi','Xs':'Xs', 'tolerancia':'Tolerance','iteraciones':'Iterations','funcion':'Function'}

    if(lang == 'Es'):
        return Es[key]
    else:
        return En[key]
app.run(host= '0.0.0.0')

