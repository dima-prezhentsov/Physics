import matplotlib.pyplot as plt
import pylab
import math


def func(r, q, u, r2, h):
    return q * u / (r * math.log1p((r2 / (r2 - h)) - 1))


def main():
    q = -1.6e-19
    m = 9.1e-31
    u = 0
    r1, r2 = 0, 0
    h = 0
    frequency = 100000
    config = [0.0001, 500, 200, 2000000, 1, 300]
    inp = open("config.txt", "r")
    tmp = inp.readline()
    if tmp != "":
        for i in range(6):
            config[i] = float(tmp)
            tmp = inp.readline()
    u = config[0]
    r2 = config[1]
    h = config[2]
    lenght = config[3]
    eps = config[4]
    velocity = config[5]

    r1 = r2 - h
    r = (r2 + r1) // 2
    velocityX = velocity
    velocityY = 0
    x = 0
    y = r - r1
    a_y = 0

    y_x = ([], [])
    y_t = ([], [])
    v_t = ([], [])
    a_t = ([], [])

    dt = 0
    while x <= lenght and r2 > r > r1:
        velocity_ = math.sqrt(velocityX ** 2 + velocityY ** 2)

        y_x[0].append(r)
        y_x[1].append(x)

        y_t[0].append(y)
        y_t[1].append(dt / frequency)

        v_t[0].append(velocity_)
        v_t[1].append(dt / frequency)

        a_t[0].append(a_y)
        a_t[1].append(dt / frequency)

        a_y = func(r, q, u, r2, h) / m
        velocityY += a_y / frequency
        r += velocityY / frequency

        x += velocityX / frequency
        y = r - r1

        dt += 1

    point_width = 0.5
    pylab.subplot(2, 2, 1)
    pylab.xlim(0, max(max(y_x[0]), max(y_x[1])))
    pylab.ylim(r1, r2)
    pylab.scatter(y_x[1], y_x[0], s=point_width)
    pylab.title('y(x)')

    pylab.subplot(2, 2, 2)
    pylab.scatter(y_t[1], y_t[0], s=point_width)
    pylab.title("y(t)")

    pylab.subplot(2, 2, 3)
    pylab.scatter(a_t[1], a_t[0], s=point_width)
    pylab.title("a(t)")

    pylab.subplot(2, 2, 4)
    pylab.scatter(v_t[1], v_t[0], s=point_width)
    pylab.title("v(t)")

    pylab.show()


if __name__ == '__main__':
    main()