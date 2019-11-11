from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import libs
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

app = Flask(__name__, template_folder='templates',static_folder='statics')
CORS(app)

@app.route('/numerico',methods =['GET'])
def numerico():
    return render_template('numerico.html', title = 'Numerico')

@app.route('/biseccion',methods =['GET'])
def biseccion():
    return render_template('biseccion.html', title = 'Biseccion')

@app.route('/biseccion',methods =['POST'])
def biseccion_post():
    Xi = float(request.form.get('Xi'))
    Xs = float(request.form.get('Xs'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    
    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]

    return redirect(url_for('biseccion_show', title = 'Biseccion',datos = datos))

@app.route('/biseccion/show',methods =['GET'])
def biseccion_show():
    datos = request.args.getlist('datos', None)
    print(datos)
    print(request.args)
    Xi =float(datos[0])
    Xs = float(datos[1])
    Tol = float(datos[2])
    Ite = float(datos[3])
    Fo = parse_expr(datos[4].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    r,lista = libs.biseccion(F,Xi,Xs,Ite,Tol)
    for item in lista:
        xx = np.linspace(Xi, Xs, 1000)
        yy = F(xx)
        #xxx = np.array([item[1],item[3]])

        #yyy = xx
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[3]),F(float(item[3])),'k*')
        #plt.axvline(x = item[3])
        plt.plot(xx, np.transpose(yy))
        #plt.plot(xxx, yyy, 'k*')
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        plt.savefig('statics/temp/{0}.png'.format(item[0]))
        plt.clf()

    #p1 = plot(Fo,(x,Xi,Xs), show = false)
    #p1.save('statics/temp/funcion.png')
    return render_template('biseccion_show.html', title = 'Biseccion Run', lista = lista, tam = len(lista),Tol = Tol, r = r)

app.run(host= '0.0.0.0')