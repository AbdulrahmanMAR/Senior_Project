#image collector for project, this is how we create a dataset

import os
import cv2

Image_Dir = 'Dataset'
if not os.path.exists(Image_Dir):
    os.mkdir(Image_Dir)

number_of_signs = 31
dataset_size = 200

capture = cv2.VideoCapture(0)
for i in range(number_of_signs):
    if not os.path.exists(os.path.join(Image_Dir, str(i))):
        os.mkdir(os.path.join(Image_Dir, str(i)))

    print('Collecting data for {}'.format(i))

    done = False
    while True:
        ret, frame = capture.read()
        cv2.putText(frame, 'Press "Q" when ready', (100, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) == ord("q"):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = capture.read()
        cv2.imshow('Frame', frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(Image_Dir, str(i), '{}.jpg'.format(counter)), frame)
        counter += 1

capture.release()
cv2.destroyAllWindows()