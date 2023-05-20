import os
import re
import numpy as np
import openmesh


def get_file_extension(filename):
    return os.path.splitext(filename)[1]


def is_xyz(filename):
    ext = get_file_extension(filename)
    return ext == ".xyz"


def is_supported_by_openmesh(filename):
    ext = get_file_extension(filename)
    return ext in [".obj", ".off", ".ply", ".stl" and ".om"]


def parse_xyz(filename: str) -> np.ndarray:
    float_pattern = r"(?P<{}>[-]?(\d+[.])?\d+(e[+-]\d+)?)"
    line_pattern = float_pattern.format("x") + r"\s+" + \
                   float_pattern.format("y") + r"\s+" + r"\s*" + \
                   float_pattern.format("z") + r"\s*"

    with open(filename, "r") as fopen:
        lines = fopen.readlines()
        n_points = len(lines)
        points = np.zeros((n_points, 3))
        for i in range(n_points):
            line = lines[i]
            res = re.match(line_pattern, line)
            if res is None:
                raise ValueError("Bad line format at index {}: {}".format(i, line))
            point_dict = res.groupdict()
            points[i, 0] = point_dict["x"]
            points[i, 1] = point_dict["y"]
            points[i, 2] = point_dict["z"]

    return points


def parse_file_supported_by_openmesh(filename: str) -> np.ndarray:
    """
    From the documentation:
    OpenMesh currently supports five file types: .obj, .off, .ply, .stl and .om
    """
    mesh = openmesh.read_polymesh(filename)
    points = mesh.points()
    return points


def validate_given_file(filename: str):
    if not os.path.exists(filename):
        raise FileNotFoundError("File could not be read: {}".format(filename))

    if not is_xyz(filename) and not is_supported_by_openmesh(filename):
        raise Exception("File format {} not supported".format(filename))


def read_point_cloud(filename) -> np.ndarray:
    if is_xyz(filename):
        return parse_xyz(filename)

    if is_supported_by_openmesh(filename):
        return parse_file_supported_by_openmesh(filename)
