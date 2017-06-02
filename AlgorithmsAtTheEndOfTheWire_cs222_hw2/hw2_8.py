#!/usr/bin/python
#Shawn Pan
#CS222 HW2
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(precision=2, linewidth=150, suppress=True)

block = np.array([
  [124 ,125 ,122 ,120 ,122 ,119 ,117 ,118],
  [120 ,120 ,120 ,119 ,119 ,120 ,120 ,120],
  [125 ,124 ,123 ,122 ,121 ,120 ,119 ,118],
  [125 ,124 ,123 ,122 ,121 ,120 ,119 ,118],
  [130 ,131 ,132 ,133 ,134 ,130 ,126 ,122],
  [140 ,137 ,137 ,133 ,133 ,137 ,135 ,130],
  [150 ,147 ,150 ,150 ,150 ,150 ,150 ,150],
  [160 ,160 ,162 ,164 ,168 ,170 ,172 ,175]
])

quant = np.array([
  [16 ,11 ,10 ,16 ,24 ,40 ,51 ,61],
  [12 ,12 ,14 ,19 ,26 ,58 ,60 ,55],
  [14 ,13 ,16 ,24 ,40 ,57 ,69 ,56],
  [14 ,17 ,22 ,29 ,51 ,87 ,80 ,62],
  [18 ,22 ,37 ,56 ,68 ,109 ,103 ,77],
  [24 ,35 ,55 ,64 ,81 ,104 ,113 ,92],
  [49 ,64 ,78 ,87 ,103 ,121 ,120 ,101],
  [72 ,92 ,95 ,98 ,112 ,100 ,103 ,99]
])

#wikipedia example
wikiblock = np.array([
  [52, 55, 61, 66, 70, 61, 64, 73],
  [63, 59, 55, 90, 109, 85, 69, 72],
  [62, 59, 68, 113, 144, 104, 66, 73],
  [63, 58, 71, 122, 154, 106, 70, 69],
  [67, 61, 68, 104, 126, 88, 68, 70],
  [79, 65, 60, 70, 77, 68, 58, 75],
  [85, 71, 64, 59, 55, 61, 65, 83],
  [87, 79, 69, 68, 65, 76, 78, 94]
])


translate = block - 128

#discrete cosine transform of 8x8 block
def dct(g):
  result = np.empty((8, 8))
  for u in xrange(8):
    for v in xrange(8):
      total = 0
      for x in xrange(8):
        for y in xrange(8):
          total += g[x, y] * np.cos((2 * x + 1) * u * np.pi / 16) * np.cos((2 * y + 1) * v * np.pi / 16)
      scale = 0.25
      if u == 0:
        scale *= 1 / np.sqrt(2)
      if v == 0:
        scale *= 1 / np.sqrt(2)
      result[u, v] = scale * total
  return result

def compress(block, quant):
  print "Compress"

  t = block - 128
  print "Shift by 128"
  print t
  print

  g = dct(t)
  print "DCT"
  print g
  print

  q = np.round(g / quant).astype(np.int)
  print "Quantized"
  print q
  print

  return q


def idct(f):
  result = np.empty((8, 8))
  for x in xrange(8):
    for y in xrange(8):
      total = 0
      for u in xrange(8):
        for v in xrange(8):
          scale = 0.25
          if u == 0:
            scale *= 1 / np.sqrt(2)
          if v == 0:
            scale *= 1 / np.sqrt(2)
          total += scale * f[u, v] * np.cos((2 * x + 1) * u * np.pi / 16) * np.cos((2 * y + 1) * v * np.pi / 16)
      result[x, y] = total
  return result

def decompress(block, quant):
  print "Decompress"

  f = block * quant
  print "Unquantized"
  print f
  print

  t = np.round(idct(f)).astype(np.int)
  print "IDCT"
  print t
  print

  s = t + 128
  print "Shift by 128"
  print s
  print

  return s


def test_block(block, quant):
  compressed = decompress(compress(block, quant), quant)
  plt.figure(figsize=(10, 5))
  # plt.subplot(221)
  # plt.title("Original (Range from Min to Max)")
  # plt.imshow(block, cmap="Greys_r", interpolation="none")
  plt.subplot(121)
  plt.title("Original")
  plt.imshow(block, cmap="Greys_r", interpolation="none", vmin=0, vmax=255)
  # plt.subplot(223)
  # plt.title("Compressed and Decompressed")
  # plt.imshow(compressed, cmap="Greys_r", interpolation="none")
  plt.subplot(122)
  plt.title("Compressed and Decompressed")
  plt.imshow(compressed, cmap="Greys_r", interpolation="none", vmin=0, vmax=255)
  #plt.show()
  plt.savefig("jpegtest.png")

#test_block(wikiblock, quant)
test_block(block, quant)