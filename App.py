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
    return render_template('biseccion.html', title = title,dic = tradudict, correr = correr, tolerancia = tolerancia, iteraciones = iteraciones,funcion = funcion, xs = Xs, xi = Xi,salir=salir)


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
    title = traduccion('raices')
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

    return render_template('biseccion_show.html', title = title, lista = lista, tam = len(lista),Tol = Tol, r = r, bshowr = rmhowr,salir = salir, anticache=anticache)


#Ruta Raiz

@app.route('/numerico',methods =['GET'])
def numerico():
    title = traduccion('title')
    biseccion = traduccion('biseccion')
    busquedas = traduccion('busquedas')
    raices = traduccion('raices')
    salir = traduccion('salir')
    return render_template('numerico.html', title = title, biseccion = biseccion, busquedas = busquedas, salir=salir, dic = tradudict())




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
        plt.suptitle('Iteracion {0}'.format(item[0]))
        
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1
    
    return render_template('newton_show.html', title = 'Newton', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/reglaFalsa',methods =['GET'])
def reglaFalsa():

    return render_template('reglaFalsa.html', title = traduccion('reglaFalsa'), dic = tradudict())

@app.route('/reglaFalsa',methods =['POST'])
def reglaFalsa_post():
    
    Xi = float(request.form.get('Xi'))
    Xs = float(request.form.get('Xs'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')

    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]
    
    return redirect(url_for('reglaFalsa_show', title = traduccion('reglaFalsa'),datos = datos))


@app.route('/reglaFalsa/show',methods =['GET'])
def reglaFalsa_show():

    datos = request.args.getlist('datos', None)
    Xi =float(datos[0])
    Xs =float(datos[1])
    Tol = float(datos[2])
    Ite = float(datos[3])
    Fo = parse_expr(datos[4].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    
    r,lista = libs.reglaFalsa(F,Xi,Xs,Ite,Tol)
    
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    #Xif = Xo
    #Xsf = r+((r-Xo)/10)
    cont = 1
    for item in lista:
        delt = (Xs-Xi)/10
        xx = np.linspace(Xi-delt,Xs+delt, 1000)
        
        yy = F(xx)


        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[3]),F(float(item[3])),'k*')
        plt.plot(float(item[2]),F(float(item[2])),'r*')
        plt.plot(xx, np.transpose(yy))

        plt.axhline(y=0, color='k')
        #plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1
        Xi = Xi if Xi == float(item[1]) else float(item[1])
        Xs = Xs if Xs == float(item[3]) else float(item[3])
    
    return render_template('reglaFalsa_show.html', title = traduccion('reglaFalsa'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/secante',methods =['GET'])
def secante():

    return render_template('secante.html', title = traduccion('secante'), dic = tradudict())

@app.route('/secante',methods =['POST'])
def secante_post():
    
    Xi = float(request.form.get('Xi'))
    Xs = float(request.form.get('Xs'))
    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')

    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]
    
    return redirect(url_for('secante_show', title = traduccion('secante'),datos = datos))



@app.route('/secante/show',methods =['GET'])
def secante_show():

    datos = request.args.getlist('datos', None)
    Xi =float(datos[0])
    Xs =float(datos[1])
    Tol = float(datos[2])
    Ite = float(datos[3])
    Fo = parse_expr(datos[4].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    
    r,lista = libs.secante(Xi,Xs,Tol,Ite,F)
    
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    Xif = Xi
    Xsf = Xs
    cont = 1
    
    for i,item in enumerate(lista):
        if(i == 0):
            continue
        temp = Xsf
        Xsf = float(item[1])
        delt = (Xs-Xi)
        xx = np.linspace(Xi-delt,Xs+delt, 1000)
        
        yy = F(xx)
        x1, y1 = [Xif, Xsf], [F(Xif), F(Xsf)]
        
        plt.plot(xx, np.transpose(yy))
        plt.plot(x1, y1, marker = 'o')
        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.axhline(y=0, color='k')
        #plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1
        Xif = temp
        
        
        #Xi = Xi if Xi == float(item[1]) else float(item[1])
        #Xs = Xs if Xs == float(item[3]) else float(item[3])
    
    return render_template('secante_show.html', title = traduccion('secante'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/puntoFijo',methods =['GET'])
def puntoFijo():
    return render_template('puntoFijo.html', title = traduccion('puntoFijo'), dic = tradudict())


@app.route('/puntoFijo',methods =['POST'])
def puntoFijo_post():
    
    Xo = float(request.form.get('Xo'))
    Tol = float(request.form.get('Tol'))
    

    Ite = float(request.form.get('Ite'))
    F = request.form.get('F')
    G = request.form.get('G')
    print(Xo,Tol,Ite,F,G)
    datos = [Xo,Tol,Ite,F,G]
    
    return redirect(url_for('puntoFijo_show', title = traduccion('puntoFijo'),datos = datos))

@app.route('/puntoFijo/show',methods =['GET'])
def puntoFijo_show():

    datos = request.args.getlist('datos', None)
    Xo =float(datos[0])
    Tol = float(datos[1])
    Ite = float(datos[2])
    Fo = parse_expr(datos[3].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    if(datos[4]!=""):
        
        Go = parse_expr(datos[4].replace('^','**'))
        x = Symbol('x')
        G = lambdify(x, Go)
    else:
        #
        #Inventarse algo pa cuando no menta G(X)
        #
        Go = Fo.diff(x)
        G = lambdify(x, Go)
    
    r,lista = libs.puntofijo(F,G,Xo,Tol,Ite)
    
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    Xif = Xo
    Xsf = r+((r-Xo)/2)
    cont = 1
    for item in lista:

        xx = np.linspace(Xif,Xsf, 1000)
        
        yy = F(xx)
        Gyy = G(xx)

        plt.plot(float(item[1]),F(float(item[1])),'k*')
        plt.plot(float(item[1]),G(float(item[1])),'r*')
        plt.plot(xx, np.transpose(yy))
        plt.plot(xx, np.transpose(Gyy))
        plt.axhline(y=0, color='k')
        #plt.axvline(x=0, color='k')
        plt.suptitle('Iteracion {0}'.format(item[0]))
        
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
        plt.clf()
        cont = cont + 1
    
    return render_template('puntoFijo_show.html', title = traduccion('puntoFijo'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/jacobi',methods =['GET'])
def jacobi():
    return render_template('jacobi.html', title = 'Jacobi', dic = tradudict())

@app.route('/jacobi',methods =['POST'])
def jacobi_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)

    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    
    x = str(request.form.get('X'))
    xv = formatearVector(x)
    
    print(xv)


    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))

    Norma = float(request.form.get('Norma'))


    print(M,b,x,Ite,Tol,Norma)
    datos = [M,b,x,Ite,Tol,Norma]
    
    return redirect(url_for('jacobi_show', title = 'Jacobi',datos = datos))


@app.route('/jacobi/show',methods =['GET'])
def jacobi_show():

    datos = request.args.getlist('datos', None)
    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)
    x = str(datos[2])
    xv = formatearVector(x)

    Ite = float(datos[3])

    Tol = float(datos[4])
    Norma = float(datos[5])

    print(Mat,bv,xv,Norma,Tol,Ite)
    lista = libs.jacobi(Mat,bv,xv,Norma,Tol,Ite)
    lar = len(lista[0][1])
    anticache = random.randint(1,99999999)
    return render_template('jacobi_show.html', title = 'Jacobi', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar)
    #Completar
def formatearMatriz(M):
    M = M.split(';')
    for i in range (len(M)):
        M[i]= M[i].split(' ')

    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == '':
                M[i].remove(M[i][j])
    
    Mat = np.zeros((len(M),len(M)))

    for i in range(len(M)):
        for j in range(len(M)):
            Mat[i,j]=float(M[i][j])
    return Mat
    
def formatearVector(b):
    b = b.split(' ')
    for i in range(len(b)):
        if b[i] == '':
                b.remove(b[i])
    bv = np.zeros(len(b))
    for i in range(len(b)):
        bv[i] = float(b[i]) 
    
    return bv



@app.route('/gaussSaidel',methods =['GET'])
def gaussSaidel():
    return render_template('gaussSaidel.html', title = 'Gauss Seidel', dic = tradudict())

@app.route('/gaussSaidel',methods =['POST'])
def gaussSaidel_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)

    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    
    x = str(request.form.get('X'))
    xv = formatearVector(x)
    
    print(xv)


    Tol = float(request.form.get('Tol'))
    Ite = float(request.form.get('Ite'))

    Norma = float(request.form.get('Norma'))


    print(M,b,x,Ite,Tol,Norma)
    datos = [M,b,x,Ite,Tol,Norma]
    
    return redirect(url_for('gaussSaidel_show', title = 'GaussSaidel',datos = datos))


@app.route('/gaussSaidel/show',methods =['GET'])
def gaussSaidel_show():

    datos = request.args.getlist('datos', None)
    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)
    x = str(datos[2])
    xv = formatearVector(x)

    Ite = float(datos[3])

    Tol = float(datos[4])
    Norma = float(datos[5])

    print(Mat,bv,xv,Norma,Tol,Ite)
    r, lista = libs.gausSeidel(Mat,bv,xv,Norma,Tol,Ite)
    lar = len(lista[0][1])
    anticache = random.randint(1,99999999)
    return render_template('gaussSaidel_show.html', title = 'Gauss Saidel', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar)

@app.route('/lagrange',methods =['GET'])
def lagrange():
    return render_template('lagrange.html', title = 'Lagrange', dic = tradudict())

@app.route('/lagrange',methods =['POST'])
def lagrange_post():
    x = str(request.form.get('X'))
    
    xv = formatearVector(x)
    print(x)
    
    y = str(request.form.get('Y'))
    yv = formatearVector(y)
    
    print(yv)


    Num = int(request.form.get('Num'))


    print(x,y,Num)
    datos = [x,y,Num]
    
    return redirect(url_for('lagrange_show', title = 'Lagreange',datos = datos))

@app.route('/lagrange/show',methods =['GET'])
def lagrange_show():

    datos = request.args.getlist('datos', None)

    x = str(datos[0])
    xv = formatearVector(x)

    y = str(datos[1])
    yv = formatearVector(y)
    Num = int(float(datos[2]))

    print(x,y,Num)

    lon,sho  = libs.lagrange(xv,yv,Num)

    x = Symbol('x')
    F = lambdify(x, sho)


    
    
    delta = (np.amax(xv)-np.amin(xv))/4
    Xi = np.amin(xv)-delta
    Xs = np.amax(xv)+delta
    cont = 1
    xx = np.linspace(Xi,Xs, 1000)
    yy = F(xx)
    plt.plot(xx, np.transpose(yy))
    for i in range(len(xv)):
        plt.plot(xv[i],yv[i],'r*')
    anticache = random.randint(1,99999999)
    plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
    plt.clf()
    return render_template('lagrange_show.html', title = 'Lagrange', dic = tradudict(), lon = lon, sho = sho, anticache= anticache)

@app.route('/gaussSimple',methods =['GET'])
def gaussSimple():
    return render_template('gaussSimple.html', title = traduccion('gaussSimple'), dic = tradudict())

@app.route('/gaussSimple',methods =['POST'])
def gaussSimple_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)

    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('gaussSimple_show', title = traduccion('gaussSimple'),datos = datos))


@app.route('/gaussSimple/show',methods =['GET'])
def gaussSimple_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    r,lista = libs.gaussSimple(Mat,bv)
    
    lar = len(lista[0][0])-1
    anticache = random.randint(1,99999999)
    return render_template('gaussSimple_show.html', title = traduccion('gaussSimple'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sol=r)


@app.route('/gaussParcial',methods =['GET'])
def gaussParcial():
    return render_template('gaussParcial.html', title = traduccion('gaussParcial'), dic = tradudict())

@app.route('/gaussParcial',methods =['POST'])
def gaussParcial_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)
    print("post")
    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('gaussParcial_show', title = traduccion('gaussParcial'),datos = datos))

@app.route('/gaussParcial/show',methods =['GET'])
def gaussParcial_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    r,lista = libs.gaussParcial(Mat,bv)
    print(r)
    lar = len(lista[0][0])-1
    anticache = random.randint(1,99999999)
    return render_template('gaussParcial_show.html', title = traduccion('gaussParcial'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sol=r)


Es = {'title':"Análisis numérico",'correr':'Correr', 'biseccion':"Bisección", 'busquedas':"Búsquedas Incrementales", 'raicesI':'raices','gaussSimple':'Gaussiana Simple','solucion':'Solucion',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerancia', 'iteraciones':'Iteraciones','funcion':'Función', 'salir':'Atras', 'gaussParcial':'Gaussiana Parcial',
          'bshowr':'se aproxima a una raiz con tolerancia de', 'Xo':'Xo','delta':'Delta', 'popxo':'Punto inicial',
          'derivada':'Derivada', 'raices':'Raices Multiples','df1':'df1','df2':'df2', 'reglaFalsa':'Regla Falsa', 'secante':'Secante', 
          'puntoFijo':'Punto Fijo', 'G':'Funcion G(x)','popm':'Separados por espacios y ; Ej: 1 2 3; 4 5 6; 7 8 9', 'matrixdata':'Datos de la Matriz',
          'B':'Vector b', 'popv':'Separados por espacios Ej: 1 2 3' , 'X':'Vector x','norma':'Norma', 'Y':'Vector y', 'lv':'Valores a tomar',
          'dBiseccion':'Es un algoritmo de búsqueda de raíz que funciona dividiendo el intervalo a la mitad y seleccionando el subintervalo que tiene la raíz.',
          'dFincremental':'Este método consiste en encontrar un intervalo que contenga al menos una raíz y se basa en el teorema del valor intermedio.\n',
          'dFincremental2':'\nTeorema del valor intermedio:Si f es una función continúa en el intervalo (a, b) y k es cualquier número entre f (a) y f (b), entonces existe un número c en el intervalo a cómo (a, b) tal que f (c)=k.',
          'dFnewton':'Se trata de un procedimiento basado en la derivada, para encontrar aproximaciones a las raíces de una función real de variable real que sea derivable.',
          'dFmultroot' : 'El método de Raíces Múltiples o Newton modificado, se creó con el fin de resolver algunos problemas que presenta el Método de Newton, cuando la derivada de la función tiende a cero al ser evaluada en "x", lo cual implica que la convergencia disminuye o incluso se suspende si se alcanza una división por cero. También, en el Método de la Secante ocurre un problema si la función es muy plana y f(x) y f(x-1) son aproximadamente iguales. Con este fin se creó el Método de las Raíces Múltiples.',
          'dFsecante' : 'Es una variación del método de Newton-Raphson, en donde se calcula la derivada de la función en el punto de análisis, luego, se aproxima la pendiente a la recta que une la función evaluada en el punto de análisis y en el punto de la iteración anterior.',
          'dFfixepo' : 'El Método de Punto Fijo es un procedimiento iterativo que permite resolver ecuaciones no necesariamente lineales y se usa principalmente para determinar raíces de una función de la forma f(x) = 0, si se cumplen las condiciones de convergencia. Para este caso no es necesario tener un intervalo, su principal objetivo es buscar la raíz de una función partiendo de un valor inicial, una tolerancia y un número de iteraciones.'
          }
En = {'title':"Numerical analysis",'correr':'Run', 'biseccion':"Bisection", 'busquedas':"Incremental search", 'raicesI':'roots', 'gaussSimple':'Simple Gaussian','solucion':'Solution',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerance','iteraciones':'Iterations','funcion':'Function', 'salir':'Back', 'gaussParcial':'Partial Gaussian',
          'bshowr':'approaches the root with a tolerance of', 'Xo':'Xo', 'delta':'Delta', 'popxo':'Initial point',
          'derivada':'Derivative','raices':'Multiple Roots','df1':'df1','df2':'df2', 'reglaFalsa':'False Rule','secante':'Secant',
          'puntoFijo':'Fixed Point','G':'Function G(x)', 'popm':'Separated by spaces and ; Ex: 1 2 3; 4 5 6; 7 8 9', 'matrixdata':'Matrix Data',
          'B':'Vector b', 'popv':'Separated by spaces Ej: 1 2 3', 'X':'Vector x', 'norma':'Norma', 'Y':'Vector y', 'lv':'Values to take',
          'dBiseccion':'It is a root search algorithm that works by dividing the interval in half and selecting the subinterval that has the root.',
          'dFincremental':'This method consists in finding an interval that contains at least one root and is based on the intermediate value theorem.\n',
          'dFincremental2': '\nIntermediate value theorem: If f is a function it continues in the interval (a, b) and k is any number between f (a) and f (b), then there is a number c in the interval to how (a, b) such that f (c) = k.',
          'dFnewton':'It is a procedure based on the derivative, to find approximations to the roots of a real function of real variable that is derivable.',
          'dFmultroot': 'The modified Multiple Roots is created in order to solve some problems presented by the Newton Method, when the derivative of the function tends to zero when evaluated in "x", which implies that convergence decreases or it is even suspended if a division by zero is reached. Also, in the Secant Method a problem occurs if the function is very flat and f (x) and f (x-1) are approximately equal. To this end, the Multiple Root Method was created.',
          'dFsecante' : 'It is a variation of the Newton-Raphson method, where the derivative of the function at the point of analysis is calculated, then, the slope is approximated to the line that joins the function evaluated at the point of analysis and at the point of the previous iteration',
          'dFfixepo' : 'The Fixed Point Method is an iterative procedure that allows solving non-determined linear equations and is mainly used to determine roots of a function of the form f (x) = 0, if convergence conditions are established. For this case it is not necessary to have an interval, its main objective is to find the root of a function based on an initial value, a tolerance and a number of iterations.'
          
          }

app.run(host= '0.0.0.0', debug=True)

