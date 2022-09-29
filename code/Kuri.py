from manimlib import *

def stereo_project_point(point, axis = 2, r = 1, max_norm = 1000):
    #(x, y, z) -> (x / (1 + z), y / (1 + z), 0)
    point = fdiv(point * r, r + point[axis] + 1e-10)
    point[axis] = 0
    #限制长度
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
        # "u_range": (TAU / 2 ** 20, TAU - TAU / 2 ** 20),
        # "v_range": (PI / 2 ** 20, PI - PI / 2 ** 20),
        "u_range": (0, TAU),
        "v_range": (0, PI),
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

        super().__init__(**kwargs)
        # self.submobjects.sort(
        #     key=lambda m: -m.get_width()
        # )
        # self.fade_far_out_submobjects()

    def uv_func(self, u, v):
        p = self.radius * Sphere.uv_func(self, u, v)
        p = np.dot(p, self.rotation_matrix.T)
        p = stereo_project_point(p)
        epsilon = 1e-6
        if np.any(np.abs(p) == np.inf) or np.any(np.isnan(p)):
            return self.uv_func(u + epsilon, v + epsilon)
        return p

    def set_rotation_matrix(self, rotation_matrix=None):
        if rotation_matrix is None:
            rotation_matrix = np.identity(3)
        self.rotation_matrix = rotation_matrix

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
                submob.fade(1)
        return self

class SPSphere(Sphere):
    CONFIG = {
        "resolution": (101, 51),
        "radius": 1,
        "u_range": (0, TAU),
        "v_range": (0, PI),
    }

    # def __init__(self, rotation_matrix=None, **kwargs):
    #     digest_config(self, kwargs)
    #     if rotation_matrix is None:
    #         rotation_matrix = np.identity(3)
    #     self.rotation_matrix = rotation_matrix

    #     super().__init__(**kwargs)
    #     self.submobjects.sort(
    #         key=lambda m: -m.get_width()
    #     )

    def uv_func(self, u: float, v: float) -> np.ndarray:
        # return self.radius * np.array([
        #     fdiv(np.cos(u) * np.sin(v), 1 - np.cos(v)),
        #     fdiv(np.sin(u) * np.sin(v), 1 - np.cos(v)),
        #     0
        # ])
        p = self.radius * Sphere.uv_func(self, u, v)
        # p = np.dot(p, self.rotation_matrix.T)
        p = fdiv(p, 1 + p[2])
        p[2] = 0
        # epsilon = 1e-4
        # if np.any(np.abs(p) == np.inf) or np.any(np.isnan(p)):
        #     return self.uv_func(u + epsilon, v + epsilon)
        return p


class Kuri(Scene):
    CONFIG = {
        "camera_class": Camera,
        "resolution": (41, 21),
        "mesh_resolution": (41, 21),
    }

    def init_camera(self):
        frame = self.camera.frame
        frame.set_focal_distance(10)
        frame.set_width(10)
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
        sp2 = StereoProjectedSphere(
            resolution = self.resolution
            )
        return square, sphere, stereo_projected_sphere, sp2

    def init_axis(self):
        axis = ThreeDAxes(
            x_range = np.array([-20.0, 20.0, 1.0]),
            y_range = np.array([-20.0, 20.0, 1.0]),
            z_range = np.array([-20.0, 20.0, 1.0]),
            axis_config = {
                "include_tip": True,
            },
            )
        axis.add_coordinate_labels()
        return axis

    def construct(self):
        surfaces, frame, axis = self.init_surfaces(), self.init_camera(), self.init_axis()

        surfaces = [TexturedSurface(surface, "../assets/image/gun.png") for surface in surfaces]
        for mob in surfaces:
            mob.mesh = SurfaceMesh(mob, resolution=self.mesh_resolution, depth_test=False)
            mob.mesh.set_stroke(BLUE, 2, opacity=1)
            # mob.add(mob.mesh)

        sf, sp = surfaces[0], surfaces[1]

        
        
        frame.add_updater(lambda m, dt: m.increment_theta(-0.03 * dt))

        self.play(
            FadeIn(sf, run_time = 1),
            ShowCreation(axis, runtime=3),
            frame.animate.increment_phi(30 * DEGREES),
            runtime = 3
            )

        self.play(
            ShowCreation(sf.mesh, lag_ratio=0.01, run_time=3),
        )
        # self.add(sf, axis, sf.mesh)
        for mob in surfaces:
            mob.add(mob.mesh)

        for sur in surfaces[1:3]:
            self.play(
                Transform(sf, sur),
                run_time=5
            )
            self.wait(2)

        # coord_point_mobs = VGroup(
        #     Vector(RIGHT, color = RED),
        #     Vector(UP, color = GREEN),
        #     Vector(OUT, color = BLUE),
        # )
        coord_point_mobs = VGroup(
            VectorizedPoint(RIGHT),
            VectorizedPoint(UP),
            VectorizedPoint(OUT),
        )
        sp.add(coord_point_mobs)

        def get_rot_matrix():
            return np.array([pm.get_location() for pm in coord_point_mobs]).T
        def get_projected_sphere():
            result = StereoProjectedSphere(get_rot_matrix(), resolution = self.resolution, max_r=32)
            result = TexturedSurface(result, "../assets/image/gun.png")
            result.mesh = SurfaceMesh(result, resolution=self.mesh_resolution, depth_test=False)
            result.mesh.set_stroke(BLUE, 2, opacity=1)
            result.add(result.mesh)
            for submob in result:
                if submob.get_center()[1] < -11:
                    submob.fade(1)
            return result

        # self.add(sp)
        projected_sphere = get_projected_sphere()
        self.remove(sf)
        self.add(projected_sphere, axis)

        print(projected_sphere.data['im_coords'].shape)

        projected_sphere.add_updater(
            lambda m: m.match_points(get_projected_sphere()).set_submobjects(get_projected_sphere().submobjects)
        )
        sp.fade(1)
        for x in sp.submobjects:
            x.fade(1)
        vec = rotate_vector(Y_AXIS, -PI / 12, Z_AXIS)
        self.play(
            Rotate(sp, PI * 3 / 4, vec),
            run_time = 3
        )
        self.wait(2)
        self.play(
            Rotate(sp, TAU - PI * 3 / 4, vec),
            run_time = 5
        )
        self.wait(2)
        self.play(
            Rotate(sp, PI * 3 / 4, vec),
            run_time = 3
        )
        self.wait(2)
        self.play(
            Rotate(sp, -PI * 3 / 4, vec),
            run_time = 3
        )
        self.wait(2)
        # self.embed()

