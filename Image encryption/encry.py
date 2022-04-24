from PIL import Image
import tkinter as tk
from tkinter import filedialog
import hashlib
import binascii
import textwrap
import cv2
import numpy as np
from scipy.integrate import odeint

from bisect import bisect_left as bsearch

''' 
GLOBAL Constants
'''
# Lorenz paramters and initial conditions
a, b, c = 10, 2.667, 28
x0, y0, z0 = 0, 0, 0

# DNA-Encoding RULE #1 A = 00, T=01, G=10, C=11
dna = {}
dna["00"] = "A"
dna["01"] = "C"
dna["10"] = "G"
dna["11"] = "T"
dna["A"] = [0, 0]
dna["T"] = [1, 1]
dna["G"] = [1, 0]
dna["C"] = [0, 1]
# DNA xor
dna["AA"] = dna["TT"] = dna["CC"] = dna["GG"] = "A"
dna["AG"] = dna["GA"] = dna["TC"] = dna["CT"] = "G"
dna["AC"] = dna["CA"] = dna["GT"] = dna["TG"] = "C"
dna["AT"] = dna["CG"] = dna["TA"] = dna["GC"] = "T"
# Maximum time point and total number of time points
tmax, N = 100, 10000


def lorenz(X, t, a, b, c):
    x, y, z = X
    x_dot = -a * (x - y)
    y_dot = c * x - y - x * z
    z_dot = -b * z + x * y
    return x_dot, y_dot, z_dot


def image_selector():  # returns path to selected image
    path = "NULL"
    root = tk.Tk()
    # we don't want a full GUI, so keep the root window from appearing
    root.withdraw()
    # show an "Open" dialog box and return the path to the selected file
    path = filedialog.askopenfilename()
    if path != "NULL":
        print("Image loaded!")
    else:
        print("Error Image not loaded!")
    return path


def split_into_rgb_channels(image):
    red = image[:, :, 2]
    green = image[:, :, 1]
    blue = image[:, :, 0]
    return red, green, blue


# Secure key generation


def securekey(iname):
    img = Image.open(iname)
    m, n = img.size
    print("pixels: {0}  width: {2} height: {1} ".format(m * n, m, n))
    pix = img.load()
    plainimage = list()  # _plainimage contains all the rgb values continuously
    for y in range(n):
        for x in range(m):
            for k in range(0, 3):
                plainimage.append(pix[x, y][k])
    # print("plainImage...")
    # print(plainimage);
    key = hashlib.sha256()
    # key is made a hash.sha256 object
    # print(key)
    key.update(bytearray(plainimage))


    return key.hexdigest(), m, n


def update_lorentz(key):
    key_bin = bin(int(key, 16))[2:].zfill(
        256)  # covert hex key digest to binary
    # print("binary key...")
    # print(key);
    # print(key_bin);
    k = {}  # key dictionary
    key_32_parts = textwrap.wrap(key_bin, 8)  # slicing key into 8 parts
    num = 1
    print("update_lorentz", key_32_parts);
    for i in key_32_parts:
        k["k{0}".format(num)] = i
        num = num + 1
    print("update_lorentz", k);
    t1 = t2 = t3 = 0
    for i in range(1, 12):
        t1 = t1 ^ int(k["k{0}".format(i)], 2)
    for i in range(12, 23):
        t2 = t2 ^ int(k["k{0}".format(i)], 2)
    for i in range(23, 33):
        t3 = t3 ^ int(k["k{0}".format(i)], 2)
    global x0, y0, z0
    x0 = x0 + t1 / 256
    y0 = y0 + t2 / 256
    z0 = z0 + t3 / 256


def decompose_matrix(iname):
    image = cv2.imread(iname)
    # print(image);
    blue, green, red = split_into_rgb_channels(image)
    # print(type(blue));
    for values, channel in zip((red, green, blue), (2, 1, 0)):
        img = np.zeros((values.shape[0], values.shape[1]), dtype=np.uint8)
        # print(values);
        img[:, :] = (values)
        if channel == 0:
            B = np.asmatrix(img)
        elif channel == 1:
            G = np.asmatrix(img)
        else:
            R = np.asmatrix(img)
    # print(type(B));
    return B, G, R


def dna_encode(b, g, r):
    b = np.unpackbits(b, axis=1)
    # print(b, b.shape)
    g = np.unpackbits(g, axis=1)
    r = np.unpackbits(r, axis=1)
    m, n = b.shape
    r_enc = np.chararray((m, int(n / 2)))
    g_enc = np.chararray((m, int(n / 2)))
    b_enc = np.chararray((m, int(n / 2)))
    # print(r_enc[0]);
    for color, enc in zip((b, g, r), (b_enc, g_enc, r_enc)):
        # print("X");
        idx = 0
        for j in range(0, m):
            for i in range(0, n, 2):
                enc[j, idx] = dna["{0}{1}".format(color[j, i], color[j, i + 1])]
                # print(color[j,i])
                # print(type(enc),enc);
                idx += 1
                if (i == n - 2):
                    idx = 0
                    break
    # print(b_enc)
    b_enc = b_enc.astype(str)
    # print(b_enc,b_enc.shape);
    g_enc = g_enc.astype(str)
    r_enc = r_enc.astype(str)
    return b_enc, g_enc, r_enc


def key_matrix_encode(key, b):
    # encoded key matrix
    b = np.unpackbits(b, axis=1)
    m, n = b.shape
    key_bin = bin(int(key, 16))[2:].zfill(256)
    # print(key_bin,key)
    Mk = np.zeros((m, n), dtype=np.uint8)
    x = 0
    for j in range(0, m):
        for i in range(0, n):
            Mk[j, i] = key_bin[x % 256]
            x += 1
    # print(Mk)
    Mk_enc = np.chararray((m, int(n / 2)))
    idx = 0
    for j in range(0, m):
        for i in range(0, n, 2):
            if idx == (n / 2):
                idx = 0
            Mk_enc[j, idx] = dna["{0}{1}".format(Mk[j, i], Mk[j, i + 1])]
            idx += 1
    Mk_enc = Mk_enc.astype(str)
    return Mk_enc


def xor_operation_new(b, g, r, mk):
    m, n = b.shape
    bx = np.chararray((m, n))
    gx = np.chararray((m, n))
    rx = np.chararray((m, n))
    b = b.astype(str)
    g = g.astype(str)
    r = r.astype(str)
    for i in range(0, m):
        for j in range(0, n):
            bx[i, j] = dna["{0}{1}".format(b[i, j], mk[i, j])]
            gx[i, j] = dna["{0}{1}".format(g[i, j], mk[i, j])]
            rx[i, j] = dna["{0}{1}".format(r[i, j], mk[i, j])]

    bx = bx.astype(str)
    gx = gx.astype(str)
    rx = rx.astype(str)
    return bx, gx, rx



def xor_operation(b, g, r, mk):
    m, n = b.shape
    bx = np.chararray((m, n))
    gx = np.chararray((m, n))
    rx = np.chararray((m, n))
    b = b.astype(str)
    g = g.astype(str)
    r = r.astype(str)
    for i in range(0, m):
        for j in range(0, n):
            bx[i, j] = dna["{0}{1}".format(b[i, j], mk[i, j])]
            gx[i, j] = dna["{0}{1}".format(g[i, j], mk[i, j])]
            rx[i, j] = dna["{0}{1}".format(r[i, j], mk[i, j])]

    bx = bx.astype(str)
    # print(bx)
    gx = gx.astype(str)
    rx = rx.astype(str)
    return bx, gx, rx


def gen_chaos_seq(m, n):
    global x0, y0, z0, a, b, c, N
    N = m * n * 4  # doubt
    x = np.array((m, n * 4))
    y = np.array((m, n * 4))
    z = np.array((m, n * 4))

    t = np.linspace(0, tmax, N)
    f = odeint(lorenz, (x0, y0, z0), t, args=(a, b, c))
    x, y, z = f.T
    print(x);
    x = x[:(N)]
    y = y[:(N)]
    z = z[:(N)]
    return x, y, z




def sequence_indexing(x, y, z):
    # print("seq",x);
    n = len(x)
    fx = np.zeros((n), dtype=np.uint32)
    fy = np.zeros((n), dtype=np.uint32)
    fz = np.zeros((n), dtype=np.uint32)
    seq = sorted(x)
    # print("seq",seq);

    for k1 in range(0, n):
        t = x[k1]
        k2 = bsearch(seq, t)
        # print(k2,k1)
        fx[k1] = k2
    seq = sorted(y)
    for k1 in range(0, n):
        t = y[k1]
        k2 = bsearch(seq, t)
        fy[k1] = k2
    seq = sorted(z)
    for k1 in range(0, n):
        t = z[k1]
        k2 = bsearch(seq, t)
        fz[k1] = k2
    return fx, fy, fz




def scramble(fx, fy, fz, b, r, g):
    p, q = b.shape
    size = p*q
    bx = b.reshape(size).astype(str)
    gx = g.reshape(size).astype(str)
    rx = r.reshape(size).astype(str)
    bx_s = np.chararray((size))
    gx_s = np.chararray((size))
    rx_s = np.chararray((size))

    for i in range(size):
        idx = fz[i]
        bx_s[i] = bx[idx]
    for i in range(size):
        idx = fy[i]
        gx_s[i] = gx[idx]
    for i in range(size):
        idx = fx[i]
        rx_s[i] = rx[idx]
    bx_s = bx_s.astype(str)
    gx_s = gx_s.astype(str)
    rx_s = rx_s.astype(str)

    b_s = np.chararray((p, q))
    g_s = np.chararray((p, q))
    r_s = np.chararray((p, q))

    b_s = bx_s.reshape(p, q)
    g_s = gx_s.reshape(p, q)
    r_s = rx_s.reshape(p, q)
    return b_s, g_s, r_s



def scramble_new(fx, fy, fz, b, g, r):
    p, q = b.shape
    size = p * q
    bx = b.reshape(size)
    gx = g.reshape(size)
    rx = r.reshape(size)

    bx_s = b.reshape(size)
    gx_s = g.reshape(size)
    rx_s = r.reshape(size)

    bx = bx.astype(str)
    gx = gx.astype(str)
    rx = rx.astype(str)
    bx_s = bx_s.astype(str)
    gx_s = gx_s.astype(str)
    rx_s = rx_s.astype(str)

    for i in range(size):
        idx = fz[i]
        bx_s[idx] = bx[i]
    for i in range(size):
        idx = fy[i]
        gx_s[idx] = gx[i]
    for i in range(size):
        idx = fx[i]
        rx_s[idx] = rx[i]

    b_s = np.chararray((p, q))
    g_s = np.chararray((p, q))
    r_s = np.chararray((p, q))

    b_s = bx_s.reshape(p, q)
    g_s = gx_s.reshape(p, q)
    r_s = rx_s.reshape(p, q)

    return b_s, g_s, r_s


def dna_decode(b, g, r):
    m, n = b.shape
    r_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    g_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    b_dec = np.ndarray((m, int(n * 2)), dtype=np.uint8)
    for color, dec in zip((b, g, r), (b_dec, g_dec, r_dec)):
        for j in range(0, m):
            for i in range(0, n):
                dec[j, 2 * i] = dna["{0}".format(color[j, i])][0]
                dec[j, 2 * i + 1] = dna["{0}".format(color[j, i])][1]
    b_dec = (np.packbits(b_dec, axis=-1))
    g_dec = (np.packbits(g_dec, axis=-1))
    r_dec = (np.packbits(r_dec, axis=-1))
    return b_dec, g_dec, r_dec

def decrypt(image, fx, fy, fz, fp, Mk, bt, gt, rt):
    r, g, b = split_into_rgb_channels(image)
    p, q = rt.shape
    benc, genc, renc = dna_encode(b, g, r)
    bs, gs, rs = scramble_new(fx, fy, fz, benc, genc, renc)
    bx, rx, gx = xor_operation_new(bs, gs, rs, Mk)
    blue, green, red = dna_decode(bx, gx, rx)
    green, red = red, green
    img = np.zeros((p, q, 3), dtype=np.uint8)
    img[:, :, 0] = red
    img[:, :, 1] = green
    img[:, :, 2] = blue
    cv2.imwrite(("Recovered.jpg"), img)





def recover_image(b, g, r, iname):
    img = cv2.imread(iname)
    img[:, :, 2] = r
    img[:, :, 1] = g
    img[:, :, 0] = b
    cv2.imwrite(("enc.jpg"), img)
    print("saved ecrypted image as enc.jpg")
    return img





if (__name__ == "__main__"):
    file_path = image_selector()
    print(file_path)
    key, m, n = securekey(file_path)  # generate key using image pixels by converting it into 1d array with byte values
    update_lorentz(key)  # calculate xo,yo,zo of chaotic equation using key with the help of secret computations
    blue, green, red = decompose_matrix(
        file_path)  # decompose image 3d matrix into seperate red, green and blue numpy 2d arrays
    blue_e, green_e, red_e = dna_encode(blue, green, red)  # dna encode the byte values of blue, green, red matrix
    Mk_e = key_matrix_encode(key,blue)  # convert key into binary format and into into 2d array and then dna encoding the key 2d array
    blue_final, green_final, red_final = xor_operation(blue_e, green_e, red_e,
    Mk_e)  # perform xor operation of key encoded matrix with all encoded red, green, blue 2d matrix
    x, y, z = gen_chaos_seq(m, n)  # gen arrays of x, y, z with random numbers using lorenz 3d lorenz equation
    fx, fy, fz = sequence_indexing(x, y, z)  # map x,y,z random array to sorted x,y,z arrays and generate x,y,z mapped index value array
    blue_scrambled, green_scrambled, red_scrambled = scramble(fx, fy, fz, blue_final, red_final,
    green_final)  # shuffle the values of blue, green, red using mapped index value arrays
    b, g, r = dna_decode(blue_scrambled, green_scrambled,red_scrambled)  # decode red, green blue matrix back to byte values
    img = recover_image(b, g, r, file_path)


    print("decrypting...")
    decrypt(img, fx, fy, fz, file_path, Mk_e, blue, green, red)


