import json

import numpy as np


def import_PPt():
    """

       :rtype: tuple[ndarray[tuple[Any, ...], dtype[generic[Any]]] | ndarray[tuple[Any, ...], dtype[Any]], ndarray[tuple[Any, ...], dtype[Any]] | Any]

       Load precision points and theta design from the JSON file.

       Returns
       -------
       PRECISION_POINTS : np.ndarray
           Precision point coordinates.
       THETA_DESIGN : float
           Design angle in radians.

       Usage
       -----
       PRECISION_POINTS, THETA_DESIGN = import_PPt()

       """

    with open("data/precision_task.json") as f:
        PRECISION_TASK = json.load(f)

    PRECISION_POINTS = np.array(PRECISION_TASK["precision_points"])
    THETA_DESIGN = np.deg2rad(PRECISION_TASK["theta_deg"])

    return PRECISION_POINTS, THETA_DESIGN

