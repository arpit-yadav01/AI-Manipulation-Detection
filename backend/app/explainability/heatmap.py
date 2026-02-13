import cv2
import numpy as np


def overlay_heatmap(image_path, cam, output_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    cam = cv2.resize(cam, (w, h))
    heatmap = cv2.applyColorMap(
        np.uint8(255 * cam),
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(img, 0.6, heatmap, 0.4, 0)
    cv2.imwrite(output_path, overlay)

    return output_path
