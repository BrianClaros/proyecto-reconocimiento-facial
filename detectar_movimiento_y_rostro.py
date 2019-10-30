# Importamos las librerías necesarias
import numpy as np
import cv2
import time
import pickle

cascPath = "Cascades/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
eyeCascade = cv2.CascadeClassifier("Cascades/haarcascade_eye.xml")
smileCascade = cv2.CascadeClassifier("Cascades/haarcascade_smile.xml")

reconocimiento = cv2.face.LBPHFaceRecognizer_create()
reconocimiento.read("entrenamiento.yml")

etiquetas = {"nombre_persona" : 1 }
with open("labels.pickle",'rb') as f:
    pre_etiquetas = pickle.load(f)
    etiquetas = { v:k for k,v in pre_etiquetas.items()}

# Cargamos el vídeo
web_cam = cv2.VideoCapture(0)

# Inicializamos el primer frame a vacío.
# Nos servirá para obtener el fondo
fondo = None

# Recorremos todos los frames
while True:
    # Obtenemos el frame
    (grabbed, frame) = web_cam.read()

    # Si hemos llegado al final del vídeo salimos
    if not grabbed:
        break

    # Convertimos a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicamos suavizado para eliminar ruido
    gris = cv2.GaussianBlur(gris, (21, 21), 0)

    # Si todavía no hemos obtenido el fondo, lo obtenemos
    # Será el primer frame que obtengamos
    if fondo is None:
        fondo = gris
        continue

    # Calculo de la diferencia entre el fondo y el frame actual
    resta = cv2.absdiff(fondo, gris)

    # Aplicamos un umbral
    umbral = cv2.threshold(resta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilatamos el umbral para tapar agujeros
    umbral = cv2.dilate(umbral, None, iterations=2)

    # Copiamos el umbral para detectar los contornos
    contornosimg = umbral.copy()

    # Buscamos contorno en la imagen
    contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Recorremos todos los contornos encontrados
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if cv2.contourArea(c) < 1:
            continue
        # Inicio deteccion rostro
        rostros = faceCascade.detectMultiScale(gris, 1.5, 5)

        # Dibujar un rectángulo alrededor de las rostros
        for (x, y, w, h) in rostros:
            #print(x,y,w,h)
            roi_gray = gris[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # reconocimiento
            id_, conf = reconocimiento.predict(roi_gray)
            if conf >= 4  and conf < 85:
                #print(id_)
                #print(etiquetas[id_])           
                font = cv2.FONT_HERSHEY_SIMPLEX            

                nombre = etiquetas[id_]

                if conf > 50:
                    nombre = "Desconocido"

                color = (255,255,255)
                grosor = 2
                cv2.putText(frame, nombre, (x,y), font, 1, color, grosor, cv2.LINE_AA)

        # Display resize del frame  
        frame_display = cv2.resize(frame, (1200, 650), interpolation = cv2.INTER_CUBIC)
        cv2.imshow('Detectando Rostros', frame_display)

        # Fin deteccion rostro        

        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        (x, y, w, h) = cv2.boundingRect(c)
        # Dibujamos el rectángulo del bounds
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostramos las imágenes de la cámara, el umbral y la resta
    cv2.imshow("Camara", frame)
    cv2.imshow("Umbral", umbral)
    cv2.imshow("Resta", resta)
    cv2.imshow("Contorno", contornosimg)

    # Capturamos una tecla para salir
    key = cv2.waitKey(1) & 0xFF

    # Tiempo de espera para que se vea bien
    time.sleep(0.015)

    # Si ha pulsado la letra s, salimos
    if key == ord("s"):
        break

# Liberamos la cámara y cerramos todas las ventanas
web_cam.release()
cv2.destroyAllWindows()