import cv2
import pickle
import serverEmail as srEmail


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

#inicio de server email
email = srEmail.ServerEmail('smtp.gmail.com','587','facedetectionunaj@gmail.com','prog_real1')
emailSend = False
web_cam = cv2.VideoCapture(0)

while True:
    # Capture el marco
    ret, marco = web_cam.read()
    grises = cv2.cvtColor(marco, cv2.COLOR_BGR2GRAY)    
    rostros = faceCascade.detectMultiScale(grises, 1.5, 5)

    # Dibujar un rectángulo alrededor de las rostros
    for (x, y, w, h) in rostros:
        #print(x,y,w,h)
        roi_gray = grises[y:y+h, x:x+w]
        roi_color = marco[y:y+h, x:x+w]

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
            cv2.putText(marco, nombre, (x,y), font, 1, color, grosor, cv2.LINE_AA)
            
            #Se establece un flag momentaneo para que el envio de mail se realice una unica vez
            if emailSend == False:
                return_value, image = web_cam.read()
                imageName = 'opencvface.jpg'
                cv2.imwrite(imageName, image)
                email.sendMsjImage('facedetectionunaj@gmail.com','prueba',imageName)
                emailSend = True
                email.stopServerEmail()

    # Display resize del marco  
    marco_display = cv2.resize(marco, (1200, 650), interpolation = cv2.INTER_CUBIC)
    cv2.imshow('Detectando Rostros', marco_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo está hecho, liberamos la captura
web_cam.release()
cv2.destroyAllWindows()