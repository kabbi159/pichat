import cv2

a = cv2.imread('../target.jpg')

print(a.shape)

top = 0.1897120624780655
left = 0.3499026894569397
width = 0.07566346973180771
height = 0.11495399475097656

top = int(a.shape[0] * top)
left = int(a.shape[1] * left)
bottom = int(top + a.shape[0] * height)
right = int(left + a.shape[1] * width)

print(top, left, bottom, right)

a = cv2.rectangle(img=a, pt1=(left, top), pt2=(right, bottom), color=(0, 255, 0), thickness=3)
cv2.imshow('hi', a)
cv2.waitKey(0)
cv2.destroyAllWindows()
