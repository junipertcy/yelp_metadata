import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

states = ['OH','NC']

for state in states:

        file_name = state + '_network_processed.gml'
        G = nx.read_gml(file_name,label='id')

        print state
        print len(G.edges())

        user_locs = []
        user_revs = []
        biz_revs = []
        user_stars = []
        biz_stars = []

        usercount = 0
        bizcount = 0 
        outct = 0

        for i in G.nodes():
            #user
            if G.nodes[i]['uid'] != '':
                usercount = usercount + 1
                user_locs.append(G.nodes[i]['localpartition'])
                if G.nodes[i]['reviewcount'] < 400:
                    user_revs.append(G.nodes[i]['reviewcount'])
                else:
                    outct = outct + 1
                user_stars.append(G.nodes[i]['averagestars'])
            #business
            if G.nodes[i]['bid'] != '':
                bizcount = bizcount + 1
                biz_revs.append(G.nodes[i]['reviewcount'])
                biz_stars.append(G.nodes[i]['averagestars'])

        print state + ' user count ' + str(usercount)
        print state + ' restaurant count ' + str(bizcount)
                
        plt.hist(user_stars,color='#000000')
        plt.title('User stars histogram - ' + state, fontsize=16)
        plt.axvline(x=2,linestyle='--',color='r')
        plt.axvline(x=3,linestyle='--',color='r')
        plt.axvline(x=4,linestyle='--',color='r')
        plt.xlabel('average stars',fontsize=16)
        plt.ylabel('count',fontsize=16)
        plt.show()

        plt.hist(biz_stars,color='#000000')
        plt.title('Business stars histogram - ' + state, fontsize=16)
        plt.axvline(x=2,linestyle='--',color='r')
        plt.axvline(x=3,linestyle='--',color='r')
        plt.axvline(x=4,linestyle='--',color='r')
        plt.xlabel('average stars',fontsize=16)
        plt.ylabel('count',fontsize=16)
        plt.show()
        

        plt.hist(user_locs,2,rwidth=0.5,align='mid',color='#000000')
        plt.title('User locals histogram - ' + state, fontsize=20)
        plt.xticks([0.25,0.75],('tourists','locals'), fontsize=20)
        plt.ylabel('count',fontsize=20)
        plt.show()


        #User review - hardcode bin axes from the entire distribution
        # only plot data from review_count < 400

        print state + ' ' + str(outct) + ' over 400' 
        
        verts = []
        if state == 'OH':
            verts = [2.000e+00,6.000e+00,2.000e+01]
        if state == 'NC':
            verts = [3.000e+00,7.000e+00,2.000e+01]
                
        plt.hist(user_revs,30,color='#000000')
        plt.title('User reviews histogram - ' + state, fontsize=16)
        #vertical lines
        plt.axvline(x=[verts[0]],linestyle='--',color='r')
        plt.axvline(x=[verts[1]],linestyle='--',color='r')
        plt.axvline(x=[verts[2]],linestyle='--',color='r')
        plt.xlabel('review count',fontsize=16)
        plt.ylabel('count',fontsize=16)

        plt.show()

        
        #Break biz reviews into 4 bins of equal size and get bin edges 
        outb, binsb = pd.qcut(biz_revs,4, retbins=True)

        plt.hist(biz_revs,30,color='#000000')
        plt.title('Business reviews histogram - ' + state, fontsize=20)
        #vertical lines
        plt.axvline(x=[binsb[1]],linestyle='--',color='r')
        plt.axvline(x=[binsb[2]],linestyle='--',color='r')
        plt.axvline(x=[binsb[3]],linestyle='--',color='r')
        plt.xlabel('review count',fontsize=16)
        plt.ylabel('count',fontsize=16)
        plt.show()
        
        

        
