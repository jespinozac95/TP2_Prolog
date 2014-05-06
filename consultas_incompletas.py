from pyswip import Prolog

prolog=Prolog()

def grabar(hecho):
    archi=open('BaseConocimientos.txt','a')
    archi.write(hecho+"\n")
    archi.close()

def leertxt():
    archi=open('BaseConocimientos.txt','r')
    linea=archi.readline()
    print(linea)
    while linea!="":
        prolog.assertz(linea)

        linea=archi.readline()
    archi.close()

def alterar(lista):
    lista2=[]
    for elemento in lista:
        if isinstance(elemento, list):
            lista2.append(alterar(elemento))
        else:
            if not isinstance(elemento,int):
##                print("este es el elemento "+elemento)
##                if isinstance(elemento,str):
##                    print ("es str")
##                else:
##                    print ("no")
                elemento=CambiarEspacios2(elemento)
                lista2.append(elemento)
                #print("Con cambios este es el elemento "+elemento)
                #print(lista2)
    return lista2



# horario es un str, al igual que platillosFavoritos. 
def nuevoRestaurante(nombre, tipo, ubicacion, telefono, horario,platillosFavoritos):
    nombre=CambiarEspacios(nombre)
    tipo=CambiarEspacios(tipo)
    ubicacion=CambiarEspacios(ubicacion)
    telefono=CambiarEspacios(telefono)
    horario=CambiarEspacios(horario)
    platillosFavoritos=CambiarEspacios(platillosFavoritos)
    pred1="restaurante("+nombre.lower()+","+tipo.lower()+","+ubicacion.lower()+","+telefono+","+horario.lower()+","+platillosFavoritos.lower()+")"
    prolog.assertz(pred1)
    grabar(pred1)


def CambiarEspacios(palabra):
    palabra=palabra.replace(" ","_")
    palabra=palabra.replace(",","xyz")
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
    pred="platillo("+restaurante.lower()+","+nombre.lower()+","+tipo.lower()+","+pais.lower()+","+receta+")"
    prolog.assertz(pred)
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
            restaurantes=alterar(restaurantes)
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
            restaurantes=alterar(restaurantes)
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
            ing=[]
            for each in e["Receta"]:
                each=str(each)
                ing.append(each)
            rest.append(ing) 
            restaurantes.append(rest)
            restaurantes=alterar(restaurantes)
        return restaurantes 


def consultaPlatilloRest(restaurante):
    restaurante=CambiarEspacios(restaurante)
    while True:
        restaurantes=[]
        for e in prolog.query("platillo("+restaurante.lower()+",Nombre,Tipo,Pais,Receta)"):        
            rest=[]
##            rest.append(restaurante)
            rest.append(e["Nombre"])
            rest.append(e["Tipo"])
            rest.append(e["Pais"])
            ing=[]
            for each in e["Receta"]:
                each=str(each)
                ing.append(each)
            rest.append(ing)
            restaurantes.append(rest)
            restaurantes=alterar(restaurantes)
        return restaurantes



leertxt()
         

         
