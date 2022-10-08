import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

def dot_product(u, v):
    return sum([i*j for i, j in zip(u, v)])


def vector_norm(u):
    return sum([i*i for i in u])**0.5


def proj_v_on_u(u, v):
    c =  dot_product(u, v)/dot_product(u, u)
    return [c*i for i in u]

def vector_sub(u, v):
    return [i-j for i, j in zip(u, v)]





b_1 = 520
b_11 = 364
y = 1170
w_f = 10
w_b = 100
x_ = 529.5
y_ = 62

u = [3, 0]
v = [5, 4]

# uv = np.array([u, v])
# proj_v = proj_v_on_u(u, v)
# sub_v = vector_sub(v, proj_v)
# plt.quiver([0, 0], [0, 0], uv[:, 0], uv[:, 1], angles='xy', scale_units='xy', scale=1, color=["r","b"])
# plt.quiver([0], [0], proj_v[0], proj_v[1], angles='xy', scale_units='xy', scale=1, color="b")
# plt.quiver(proj_v[0], proj_v[1], sub_v[0], sub_v[1], angles='xy', scale_units='xy', scale=1, color="g")
# plt.xlim([-1, 10])
# plt.ylim([-1, 10])

# plt.show()


plt.plot(x_, y_, "o")
xy_ = [x_, y_]
k = (b_11 + w_b - w_f)/2/y

# w_b = w_b/2
# w_f = w_f/2

print(k)
x_eval = np.linspace(0, y, 100)
y_eval_1 = w_f/2 + k*x_eval
y_eval_2 = -w_f/2 - k*x_eval
plt.plot(x_eval, y_eval_1, "r")
plt.plot(x_eval, y_eval_2, "r")
xy_1 = [x_eval[-1]-x_eval[0], y_eval_1[-1]-y_eval_1[0]]
xy_2 = [x_eval[-1]-x_eval[0], y_eval_2[-1]-y_eval_2[0]]

proj_1 = proj_v_on_u(xy_1, [x_, y_-w_f/2])
proj_2 = proj_v_on_u(xy_2, [x_, y_+w_f/2])

sub_1 = vector_sub(proj_1, [x_, y_-w_f/2])
sub_2 = vector_sub(proj_2, [x_, y_+w_f/2])

print(sum([i**2 for i in sub_1])**0.5)
print(sum([i**2 for i in sub_2])**0.5)




plt.quiver(x_, y_, sub_1[0], sub_1[1], angles="xy", scale_units="xy", scale=1)
plt.quiver(x_, y_, sub_2[0], sub_2[1], angles="xy", scale_units="xy", scale=1)

plt.xlim([0, y])
plt.show()