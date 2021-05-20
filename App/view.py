"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config
import folium
from branca.element import Figure
import webbrowser


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________


servicefile = 'bus_routes_14000.csv'
initialStation = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de buses de singapur")
    print("3- Calcular componentes conectados")
    print("4- Establecer estación base:")
    print("5- Hay camino entre estacion base y estación: ")
    print("6- Ruta de costo mínimo desde la estación base y estación: ")
    print("7- Estación que sirve a mas rutas: ")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, servicefile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))


def optionThree(cont):
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))


def optionFour(cont, initialStation):
    controller.minimumCostPaths(cont, initialStation)


def optionFive(cont, destStation):
    haspath = controller.hasPath(cont, destStation)
    print('Hay camino entre la estación base : ' +
          'y la estación: ' + destStation + ': ')
    print(haspath)


def optionSix(cont, destStation, initialStation):
    path = controller.minimumCostPath(cont, destStation)
    if path is not None:
        pathlen = stack.size(path)
        print('El camino es de longitud: ' + str(pathlen))
        resp = input
        # while (not stack.isEmpty(path)):
        #     stop = stack.pop(path)
        #     print(stop)
        plotstack(cont, path, initialStation, destStation)
    else:
        print('No hay camino')

def plotstack(cont,path,initialStation,destStation):
    
    fig = Figure(width=550,height=350)
    my_map = folium.Map(location=[1.29,103.85])
    fig.add_child(my_map)
    name = initialStation.split('-')[0]
    base_coords,base_road,base_descr = controller.getCoords(cont,name)
    folium.Marker(location=base_coords,popup=base_road+'\n'+base_descr).add_to(my_map)

    feat = folium.FeatureGroup('Route from {} to {}'.format(initialStation,destStation))
    all_coords = [base_coords]
    while (not stack.isEmpty(path)):
        stop = stack.pop(path)
        w = stop['weight']
        if w>0:
            vB = stop['vertexB']
            new_coords,new_road,new_descr = controller.getCoords(cont,vB.split('-')[0])

            folium.Marker(location=new_coords,popup=new_road+'\n'+new_descr).add_to(my_map)
            all_coords.append(new_coords)

    line = folium.vector_layers.PolyLine(all_coords,popup='Route from {} to {}'.format(initialStation,destStation)).add_to(feat)
    feat.add_to(my_map)

    folium.LayerControl().add_to(my_map)

    my_map.save('Mi_mapa.html')
    webbrowser.open('Mi_mapa.html')








def optionSeven(cont):
    maxvert, maxdeg = controller.servedRoutes(cont)
    print('Estación: ' + maxvert + '  Total rutas servidas: '
          + str(maxdeg))


"""
Menu principal
"""


def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(cont)

        elif int(inputs[0]) == 3:
            optionThree(cont)

        elif int(inputs[0]) == 4:
            msg = "Estación Base: BusStopCode-ServiceNo (Ej: 75009-10): "
            initialStation = input(msg)
            optionFour(cont, initialStation)

        elif int(inputs[0]) == 5:
            destStation = input("Estación destino (Ej: 15151-10): ")
            optionFive(cont, destStation)

        elif int(inputs[0]) == 6:
            destStation = input("Estación destino (Ej: 15151-10): ")
            # optionSix(cont, destStation)
            optionSix(cont, destStation, initialStation)

        elif int(inputs[0]) == 7:
            optionSeven(cont)

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()