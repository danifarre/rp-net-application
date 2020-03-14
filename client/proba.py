import sys, select

i = []

while i == []:
    print ("You have ten seconds to answer!")

    i, o, e = select.select( [sys.stdin], [], [], 0.1 )


    if (i):
      print ("You said", sys.stdin.readline().strip())
    else:
      print ("You said nothing!")