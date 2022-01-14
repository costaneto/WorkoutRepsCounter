import cv2

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # default camera is 0
        if not self.camera.isOpened():
            raise ValueError("Camera not found")

        self.width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # delete
    def __del__(self):
        self.camera.release()

    # get current image
    def get_frame(self):
        if self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                # opencv default is BGR, so we have to convert to RGB
                return ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return ret, None

        else:
            return None
