from keras.models import load_model
import time
import numpy as np
import cv2
from PIL import Image
from numpy.matlib import repmat
import math
import os
import pandas as pd

from funciones import msf
from funciones import segs

#Cargar modelo
model = load_model('Clasificador.h5')

archivo = pd.read_csv('video.csv', sep=',')

now_origin = time.time()

for k in range (0,len(archivo)):
    now = time.time()
    
    csv_salida = open(archivo['nombre_video'][k]+'.csv', 'w') #Creación del csv que se sobreescribirá
    csv_salida.write(f'intervalo,inicio,fin\n')
    
    cap = cv2.VideoCapture(archivo['nombre_video'][k]) 
    fps = cap.get(cv2.CAP_PROP_FPS)
        
    inicio_video = archivo['inicio'][k]
    final_video = archivo['final'][k]
    seg = segs(inicio_video, final_video)
    fpsextr = 3
    
    a = np.zeros((seg*fpsextr, 224,224,3))
    cont = 1
    cont1 = 0
    tiempos = []
    
    frec_intervalo = 10
    tomador_decision = 2
    
    while cap.isOpened():
        
        ret, frame = cap.read()

        if ret == False:
            break

        if(msf(inicio_video) <= cont <= msf(final_video)):
            if(cont%(30//fpsextr) == 0):
                image = np.array(frame)
                image.resize(1,224,224,3)

                if (cont1 < seg*fpsextr):
                    a[cont1,:,:,:] = image
                    cont1+=1

                elif (cont1 == seg*fpsextr):
                    cont1 = 0

                duration = cont/fps
                minutes = int(duration/60)
                seconds = int(duration%60)
                tiempos.append(str(minutes) + ':' + str(seconds))

        cont = cont+1         

        if (cont == (msf(final_video)+1)):
            break
        
    cap.release
    
    #print(tiempos)
    print(f'PRIMERA FASE LISTA EN : {(time.time()-now)/60} MINUTOS')
    
    result = model.predict(a)
    resultados_b = (result>0.5)*1
    
    resultados_f = np.zeros(resultados_b.shape[0]-frec_intervalo)

    for i in range (0, resultados_b.shape[0]-frec_intervalo, 1):
        temp = resultados_b[i:i+frec_intervalo]
        resultados_f[i] = temp.sum() > tomador_decision
    
 #   print(f'SEGUNDA FASE LISTA EN : {(time.time()-now)/60} MINUTOS')
    
    
    intervalos = []
    i = 0 
    while (i < resultados_f.shape[0]):
        if resultados_f[i] == 1:
            inic = i
            i+=1    

            while resultados_f[i] == 1:
                    i+=1
                    if i == resultados_f.shape[0]:
                        break 
            fin = i-1
            intervalos.append((inic,fin))

        i+=1
    
    #print(intervalos)
    #print(f'TERCERA FASE LISTA EN : {(time.time()-now)/60} MINUTOS')
    
    for j in range (0, len(intervalos)):
        
        csv_salida.write(f'{j},{tiempos[intervalos[j][0]]},{tiempos[intervalos[j][1]]}\n')
        #print(f'duración: {tiempos[intervalos[j][0]]}-{tiempos[intervalos[j][1]]}')

    csv_salida.close()
    #print(f'Duración evaluación del video : {(time.time()-now)/60} Minutos Aprox.')
    
#print(f'Duración evaluación TOTAL : {(time.time()-now_origin)/60} Minutos Aprox.')