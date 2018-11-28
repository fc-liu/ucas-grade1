import cv2
import numpy as np

"""
empty listener
"""


def none_listener(event, x, y, flags, param):
    return


"""
listener to initial the location of boxs of balls
"""


def init_listener(event, x, y, flags, param):
    global drawing, ix, iy, img, bimg, count, finished, a, b, c, d

    # when mouse is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        count += 1
        ix, iy = x, y

    # when mouse is draged
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img = bimg.copy()
            cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 255), 1)

    # when mouse is released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (ix, iy), (x, y), (0, 0, 255), 1)
        if ix < x:
            a = ix
            c = x
        else:
            a = x
            c = ix
        if iy < y:
            b = iy
            d = y
        else:
            b = y
            d = iy

        print("ball" + str(count) + ": (" + str(a) + " , " + str(b) + ") , (" + str(c) + " , " + str(d) + ")")
        balls.append([[a, b], [c, d]])
        if count >= 3:
            finished = True
            # cv2.destroyAllWindows()
            cv2.setMouseCallback('image', none_listener)
        bimg = img


vedio = "Ball.avi"
output = "output.avi"
drawing = False
ix, iy, a, b, c, d = -1, -1, -1, -1, -1, -1
balls = []
count = 0
finished = False

cap = cv2.VideoCapture(vedio)

ret, img = cap.read()

# initial the first frame, and listener to de motions
if ret:
    bimg = img.copy()
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', init_listener)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, 'please use mouse to select 3 balls, and don\'t overlay each other', (100, 100), font, 0.5,
                (255, 255, 255), 1,
                cv2.LINE_AA)
    while not finished:
        cv2.imshow('image', img)
        cv2.waitKey(20)
    cap.release()

cap = cv2.VideoCapture(vedio)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# take first frame of the video
ret, frame = cap.read()
# setup initial location of window

track_wins = []
track_wins_val = []
term_cs = []
roi_hists = []
channel = 0

# for each ball, only deal the selected area,
for ball in balls:
    ix = ball[0][0]
    iy = ball[0][1]
    x = ball[1][0]
    y = ball[1][1]
    print("ball: (" + str(ix) + " , " + str(iy) + ") , (" + str(x) + " , " + str(y) + ")")

    r, h, c, w = iy, y - iy, ix, x - ix
    track_window = (c, r, w, h)
    # set up the ROI for tracking
    roi = frame[r:r + h, c:c + w]

    # convert to hsv, use threshold to filt the background, and compute the histogram
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    # hsv_roi = roi
    mask = cv2.inRange(hsv_roi, np.array((50., 50., 50.)), np.array((255., 90., 255.)))
    # cv2.imshow('mask', mask)
    # cv2.waitKey(100000)

    roi_hist = cv2.calcHist([hsv_roi], [channel], mask, [255], [0, 255])
    # cv2.imshow('roi', roi_hist)
    # cv2.waitKey(1000000)
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 10)

    roi_hists.append(roi_hist)
    track_wins.append(track_window)
    track_win_val = sum(sum(mask))

    track_wins_val.append(track_win_val)
    # print("track win val : " + str(track_win_val))
    term_cs.append(term_crit)

    cv2.rectangle(frame, (ix, iy), (x, y), (0, 0, 255), 1)

out.write(frame)
cv2.imshow('image', frame)
cv2.waitKey(20)
y_max = frame.shape[0]
x_max = frame.shape[1]
y_min = iy

# begin tracking
while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        mod_frame = frame.copy()
        for i in range(balls.__len__()):
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # hsv = frame
            mask = cv2.inRange(hsv, np.array((50., 50., 50.)), np.array((255., 90., 255.)))

            hsv = cv2.bitwise_and(hsv, hsv, mask=mask)

            dst = cv2.calcBackProject([hsv], [channel], roi_hists[i], [0, 255], 1)
            # multi = 1

            # the meanshift algo openCV applied performs quit terrible, so I rerule the search path
            while True:
                # apply meanshift to get the new location
                ret, track_wins[i] = cv2.meanShift(dst, track_wins[i], term_cs[i])
                # Draw it on image
                c, r, w, h = track_wins[i]
                roi = dst[r:r + h, c:c + w]
                roi_val = sum(sum(roi))
                print("roi val : " + str(roi_val))
                print("x : " + str(c) + " y : " + str(r))

                if roi_val > (track_wins_val[i] / 20):
                    break

                # in this case, the ball is not tracked, so I should move the track window,
                # the search is vertical first, then horizonal, each step is 5px
                else:
                    if r + h + 5 >= y_max:
                        track_wins[i] = (c + 5, y_min, w, h)
                        # multi = -1 * multi
                    elif c + w >= x_max:
                        break
                    else:
                        track_wins[i] = (c, r + 5, w, h)

            mod_frame = cv2.rectangle(mod_frame, (c, r), (c + w, r + h), (0, 0, 255), 1)

        cv2.imshow('image', mod_frame)
        out.write(mod_frame)

        # When everything done, release the capture
        k = cv2.waitKey(50) & 0xFF
        if k == 27:
            break
    else:
        img = mod_frame.copy()
        break

print("finish!! please press Esc to exit!")
# hold the vedio, and press esc to quit
while True:
    cv2.imshow("image", img)
    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
