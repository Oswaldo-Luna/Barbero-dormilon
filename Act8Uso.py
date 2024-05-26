from threading import Semaphore, Thread
import time, random

NTHREADS = 7
sillas = Semaphore(3)
sillaCorte = Semaphore(1)

clienteTiempoMin = 2
clienteTiempoMax = 5
corteTiempoMin = 2
corteTiempoMax = 5

def barberia(i):
    if(sillas.acquire(blocking=False)):
        espera = False
        while not sillaCorte.acquire(blocking=False):
            if not espera:
                print("[>] El cliente {0} se formo para esperar su turno".format(i))
                espera = True
        sillas.release()
        corteCabello(i, espera)
    else:
        print("[x] El cliente {0} llego, pero estaba lleno asi que se fue".format(i))

def corteCabello(i, espera):
    if not espera:
        print("[Zz..] EL barbero fue despertado por el cliente {0}".format(i))

    print("[>>] El cliente {0} esta siendo atendido".format(i))
    tiempoCliente = random.randrange(corteTiempoMin,corteTiempoMax+1)
    time.sleep(tiempoCliente)
    sillaCorte.release()
    print("[-] Ya se termino el corte el cliente {0} ".format(i))

    if sillas._value == 3 and sillaCorte._value ==1:
        print("[ZzZz] No hay nadie, el barbero se fue a dormir ZzZzZz")

if __name__ == '__main__':
    # Valores de tiempo
    print ('[ ] Tiempo minimo de cliente: {0}s'.format(clienteTiempoMin))
    print ('[ ] Tiempo maximo de cliente: {0}s'.format(clienteTiempoMax))
    print ('[ ] Tiempo minimo de corte: {0}s'.format(corteTiempoMin))
    print ('[ ] Tiempo maximo de corte: {0}s'.format(corteTiempoMax))
    print ('---------------------------------------')

    clientes = []

    for i in range(NTHREADS):
        clientes.append(Thread(target=barberia, args=[i]))
        tiempoCliente = random.randrange(clienteTiempoMin,clienteTiempoMax+1)
        time.sleep(tiempoCliente)
        print("[+] El proceso {0} ha sido creado".format(i))
        clientes[i].start()
