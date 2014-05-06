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

def nuevoRestaurante(nombre, tipo, ubicacion, telefono, horario,platillosFavoritos):
    pred1="restaurante("+nombre.lower()+","+tipo.lower()+","+ubicacion.lower()+","+telefono+","+horario.lower()+","+platillosFavoritos.lower()+")"
    prolog.assertz(pred1)
    grabar(pred1)


def nuevaComida(resturante, nombre, tipo, pais, receta):
    pred="platillo("+resturante.lower()+","+nombre.lower()+","+tipo.lower()+","+pais.lower()+","+receta+")"
    prolog.assertz(pred)
    grabar(pred)

def consultaNombre(nombre):
    for e in prolog.query("restaurante("+nombre.lower()+",Tipo,Ubicacion,Telefono,Horario,PlatFav)"):
        print(nombre)
        print e["Tipo"]
        print e["Ubicacion"]
        print e["Telefono"]
        print e["Horario"]
        print e["PlatFav"]
        print("-------------------------")
        
def consultaRestaurantes():
    for e in prolog.query("restaurante(Nombre,Tipo,Ubicacion,Telefono,Horario,PlatFav)"):
        print e["Nombre"]
        print e["Tipo"]
        print e["Ubicacion"]
        print e["Telefono"]
        print e["Horario"]
        print e["PlatFav"]
        print("-------------------------")
        
def consultaTipo(tipo):
    for e in prolog.query("restaurante(Nombre,"+tipo.lower()+",Ubicacion,Telefono,Horario,PlatFav)"):
        print e["Nombre"]
        print (tipo)
        print e["Ubicacion"]
        print e["Telefono"]
        print e["Horario"]
        print e["PlatFav"]
        print("-------------------------")
        
def consultaPlatilloPais(pais):
    for e in prolog.query("platillo(Restaurante,Nombre,Tipo,"+pais.lower()+",Receta)"):
        print("El pais de origen es: "+pais)
        print e["Restaurante"]
        print e["Nombre"]
        print e["Tipo"]
        print("Los ingredientes del platillo son:")
        for each in e["Receta"]:
            print (each)
        print("-------------------------")
def consultaPlatilloRest(restaurante):
    for e in prolog.query("platillo("+restaurante.lower()+",Nombre,Tipo,Pais,Receta)"):        
        print (restaurante)
        print e["Nombre"]
        print e["Tipo"]
        print e["Pais"]
        print("Los ingredientes del platillo son:")
        for each in e["Receta"]:
            print (each)
        print("-------------------------")

# Consulta de platillos por restaurante que contengan un ingrediente especifico
def RestIng(restaurante,ingrediente): 
    for e in prolog.query("platillo("+restaurante.lower()+",Nombre,Tipo,Pais,Receta)"):
        ingredientes=e["Receta"]
        cont=0
        while cont!=len(ingredientes):
            if ingredientes[cont]==ingrediente:
                cont+=1
                print (restaurante)
                print e["Nombre"]
                print e["Tipo"]
                print e["Pais"]
                print("-------------------------")
            else:
                print(ingrediente)
                print(ingredientes[cont])
                cont+=1
         

