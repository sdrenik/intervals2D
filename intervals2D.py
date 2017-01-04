
import scipy as sp

   
def borders(selected):
    """Returns pairs of lists of first and last element of ranges of consecutive integers in a list"""
    
    selected_sh = sp.zeros(len(selected), dtype=int)
    for i in range(1,len(selected)):
        selected_sh[i] = selected[i-1]
    selected_i = sp.zeros(len(selected), dtype=int)
    for i in range(1,len(selected_i)):
        selected_i[i] = i
    
    islands = selected_i[selected - selected_sh == 1]
     
    if len(islands) > 0:
        borders=[]
        borders.append([islands[0]])
        for i in range(1,len(islands)):
            if islands[i] > islands[i-1] + 1:
                borders[-1].append(islands[i-1])
                borders.append([islands[i]])
        borders[-1].append(islands[-1])
        
        i_borders = []
        for pair in borders:
            i_borders.append([selected[pair[0]],selected[pair[1]]])
    
        return i_borders
    else:
        return []
        
def islands(in_list, low, high=None):
    """Returns indexes of values between low and high (optional) borders. in_list must be scipy array"""
    if len(in_list)==0:
        return []
    if high == None:
        high = max(in_list)
    i_list = sp.zeros(len(in_list), dtype=int)
    for i in range (0,len(i_list)):
        i_list[i] = i
        
    selected = i_list[(in_list >= low) * (in_list <= high)]
    return borders(selected)

def islands_to_intervals(tcol,islands):
    """Translate index-written intervals into time-written intervals"""
    intervals = []
    for island in islands:
        intervals.append([tcol[island[0]],tcol[island[1]]])
    return intervals

def make_intervals(tcol, ycol, low, high=None):
    isl = islands(ycol, low, high)
    ivls = islands_to_intervals(tcol, isl)
    return ivls
#Below defined are functions for processing intervals
#Intervals are in the forms of lists [....,[t1,t2],....]
#Where t1 and t2 are the beginning and the end of an interval
    
def IntervalIntersection(t,q):
    """Returns cross section of intervals in t and q"""
    a = []
    for pair in t:
        t1 = pair[0]
        t2 = pair[1]
        
        for pair2 in q:
            q1 = pair2[0]
            q2 = pair2[1]
            
            if (q1 < t2) and (q2 > t1):
                a1 = max(q1,t1)
                a2 = min(q2,t2)
                a.append([a1,a2])
    return a

def IntervalCleanup(b):
    """ Combines adjacent and/or overlapping intervals"""
    if len(b) <= 1:
        return b
    a = []
    a1, a2 = b[0]
    remainder = b[1:]
    while len(remainder) > 0:
        removeme=[]
        for pair in remainder:       
            q1 = pair[0]
            q2 = pair[1]
            if (q1 <= a2) and (q2 >= a1):
                a1 = min(q1,a1)
                a2 = max(q2,a2)
                removeme.append(pair)
        for pair in removeme:
            remainder.remove(pair)
        a.append([a1,a2])
        if len(remainder) > 0:
            a1, a2 = remainder[0]
            remainder = remainder[1:]
    if [a1,a2]!=a[-1]:
        a.append([a1,a2])
    return a

def focus(x_list, y_list, area):
    #returns x and y columns where x is within defined area
    
    x_col = sp.array(x_list)
    y_col = sp.array(y_list)
    
    selection = (x_col >= area[0]) * (x_col <= area[1])
    
    return x_col[selection], y_col[selection]
    
def pin_point(input_list, sought_value):
    input_col = sp.array(input_list)
    temp_list = list(map(abs, input_col - sought_value))
    nearest_index = temp_list.index(min(temp_list))
    return nearest_index
