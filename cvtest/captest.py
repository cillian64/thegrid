from __future__ import print_function
import cv2

clicks = []


def mouse_cb(event, x, y, flags, param):
    global clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(clicks) in [0, 4]:
            clicks = [(x, y)]
        else:
            clicks.append((x, y))


def draw_grid(frame, corners, splits=6):
    cv2.line(frame, corners[0], corners[1], (0, 255, 0), 3)
    cv2.line(frame, corners[1], corners[2], (0, 255, 0), 3)
    cv2.line(frame, corners[2], corners[3], (0, 255, 0), 3)
    cv2.line(frame, corners[3], corners[0], (0, 255, 0), 3)

    segments = [(corners[0], corners[1]), (corners[1], corners[2]),
                (corners[2], corners[3]), (corners[3], corners[0])]

    points = [[], [], [], []]
    for i, corners in enumerate(segments):
        u, v = corners
        a = (v[0] - u[0], v[1] - u[1])
        for j in range(1, splits):
            x = int(u[0] + (j / float(splits)) * a[0])
            y = int(u[1] + (j / float(splits)) * a[1])
            points[i].append((x, y))

    for i in range(1, splits):
        cv2.line(frame, points[0][i - 1], points[2][-i], (0, 255, 0), 2)
        cv2.line(frame, points[1][i - 1], points[3][-i], (0, 255, 0), 2)


cap = cv2.VideoCapture(-1)

cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_cb)

while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    draw = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

    for click in clicks:
        cv2.circle(draw, (click[0], click[1]), 5, (0, 255, 0), -1)

    if len(clicks) == 4:
        draw_grid(draw, clicks)

    cv2.imshow('image', draw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
