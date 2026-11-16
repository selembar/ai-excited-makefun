import math
import random

W = H = 768
random.seed(73)
p = bytearray(W * H * 3)
for y in range(H):
    for x in range(W):
        r = math.hypot(x - W / 2, y - H / 2)
        glow = max(0, 1 - r / 520)
        i = (y * W + x) * 3
        p[i:i + 3] = bytes((int(4 + 12 * glow), int(7 + 8 * glow), int(20 + 45 * glow)))

def dot(x, y, col, radius=2):
    for yy in range(max(0, int(y - radius - 1)), min(H, int(y + radius + 2))):
        for xx in range(max(0, int(x - radius - 1)), min(W, int(x + radius + 2))):
            d = math.hypot(xx - x, yy - y)
            if d < radius:
                a = min(1, (radius - d) * 1.5)
                q = (yy * W + xx) * 3
                for k in range(3):
                    p[q + k] = min(255, int(p[q + k] * (1 - a) + col[k] * a))

def line(x0, y0, x1, y1, col, radius=1):
    n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for j in range(n):
        t = j / max(1, n - 1)
        dot(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, col, radius)

for j in range(2400):
    a = j / 2400 * math.tau
    rad = 235 + 6 * math.sin(7 * a) + 3 * math.sin(19 * a)
    hue = (math.sin(a * 2) + 1) / 2
    col = (int(60 + 60 * hue), int(210 - 50 * hue), 255) if math.sin(a * 5) > 0 else (255, int(40 + 70 * hue), int(160 + 70 * hue))
    dot(W / 2 + rad * math.cos(a), H / 2 + rad * math.sin(a), col, 4.5 if j % 4 == 0 else 2.8)

for _ in range(104):
    a = random.random() * math.tau
    inner, outer = random.uniform(95, 190), random.uniform(280, 530)
    x0, y0 = W / 2 + inner * math.cos(a), H / 2 + inner * math.sin(a)
    x1 = W / 2 + outer * math.cos(a + random.uniform(-.10, .10))
    y1 = H / 2 + outer * math.sin(a + random.uniform(-.10, .10))
    line(x0, y0, x1, y1, random.choice([(30, 220, 255), (255, 45, 170), (130, 90, 255), (255, 205, 75), (235, 250, 255)]), random.uniform(.7, 2.4))

for k in range(12):
    a = k * math.tau / 12 + .12
    pts = [(W / 2 + r * math.cos(t), H / 2 + r * math.sin(t)) for r, t in [(180, a), (265, a + .12), (297, a + .19)]]
    col = (255, 55, 183) if k % 2 else (42, 232, 255)
    line(*pts[0], *pts[1], col, 3)
    line(*pts[1], *pts[2], col, 1.7)

for radius, col in [(82, (25, 65, 180)), (62, (30, 170, 255)), (43, (245, 38, 165)), (28, (255, 145, 55)), (17, (255, 245, 215)), (8, (255, 255, 255))]:
    for y in range(int(H / 2 - radius - 1), int(H / 2 + radius + 2)):
        for x in range(int(W / 2 - radius - 1), int(W / 2 + radius + 2)):
            if math.hypot(x - W / 2, y - H / 2) < radius:
                q = (y * W + x) * 3
                for k in range(3):
                    p[q + k] = int(p[q + k] * .28 + col[k] * .72)
for j in range(12):
    a = j * math.tau / 12
    line(W / 2 + 20 * math.cos(a), H / 2 + 20 * math.sin(a), W / 2 + 82 * math.cos(a), H / 2 + 82 * math.sin(a), (255, 246, 225), 1.5)
for _ in range(1900):
    a, r = random.random() * math.tau, random.uniform(90, 360)
    dot(W / 2 + r * math.cos(a), H / 2 + r * math.sin(a), random.choice([(90, 230, 255), (255, 110, 200), (250, 240, 210)]), random.choice([.7, 1, 1.4]))
with open('assets/rift.ppm', 'wb') as f:
    f.write(f'P6\n{W} {H}\n255\n'.encode())
    f.write(p)
