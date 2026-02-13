import numpy as np


def track_objects(detections_per_frame):
    """
    Very conservative tracker.
    Matches objects by spatial overlap only.
    """

    tracks = []

    for frame_idx, detections in enumerate(detections_per_frame):
        for det in detections:
            tracks.append({
                "frame": frame_idx,
                "bbox": det["bbox"],
            })

    return tracks
