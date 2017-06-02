#!/usr/bin/python
#Shawn Pan
#CS222 HW2

def lz77(data, window_size, buffer_size):
  i = 0
  result = []
  while i < len(data):
    window_start = max(0, i - window_size)
    buffer_end = min(i + buffer_size, len(data))
    offset = 0
    length = 0
    next = data[i]
    #find match (for loop for simplicity: there are better substring matching algorithms)
    for j in xrange(i - 1, window_start - 1, -1):
    #for j in xrange(window_start, i):
      match_length = 0
      while i + match_length < buffer_end and data[j + match_length] == data[i + match_length]:
        match_length = match_length + 1
      if match_length > length:
        length = match_length
        offset = i - j
        if i + match_length < len(data):
          next = data[i + match_length]
        else:
          next = None
    result.append((offset, length, next))
    i = i + length + 1
  return result

def lz78(data):
  next_index = 1
  dictionary = {"": 0}
  result = []
  i = 0
  while i < len(data):
    end = i
    #find longest match
    while end + 1 <= len(data) and data[i:end+1] in dictionary:
      end += 1
    match_index = dictionary[data[i:end]]
    next_char = None
    if end < len(data):
      #add to dictionary
      dictionary[data[i:end+1]] = next_index
      next_index += 1
      next_char = data[end]
    pair = (match_index, next_char)
    result.append(pair)
    # print pair
    # print dictionary
    # print
    i = end + 1
  return result

def lzw(data):
  next_index = 0
  dictionary = {}
  #add all characters
  for c in sorted(set(data)):
    dictionary[c] = next_index
    next_index += 1
  result = []
  i = 0
  while i < len(data):
    end = i
    #find longest match
    while end + 1 <= len(data) and data[i:end+1] in dictionary:
      end += 1
    match_index = dictionary[data[i:end]]
    if end < len(data):
      #add to dictionary
      dictionary[data[i:end+1]] = next_index
      next_index += 1
    #print dictionary
    #print match_index
    result.append((match_index))
    i = end
  return result


data = "abracadabraarbadacarba"
print "LZ77"
result = lz77(data, 6, 6)
for r in result:
  print r
print

print "LZ78"
result = lz78(data)
for r in result:
  print r
print

print "LZW"
print lzw(data)


#wikipedia examples
#print lz77("aacaacabcabaaac", 12, 9)
#print
#print lzw("TOBEORNOTTOBEORTOBEORNOT#ABCDEFGHIJKLMNOPQRSTUVWXYZ")