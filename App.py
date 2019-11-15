import matplotlib.pyplot as plt
import numpy as np
import libs
import random

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from flask_cors import CORS
from flask_session import Session
from sympy import *
from sympy.parsing.sympy_parser import parse_expr





lang = 'Es'
#Inicializacion de la App
app = Flask(__name__, template_folder='templates',static_folder='statics')
sess = Session()
app.config['SECRET_KEY'] = 'reds209ndsldssdsljdsldsdsljdsldksdksdsdfsfsfsfis'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
CORS(app)



@app.route('/biseccion',methods =['GET'])
def biseccion():
    return render_template('biseccion.html', title = traduccion('biseccion'),dic = tradudict())


@app.route('/biseccion',methods =['POST'])
def biseccion_post():
    try:
        Xi = float(request.form.get('Xi'))
        Xs = float(request.form.get('Xs'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
        Fo = request.form.get('F').replace('^','**')
        x = Symbol('x')
        Fo = lambdify(x, Fo)
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('biseccion.html', title = traduccion('biseccion'),dic = tradudict())
    

    error = False
    if(Tol<=0):
        error = True    
        flash("La tolerancia no puede ser negativa")
    
    if(Xi>Xs):
        error = True    
        flash("Xi debe ser mayor que Xs")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")
    
    
    if(error):
        return render_template('biseccion.html',title = traduccion('biseccion'),dic = tradudict())

    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]

    return redirect(url_for('biseccion_show', title = traduccion('biseccion'),datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/biseccion/show',methods =['GET'])
def biseccion_show():
    salir = traduccion('salir')

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

    try:
        r,lista = libs.biseccion(F,Xi,Xs,Ite,Tol)
        corrio = True
        if (F(Xi).imag!=0 or F(Xs).imag!=0):
            corrio = False    
            flash("Valor inicial invalido F(Xo) no esta definido")
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz")

    
    #Ejecucion del metodo
    Xitemp=Xi
    Xstemp =Xs
    anticache = random.randint(1,99999999)
    if corrio:
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
    else:

        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        plt.plot(Xi,F(Xi),'k*')
        plt.plot(Xs,F(Xs),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = traduccion('biseccion'), anticache=anticache,dic = tradudict())

    return render_template('biseccion_show.html', title = traduccion('biseccion'), lista = lista, tam = len(lista),Tol = Tol, r = r, bshowr = bshowr,salir = salir, anticache=anticache,dic = tradudict(), corrio= corrio)


####################################################################################################################################################################################
@app.route('/busquedas',methods =['GET'])
def busquedas():
    return render_template('busquedas.html', title = traduccion('busquedas'), dic = tradudict())

@app.route('/busquedas',methods =['POST'])
def busquedas_post():
    try:
        Xo = float(request.form.get('Xo'))
        Delta = float(request.form.get('Delta'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
        Fo = parse_expr(F)
        x = Symbol('x')
        Fo = lambdify(x, Fo)
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('busquedas.html', title = traduccion('busquedas'),dic = tradudict())
    
    error = False


    
    if(Delta<=0):
        error = True    
        flash("Delta debe ser mayor que 0")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")

    if(error):
        return render_template('busquedas.html', title= traduccion('busquedas'),dic = tradudict())

    
    print(Xo,Delta,Ite,F)
    datos = [Xo,Delta,Ite,F]
    
    return redirect(url_for('busquedas_show', title = traduccion('busquedas'),datos = datos))

@app.route('/busquedas/show',methods =['GET'])
def busquedas_show():
    datos = request.args.getlist('datos', None)
    Xo =float(datos[0])
    Delta = float(datos[1])
    Ite = float(datos[2])
    Fo = parse_expr(datos[3].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    
    try:
        r,lista = libs.busquedasincrementales(F,Xo,Delta,Ite)
        corrio = True
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz")

    if (len(lista)==0):
        corrio = False
        flash("Intervalo Invalido, no existe raiz")
    if (F(Xo).imag!=0):
        corrio = False    
        flash("Valor inicial invalido F(Xo) no esta definido")
    print(r,lista)
    anticache = random.randint(1,99999999)


    Xi = min(lista)
    Xs = max(lista)
    Xif = Xi-((Xs-Xi)/4)
    Xsf = Xs+((Xs-Xi)/4)
    cont = 1
    if corrio:
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
    else:
        Xif = Xi
        Xsf = Xi + Delta*Ite
        xx = np.linspace(Xif,Xsf, 1000)
        yy = F(xx)
        plt.plot(Xi,F(Xi),'k*')
        plt.plot(Xs,F(Xs),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle('Funcion'.format(cont))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title =traduccion('busquedas'), anticache=anticache,dic = tradudict())

    return render_template('busquedas_show.html', title =traduccion('busquedas'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(),corrio = corrio)
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
###############################################################################################################################################################################
@app.route('/raices',methods =['GET'])
def raices():
    return render_template('raices.html', title = traduccion('raices'),dic = tradudict() )


@app.route('/raices',methods =['POST'])
def raices_post():
    error = False
    try:
        Xo = float(request.form.get('Xo'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
        df1 = request.form.get('df1')
        df2 = request.form.get('df2')
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('raices.html', title = traduccion('raices'),dic = tradudict())
    error = False
    if(Tol<=0):
        error = True
        flash("La tolerancia no puede ser negativa")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")
    
    if(error):
        return render_template('raices.html', title = 'raices',dic = tradudict())

    
    #Captura de datos del formulario
    print(Xo,Tol,Ite,F)
    datos = [Xo,Tol,Ite,F,df1,df2]

    return redirect(url_for('raices_show', title = traduccion('raices'),datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/raices/show',methods =['GET'])
def raices_show():
    salir = traduccion('salir')
    title = traduccion('raices')
    rmhowr = traduccion('bshowr')
    datos = request.args.getlist('datos', None)  
    #Traer los datos que se enviaron previamente
    Xo =float(datos[0])
    Tol = float(datos[1])
    Ite = float(datos[2])
    Fo = parse_expr(datos[3].replace('^','**'))
    if(datos[4]!=""):
        Dfo1 = parse_expr(datos[4].replace('^','**'))
        x = Symbol('x')
        df1 = lambdify(x, Dfo1)
    else:
        x = Symbol('x')
        Dfo1 = Fo.diff(x)
        df1 = lambdify(x, Dfo1)
    if(datos[5]!=""):
        Dfo2 = parse_expr(datos[5].replace('^','**'))
        x = Symbol('x')
        df2 = lambdify(x, Dfo2)
    else:
        Dfo2 = Dfo1.diff(x)
        df2 = lambdify(x, Dfo2)


    x = Symbol('x')
    F = lambdify(x, Fo)
    #Formateo de los datos

    corrio = True


    
    try:
        r,lista = libs.RaizM(F,df1,df2,Xo,Tol,Ite)
        corrio = True
        if((F(Xo)*df2(Xo))<0):
            corrio = False    
            flash('Valor inicial Invalido')

        if (F(Xo).imag!=0):
            corrio = False    
            flash("Valor inicial invalido F(Xo) no esta definido")
        
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz o la funcion o derivada no esta definida")
    #Ejecucion del metodo
    anticache = random.randint(1,99999999)

    

    
    if corrio:
        Xitemp=Xo
        Xstemp =r+((r-Xo)/10)

        print (df1)
        print (df2)
        for item in lista:

            xx = np.linspace(Xitemp, Xstemp, 1000)
            
            yy = F(xx)
            yy1 = df1(xx)
            yy2 = df2(xx)
            plt.plot(xx, np.transpose(yy),'g')
            plt.plot(xx, np.transpose(yy1),'b')
            plt.plot(xx, np.transpose(yy2),'r')
            plt.axhline(y=0, color='k')
            #plt.axvline(x=0, color='k')
            #plt.suptitle('Iteracion {0}'.format(item[0]))
            plt.savefig('statics/temp/{0}{1}.png'.format(anticache,item[0]))
            plt.clf()
    else:
        Xi = Xo-abs(Xo/4)
        Xs = 10
        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        #plt.plot(Xi,F(Xi),'k*')

        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = traduccion('raices'), anticache=anticache,dic = tradudict())


    return render_template('raices_show.html', title = traduccion('raices'), lista = lista, tam = len(lista),Tol = Tol, r = r, bshowr = rmhowr,salir = salir, anticache=anticache,dic = tradudict())


#Ruta Raiz

@app.route('/tlineal',methods =['GET'])
def tlineal():
    X = traduccion('X')
    Y = traduccion('Y')
    correr = traduccion('correr')
    salir = traduccion('salir')
    return render_template('tlineal.html',title = traduccion('line'), correr = correr,dic = tradudict() )


@app.route('/tlineal',methods =['POST'])
def tlineal_post():
    
    title = traduccion('line')
    try:
        x = (request.form.get('X'))
        xv = formatearVector(x)

        y = (request.form.get('Y'))
        yv = formatearVector(y)

        #Captura de datos del formulario
        #print(X,Y)
        datos = [x,y]
    except:        
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('tlineal.html', title = title,dic = tradudict())
    
    return redirect(url_for('tlineal_show', title = title,datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/tlineal/show',methods =['GET'])
def tlineal_show():
    salir = traduccion('salir')
    title = traduccion('line')
    datos = request.args.getlist('datos', None)  
    #Traer los datos que  se enviaron previamente
    x =str(datos[0])
    xv = formatearVector(x)

    y = str(datos[1])
    yv = formatearVector(y)


    #Formateo de los datos
    lista,r = libs.trazaLinea(xv,yv)
    #Ejecucion del metodo
    Xitemp = np.amin(xv)
    Xstemp = np.amax(xv)

    lar = len(lista[0])

    anticache = random.randint(1,99999999)
    cont=1
    for item in r:

        xx = np.linspace(Xitemp, Xstemp, 1000)
        
        x = Symbol('x')
        F = lambdify(x, item)
        yy = F(xx)

        plt.plot(xx, np.transpose(yy),'g')
        plt.axhline(y=0, color='k')

    plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
    plt.clf()
    return render_template('tlineal_show.html', title = title, lista = lista, lar = lar,r = r, salir = salir, anticache=anticache, tam = len(r),dic=tradudict())


@app.route('/tcuadra',methods =['GET'])
def tcuadra():
    X = traduccion('X')
    Y = traduccion('Y')
    correr = traduccion('correr')
    salir = traduccion('salir')
    return render_template('tcuadra.html',title = traduccion('quap'), correr = correr,dic = tradudict() )


@app.route('/tcuadra',methods =['POST'])
def tcuadra_post():
    
    title = traduccion('quap')
    try:
        x = (request.form.get('X'))
        xv = formatearVector(x)

        y = (request.form.get('Y'))
        yv = formatearVector(y)

        #Captura de datos del formulario
        #print(X,Y)
        datos = [x,y]
    except:        
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('tlineal.html', title = title,dic = tradudict())
    
    return redirect(url_for('tcuadra_show', title = title,datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/tcuadra/show',methods =['GET'])
def tcuadra_show():
    salir = traduccion('salir')
    title = traduccion('quap')
    datos = request.args.getlist('datos', None)  
    #Traer los datos que  se enviaron previamente
    x =str(datos[0])
    xv = formatearVector(x)

    y = str(datos[1])
    yv = formatearVector(y)


    #Formateo de los datos
    lista,r = libs.trazaCuadra(xv,yv)
    #Ejecucion del metodo
    Xitemp = np.amin(xv)
    Xstemp = np.amax(xv)

    lar = len(lista[0])

    anticache = random.randint(1,99999999)
    cont=1
    for item in r:

        xx = np.linspace(Xitemp, Xstemp, 1000)
        
        x = Symbol('x')
        F = lambdify(x, item)
        yy = F(xx)

        plt.plot(xx, np.transpose(yy),'g')
        plt.axhline(y=0, color='k')
        
    plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
    plt.clf()
    return render_template('tcuadra_show.html', title = title, lista = lista, lar = lar,r = r, salir = salir, anticache=anticache, tam = len(r),dic=tradudict())


@app.route('/tcubi',methods =['GET'])
def tcubi():
    X = traduccion('X')
    Y = traduccion('Y')
    correr = traduccion('correr')
    salir = traduccion('salir')
    return render_template('tcubi.html',title = traduccion('cubi'), correr = correr,dic = tradudict() )


@app.route('/tcubi',methods =['POST'])
def tcubi_post():
    
    title = traduccion('cubi')
    try:
        x = (request.form.get('X'))
        xv = formatearVector(x)

        y = (request.form.get('Y'))
        yv = formatearVector(y)

        #Captura de datos del formulario
        #print(X,Y)
        datos = [x,y]
    except:        
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('tlineal.html', title = title,dic = tradudict())
    
    return redirect(url_for('tcubi_show', title = title,datos = datos))
    #Redirecion y envio de datos a la pantalla de muestra

@app.route('/tcubi/show',methods =['GET'])
def tcubi_show():
    salir = traduccion('salir')
    title = traduccion('cubi')
    datos = request.args.getlist('datos', None)  
    #Traer los datos que  se enviaron previamente
    x =str(datos[0])
    xv = formatearVector(x)

    y = str(datos[1])
    yv = formatearVector(y)


    #Formateo de los datos
    lista,r = libs.trazaCubo(xv,yv)
    #Ejecucion del metodo
    Xitemp = np.amin(xv)
    Xstemp = np.amax(xv)

    lar = len(lista[0])

    anticache = random.randint(1,99999999)
    cont=1
    for item in r:

        xx = np.linspace(Xitemp, Xstemp, 1000)
        
        x = Symbol('x')
        F = lambdify(x, item)
        yy = F(xx)

        plt.plot(xx, np.transpose(yy),'g')
        plt.axhline(y=0, color='k')
        
    plt.savefig('statics/temp/{0}{1}.png'.format(anticache,cont))
    plt.clf()
    return render_template('tcubi_show.html', title = title, lista = lista, lar = lar,r = r, salir = salir, anticache=anticache, tam = len(r),dic=tradudict())


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
    error = False
    try:
        Xo = float(request.form.get('Xo'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
        D = request.form.get('D')
        Fo = parse_expr(F)
        x = Symbol('x')
        Fo = lambdify(x, Fo)
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('newton.html', title = 'Newton',dic = tradudict())
    
    if(Tol<=0):
        error = True
        flash("La tolerancia no puede ser negativa")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")
    
    
    
    if(error):
        return render_template('newton.html', title = 'Newton',dic = tradudict())

    
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
    
    D2o = Do.diff(x)
    D2 = lambdify(x, D2o)
    
    corrio = True
    
    
   
    try:
        r,lista = libs.newton(F,D,Xo,Tol,Ite)
        if((F(Xo)*D2(Xo))<0):
            corrio = False    
            flash('Valor inicial Invalido')

        if (F(Xo).imag!=0):
            corrio = False    
            flash("Valor inicial invalido F(Xo) no esta definido")
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz o la funcion no esta definida")
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    if corrio:
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
    else:
        Xi = Xo-abs(Xo/4)
        Xs = 10
        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        #plt.plot(Xi,F(Xi),'k*')

        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = 'Newton', anticache=anticache,dic = tradudict())
    
    return render_template('newton_show.html', title = 'Newton', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/reglaFalsa',methods =['GET'])
def reglaFalsa():

    return render_template('reglaFalsa.html', title = traduccion('reglaFalsa'), dic = tradudict())

@app.route('/reglaFalsa',methods =['POST'])
def reglaFalsa_post():
    
    try:
        Xi = float(request.form.get('Xi'))
        Xs = float(request.form.get('Xs'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
    except:
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('reglaFalsa.html', title = traduccion('reglaFalsa'),dic = tradudict())
    
    error = False
    if(Tol<=0):
        error = True    
        flash("La tolerancia no puede ser negativa")
    
    if(Xi>Xs):
        error = True    
        flash("Xi debe ser mayor que Xs")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")
    
    if(error):
        return render_template('reglaFalsa.html', title = traduccion('reglaFalsa'),dic = tradudict())

    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]
    
    return redirect(url_for('reglaFalsa_show', title = traduccion('reglaFalsa'),datos = datos))


@app.route('/reglaFalsa/show',methods =['GET'])
def reglaFalsa_show():
    corrio = False
    datos = request.args.getlist('datos', None)
    Xi =float(datos[0])
    Xs =float(datos[1])
    Tol = float(datos[2])
    Ite = float(datos[3])
    Fo = parse_expr(datos[4].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    


    try:
        r,lista = libs.reglaFalsa(F,Xi,Xs,Ite,Tol)
        corrio = True
        if (F(Xi).imag!=0 or F(Xs).imag!=0):
            corrio = False
            flash("Valor inicial invalido F(Xo) no esta definido")
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz o la funcion no esta definida")
    
    
    
    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    #Xif = Xo
    #Xsf = r+((r-Xo)/10)
    cont = 1
    if corrio:
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
    else:
        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        plt.plot(Xi,F(Xi),'k*')
        plt.plot(Xs,F(Xs),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = traduccion('reglaFalsa'), anticache=anticache,dic = tradudict())

    return render_template('reglaFalsa_show.html', title = traduccion('reglaFalsa'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/secante',methods =['GET'])
def secante():

    return render_template('secante.html', title = traduccion('secante'), dic = tradudict())

@app.route('/secante',methods =['POST'])
def secante_post():
    try:
        Xi = float(request.form.get('Xi'))
        Xs = float(request.form.get('Xs'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('secante.html', title = traduccion('secante'),dic = tradudict())
    
    error = False
    

    print(Xi,Xs,Tol,Ite,F)
    datos = [Xi,Xs,Tol,Ite,F]
    
    

    if(Tol<=0):
        error = True    
        flash("La tolerancia no puede ser negativa")
    
    if(Xi>Xs):
        error = True    
        flash("Xi debe ser mayor que Xs")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")

    if(error):
        return render_template('secante.html', title = traduccion('secante'),dic = tradudict())

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
    
    try:
        r,lista = libs.secante(Xi,Xs,Tol,Ite,F)
        corrio = True
        if (F(Xi).imag!=0 or F(Xs).imag!=0):
            corrio = False    
            flash("Valor inicial invalido F(Xo) no esta definido")
    except:
        corrio = False
        flash("Intervalo Invalido, no existe raiz")
    

    anticache = random.randint(1,99999999)


    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    Xif = Xi
    Xsf = Xs
    cont = 1
    if corrio:
        for i,item in enumerate(lista):
            if(i == 0):
                continue
            temp = Xsf
            Xsf = float(item[1])
            delt = (Xs-Xi)*5
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
    else:
        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        plt.plot(Xi,F(Xi),'k*')
        plt.plot(Xs,F(Xs),'k*')
        plt.plot(xx, np.transpose(yy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = traduccion('biseccion'), anticache=anticache,dic = tradudict())
        
        
        #Xi = Xi if Xi == float(item[1]) else float(item[1])
        #Xs = Xs if Xs == float(item[3]) else float(item[3])
    
    return render_template('secante_show.html', title = traduccion('secante'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


@app.route('/puntoFijo',methods =['GET'])
def puntoFijo():
    return render_template('puntoFijo.html', title = traduccion('puntoFijo'), dic = tradudict())


@app.route('/puntoFijo',methods =['POST'])
def puntoFijo_post():
    
    error = False
    try:
        Xo = float(request.form.get('Xo'))
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        F = request.form.get('F')
        G = request.form.get('G')
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('puntoFijo.html', title = traduccion('puntoFijo'),dic = tradudict())
    
    if(Tol<=0):
        error = True
        flash("La tolerancia no puede ser negativa")
    
    if(Ite<=0):
        error = True    
        flash("Las iteraciones no pueden ser negativas")

    if(error):
        return render_template('puntoFijo.html', title = traduccion('puntoFijo'),dic = tradudict())


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
        x = Symbol('x')
        G = lambdify(x, Go)
    r=''
    corrio = True
    print(F(Xo))
    if not (definido(F,Xo) or definido(G,Xo) ):
        corrio = False    
        flash("Valor inicial invalido F(Xo) no esta definido")
    else:
        try:
            r,lista = libs.puntofijo(F,G,Xo,Tol,Ite)
            corrio = True
        except:
            corrio = False
            flash("Intervalo Invalido, no existe raiz")
    
    anticache = random.randint(1,99999999)
    if(r=='f'):
        corrio = False
        flash("Valor inicial invalido F(Xo) no esta definido")
    # Xi = min(lista)
    # Xs = max(lista)
    # Xif = Xi-((Xs-Xi)/4)
    # Xsf = Xs+((Xs-Xi)/4)
    cont = 1
    if corrio:
        for item in lista:

            Xif = Xo
            Xsf = r+((r-Xo)/2)
            
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
    else:
        Xi = Xo-abs(Xo/4)
        Xs = 10
        Xif = Xi-((Xs-Xi)/4)
        Xsf = Xs+((Xs-Xi)/4)

        xx = np.linspace(Xif, Xsf, 1000)
        yy = F(xx)
        Gyy = G(xx)
        #plt.plot(Xi,F(Xi),'k*')

        plt.plot(xx, np.transpose(yy))
        plt.plot(xx, np.transpose(Gyy))
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        plt.suptitle(traduccion('funcion'))
        plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
        plt.clf()
        return  render_template('error.html', title = traduccion('puntoFijo'), anticache=anticache,dic = tradudict())


    
    return render_template('puntoFijo_show.html', title = traduccion('puntoFijo'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict() )
    #Completar


def definido(F,x):
    if (F(x).imag!=0 or F(x)==float('NaN') or F(x)==float('-inf') or F(x)==float('inf')):
        return False
    return True

@app.route('/jacobi',methods =['GET'])
def jacobi():
    return render_template('jacobi.html', title = 'Jacobi', dic = tradudict())

@app.route('/jacobi',methods =['POST'])
def jacobi_post():
    error = False
    try:
        M =str(request.form.get('Matrix'))
        Mat = formatearMatriz(M)
        b = str(request.form.get('B'))
        bv = formatearVector(b)
        x = str(request.form.get('X'))
        xv = formatearVector(x)
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        Norma = float(request.form.get('Norma'))
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos, comprobar que la matriz sea cuadrada")
        return render_template('jacobi.html', title = 'Jacobi',dic = tradudict())
    
    if not(len(Mat)==len(Mat[0])):
        error = True
        flash("La matriz no es cuadrada")
    if not(len(Mat[0])==len(bv) and len(bv)==len(xv)):
        error = True
        flash("Los vectores y la matriz no tienen el mismo tamaño")
    
    if(np.linalg.det(Mat) == 0):
        error = True
        flash("La matriz tiene determinante 0")

    if(error):
        return render_template('jacobi.html', title = 'Jacobi6',dic = tradudict())
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
        for j in range(len(M[0])):
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
    
    error = False
    try:
        M =str(request.form.get('Matrix'))
        Mat = formatearMatriz(M)
        b = str(request.form.get('B'))
        bv = formatearVector(b)
        x = str(request.form.get('X'))
        xv = formatearVector(x)
        Tol = float(request.form.get('Tol'))
        Ite = float(request.form.get('Ite'))
        Norma = float(request.form.get('Norma'))
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos, comprobar que la matriz sea cuadrada")
        return render_template('gaussSaidel.html', title = 'GaussSaidel',dic = tradudict())
    
    if not(len(Mat)==len(Mat[0])):
        error = True
        flash("La matriz no es cuadrada")
    if not(len(Mat[0])==len(bv) and len(bv)==len(xv)):
        error = True
        flash("Los vectores y la matriz no tienen el mismo tamaño")
    
    if(np.linalg.det(Mat) == 0):
        error = True
        flash("La matriz tiene determinante 0")

    if(error):
        return render_template('gaussSaidel.html', title = 'GaussSaidel',dic = tradudict())
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
    error = False
    try: 
        x = str(request.form.get('X'))
        xv = formatearVector(x)
        y = str(request.form.get('Y'))
        yv = formatearVector(y)
        Num = int(request.form.get('Num'))
    except:
        error = True
        flash("Error al leer los datos, por favor comprobarlos, comprobar que la matriz sea cuadrada")
        return render_template('lagrange.html', title = 'Lagreange',dic = tradudict())
    
    if not(len(xv)==len(yv)):
        error = True
        flash("El tamaño de los vectores no coinside")
    
    if(error):
        return render_template('lagrange.html', title = 'Lagreange',dic = tradudict())

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
    title = traduccion('gaussSimple')
    try:
        M =str(request.form.get('Matrix'))
          
        Mat = formatearMatriz(M)
        deter = np.linalg.det(Mat) 
        print(Mat)

        b = str(request.form.get('B'))
        
        bv = formatearVector(b)
        print(b)
        print(M,b)
        datos = [M,b]

    except:        
        flash("Error al leer los datos, por favor comprobarlos")
        return render_template('gaussSimple.html', title = title,dic = tradudict())
    
    
    if deter <= 0:        
        flash("Error, determinante cercana a 0")
        return render_template('gaussSimple.html', title = title,dic = tradudict())
    
    if not(len(Mat[0])==len(bv)):
        error = True
        flash("Los vectores y la matriz no tienen el mismo tamaño")
    
    if not(len(Mat)==len(Mat[0])):
        error = True
        flash("Los vectores y la matriz no tienen el mismo tamaño")
    
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


@app.route('/gaussTotal',methods =['GET'])
def gaussTotal():
    return render_template('gaussTotal.html', title = traduccion('gaussTotal'), dic = tradudict())

@app.route('/gaussTotal',methods =['POST'])
def gaussTotal_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)
    print("post")
    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('gaussTotal_show', title = traduccion('gaussTotal'),datos = datos))

@app.route('/gaussTotal/show',methods =['GET'])
def gaussTotal_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    r,lista = libs.gauss(Mat,bv)
    print(r)
    lar = len(lista[0][0])-1
    anticache = random.randint(1,99999999)
    return render_template('gaussTotal_show.html', title = traduccion('gaussTotal'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sol=r)



@app.route('/lu',methods =['GET'])
def lu():
    return render_template('lu.html', title = traduccion('lu'), dic = tradudict())

@app.route('/lu',methods =['POST'])
def lu_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)
    print("post")
    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('lu_show', title = traduccion('lu'),datos = datos))


@app.route('/lu/show',methods =['GET'])
def lu_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    r,lista = libs.lu(Mat,bv)
    print(r)
    lar = len(lista[0][0])
    anticache = random.randint(1,99999999)
    return render_template('lu_show.html', title = traduccion('lu'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sol=r)


@app.route('/lup',methods =['GET'])
def lup():
    return render_template('lup.html', title = traduccion('lup'), dic = tradudict())

@app.route('/lup',methods =['POST'])
def lup_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)
    print("post")
    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('lup_show', title = traduccion('lu'),datos = datos))


@app.route('/lup/show',methods =['GET'])
def lup_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    r,lista = libs.luP(Mat,bv)
    print(r)
    lar = len(lista[0][0])
    anticache = random.randint(1,99999999)
    return render_template('lup_show.html', title = traduccion('lup'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sol=r)



@app.route('/dd',methods =['GET'])
def dd():
    return render_template('dd.html', title = traduccion('dd'), dic = tradudict())

@app.route('/dd',methods =['POST'])
def dd_post():
    
    x = str(request.form.get('X'))
    xv = formatearVector(x)



    y = str(request.form.get('Y'))
    
    yv = formatearVector(y)
    print(y)
    datos = [x,y]
    
    return redirect(url_for('dd_show', title = traduccion('dd'),datos = datos))


@app.route('/dd/show',methods =['GET'])
def dd_show():

    datos = request.args.getlist('datos', None)

    x =str(datos[0])
    xv = formatearVector(x)
    y = str(datos[1])
    yv = formatearVector(y)



    print(xv,yv)
    lista,lon,sho = libs.divi(xv,yv)
    
    lar = len(lista[0])
    anticache = random.randint(1,99999999)
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

    return render_template('dd_show.html', title = traduccion('dd'), lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar,sho =sho,lon = lon)


@app.route('/crout',methods =['GET'])
def crout():
    return render_template('crout.html', title = "Crout", dic = tradudict())

@app.route('/crout',methods =['POST'])
def crout_post():
    
    M =str(request.form.get('Matrix'))

    Mat = formatearMatriz(M)
    print(Mat)

    b = str(request.form.get('B'))
    
    bv = formatearVector(b)
    print(b)
    print(M,b)
    datos = [M,b]
    
    return redirect(url_for('crout_show', title = 'Crout',datos = datos))

@app.route('/crout/show',methods =['GET'])
def crout_show():

    datos = request.args.getlist('datos', None)

    M =str(datos[0])
    Mat = formatearMatriz(M)
    b = str(datos[1])
    bv = formatearVector(b)



    print(Mat,bv)
    lista = libs.crout(Mat,b)
    
    lar = len(lista[0][0])
    anticache = random.randint(1,99999999)
    return render_template('crout_show.html', title = 'Crout', lista = lista, tam = len(lista),anticache = anticache, dic = tradudict(), lar = lar)

@app.route('/fun',methods =['GET'])
def fun():
    return render_template('fun.html', title =traduccion('graficadora'), dic = tradudict())

@app.route('/fun',methods =['POST'])
def fun_post():
    
    F =str(request.form.get('F'))
    Xi = str(request.form.get('Xi'))
    Xs = str(request.form.get('Xs'))
    datos = [F,Xi,Xs]


    
    return redirect(url_for('fun_show', title = traduccion('graficadora'),datos = datos))


@app.route('/fun/show',methods =['GET'])
def fun_show():

    datos = request.args.getlist('datos', None)

    Fo = parse_expr(datos[0].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)

    if(datos[0]=='' or datos[1]==''):
        Xi = -50
        Xs = 50
    else:
        Xi = float(datos[1])
        Xs = float(datos[2])


    
    
    anticache = random.randint(1,99999999)




    xx = np.linspace(Xi,Xs, 1000)
        
    yy = F(xx)



    plt.plot(xx, np.transpose(yy))

    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    #plt.suptitle('Iteracion {0}'.format(item[0]))
        
    plt.savefig('statics/temp/{0}{1}.png'.format(anticache,1))
    plt.clf()

    
    return render_template('fun_show.html', title = traduccion('graficadora'),anticache = anticache, dic = tradudict() )
    #Completar



@app.route('/eva',methods =['GET'])
def eva():
    return render_template('eva.html', title =traduccion('evaluador'), dic = tradudict(), eval = False)

@app.route('/eva',methods =['POST'])
def eva_post():
    
    F =str(request.form.get('F'))
    Fo = parse_expr(F.replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    Xi = float(request.form.get('Xi'))
    result = F(Xi)
    datos = [Fo,Xi]


    
    return redirect(url_for('eva_show', title = traduccion('graficadora'),datos = datos))


@app.route('/eva/show',methods =['GET'])
def eva_show():

    datos = request.args.getlist('datos', None)

    Fo = parse_expr(datos[0].replace('^','**'))
    x = Symbol('x')
    F = lambdify(x, Fo)
    Xi = float(datos[1])
    result = F(Xi)



    
    
    anticache = random.randint(1,99999999)

    
    return render_template('eva_show.html', title = traduccion('evaluador'),anticache = anticache, dic = tradudict(),result = result )
    #Completar

@app.route('/lenguaje',methods =['GET'])
def lenguaje():
    return render_template('lenguaje.html', title =traduccion('idioma'), dic = tradudict(), eval = False)

@app.route('/esp',methods =['POST'])
def esp():
    global lang
    lang = 'Es'
    return redirect(url_for('numerico', title = traduccion('title')))

@app.route('/eng',methods =['POST'])
def eng():
    global lang
    lang = 'En'
    return redirect(url_for('numerico', title = traduccion('title')))


Es = {'title':"Análisis numérico",'correr':'Correr', 'biseccion':"Bisección", 'busquedas':"Búsquedas Incrementales", 'raicesI':'raices','gaussSimple':'Gaussiana Simple','solucion':'Solucion', 'graficadora':'Graficadora',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerancia', 'iteraciones':'Iteraciones','funcion':'Función', 'salir':'Atras', 'gaussParcial':'Gaussiana Parcial', 'gaussTotal':'Gaussiana Total', 'evaluador':'Evaluador',
          'bshowr':'se aproxima a una raiz con tolerancia de', 'Xo':'Xo','delta':'Delta', 'popxo':'Punto inicial','lu':'Factorizacion LU', 'lup':'Factorizacion LUP', 'iteracion':'Iteracion','idioma':'Idioma',
          'derivada':'Derivada', 'raices':'Raices Multiples','df1':'df1','df2':'df2', 'reglaFalsa':'Regla Falsa', 'secante':'Secante', 
          'puntoFijo':'Punto Fijo', 'G':'Funcion G(x)','popm':'Separados por espacios y ; Ej: 1 2 3; 4 5 6; 7 8 9', 'matrixdata':'Datos de la Matriz',
          'B':'Vector b', 'popv':'Separados por espacios Ej: 1 2 3' , 'X':'Vector x','norma':'Norma', 'Y':'Vector y', 'lv':'Valores a tomar',
          'dBiseccion':'- Debe haber certeza sobre la continuidad de la función f (x) en el intervalo [a, b]',
          'dFincremental':'- Se debe tener cuidado al elegir el aumento (Delta) para el que se va a evaluar la función, si el aumento es muy pequeño, existe el riesgo de que el proceso sea muy costoso, y si es muy grande, existe el riesgo de no detectar la raíz',
          'dFnewton':'- Seleccionar un valor inicial lo suficientemente cercano a la raíz buscada',
          'dFmultroot' : '- El método de Raíces Múltiples o Newton modificado, se creó con el fin de resolver algunos problemas que presenta el Método de Newton, cuando la derivada de la función tiende a cero al ser evaluada en "x", lo cual implica que la convergencia disminuye o incluso se suspende si se alcanza una división por cero. También, en el Método de la Secante ocurre un problema si la función es muy plana y f(x) y f(x-1) son aproximadamente iguales. Con este fin se creó el Método de las Raíces Múltiples.',
          'dFsecante' : '- Lo que básicamente hace es lanzar líneas secantes a la curva de la ecuación que originalmente se tenía, y verifica la intersección de esas líneas con el eje de la X para ver si se busca la raíz.',
          'dFfixepo' : 'El Método de Punto Fijo es un procedimiento iterativo que permite resolver ecuaciones no necesariamente lineales y se usa principalmente para determinar raíces de una función de la forma f(x) = 0, si se cumplen las condiciones de convergencia. Para este caso no es necesario tener un intervalo, su principal objetivo es buscar la raíz de una función partiendo de un valor inicial, una tolerancia y un número de iteraciones.',
          'dFfalsa' : 'Este método es una versión mejorada del método de bisección, su principal mejora es unir los puntos extremos del intervalo con una línea recta y la intersección con el eje "x" proporcionará una mejor aproximación de la raíz.',
          'dFjaco' : 'Este método parte de una aproximación inicial, a partir de esta recalcula los valores de x al despejarla de una ecuación, este proceso se realiza para las n incógnitas x y cada cálculo se realiza con los valores de la aproximación anterior.',
          'dFsaidel' : 'Este método es básicamente igual al método de Jacobi, la principal diferencia es que cada valor calculado de xk es usado para recalcular el valor de xk+1por ende converge más rápido a la solución que el método de Jacob',
          'dFlagran' : 'Es un procedimiento para encontrar los valores máximos y mínimos de funciones de múltiples variables sujetas a restricciones. Este método reduce el problema restringido con n variables a uno sin restricciones de n + k variables, donde k es igual al número de restricciones y cuyas ecuaciones se pueden resolver más fácilmente.',
          'dFgaussim' : 'Este método se aplica para resolver sistemas lineales. Consiste en escalonar la matriz aumentada del sistema aumentado para obtener un sistema equivalente.',
          'dFgauspar' : 'El pivoteo parcial es una de las técnicas de pivoteo. Dicta que el elemento pivote que debe escogerse es el mayor absolutamente de cada columna.',
          'dFgausto' : '    La eliminación gaussiana con pivote total es un método directo, que utiliza la eliminación gaussiana para encontrar el valor de sus incógnitas a través de la sustitución regresiva, pero tiene una diferencia en el procedimiento utilizado que se encuentra en el intercambio de filas y columnas, de modo que el elemento pivote sea el valor máximo de cada submatriz obtenido en las operaciones de cada etapa.',
          'dFlus' : 'La factorización de una matriz A en el producto de dos matrices LU por medio de las cuales se obtiene la matriz triangular inferior L colocando los multiplicadores en los lugares indicados por sus índices y en los números diagonales principales 1. La matriz U se obtiene de la matriz resultante del proceso de eliminación al eliminar la columna que corresponde a los términos independientes.',
          'dFlup' : 'En este método, se debe usar una matriz de permutación P que obtiene la sucesión de intercambios de filas desde una matriz de identidad.',
          'dFcholes': 'Una matriz cuadrada A con pivotes distintos de cero se puede escribir como el producto de una matriz triangular inferior L y una matriz triangular superior U. Sin embargo, si A es simétrico, factores tales que U es la transposición de L.',
          'dFcrout':'En el método de Crout, la matriz A se factoriza como A = LU, donde la matriz L es una matriz triangular inferior y U una matriz triangular superior con unidad diagonal.',
          'dFdividi' :'Fn es una variable discreta de n elementos y Xn es otra variable discreta de n elementos que corresponden, en pares, a la imagen o datos ordenados y abruptos que desea interpolar',
          'dFdooli' :'El método Doolitle es una variación de Crout que obtiene las matrices de factorización LU fila por fila o columna por columna. Es útil para matrices grandes en las que solo se almacenan elementos distintos de cero fila por fila o columna por columna.',
          'dFcuadra' :'El método define una función por secciones, en la que cada sección es un polinomio. La función obtenida debe pasar por los puntos dados, debe ser continua y suave. La suavidad está garantizada con la existencia de la primera derivada y la segunda derivada en los puntos de unión.',
          'dFcubi' :'Esta función consiste en una unión de polinomios cúbicos, uno para cada intervalo. La idea central es que, en lugar de usar un solo polinomio para interpolar todos los datos, se pueden usar segmentos de polinomios entre pares de datos de coordenadas y cada uno de ellos correctamente vinculado para ajustarse a los datos.',
          'dFlinea' :'La unión más simple entre dos puntos es una línea recta. Los trazadores de primer grado para un grupo de datos ordenados se pueden definir como un conjunto de funciones lineales.',
          'dFvander' :'Una matriz de Vandermonde es aquella que presenta una progresión geométrica en cada fila.', 'polinomio':'Polinomio',
          'dd':'Diferencias divididas y el polinomio de Newton', 'quap':'Trazadores Cuadráticos','cubi':'Trazadores Cubicos','line':'Trazadores lineales','abr':'Abrir', 'mdd':'Matriz de diferencias divididas',
          'dFgrafi' : 'Permite gracificar funciones', 'dFeval':'Permitir evaluar una función ingresada', 'dFidio':'Cambiar el idioma a Ingles', 'popf':'Ex: x**2+2*sin(x)*log(x)-exp(x)',
          'info' : 'Información', 'popxi':'Punto Inferior(Debe ser menor a Xs)', 'popxs':'Punto Superior(Debe ser mayor a Xi)','poptol':'La Tolerancia debe ser mayor que 0', 'popite':'Las Iteraciones deben ser mayor que 0','popdel':'Delta debe ser mayor que 0'
          }
En = {'title':"Numerical analysis",'correr':'Run', 'biseccion':"Bisection", 'busquedas':"Incremental search", 'raicesI':'roots', 'gaussSimple':'Simple Gaussian','solucion':'Solution','graficadora':'Plotter',
          'Xi':'Xi','Xs':'Xs', 'tolerancia':'Tolerance','iteraciones':'Iterations','funcion':'Function', 'salir':'Back', 'gaussParcial':'Partial Gaussian', 'gaussTotal':'Total Gaussian', 'evaluador':'Evaluator',
          'bshowr':'approaches the root with a tolerance of', 'Xo':'Xo', 'delta':'Delta', 'popxo':'Initial point', 'lu':'LU Factorization', 'lup':'LUP Factorization', 'iteracion':'Iteration','idioma':'Languaje',
          'derivada':'Derivative','raices':'Multiple Roots','df1':'df1','df2':'df2', 'reglaFalsa':'False Rule','secante':'Secant',
          'puntoFijo':'Fixed Point','G':'Function G(x)', 'popm':'Separated by spaces and ; Ex: 1 2 3; 4 5 6; 7 8 9', 'matrixdata':'Matrix Data',
          'B':'Vector b', 'popv':'Separated by spaces Ej: 1 2 3', 'X':'Vector x', 'norma':'Norma', 'Y':'Vector y', 'lv':'Values to take',
          'dBiseccion':'- There must be certainty about the continuity of the function f (x) in the interval [a, b].',
          'dFincrementa l':'- Care should be taken when choosing the increase (Delta) for which the function is to be evaluated, if the increase is very small, there is a risk that the process is very expensive, and if it is very large, there is a risk of not detect the root\n',
          'dFnewton':'- Select an initial value close enough to the searched root',
          'dFmultroot': '- It solves some problems presented by Newton´s Method, when the derivative of the function tends to zero when evaluated in "x", which implies that convergence decreases or is even suspended if a division by zero. In addition, in the drying method a problem occurs if the function is very flat and f (x) and f (x-1) are approximately equal.',
          'dFsecante' : '- What it basically does is to throw secant lines to the curve of the equation that is originally had, and it checks the intersection of those lines with the axis of the X to see if it is the root that is sought.',
          'dFfixepo' : 'Is an iterative procedure that allows solving non-determined linear equations and is mainly used to determine roots of a function of the form f (x) = 0, if convergence conditions are established. For this case it is not necessary to have an interval, its main objective is to find the root of a function based on an initial value, a tolerance and a number of iterations.',
          'dFfalsa' : 'This Method is an improved version of the Bisection Method, its main improvement is to join the extreme points of the interval with a straight line and the intersection with the "x" axis will provide a better approximation of the root.',
          'dFjaco' : 'This method is based on an initial approximation, from this calculation of the values ​​of x when obtained from an equation, this process is performed for the unknowns x and each calculation is performed with the values ​​of the previous approximation',
          'dFsaidel' : 'This method is basically the same as the Jacobi method, the main difference is that each calculated value of xk is used to recalculate the value of xk + 1 therefore converges faster to the solution than the Jacob method',
          'dFlagran' : 'It is a procedure to find the maximum and minimum values of functions of multiple variables subject to restrictions. This method reduces the restricted problem with n variables to one without restrictions of n + k variables, where k is equal to the number of restrictions, and whose equations can be solved more easily.',
          'dFgaussim' : 'This method is applied to solve linear systems. It consists of staggering the augmented matrix of the augmented system to obtain an equivalent system.',
          'dFgauspar' : 'Partial pivoting is one of the pivoting techniques. It dictates that the pivot element that must be chosen is the largest absolutely in each column.',
          'dFgausto' : 'Gaussian elimination with total pivoting is a direct method, which uses Gaussian elimination to find the value of its unknowns through regressive substitution, but it has a difference in the procedure used that lies in the exchange of rows and columns, so that the pivot element be the maximun value of each submatrix obtained in the operations of each stage',
          'dFlus' : 'It requires two LU matrices through which the lower triangular matrix L is obtained by placing the multipliers in the places indicated by their indexes and in the main diagonal numbers 1. Matrix U is obtained from the matrix resulting from the elimination process by eliminating the column that corresponds to the independent terms.',
          'dFlup' : 'In this method, a permutation matrix P must be used which obtains the succession of row exchanges from an identity matrix.',
          'dFcholes': 'A square matrix A with non-zero pivots can be written as the product of a lower triangular matrix L and an upper triangular matrix U. However, if A is symmetric, factors such that U is the transpose of L.',
          'dFcrout':'In Crout´s method the matrix A is factored as A = LU where the matrix L is a lower triangular matrix and U a superior triangular matrix with unit diagonal.',
          'dFdividi' :'Fn is a discrete variable of n elements and Xn is another discrete variable of n elements that correspond, in pairs, to the ordered and abrupt image or data that you want to interpolate',
          'dFdooli' :'The Doolitle method is a Crout variation that obtains the LU factorization matrices row by row or column by column. It is useful for large arrays of which only nonzero elements are stored row by row or column by column.',
          'dFcuadra' :'The method defines a function by sections, in which each section is a polynomial. The function obtained must pass through the given points, it must be continuous and smooth. Smoothness is guaranteed with the existence of the first derivative and the second derivative at the junction points.',
          'dFcubi' :'This function consists of a union of cubic polynomials, one for each interval. The central idea is that, instead of using a single polynomial to interpolate all the data, segments of polynomials between coordinate pairs of data can be used and each one properly linked to fit the data.',
          'dFlinea' :'The simplest union between two points is a straight line. First-degree plotters for a group of ordered data can be defined as a set of linear functions.',
          'dFvander' :'A Vandermonde matrix is ​​one that presents a geometric progression in each row.', 'polinomio':'Polynomial',
          'dd':'Split differences and the Newton polynomial', 'quap':'Quadratic Spline', 'cubi':'Cubic Spline', 'line':'Linear Spline','abr':'Open', 'mdd':'Split differences Matrix',
          'dFgrafi' : 'It allows to gracify functions', 'dFeval':'Allow to evaluate an entered function', 'dFidio':'Change language to Spanish', 'popf':'Ex: x**2+2*sin(x)*log(x)-exp(x)',
          'info':'Information', 'popxi':'Inferior Point(Must be less than Xs)','popxs': 'Superior Point(Must be higher than Xi)', 'poptol':'Tolerance must be higher than 0', 'popite':'Iterations must be higher than 0', 'popdel':'Delta must be higher than 0'
          }

app.run(host= '0.0.0.0', debug=True)

