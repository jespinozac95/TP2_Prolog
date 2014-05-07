from flask import Flask
from flask import request, redirect, url_for, abort, session 
from flask import render_template
from pyswip import Prolog
from pyswip import *

prolog = Prolog()
app = Flask("Bumbur")



@app.route('/')
def home():
	return render_template('home.html', name='home')

@app.route('/consultar')
def consultar():
    return render_template('consultar.html')

@app.route('/mantenimiento')
def mantenimiento():
    return render_template('mantenimiento.html')
    
@app.route('/platillo')
def platillo():
    return render_template('platillo.html')
    
@app.route('/newRestaurante', methods=['POST'])
def newRestaurante():
    Nombre = request.form['nombre']
    TipoDeComida = request.form['tipoDeComida']
    Ubicacion = request.form['ubicacion']
    Telefono = request.form['telefono']
    Horario = request.form['horario']
    nuevoRestaurante(Nombre,TipoDeComida,Ubicacion,Telefono,Horario)
    return render_template('felicidades.html')
    
@app.route('/newPlatillo', methods=['POST'])
def newPlatillo():
    Restaurante = request.form['restaurante']
    Nombre = request.form['nombre']
    Tipo = request.form['tipo']
    Pais = request.form['pais']
    Receta = request.form['receta']
    nuevaComida(Restaurante,Nombre,Tipo,Pais,Receta)
    return render_template('felicidades.html')    
    
@app.route('/consultarTodosRestaurantes')
def consultarTodosRestaurantes():
	lista = consultaRestaurantes()
	print "La lista es: "+lista
	return render_template('mostrarConsulta.html',lista = lista)
	
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------			BACKEND				-----------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

def nuevoRestaurante(nombre,tipo,ubicacion,telefono,horario):
    nombre=CambiarEspacios(nombre)
    tipo=CambiarEspacios(tipo)
    ubicacion=CambiarEspacios(ubicacion)
    telefono=CambiarEspacios(telefono)
    horario=CambiarEspacios(horario)
    pred1="restaurante("+nombre.lower()+","+tipo.lower()+","+ubicacion.lower()+","+telefono+","+horario.lower()+")"
    prolog.assertz(pred1)
    grabar(pred1)

def nuevaComida(restaurante, nombre, tipo, pais, receta):
    restaurante=CambiarEspacios(restaurante)
    nombre=CambiarEspacios(nombre)
    tipo=CambiarEspacios(tipo)
    pais=CambiarEspacios(pais)
    receta=CambiarEspacios(receta)
    pred="platillo("+restaurante.lower()+","+nombre.lower()+","+tipo.lower()+","+pais.lower()+","+receta+")"
    prolog.assertz(pred)
    grabar(pred)
    
def alterar(lista):
    for elemento in lista:
        if isinstance(elemento, list):
            alterar(elemento)
        else:
            if not isinstance(elemento,int):
                elemento=elemento.replace("_"," ")                
                #print("Con cambios este es el elemento "+elemento)
                #print(lista)
            
    return lista

def div(palabra):
    palabra=palabra.split("xyz")
    return palabra
    
def CambiarEspacios2(palabra):
    palabra=palabra.replace("_"," ")
    palabra=palabra.replace("xyz",",")
    return palabra

def consultaNombre(nombre):
    nombre=CambiarEspacios(nombre)
    while True:  
        restaurantes=[]
        for e in prolog.query("restaurante("+nombre.lower()+",Tipo,Ubicacion,Telefono,Horario)"):
            rest=[]
            rest.append(nombre)
            rest.append(e["Tipo"])
            rest.append(e["Ubicacion"])
            rest.append(e["Telefono"])
            rest.append(e["Horario"])
            rest.append(e['Tipo'])
            restaurantes.append(rest)
            restaurantes=alterar(restaurantes)
        return restaurantes

        
def consultaRestaurantes():
    while True:
        restaurantes=[]
        for e in prolog.query("restaurante(Nombre,Tipo,Ubicacion,Telefono,Horario)"):
            restaurantes.append(e["Nombre"])
        print restaurantes
        return restaurantes

            
def consultaTipo(tipo):
    tipo=CambiarEspacios(tipo)
    while True:
        restaurantes=[]
        for e in prolog.query("restaurante(Nombre,"+tipo.lower()+",Ubicacion,Telefono,Horario)"):
            rest=[]
            rest.append(e["Nombre"])
            rest.append(tipo)
            rest.append(e["Ubicacion"])
            rest.append(e["Telefono"])
            rest.append(e["Horario"])
            restaurantes.append(rest)
        return restaurantes
        
def consultaPlatilloPais(pais):
    pais=CambiarEspacios(pais)
    while True:
        restaurantes=[]
        for e in prolog.query("platillo(Restaurante,Nombre,Tipo,"+pais.lower()+",Receta)"):
            rest=[]
            rest.append(e["Restaurante"])
            rest.append(e["Nombre"])
            rest.append(e["Tipo"])
            rest.append(pais)
##            for each in e["Receta"]:
##                ing=[]
##                ing.append(e["Receta"][0])                
##                rest.append(ing)
            restaurantes.append(rest)
        return restaurantes 

def consultaPlatilloRest(restaurante):
    restaurante=CambiarEspacios(restaurante)
    while True:
        restaurantes=[]
        for e in prolog.query("platillo("+restaurante.lower()+",Nombre,Tipo,Pais,Receta)"):        
            rest=[]
            rest.append(restaurante)
            rest.append(e["Nombre"])
            rest.append(e["Tipo"])
            rest.append(e["Pais"])
            for each in e["Receta"]:
                ing=[]
                ing.append(each)
                rest.append(ing)
            restaurantes.append(rest)
        return restaurantes

def RestDeIng(restaurante,ingrediente):
    restaurante=CambiarEspacios(restaurante)
    ingrediente=CambiarEspacios(ingrediente)
    while True:
        restaurantes=[]
    for e in prolog.query("platillo("+restaurante.lower()+",Nombre,Tipo,Pais,Receta)"):
        rest=[]
        ingredientes=e["Receta"]
        cont=0
        while cont!=len(ingredientes):
            if ingredientes[cont]==ingrediente:
                cont+=1
                rest.append(restaurante)
                rest.append(e["Nombre"])
                rest.append(e["Tipo"])                
                rest.append(e["Pais"])
                restaurantes.append(rest)
            else:
                ing=[]
                ing.append(ingrediente)                
                cont+=1
        return restaurantes
        
def leertxt():
    archi=open('BaseConocimientos.txt','r+')
    linea=archi.readline()
    #print(linea)
    while linea!="":
        prolog.assertz(linea)
        linea=archi.readline()
        #print(linea)
    archi.close()

def CambiarEspacios(palabra):
    palabra=palabra.replace(" ","_")
    palabra=palabra.replace(",","xyz")
    return palabra
    
#por si no esta creado todavia el archivo    
archi=open('BaseConocimientos.txt','a+') 
archi.close()
leertxt()

def grabar(hecho):
    archi=open('BaseConocimientos.txt','a+')
    archi.write(hecho+"\n")
    archi.close()

#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------			BACKEND				-----------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	#app.debug = True
	app.run(host='192.168.0.6')
