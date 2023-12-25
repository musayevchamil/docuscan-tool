import cv2
import numpy as np

def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

points = []

def auto_detect_document(image):
    detection_image = image.copy()
    gray = cv2.cvtColor(detection_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            cv2.drawContours(detection_image, [approx], -1, (0, 255, 0), 2)
            return approx, detection_image

    return None, detection_image

selected_corner = -1

def mouse_callback(event, x, y, flags, param):
    global points, orig, selected_corner
    threshold = 10

    if event == cv2.EVENT_LBUTTONDOWN:
        for i, point in enumerate(points):
            if abs(x - point[0]) < threshold and abs(y - point[1]) < threshold:
                selected_corner = i
                return

    elif event == cv2.EVENT_MOUSEMOVE and selected_corner != -1:
        points[selected_corner] = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        selected_corner = -1

    display = orig.copy()
    if len(points) == 4:
        cv2.polylines(display, [np.array(points)], True, (0, 255, 0), 2)
        for point in points:
            cv2.circle(display, point, 5, (0, 255, 0), -1)

    cv2.imshow("Original", display)

image = cv2.imread('1.jpg')
orig = image.copy()

detected_edges, detection_img = auto_detect_document(orig)
if detected_edges is not None:
    points = [tuple(p[0]) for p in detected_edges]

display = orig.copy()
if len(points) == 4:
    cv2.polylines(display, [np.array(points)], True, (0, 255, 0), 2)
    for point in points:
        cv2.circle(display, point, 5, (0, 255, 0), -1)
cv2.imshow("Original", display)

cv2.namedWindow("Original")
cv2.setMouseCallback("Original", mouse_callback)

while True:
    display = orig.copy()
    if len(points) == 4:
        cv2.polylines(display, [np.array(points)], True, (0, 255, 0), 2)
        for point in points:
            cv2.circle(display, point, 5, (0, 255, 0), -1)
    cv2.imshow("Original", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p') and len(points) == 4:
        processed_image = four_point_transform(orig, np.array(points))
        cv2.imshow("Processed", processed_image)

cv2.destroyAllWindows()
