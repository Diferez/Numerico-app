import matplotlib.pyplot as plt
import numpy as np
import libs
import random

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
    Xi = traduccion('Xi')
    Xs = traduccion('Xs')
    title = traduccion('biseccion')
    tolerancia = traduccion('tolerancia')
    correr = traduccion('correr')
    iteraciones = traduccion('iteraciones')
    funcion = traduccion('funcion')
    salir = traduccion('salir')
    return render_template('biseccion.html', title = title, correr = correr, tolerancia = tolerancia, iteraciones = iteraciones,funcion = funcion, xs = Xs, xi = Xi,salir=salir)


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
    salir = traduccion('salir')
    title = traduccion('biseccion')
    bshowr = traduccion('bshowr')
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
    Xitemp=Xi
    Xstemp =Xs
    anticache = random.randint(1,99999999)
    for item in lista:

        xx = np.linspace(Xitemp, Xstemp, 1000)
        
        yy = F(xx)
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[3]),F(float(item[3])),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,item[0]))
        plt.clf()
        # Xitemp = Xitemp if Xitemp ==float(item[1]) else float(item[1])
        # Xstemp = Xstemp if Xstemp ==float(item[3]) else float(item[3])
        #Creacion de las imagenes para la animacion de la grafica

    return render_template('biseccion_show.html', title = title, lista = lista, tam = len(lista),Tol = Tol, r = r, bshowr = bshowr,salir = salir, anticache=anticache)

@app.route('/busquedas',methods =['GET'])
def busquedas():
    salir = traduccion('salir')
    title = traduccion('busquedas')
    Xo = traduccion('Xo')
    delta = traduccion('delta')
    iteraciones = traduccion('iteraciones')
    tolerancia = traduccion('tolerancia')
    funcion = traduccion('funcion')
    return render_template('busquedas.html', title = title, Xo = Xo, delta = delta, iteraciones = iteraciones, funcion = funcion, salir = salir, dic = tradudict())

@app.route('/busquedas',methods =['POST'])
def busquedas_post():
    title = traduccion('busquedas')
    Xo = float(request.form.get('Xo'))
    Delta = float(request.form.get('Delta'))

    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    print(Xo,Delta,Ite,F)
    datos = [Xo,Delta,Ite,F]
    
    return redirect(url_for('busquedas_show', title = title,datos = datos))

@app.route('/busquedas/show',methods =['GET'])
def busquedas_show():
    salir = traduccion('salir')
    title = traduccion('busquedas')
    datos = request.args.getlist('datos', None)
    Xo =float(datos[0])
    Delta = float(datos[1])
    Ite = float(datos[2])
    Fo = parse_expr(datos[3].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    r,lista = libs.busquedasincrementales(F,Xo,Delta,Ite)
    anticache = random.randint(1,99999999)


    Xi = min(lista)
    Xs = max(lista)
    Xif = Xi-((Xs-Xi)/4)
    Xsf = Xs+((Xs-Xi)/4)
    cont = 1
    for item in lista:

        xx = np.linspace(Xif,Xsf, 1000)
        
        yy = F(xx)
        plt.plot(float(item[0]),F(float(item[0])),'k*')
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(cont))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1

    return render_template('busquedas_show.html', title = title, lista = lista, tam = len(lista),anticache = anticache,salir = salir, dic = tradudict() )
    #Completar
    pass

def max(lista):
    maxn = 0
    for item in lista:
        for x in item:
            maxn = float(x) if maxn<float(x) else maxn
    return maxn
def min(lista):
    minn = 0
    for item in lista:
        for x in item:
            minn = float(x) if minn>float(x) else minn
    return minn

@app.route('/raices',methods =['GET'])
def raices():
    Xo = traduccion('Xo')
    title = traduccion('raices multiples')
    tol = traduccion('tolerancia')
    correr = traduccion('correr')
    iteraciones = traduccion('iteraciones')
    Df2 = traduccion('df2')
    Df1 = traduccion('df1')
    funcion = traduccion('funcion')
    salir = traduccion('salir')
    return render_template('raices.html', title = title, correr = correr, tolerancia = tol, iteraciones = iteraciones,funcion = funcion, xo = Xo,df1 = Df1, df2 = Df2, salir=salir)


@app.route('/raices',methods =['POST'])
def raices_post():
    
    title = traduccion('raices')
    Xo = float(request.form.get('Xo'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    f = request.form.get('f')
    df1 = request.form.get('df1')
    df2 = request.form.get('df2')
    #Captura de datos del formulario
    print(Xo,Tol,Ite,f)
    datos = [Xo,Tol,Ite,f,df1,df2]

    return redirect(url_for('raices_show', title = title,datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/raices/show',methods =['GET'])
def raices_show():
    salir = traduccion('salir')
    title = traduccion('raices')
    rmhowr = traduccion('bshowr')
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
    r,lista = libs.raices(f,Xo,Ite,Tol,df1,df2)
    #Ejecucion del metodo
    Xitemp=Xi
    Xstemp =Xs
    anticache = random.randint(1,99999999)
    for item in lista:

        xx = np.linspace(Xitemp, Xstemp, 1000)
        
        yy = F(xx)
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[3]),F(float(item[3])),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,item[0]))
        plt.clf()
        # Xitemp = Xitemp if Xitemp ==float(item[1]) else float(item[1])
        # Xstemp = Xstemp if Xstemp ==float(item[3]) else float(item[3])
        #Creacion de las imagenes para la animacion de la grafica

    return render_template('biseccion_show.html', title = title, lista = lista, tam = len(lista),Tol = Tol, r = r, bshowr = bshowr,salir = salir, anticache=anticache)


#Ruta Raiz

@app.route('/numerico',methods =['GET'])
def numerico():
    title = traduccion('title')
    biseccion = traduccion('biseccion')
    busquedas = traduccion('busquedas')
    raices = traduccion('raices')
    salir = traduccion('salir')
    return render_template('numerico.html', title = title, biseccion = biseccion, busquedas = busquedas, salir=salir)


Es = {'title':"Análisis numérico",'correr':'Correr', 'biseccion':"Bisección", 'busquedas':"Búsquedas Incrementales", 'raicesI':'raices',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerancia', 'iteraciones':'Iteraciones','funcion':'Función', 'salir':'Salir',
          'bshowr':'se aproxima a una raiz con tolerancia de', 'Xo':'Xo','delta':'Delta', 'popxo':'Punto inicial',
          'derivada':'Derivada', 'raices':'Raices Multiples','df1':'df1','df2':'df2'
          }
En = {'title':"Numerical analysis",'correr':'Run', 'biseccion':"Bisection", 'busquedas':"Incremental search", 'raicesI':'roots',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerance','iteraciones':'Iterations','funcion':'Function', 'salir':'Exit',
          'bshowr':'approaches the root with a tolerance of', 'Xo':'Xo', 'delta':'Delta', 'popxo':'Initial point',
          'derivada':'Derivative','raices':'Multiple Roots','df1':'df1','df2':'df2'
          }
def traduccion(key):


    if(lang == 'Es'):
        return Es[key]
    else:
        return En[key]

def tradudict():
    return Es if lang == 'Es' else En

@app.route('/newton',methods =['GET'])
def newton():

    return render_template('newton.html', title = 'Newton', dic = tradudict())


@app.route('/newton',methods =['POST'])
def newton_post():
    
    Xo = float(request.form.get('Xo'))
    Tol = float(request.form.get('Tol'))
    

    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    D = request.form.get('D')
    print(Xo,Tol,Ite,F,D)
    datos = [Xo,Tol,Ite,F,D]
    
    return redirect(url_for('newton_show', title = 'Newton',datos = datos))

@app.route('/newton/show',methods =['GET'])
def newton_show():

    datos = request.args.getlist('datos', None)
    Xo =float(datos[0])
    Tol = float(datos[1])
    Ite = float(datos[2])
    Fo = parse_expr(datos[3].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    if(datos[4]!=""):
        Do = parse_expr(datos[4].replace('^','**'))
        x = Symbol('x')
        D = lambdify(x, Do)
    else:
        Do = Fo.diff(x)
        D = lambdify(x, Do)
    
    r,lista = libs.newton(F,D,Xo,Tol,Ite)
    
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    Xif = Xo
    Xsf = r+((r-Xo)/10)
    cont = 1
    for item in lista:

        xx = np.linspace(Xif,Xsf, 1000)
        
        yy = F(xx)
        Dyy = D(xx)

        plt.plot(float(item[1]),F(float(item[1])),'k*')

        plt.plot(xx, np.transpose(yy))
        plt.plot(xx, np.transpose(Dyy))
        plt.axhline(y=0, color='k')
        #plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(cont))
        
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1
    
    return render_template('newton_show.html', title = 'Newton', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar

app.run(host= '0.0.0.0', debug=True)

