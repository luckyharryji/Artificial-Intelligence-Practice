'''
Name: Xiangyu Ji
NetID: XJQ158
'''

def binarySearch(L, v):
    cut_time = 0
    if v == None:
        return (False, cut_time)
    length_of_list = len(L)
    if length_of_list == 0:
        return (False, cut_time)
    elif length_of_list == 1:
        return (L[0] == v, cut_time)
    else:
        top = 0
        tail = length_of_list - 1
        while top <= tail:
            mid = (top + tail) / 2
            if L[mid] == v:
                return (True, cut_time)
            elif L[mid] < v:
                top = mid + 1
                cut_time += 1
            else:
                tail = mid - 1
                cut_time += 1
        return (False, cut_time)

L = [0,4,6,12,13,25,27]
print "binarySearch test case #1: " + str(binarySearch(L,-1) == (False,3))
print "binarySearch test case #2: " + str(binarySearch(L,12) == (True,0))
print "binarySearch test case #3: " + str(binarySearch(L,25) == (True,1))
