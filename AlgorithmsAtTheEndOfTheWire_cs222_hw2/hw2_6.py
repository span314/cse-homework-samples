#!/usr/bin/python
#Shawn Pan
#CS222 HW2

def encode(text, intervals):
  n = len(text)
  window_start = 0.0
  window_end = 1.0
  for i in xrange(n):
    interval_start, interval_end = intervals[text[i]]
    new_start = window_start + (window_end - window_start) * interval_start
    new_end = window_start + (window_end - window_start) * interval_end
    window_start = new_start
    window_end = new_end
    print (window_start, window_end, i + 1)

def decode(code, n, intervals):
  result = []
  for i in xrange(n):
    for (char, (start, end)) in intervals.iteritems():
      if code >= start and code < end:
        result.append(char)
        code = (code - start) / (end - start)
        break
    print "".join(result), code #print result and rescaled code

intervals = {"a": (0.0, 0.2), "b": (0.2, 0.5), "c": (0.5, 1.0)}

print "Encode"
encode("aacbca", intervals)

print "Decode"
decode(0.63215699, 10, intervals)

#sanity check
#encode("cbbabacbbc", intervals)