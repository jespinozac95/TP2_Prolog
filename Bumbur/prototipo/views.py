from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.core.files import File
from pyswip import Prolog
from pyswip import *
#import imp
#backEnd = imp.load_source('backEnd', '/home/josue/TP2_Prolog/Bumbur/backEnd.py')
#from backEnd import *
#prolog=Prolog()

#Vista al template de la pagina de inicio
def home(request):
	#main()
	return render_to_response('home.html')

#Definicion de la clase restaurantes para el uso de una form
class restaurante(forms.Form):
	Nombre = forms.CharField(max_length=100)
	Tipo_de_comida = forms.CharField(max_length=100)
	Ubicacion = forms.CharField(max_length=100)
	Telefono = forms.CharField(max_length=100)
	Horario = forms.CharField(max_length=100)
	Platillos_Favoritos = forms.CharField(max_length=200)

#Vista al template de la pagina de mantenimiento de datos
def mantenimiento(request):
	if request.method == 'POST':
		form = restaurante(request.POST)
		if form.is_valid():
			#si los datos son validos, bound-earlos y obtenerlos para insertarlos
			nombre = form.cleaned_data['Nombre']
			tipo = form.cleaned_data['Tipo_de_comida']
			horario = form.cleaned_data['Horario']
			ubicacion = form.cleaned_data['Ubicacion']
			telefono = form.cleaned_data['Telefono']
			favoritos = form.cleaned_data['Platillos_Favoritos']
			print "El nuevo restaurante es: "+nombre+"  "+tipo+"  "+ubicacion+"  "+telefono+"  "+horario+"  "+favoritos
			print "El nuevo restaurante es: "+nombre+"  "+tipo+"  "+ubicacion+"  "+telefono+"  "+horario+"  "+favoritos
			nuevoRestaurante(nombre,tipo,ubicacion,telefono,horario,favoritos) #platillos favoritos
			#print "El nuevo restaurante es: "+nombre+"  "+tipo+"  "+ubicacion+"  "+telefono+"  "+horario
			return HttpResponseRedirect('/thanks') #('felicidades.html')
	else:
		form = restaurante()
	return render(request, 'mantenimiento.html', {
        'form': form,
    })

def felicidades(request):
	return render_to_response('felicidades.html')

#Vista al template de la pagina de consultar datos
def consultar(request):
	leertxt()
	return render_to_response('consultar.html')

#Definicion de la clase platillos para el uso de una form
class platillos(forms.Form):
	Restaurante = forms.CharField(max_length=100)
	Nombre = forms.CharField(max_length=100)
	Tipo_de_comida = forms.CharField(max_length=100)
	Pais_de_origen = forms.CharField(max_length=100)
	Lista_Ingredientes = forms.CharField(max_length=200)

#Vista al template de la pagina de consultar datos
def platillo(request):
	if request.method == 'POST':
		form = platillos(request.POST)
		if form.is_valid():
			#si los datos son validos, bound-earlos y obtenerlos para insertarlos
			restaurante = form.cleaned_data['Restaurante']
			nombre = form.cleaned_data['Nombre']
			tipo = form.cleaned_data['Tipo_de_comida']
			pais = form.cleaned_data['Pais_de_origen']
			ingredientes = form.cleaned_data['Lista_Ingredientes']
			print "El nuevo platillo es: "+nombre+"  "+tipo+"  "+pais+"  "+ingredientes
			nuevaComida(restaurante,nombre,tipo,pais,ingredientes) #platillos favoritos
			return render_to_response('felicidades.html')
	else:
		form = platillos()
	return render(request, 'platillo.html', {
        'form': form,
    })

def respuesta(request):
	return HttpResponse("El restaurante es Mac Donalds")

#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------			PYTHON				-----------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

prolog=Prolog()

def nuevoRestaurante(nombre,tipo,ubicacion,telefono,horario,platillosFavoritos):
    print "Entro a nuevo restaurante"
    #p = Prolog()
    nombre=CambiarEspacios(nombre)
    tipo=CambiarEspacios(tipo)
    ubicacion=CambiarEspacios(ubicacion)
    telefono=CambiarEspacios(telefono)
    horario=CambiarEspacios(horario)
    platillosFavoritos=CambiarEspacios(platillosFavoritos)
    pred1="restaurante("+nombre.lower()+","+tipo.lower()+","+ubicacion.lower()+","+telefono+","+horario.lower()+","+platillosFavoritos.lower()+")"
    print pred1
    #print "Antes de assertz"
    #prolog.assertz("restaurante(ea,aeaea,cvcvc,dfdttt,dghg,hhnnnn)")
    #print "Despues del primer assertz"
    #prolog.assertz(pred1)
    #print "Despues del segundo assertz"
    grabar(pred1)
    print "Despues de grabar"

def alterar(lista):
    for elemento in lista:
        if isinstance(elemento, list):
            alterar(elemento)
        else:
            if not isinstance(elemento,int):
##                print("este es el elemento "+elemento)
##                if isinstance(elemento,str):
##                    print ("es str")
##                else:
##                    print ("no")
                elemento=elemento.replace("_"," ")                
                print("Con cambios este es el elemento "+elemento)
                print(lista)
            
    return lista

def div(palabra):
    palabra=palabra.split("xyz")
    return palabra
    
def CambiarEspacios2(palabra):
    palabra=palabra.replace("_"," ")
    palabra=palabra.replace("xyz",",")
    return palabra


def nuevaComida(restaurante, nombre, tipo, pais, receta):
    restaurante=CambiarEspacios(restaurante)
    nombre=CambiarEspacios(nombre)
    tipo=CambiarEspacios(tipo)
    pais=CambiarEspacios(pais)
    receta=CambiarEspacios(receta)
    
    pred="platillo("+restaurante.lower()+","+nombre.lower()+","+tipo.lower()+","+pais.lower()+","+receta+")"
    #prolog.assertz(pred)
    grabar(pred)

def consultaNombre(nombre):
    nombre=CambiarEspacios(nombre)
    while True:  
        restaurantes=[]
        for e in prolog.query("restaurante("+nombre.lower()+",Tipo,Ubicacion,Telefono,Horario,PlatFav)"):
            rest=[]
            rest.append(nombre)
            rest.append(e["Tipo"])
            rest.append(e["Ubicacion"])
            rest.append(e["Telefono"])
            rest.append(e["Horario"])
            rest.append(e["PlatFav"])
            rest.append(e['Tipo'])
            restaurantes.append(rest)
            restaurantes=alterar(restaurantes)
        return restaurantes

        
def consultaRestaurantes():
    while True:
        restaurantes=[]
        for e in prolog.query("restaurante(Nombre,Tipo,Ubicacion,Telefono,Horario,PlatFav)"):
            rest=[]
            rest.append(e["Nombre"])
            rest.append(e["Tipo"])
            rest.append(e["Ubicacion"])
            rest.append(e["Telefono"])
            rest.append(e["Horario"])
            rest.append(e["PlatFav"])
            restaurantes.append(rest)
        print restaurantes
        return restaurantes

            
def consultaTipo(tipo):
    tipo=CambiarEspacios(tipo)
    while True:
        restaurantes=[]
        for e in prolog.query("restaurante(Nombre,"+tipo.lower()+",Ubicacion,Telefono,Horario,PlatFav)"):
            rest=[]
            rest.append(e["Nombre"])
            rest.append(tipo)
            rest.append(e["Ubicacion"])
            rest.append(e["Telefono"])
            rest.append(e["Horario"])
            rest.append(e["PlatFav"])
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
    print "Entrar a leertxt()"
    archi=open('BaseConocimientos.txt','r+')
    print "despues de open BaseConocimientos.txt"
    linea=archi.readline()
    prolog.assertz("restaurante(d,t,r,y,u,y)")
    prolog.assertz("restaurante(u,y,i,y,urrr,y)")
    print "ASSERTZ DONE"
    print(linea)
    while linea!="":
        prolog.assertz(linea)
        linea=archi.readline()
        print(linea)
    archi.close()

def CambiarEspacios(palabra):
    palabra=palabra.replace(" ","_")
    palabra=palabra.replace(",","xyz")
    return palabra
    
##por si el archivo BasaeConocimientos.txt no esta hecho
archi=open('BaseConocimientos.txt','a+')
archi.close()
leertxt()

def grabar(hecho):
    archi=open('BaseConocimientos.txt','a+')
    archi.write(hecho+"\n")
    archi.close()
