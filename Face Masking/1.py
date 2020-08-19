import cv2
 
img = cv2.imread('test.jpg')
 
cv2.imshow('sample image',img)
 
cv2.waitKey(0)
cv2.destroyAllWindows()