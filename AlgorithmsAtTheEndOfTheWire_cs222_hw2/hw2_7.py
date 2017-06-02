#!/usr/bin/python
#Shawn Pan
#CS222 HW2
from collections import OrderedDict

#apply sequitur algorithm and print out steps
#note this is not a efficient (linear) implmentation - in each step it alternates applying
#digram uniqueness and rule utility constraints as many times as possible in a brute force manner
#as mentioned in the paper, multiple valid solutions satisfying the two constraints
#are possible for some inputs and this will only return one of them
#only allows up to rule R
def sequitur(text):
  rule_label_cnt = ord("A")
  rules = OrderedDict({"S": ""})
  for char in text:
    #add new character
    rules["S"] = rules["S"] + char
    print_step("Add character", char, rules)

    check_rules = True #flag to check rules again if any actually gets applied
    while check_rules:
      check_rules = False

      #enforce digram uniqueness
      duplicate_digram = find_duplicate_digram(rules)
      if duplicate_digram:
        check_rules = True
        #attempt to find existing rule
        new_label = None
        for label, rule in rules.iteritems():
          if rule == duplicate_digram:
            new_label = label
            break
        #create new rule
        if not new_label:
          new_label = chr(rule_label_cnt)
          rule_label_cnt += 1
        #apply rule
        for label, rule in rules.iteritems():
          rules[label] = rule.replace(duplicate_digram, new_label)
        rules[new_label] = duplicate_digram
        print_step("Enforce digram uniqueness for", duplicate_digram, rules)
        duplicate_digram = find_duplicate_digram(rules)

      #enforce rule utility
      unused_rule = find_unused_rule(rules)
      if unused_rule:
        check_rules = True
        #delete unused rule
        for label, rule in rules.iteritems():
          rules[label] = rule.replace(unused_rule, rules[unused_rule])
        del rules[unused_rule]
        print_step("Enforce rule utility for", unused_rule, rules)
        unused_rule = find_unused_rule(rules)

  return rules

#find digram occuring more than once
def find_duplicate_digram(rules):
  digrams = set()
  for rule in rules.values():
    for i in xrange(len(rule)-1):
      digram = rule[i:i+2]
      if digram in digrams:
        return digram
      else:
        digrams.add(digram)
  return None

#find label of rule occuring less than 2 times
def find_unused_rule(rules):
  used_chars = ""
  for rule in rules.values():
    used_chars += rule
  for label in rules.keys():
    if label != "S" and used_chars.count(label) < 2:
      return label
  return None

#print step
def print_step(action, obj, rules):
  print action, obj
  print ", ".join([label + ": " + rule for label, rule in rules.iteritems()])


sequitur("aactgaacatgagagacatagagacag")
print
sequitur("aactgaacatgagagacatagagacag"[::-1])

#example in paper
#sequitur("abcdbcabcd")