'''
Bubble sort for Object Detect by x-axis
'''

#Bubble Sort (Sort For NAME by X-AXIS)
def bubble_sort2(x_list,name_list):
    for t in range(len(x_list)-1):
        for j in range(0, len(x_list)-1):
            x_tmp = x_list[j]
            y_tmp = name_list[j]
            if x_list[j] > x_list[j+1]:
                #x-axis sort
                x_list[j] = x_list[j+1]
                x_list[j+1] =x_tmp
                #name sort
                name_list[j]=name_list[j+1]
                name_list[j+1]=y_tmp
    return x_list,name_list

#Bubble Sort (Sort For [x,y,h,w] by X-AXIS)
def bubble_sort4(x,y,h,w):
    for t in range(len(x)-1):
        for j in range(0, len(x)-1):
            x_tmp = x[j]
            y_tmp = y[j]
            h_tmp = h[j]
            w_tmp = w[j]
            if x[j] > x[j+1]:
                #x sort
                x[j] = x[j+1]
                x[j+1] =x_tmp
                #y sort
                y[j]=y[j+1]
                y[j+1]=y_tmp
                #h sort
                h[j]=h[j+1]
                h[j+1]=h_tmp
                #w sort
                w[j]=w[j+1]
                w[j+1]=w_tmp
    return x,y,h,w