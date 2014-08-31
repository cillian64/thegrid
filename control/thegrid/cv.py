from __future__ import division
import sys
try:
    import cv2
except ImportError:
    cv2 = None # This will crash later but it doesn't matter.
import numpy as np

diff_th = 20
closing_kernel = np.ones((10, 10), np.uint8)
grid_corners = ((57, 346), (159, 211), (508, 183), (649, 303))
grid_left = grid_corners[0][0] - 20
grid_right = grid_corners[3][0] + 20
grid_top = grid_corners[0][1] + 20
grid_bottom = grid_corners[1][1] - 20


def draw_grid(frame, corners, splits=6):
    cv2.line(frame, corners[0], corners[1], (0, 155, 0), 2)
    cv2.line(frame, corners[1], corners[2], (0, 155, 0), 2)
    cv2.line(frame, corners[2], corners[3], (0, 155, 0), 2)
    cv2.line(frame, corners[3], corners[0], (0, 155, 0), 2)

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
        cv2.line(frame, points[0][i - 1], points[2][-i], (0, 155, 0), 1)
        cv2.line(frame, points[1][i - 1], points[3][-i], (0, 155, 0), 1)

if cv2 is not None:
    cap = cv2.VideoCapture(1);
    last_frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

def get_centroids():
    global last_frame
    cur_frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
    diff = np.abs(cur_frame.astype(int) - last_frame)
    moved = (diff > diff_th).astype(np.uint8) * 255
    closed = cv2.morphologyEx(moved, cv2.MORPH_CLOSE, closing_kernel)
    rv, labels, stats, centroids = cv2.connectedComponentsWithStats(closed)
    draw_frame = cv2.cvtColor(cur_frame.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    exported_centroids = []
    for idx, centroid in enumerate(centroids):
        if stats[idx][0] == 0 and stats[idx][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue
        x, y, w, h, a = stats[idx]
        cx, cy = int(centroid[0]), int(centroid[1])
        if not grid_left < cx < grid_right or not grid_bottom < cy < grid_top:
            cv2.rectangle(draw_frame, (x, y), (x+w, y+h), (0, 255, 255))
            continue
        if w < 14 or w > 80 or h < 14 or h > 80:
            cv2.rectangle(draw_frame, (x, y), (x+w, y+h), (0, 0, 255))
        else:
            cv2.rectangle(draw_frame, (x, y), (x+w, y+h), (0, 255, 0))
            cv2.circle(draw_frame, (cx, cy), 5, (0, 255, 0), -1)
            cxx = (cx - grid_left) / (grid_right - grid_left)
            cyy = (cy - grid_bottom) / (grid_top - grid_bottom)
            exported_centroids.append((cxx, cyy))
    draw_grid(draw_frame, grid_corners)
    cv2.imshow('video', draw_frame.astype(np.uint8))
    cv2.imshow('moved', moved)
    cv2.imshow('closed', closed)
    ch = cv2.waitKey(1)
    #if ch & 0xFF == 27:
    #    break
    last_frame = cur_frame
    return exported_centroids

#cv2.destroyAllWindows()
