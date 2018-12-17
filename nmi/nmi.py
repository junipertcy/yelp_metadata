import math as math
import networkx as nx

#input - state, two partitions to compare
def nmi(state,partone,parttwo,useronly,bizonly,force,forcepartone,forceparttwo):

    #only do the nmi calculation
    if force == True:
        partitionone = forcepartone
        partitiontwo = forceparttwo
    else:
        file_name = state + '_network_processed.gml'
        G = nx.read_gml(file_name,label='id')
        
        #create map partition id -> ids of elements in the partition {'1': [1,2,3]}
        partitionone = {}
        partitiontwo = {}

        #add values to the dictionaries
        for i in G.nodes():
            #only compute for user nodes
            if useronly == True:
                #if is business don't count 
                if G.nodes[i]['bid'] != '':
                    continue
            #only compute for business nodes
            if bizonly == True:
                #if is user don't count
                if G.nodes[i]['uid'] != '':
                    continue
            partoneid = G.nodes[i][partone]
            parttwoid = G.nodes[i][parttwo]
            if partoneid not in partitionone:
                partitionone[partoneid] = [i] 
            else:
                partitionone[partoneid].append(i)
            if parttwoid not in partitiontwo:
                partitiontwo[parttwoid] = [i] 
            else:
                partitiontwo[parttwoid].append(i)

    #calculate nmi between the two partitions (used code from PS3)

    n= 0 
    for k,v in partitionone.items():
        n = n + len(v)
    #print n

    #mutual information between assignments c and c_prime
    icc_prime = 0

    for x,group_x in partitionone.items():
        for y,group_y in partitiontwo.items():
            #find intersection between groups
            inter = set(group_x).intersection(group_y)
            pxy = len(inter)/float(n)
            px = len(group_x)/float(n)
            py = len(group_y)/float(n)
            if pxy == 0:
                continue
            else:
                icc_prime = icc_prime + (pxy * math.log(pxy/float(px*py),2))
            
    #print "icc_prime"
    #print icc_prime

    #entropy of assignment c (partition one)
    hc = 0
    for x,group_x in partitionone.items():
        #probability that a node is in group_X in set of alg partitions
        px = len(group_x)/float(n)
        hc = hc - (px * math.log(px,2))

    #print "hc"
    #print hc 

    #entropy of assignment c_prime (partition two)
    hc_prime = 0
    for y,group_y in partitiontwo.items():
        py = len(group_y)/float(n)
        hc_prime = hc_prime - (py * math.log(py,2))

    #print "h_cprime"
    #print hc_prime

    i_norm = (2*icc_prime)/float(hc+hc_prime)
    #print "i_norm"
    #print i_norm
    return i_norm

if __name__ == "__main__":    

    #state constants
    states = ['OH','NC']


    #for user nodes only, compare local v. tourist, review count, average stars
    sbmusercomps = ['localpartition','revpartitionu','starpartition','locationpartition']
    wsbmusercomps = ['localpartition','revpartitionu','starpartition','locationpartition']

    #for business nodes only, compare average stars, review count
    sbmbizcomps = ['starpartition','revpartitionb', 'locationpartition']
    wsbmbizcomps = ['starpartition','revpartitionb','locationpartition']



    for state in states:

        results = open('nmi_results_'+ state,'w')
        results.truncate()

        #Compare sbm for user nodes only 
        partone = 'partition'
        for parttwo in sbmusercomps:
            nmi_ = nmi(state,partone,parttwo,True,False,False,0,0)
            line = 'user ' + state + ' ' + partone+ ' ' + parttwo + ' ' + str(nmi_) +'\n'
            print line
            results.write(line)

        #Compare w sbm for user nodes only 
        partone = 'partitionw'
        for parttwo in wsbmusercomps:
            nmi_ = nmi(state,partone,parttwo,True,False,False,0,0)
            line = 'user ' + state + ' ' + partone+ ' ' + parttwo + ' ' + str(nmi_) +'\n'
            print line
            results.write(line)

        #Compare sbm for biz nodes only 
        partone = 'partition'
        for parttwo in sbmbizcomps:
            nmi_ = nmi(state,partone,parttwo,False,True,False,0,0)
            line = 'business ' + state + ' ' + partone+ ' ' + parttwo + ' ' + str(nmi_) +'\n'
            print line
            results.write(line)

        #Compare w sbm for biz nodes only 
        partone = 'partitionw'
        for parttwo in wsbmbizcomps:
            nmi_ = nmi(state,partone,parttwo,False,True,False,0,0)
            line = 'business ' + state + ' ' + partone+ ' ' + parttwo + ' ' + str(nmi_) +'\n'
            print line
            results.write(line)
            
        results.close()


