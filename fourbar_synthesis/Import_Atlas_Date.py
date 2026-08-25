import json


def import_atlas():

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

    with open("data/atlas_seeds.json") as f:
        atlas_data = json.load(f)

    SEED_LINKAGES = [
        (entry["a"], entry["b"], entry["c"], entry["AD"])
        for entry in atlas_data
    ]

    SEED_NAMES = [entry["name"] for entry in atlas_data]

    return (SEED_LINKAGES, SEED_NAMES)