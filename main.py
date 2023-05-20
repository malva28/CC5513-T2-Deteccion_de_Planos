import openmesh
import polyscope as ps
import numpy as np
import file_parser
import transforms
import argparse
import polyscope as ps
from progress_bar import print_progress_bar
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Detección de Planos en Nubes de Puntos',
        description='Estima planos en una nube de puntos mediante un algoritmo RANSAC.',
        epilog='Tarea 2 del curso CC5513: Procesamiento geométrico y análisis de formas')

    parser.add_argument('--file', default="clouds/cube.xyz", help="Ruta del archivo con la información de la nube de "
                                                                  "puntos")  # positional argument
    parser.add_argument('--inliers', default=100, type=int,
                        help="Controla la cantidad de puntos que deben caer dentro de un plano para que éste se "
                             "considere válido.")
    parser.add_argument('--cmap', default="viridis", help="Mapa de colores para la curvatura mostrada en polyscope. "
                                                          "Opciones de colores disponibles en: "
                                                          "https://polyscope.run/py/features/color_maps/")
    parser.add_argument('--threshold', default=0.1, type=float,
                        help="Distancia máxima a la que un punto se considera que está dentro de un plano")

    args = parser.parse_args()

    file_parser.validate_given_file(args.file)
    points = file_parser.read_point_cloud(args.file)

    cloud_len = points.shape[0]
    #n_iterations = cloud_len * 5
    n_iterations = int(cloud_len/1000)
    p_index_set = np.arange(stop=cloud_len, dtype=int)

    normal_planes = [np.zeros(6)]
    point_plane_indices = np.zeros(cloud_len, dtype=int)
    invalid_plane_indices = np.zeros(cloud_len, dtype=int)
    n_planes = 0
    n_inv_planes = 0
    for it in range(n_iterations):
        # En general, la eficiencia aquí viene dada por el uso de operaciones de numpy,
        # evitando los ciclos for de python
        print_progress_bar(it, n_iterations, print_end="")
        # si no quedan suficientes puntos o los puntos que sobran pertenecen a un mismo
        # plano descartado, rompemos la ejecución
        if len(p_index_set) < 3 or ((invalid_plane_indices != 0).all() and
                                    (invalid_plane_indices != invalid_plane_indices[0]).all()):
            break
        selection = np.random.choice(p_index_set, size=3, replace=False)
        if invalid_plane_indices[selection[0]] == invalid_plane_indices[selection[1]] and \
                invalid_plane_indices[selection[0]] == invalid_plane_indices[selection[2]] and \
                invalid_plane_indices[selection[0]] != 0:
            # Optimización: si tres puntos previamente tomados pertenecen a un mismo plano descartado, evitamos
            # procesarlos nuevamente pues debieran entregarnos un plano casi idéntico a otro anterior
            # en su lugar, escogemos un punto de otro plano inválido o que no haya sido procesado antes
            repeated_plane = invalid_plane_indices[selection[0]]
            outside_indices = p_index_set[np.where(invalid_plane_indices[p_index_set] != repeated_plane)]
            selection[2] = np.random.choice(outside_indices, size=1)

        normal = transforms.calculate_unit_normal_from_three_points(*[points[idx, :] for idx in selection])

        distance = np.zeros((len(p_index_set), 2))
        distance[:, 0] = p_index_set
        distance[:, 1] = np.abs((points[p_index_set] - points[selection[0]]).dot(normal.transpose())) / np.linalg.norm(
            normal)

        i_inliers = distance[np.where(distance[:, 1] < args.threshold)][:, 0]
        i_inliers = i_inliers.astype(int)
        if isinstance(i_inliers, tuple):
            i_inliers = i_inliers[0]
        n_inliers = len(i_inliers)
        if n_inliers >= args.inliers:
            # a probably valid plane was found
            n_planes += 1

            plane_coefs = np.zeros(6)
            plane_coefs[0:3] = normal
            plane_coefs[3:6] = points[selection[0]]
            normal_planes.append(plane_coefs)

            point_plane_indices[i_inliers] = n_planes
            # updateamos también el registro de planos inválidos, en caso de que
            # algún punto ya no pertenezca a uno de ellos
            invalid_plane_indices[i_inliers] = 0
            # i_i_inliers = np.zeros(i_inliers.shape, dtype=int)
            # for i in range(len(i_inliers)):
            #    index = np.where(p_index_set == i_inliers[i])[0][0]
            #    i_i_inliers[i] = index
            i_i_inliers = np.where(np.in1d(p_index_set, i_inliers))
            if isinstance(i_i_inliers, tuple):
                i_i_inliers = i_i_inliers[0]
            p_index_set = np.delete(p_index_set, i_i_inliers)
        else:
            # invalid plane
            n_inv_planes += 1
            invalid_plane_indices[i_inliers] = n_inv_planes
    normal_planes = np.array(normal_planes)

    ps.init()
    ps_cloud = ps.register_point_cloud("my points", points)
    ps_cloud.add_scalar_quantity("plane", point_plane_indices, enabled=True, cmap=args.cmap)
    ps_plane = ps.register_point_cloud("plane points", normal_planes[:, 3:6])
    ps_plane.add_vector_quantity("normals", normal_planes[:, 0:3])

    ps.show()
