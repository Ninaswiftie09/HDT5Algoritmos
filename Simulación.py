#Nina Nájera 231088 
#Hoja de Trabajo 5 Algoritmos

#Importamos las librerias
import simpy
import random
import matplotlib.pyplot as plt

#Se definen las constantes que dicen en las instrucciones
SEED = 42
RAM = 100
PROCESOS = [25, 50, 100, 150, 200]
INTERVALOS = [10, 5, 1]
TIEMPO_SIMULACION = 1000

promedio_de_tiempos = []

#Se crea la clase que simulará el sistema operativo
class Sistema:
    def __init__(self, entorno, cantidad_proceso, intervalo):
        self.entorno = entorno
        self.cpu = simpy.Resource(entorno, capacity=1)
        self.memoria = simpy.Container(entorno, capacity=RAM, init=RAM)
        self.cantidad_proceso = cantidad_proceso
        self.intervalo = intervalo
        self.tiempos_procesos = []

    def proceso(self, nombre, ver):
        llegada = self.entorno.now
        yield self.memoria.get(ver)
        with self.cpu.request() as req:
            yield req
            while ver > 0:
                yield self.entorno.timeout(random.expovariate(1))
                ver -= 1
            self.tiempos_procesos.append(self.entorno.now - llegada)

            #Hace la simulación  del sistema con cierta cantidad de procesos y un intervalo
def simular(cantidad_proceso, intervalo):
    random.seed(SEED) 
    entorno = simpy.Environment()
    sistema = Sistema(entorno, cantidad_proceso, intervalo)
    for i in range(cantidad_proceso):
        entorno.process(sistema.proceso(f'P{i}', random.randint(1, 10)))
    entorno.run(until=TIEMPO_SIMULACION)
    return sistema

#Bucle donde se simulan diferentes procesos con diferentes cantidades e intervalos
for cantidad_procesos in PROCESOS:
    for intervalo in INTERVALOS:
        sistema = simular(cantidad_procesos, intervalo)
        promedio = sum(sistema.tiempos_procesos) / len(sistema.tiempos_procesos)
        promedio_de_tiempos.append(promedio)
        print(f'Procesos: {cantidad_procesos}, Intervalo: {intervalo}, Promedio: {promedio}')
