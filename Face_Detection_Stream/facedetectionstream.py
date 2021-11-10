import cv2 

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
video_capture = cv2.VideoCapture(0)
ret = video_capture.set(3,640)
ret = video_capture.set(4,480)
 
while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

