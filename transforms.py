import numpy as np


def calculate_unit_normal_from_three_points(p_1: np.ndarray, p_2: np.ndarray, p_3: np.ndarray) -> np.ndarray:
    vec_a = p_2-p_1
    vec_b = p_3-p_1
    normal = np.cross(vec_a, vec_b)
    return normal/np.linalg.norm(normal)