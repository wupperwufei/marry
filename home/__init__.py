# from flask import Blueprint
# home=Blueprint('home',__name__)
# from home import view

for i in range(1,10):
    for j in range(i):
        j=j+1
        print("%d*%d=%-3d" % (i,j,i*j),end=" ")
    print("")