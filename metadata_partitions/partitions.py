import networkx as nx
import pandas as pd
    
#state constant
states = ['OH','NC']

for state in states:
    file_name = state + '_network_temp.gml'

    #Load gml file
    G = nx.read_gml(file_name,label='id')
        
    #Save location -> partition id {"Austin,TX" : 12}
    location_ids = {}
    next_loc = 0

    #get distribution of review count, to figure out bins 
    rcuser = []
    rcbus = []
    for i in G.nodes():
        if G.nodes[i]['uid'] !='' :
            rcuser.append(G.nodes[i]['review_count'])
        if G.nodes[i]['bid'] !='' :
           rcbus.append(G.nodes[i]['review_count'])
    #Break into 4 bins of equal size and get bin edges 
    outu, binsu = pd.qcut(rcuser,4, retbins=True)
    outb, binsb = pd.qcut(rcbus,4, retbins=True)

    #Loop through and add new partition information (all are integers)
    for node in G.nodes():
        #node is a user 
        if G.nodes[node]['uid'] !='' :
            #add trivial user partition
            G.nodes[node]['trivialpartition'] = 0
            #add user-specific partition information
            #add local v. tourist partition information
            try:
                #note, that this can also be a country
                node_state = G.nodes[node]['location'].split()[1]
            except:
                print G.nodes[node]['location']
                print G.nodes[node]['uid']
                print G.nodes[node]['bid']
                #This only seems to be happening when people just have a country
                node_state = G.nodes[node]['location'].split()[0]
            if node_state == state:
                #person is from the same state as businesses
                G.nodes[node]['localpartition'] = 1
            else:
                #person is from different state than businesses
                G.nodes[node]['localpartition'] = 0
            #add user binned review count partition information
            rcu = G.nodes[node]['review_count']
            if rcu >= binsu[0] and rcu < binsu[1]:
                G.nodes[node]['revpartitionu'] = 0 
            if rcu >= binsu[1] and rcu < binsu[2]:
                G.nodes[node]['revpartitionu'] = 1
            if rcu >= binsu[2] and rcu < binsu[3]:
                G.nodes[node]['revpartitionu'] = 2 
            if rcu >= binsu[3] and rcu <= binsu[4]:
                G.nodes[node]['revpartitionu'] = 3 
        #node is a business
        if G.nodes[node]['bid'] !='' :
            #add trivial business partition
            G.nodes[node]['trivialpartition'] = 1
            #add business binned review count partition information
            rcb = G.nodes[node]['review_count']
            if rcb >= binsb[0] and rcb < binsb[1]:
                G.nodes[node]['revpartitionb'] = 0 
            if rcb >= binsb[1] and rcb < binsb[2]:
                G.nodes[node]['revpartitionb'] = 1
            if rcb >= binsb[2] and rcb < binsb[3]:
                G.nodes[node]['revpartitionb'] = 2 
            if rcb >= binsb[3] and rcb <= binsb[4]:
                G.nodes[node]['revpartitionb'] = 3 
        #add binned average stars partition information for both node types
        stars = G.nodes[node]['average_stars']
        if stars >=1 and stars < 2:
            G.nodes[node]['starpartition'] = 1
        if stars >=2 and stars < 3:
            G.nodes[node]['starpartition'] = 2 
        if stars >=3 and stars < 4:
            G.nodes[node]['starpartition'] = 3 
        if stars >=4 and stars <=5:
            G.nodes[node]['starpartition'] = 4
        #add location partition for either user or business
        loc = G.nodes[node]['location']
        if loc in location_ids:
            loc_id = location_ids[loc]
            G.nodes[node]['locationpartition'] = loc_id
        else:
            location_ids[loc] = next_loc
            G.nodes[node]['locationpartition'] = next_loc
            next_loc = next_loc + 1
        #change gml attributes with underscores (error on write)
        #known issue - https://github.com/networkx/networkx/issues/2131
        rc = G.nodes[node]['review_count']
        del G.nodes[node]['review_count']
        G.nodes[node]['reviewcount'] = rc
        ast = G.nodes[node]['average_stars']
        del G.nodes[node]['average_stars']
        G.nodes[node]['averagestars'] = ast
        pw = G.nodes[node][u'partition_w']
        del G.nodes[node][u'partition_w']
        G.nodes[node]['partitionw'] = pw

                                    
    #re-save gml file as a processed version
    new_name = state + '_network_processed.gml'
    nx.write_gml(G,new_name)
    print "saved " + new_name

