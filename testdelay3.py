import matplotlib.pyplot as plt
import numpy as np

def delay3(val, dt, ts):
    dl = dt / 3
    n = len(val)
    I1 = [val[0] * dl] * (n+1)
    I2 = [val[0] * dl] * (n+1)
    I3 = [val[0] * dl] * (n+1)
    for i, vali in enumerate(val):
        RT3 = I3[i] / dl
        I3[i + 1] = I3[i] + (vali - I3[i]) * ts
        RT2 = I2[i] / dl
        I2[i + 1] = I2[i] + (RT3 - I2[i]) * ts
        I1[i + 1] = I1[i] + (RT2 - I1[i]) * ts
    return np.array(I1) / dl

def delay3V(val, dt, ts):
    DL = dt / 3
    n = len(val)
    LV3 = [DL*val[0]] * (n+1)
    LV2 = [DL*val[0]] * (n+1)
    LV1 = [DL*val[0]] * (n+1)
    for i, vali in enumerate(val):
        RT1 = LV1[i] / DL
        LV1[i + 1] = LV1[i] + (vali - RT1) * ts
        RT2 = LV2[i] / DL
        LV2[i + 1] = LV2[i] + (RT1 - RT2) * ts
        LV3[i + 1] = LV3[i] + (RT2 - LV3[i] / DL) * ts
    return np.array(LV3) / DL

def smooth(val, dt, ts):
    n = len(val)
    Y = [val[0]] * (n+1)
    for i, vali in enumerate(val):
        Y[i+1] = Y[i] + (vali - Y[i]) * ts / dt
    return np.array(Y)

def smooth3(val, dt, ts):
    n = len(val)
    Y = [val[0]] * (n+1)
    I1 = [val[0]] * (n+1)
    I2 = [val[0]] * (n + 1)
    dl = dt / 3
    for i, vali in enumerate(val):
        Y[i+1] = Y[i] + (I1[i] - Y[i]) * ts / dl
        I1[i+1] = I1[i] + (I2[i] - I1[i]) * ts / dl
        I2[i+1] = I2[i] + (vali - I2[i]) * ts / dl
    return np.array(Y)

def smooth3V(val, dt, ts):
    d = delay3V(val, dt, ts)
    n = len(val)
    Y = [val[0]] * (n + 1)
    for i, vali in enumerate(val):
        Y[i + 1] = Y[i] + d[i] * ts
    return np.array(Y)

def display():
    n = 200
    t = [i for i in range(n)]
    #val = [0] * (n//2) + [1] * (n//2)
    val = [0, 0, 1, 1] * (n//4)
    dt = 20
    ts = 1
    y1 = delay3V(val, dt, ts)
    y2 = smooth(val, dt, ts)
    y3 = smooth3V(val, dt, ts)
    plt.plot(t, val)
    plt.plot(t, y1[1:], label="Delay3")
    plt.plot(t, y2[1:], label="Smooth")
    plt.plot(t, y3[1:], label="Smooth3")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    display()