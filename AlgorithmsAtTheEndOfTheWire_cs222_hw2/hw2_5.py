#!/usr/bin/python
#Shawn Pan
#CS222 HW2

#generate all cyclic shifts
s = "wabbawabbawoo|"
n = len(s)
ss = s + s
shifts = [ss[i:i+n] for i in range(n)]
print "Shifts"
print "\n".join(shifts)

print "Sorted Shifts"
shifts.sort()
print "\n".join(shifts)

print "Last Column"
last = [s[-1] for s in shifts]
print "".join(last)
print last.index("|")

print "First Column"
first = [s[0] for s in shifts]
print "".join(first)

#move-to-front encode
alphabet = list(set(c for c in s))
alphabet.sort()

output = []
for c in last:
  i = alphabet.index(c)
  output.append(i)
  print alphabet, output
  #shift down
  while i:
    alphabet[i] = alphabet[i-1]
    i -= 1
  alphabet[0] = c


#print pairs of last, first
print "Pairs"
for l, f in zip(last, first):
  print l + f