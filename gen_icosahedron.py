import numpy as np
import polyscope as ps
import os


def icosahedron_vertices(edge_length):
    # source: https://en.wikipedia.org/wiki/Regular_icosahedron
    golden = (1 + 5**0.5) / 2
    circumradius = (golden ** 2 + 1)**2
    # Scaling factor
    scale = edge_length / circumradius

    vertices = np.zeros((12, 3))
    faces = np.zeros((20, 3), dtype=int)

    ind = 0
    # Calculate 12 vertices
    for i in range(2):
        sign_1 = i * 2 - 1  # Determines the direction of the vertex

        for j in range(2):
            sign_2 = j * 2 - 1

            ind = i*6 + j*3

            vertices[ind, :] = (0, sign_2, sign_1*golden)
            vertices[ind+1,:] = (sign_2, sign_1*golden,0)
            vertices[ind+2,:] = (sign_1*golden, 0, sign_2)

    faces = np.array([
        [0, 3, 2],
        [0, 8, 3],
        [1, 4, 0],
        [1, 4, 6],
        [2, 5, 1],
        [2, 5, 7],

        [6, 9, 5],
        [6, 9, 11],
        [7, 10, 3],
        [7, 10, 9],
        [8, 11, 4],
        [8, 11, 10],

        [4, 0, 8],
        [4, 6, 11],
        [1, 0, 2],
        [1, 6, 5],
        [7, 3, 2],
        [7, 9, 5],
        [10, 3, 8],
        [10, 11, 9],
    ])

    return scale*vertices, faces


def generate_random_points_inside_triangle(p1, p2, p3, n):
    # https://blogs.sas.com/content/iml/2020/10/19/random-points-in-triangle.html
    vecs = np.zeros((3,2))
    vecs[:,0] = p2-p1
    vecs[:,1] = p3-p1

    points = np.zeros((n,3))
    for i in range(n):
        u = np.random.random(2)
        if u.sum() > 1:
            u = 1-u
        points[i, :] = vecs.dot(u) + p1
    return points


def fill_icosahedron(points_per_face):
    vertices, faces = icosahedron_vertices(2)
    n_faces = faces.shape[0]
    points = np.zeros((points_per_face*n_faces, 3))
    for i in range(n_faces):
        face = faces[i]
        points[points_per_face*i: points_per_face*(i+1), :] = generate_random_points_inside_triangle(*vertices[face], points_per_face)
    return points


def save_icosahedron_as_xzy(n_points):
    points = fill_icosahedron(n_points)
    filename = os.path.join("clouds", "icosahedron.xyz")
    with open(filename, "w") as fopen:
        lines = []
        for i in range(points.shape[0]):
            point = points[i, :]
            lines.append(" ".join([str(np.round(coord, 6)) for coord in point]))
        fopen.write("\n".join(lines))


if __name__ == "__main__":
    ico_n_points = 500

    ps.init()
    ico_vertices, ico_faces = icosahedron_vertices(2)
    print(ico_vertices)
    ico_points = fill_icosahedron(ico_n_points)
    ps_cloud = ps.register_point_cloud("my points", ico_points)
    ps_mesh = ps.register_surface_mesh("my mesh", ico_vertices, ico_faces)
    ps.show()

    save_icosahedron_as_xzy(ico_n_points)