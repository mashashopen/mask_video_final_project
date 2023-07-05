from PIL import Image
from retinaface import RetinaFace
import cv2
import numpy as np


class MaskFrame:

    def __init__(self, unmasked_frame_path):

        self.unmasked_image = Image.open(unmasked_frame_path)
        self.faces_locations = self.all_faces_locations()

    def all_faces_locations(self) -> list:
        faces_locations = []
        resp = RetinaFace.detect_faces(np.array(self.unmasked_image))
        try:
            count_faces = len(resp.keys())
            for key in resp.keys():
                identity = resp[key]
                facial_area = identity["facial_area"]
                x1, y1, x2, y2 = facial_area
                faces_locations.append((x1, y1, x2, y2))
        except AttributeError:
            return []

        return faces_locations

    def mask_frame(self, kernel_size, epsilon):

        if not self.faces_locations:
            return cv2.cvtColor(np.array(self.unmasked_image), cv2.COLOR_BGR2RGB)

        img = np.array(self.unmasked_image)
        img = img[:, :, ::-1].copy()

        for face_loc in self.faces_locations:

            x1, y1, x2, y2 = face_loc
            x1 -= epsilon
            y1 -= epsilon
            x2 += epsilon
            y2 += epsilon

            # Ensure face region is within image boundaries
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(x2, img.shape[1])
            y2 = min(y2, img.shape[0])

            # Check if face region is still valid
            if x1 >= x2 or y1 >= y2:
                continue
            face_img = img[y1:y2, x1:x2]
            if kernel_size[0] % 2 == 0 or kernel_size[0] < 1:
                kernel_dim = max(3, kernel_size[0] + 1)
                kernel_size = (kernel_dim, kernel_dim)
            blurred_face = cv2.GaussianBlur(face_img, kernel_size, epsilon)
            img[y1:y2, x1:x2] = blurred_face

        return img

