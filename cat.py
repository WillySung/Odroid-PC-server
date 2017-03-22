# import the necessary packages
import cv2

cap = cv2.VideoCapture(0)
while(1):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # load the cat detector Haar cascade, then detect cat faces in the input image
    detector = cv2.CascadeClassifier("cascades/closed_frontal_palm.xml")
    rects = detector.detectMultiScale(gray, scaleFactor=1.3,minNeighbors=10, minSize=(75, 75))

    # loop over the cat faces and draw a rectangle surrounding each
    for (i, (x, y, w, h)) in enumerate(rects):
	    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
	    cv2.putText(img, "Cat #{}".format(i + 1), (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)
 
    # show the detected cat faces
    cv2.imshow("Cat Faces", img)
    cv2.waitKey(1)