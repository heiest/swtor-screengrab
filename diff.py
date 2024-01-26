# import the necessary packages
from skimage.metrics import structural_similarity
import imutils
import cv2
before = cv2.imread('./tooltips/Before5.png', cv2.IMREAD_COLOR)
after = cv2.imread('./tooltips/After5.png', cv2.IMREAD_COLOR)
(score, diff) = structural_similarity(cv2.cvtColor(before, cv2.COLOR_BGRA2GRAY), cv2.cvtColor(after, cv2.COLOR_BGRA2GRAY), full=True)
diff = (diff * 255).astype("uint8")
print("SSIM: {}".format(score))
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
bounding_rects = []
for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    bounding_rects.append((x, y, w, h))
    cv2.rectangle(before, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.rectangle(after, (x, y), (x + w, y + h), (0, 0, 255), 2)
# show the output images
# cv2.imshow("Original", before)
# cv2.imshow("Modified", after)
cv2.imwrite('./tooltips/Before-After Diff5.png', after)
# cv2.imshow("Diff", diff)
# cv2.imshow("Thresh", thresh)
# cv2.waitKey(0)
print(bounding_rects)