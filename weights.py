import math
    
def InHypOWA(v,n):
    weight_list = []
    deno = math.comb(v+n-1,n-1)
    for i in range (n,0,-1):
        weight_list.append(math.comb(v+i-2,i-1)/deno)       
    # print(weight_list)
    return weight_list