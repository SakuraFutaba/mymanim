from manimlib import *

def stereo_project_point(point, axis = 2, r = 1, max_norm = 10000):
    #(x, y, z) -> (x / (1 - z), y / (1 - z), 0)
    point = fdiv(point * r, point[axis] + r)
    point[axis] = 0
    #求长度
    norm = get_norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point

def stereo_project(mobject, axis = 2, r = 1, outer_r = 20, **kwargs):
    epsilon = 1
    for submob in mobject.family_members_with_points():
        points = submob.get_points()
        n = len(points)
        for i in range(n):
            if points[i, axis] == -r:
                js = it.chain(
                    range(i + 1, n),
                    range(i - 1, -1, -1)
                )
                for j in js:
                    if points[j, axis] == -r:
                        continue
                    else:
                        vect = points[j] - points[i]
                        points[i] += epsilon * vect
                        break
        submob.apply_function(
            lambda p: stereo_project_point(p, axis, r, **kwargs)
        )

        # If all points are outside a certain range, this
        # shouldn't be displayed
        norms = np.apply_along_axis(get_norm, 1, submob.get_points())
        if np.all(norms > outer_r):
            # TODO, instead set opacity?
            # submob.get_points()[:, :] = 0
            submob.set_fill(opacity=0)
            submob.set_stroke(opacity=0)

    return mobject

class StereoProjectedSphere(Sphere):
    CONFIG = {
        "stereo_project_config": {
            "axis": 2,
        },
        "max_r": 32,
        "max_width": FRAME_WIDTH,
        "max_height": FRAME_WIDTH,
        "max_depth": FRAME_WIDTH,
        "radius": 1,
    }

    def __init__(self, rotation_matrix=None, **kwargs):
        digest_config(self, kwargs)
        if rotation_matrix is None:
            rotation_matrix = np.identity(3)
        self.rotation_matrix = rotation_matrix

        self.stereo_project_config["r"] = self.radius
        ParametricSurface.__init__(
            self, self.post_projection_func, **kwargs
        )
        self.submobjects.sort(
            key=lambda m: -m.get_width()
        )
        self.fade_far_out_submobjects()

    def post_projection_func(self, u, v):
        point = self.radius * Sphere.func(self, u, v)
        rot_point = np.dot(point, self.rotation_matrix.T)
        result = stereo_project_point(
            rot_point, **self.stereo_project_config
        )
        epsilon = 1e-4
        if np.any(np.abs(result) == np.inf) or np.any(np.isnan(result)):
            return self.func(u + epsilon, v)
        return result

    def fade_far_out_submobjects(self, **kwargs):
        max_r = kwargs.get("max_r", self.max_r)
        max_width = kwargs.get("max_width", self.max_width)
        max_height = kwargs.get("max_height", self.max_height)
        max_depth = kwargs.get("max_depth", self.max_depth)
        for submob in self.submobjects:
            violations = [
                np.any(np.apply_along_axis(get_norm, 1, submob.get_anchors()) > max_r),
                submob.get_width() > max_width,
                submob.get_height() > max_height,
                submob.get_depth() > max_depth
            ]
            if any(violations):
                # self.remove(submob)
                submob.fade(1)
        return self

class SPSphere(Sphere):
    CONFIG = {
        "resolution": (101, 51),
        "radius": 1,
        "u_range": (0, TAU),
        "v_range": (0, PI),
    }


    def uv_func(self, u: float, v: float) -> np.ndarray:
        return self.radius * np.array([
            fdiv(np.cos(u) * np.sin(v), 1 - np.cos(v)),
            fdiv(np.sin(u) * np.sin(v), 1 - np.cos(v)),
            0
        ])

class Kuri(Scene):
    CONFIG = {
        "camera_class": Camera,
        "resolution": (201, 101),
    }

    def init_camera(self):
        frame = self.camera.frame
        frame.set_focal_distance(10)
        frame.set_euler_angles(
            theta = 0 * DEGREES,
            phi = 0 * DEGREES,
        )
        return frame

    def init_surfaces(self):
        square = Square3D(
            side_length = 5, 
            u_range = (0, ASPECT_RATIO), 
            v_range = (0, 1), 
            resolution = self.resolution
            )
        square.move_to(ORIGIN, aligned_edge=ORIGIN)
        sphere = Sphere(
            resolution = self.resolution
            )
        stereo_projected_sphere = SPSphere(
            resolution = self.resolution
            )
        return square, sphere, stereo_projected_sphere

    def init_axis(self):
        axis = ThreeDAxes(
            x_range = np.array([-10.0, 10.0, 1.0]),
            y_range = np.array([-10.0, 10.0, 1.0]),
            z_range = np.array([-10.0, 10.0, 1.0]),
            )
        axis.add_coordinate_labels()
        return axis

    def construct(self):
        surfaces = self.init_surfaces()
        frame = self.init_camera()
        axis = self.init_axis()

        surfaces = [
            TexturedSurface(surface, "../assets/image/gun.png")
            for surface in surfaces
        ]

        for mob in surfaces:
            mob.mesh = SurfaceMesh(mob, resolution=(41, 21), depth_test=False)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)
            mob.add(mob.mesh)
        
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        sf = surfaces[0]

        self.play(
            frame.animate.increment_phi(45 * DEGREES),
            runtime = 3
        )

        # self.play(
        #     FadeIn(sf),
        #     ShowCreation(axis, runtime=3),
        #     ShowCreation(sf.mesh, lag_ratio=0.01, run_time=3),
        # )
        self.add(sf, axis, sf.mesh)


        self.play(
            Transform(sf, surfaces[1]),
            run_time=2
        )
        self.wait(2)

        self.play(
            Transform(sf, surfaces[2]),
            run_time=2
        )