import networkx as nx
import random
import nmi 

#Goal of this fn is to count things for the slide deck
#And then load nmi's and compare to random
def counts_random(states):

    for state in states:

        print 'state is ' + state

        file_name = state + '_network_processed.gml'
        G = nx.read_gml(file_name,label='id')

        #overall # of users and businesses
        uids = []
        bids = []

        user_p = ['partition','partitionw','localpartition','revpartitionu','starpartition','locationpartition']
        biz_p = ['partition','partitionw','starpartition','revpartitionb', 'locationpartition']


        #for each partition we need # of groups in each and # of elements in each group
        #{partition name: {partion value: count})
        #   Ex - {location: {5:9}}
        user_counts = {}
        biz_counts = {}
        for i in user_p:
            user_counts[i] = {}
        for i in biz_p:
            biz_counts[i] = {}

        count = 0 
        for i in G.nodes():
            #user
            if G.nodes[i]['uid'] != '':
                uids.append(G.nodes[i]['uid'])
                for j in user_p:
                    if G.nodes[i][j] not in user_counts[j]:
                        user_counts[j][G.nodes[i][j]] = 1
                    else:
                        user_counts[j][G.nodes[i][j]] = user_counts[j][G.nodes[i][j]] + 1
            #business
            if G.nodes[i]['bid'] != '':
                bids.append(G.nodes[i]['bid'])
                for j in biz_p:
                    if G.nodes[i][j] not in biz_counts[j]:
                        biz_counts[j][G.nodes[i][j]] = 1
                    else:
                        biz_counts[j][G.nodes[i][j]] = biz_counts[j][G.nodes[i][j]] + 1

        #save the overall counts somewhere (for reporting)
        results = open('count_results_' + state,'w')
        results.truncate()
        for i in user_p:
            # Example: user locationpartition 5 groups
            line = ' user ' + i + ' ' + str(len(user_counts[i].keys())) + ' groups\n' 
            print line
            results.write(line)
        for i in biz_p:
            line = 'biz ' + i + ' ' + str(len(biz_counts[i].keys())) + ' groups\n'
            print line
            results.write(line)

        results.close()

        ## Now for the NMI comparison to random...

        #Save the Yelp NMI's
    
        #{(partone,partwo):nmi}
        pair_yelp_nmi_user = {}
        pair_yelp_nmi_biz = {}

        
        nmis = open('nmi_results_' + state,'r')
        lines = nmis.readlines()
        for line in lines:
            a = line.split()
            if a[1] == state:
                if a[0] == 'user':
                    pair_yelp_nmi_user[(a[2],a[3])] = a[4]
                if a[0] == 'business':
                    pair_yelp_nmi_biz[(a[2],a[3])] = a[4]


        nmis.close()

        num_trials = 10

        output = open('baseline_results_' + state,'w')
        output.truncate()

        #For each combination of user partitions
        for pair in pair_yelp_nmi_user.keys():

            print 'calculating random baseline for user pair ' + pair[0] + ' ' + pair[1]

            nmirsum = 0 
            for trial in range(0,num_trials):
                
                #Create a new random order of all the users
                random.shuffle(uids)
                curr = 0

                #Assign uids in order to relevantly structured random partitions (same # groups, # of elements in each group)
                #Partition format is group label -> ids of elements in the partition,  {'1': [1,2,3]}
                random_p_one = {}
                random_p_two = {}

                #partition one
                for k,v in user_counts[pair[0]].items():
                    #k is group label
                    random_p_one[k] = []
                    #v is # of elements to add
                    for el in range(0,v):
                        random_p_one[k].append(uids[curr])
                        curr = curr + 1
                assert curr == len(uids)

                #Create a new random order of all the users
                random.shuffle(uids)
                curr = 0

                #partition two
                for k,v in user_counts[pair[1]].items():
                    #k is group label
                    random_p_two[k] = []
                    #v is # of elements to add
                    for el in range(0,v):
                        random_p_two[k].append(uids[curr])
                        curr = curr + 1
                assert curr == len(uids)

                nmirtrial = nmi.nmi(0,0,0,0,0,True,random_p_one,random_p_two)
                nmirsum = nmirsum + nmirtrial 

            nmir = nmirsum/float(num_trials)
            yelp_nmi = pair_yelp_nmi_user[(pair[0],pair[1])]
            diff = float(yelp_nmi)-float(nmir)
            outline = 'user ' + pair[0] + ' ' + pair[1] + ' ' + str(yelp_nmi) + ' ' + str(nmir) + ' ' + str(diff) + '\n'
            output.write(outline)
            print outline

        #For each combination of business partitions
        for pair in pair_yelp_nmi_biz.keys():

            print 'calculating random baseline for business pair ' + pair[0] + ' ' + pair[1]

            nmirsum = 0 
            for trial in range(0,num_trials):
                
                #Create a new random order of all the businesses
                random.shuffle(bids)
                curr = 0

                #Assign uids in order to relevantly structured random partitions (same # groups, # of elements in each group)
                #Partition format is group label -> ids of elements in the partition,  {'1': [1,2,3]}
                random_p_one = {}
                random_p_two = {}

                #partition one
                for k,v in biz_counts[pair[0]].items():
                    #k is group label
                    random_p_one[k] = []
                    #v is # of elements to add
                    for el in range(0,v):
                        random_p_one[k].append(bids[curr])
                        curr = curr + 1
                assert curr == len(bids)

                #Create a new random order of all the users
                random.shuffle(bids)
                curr = 0

                #partition two
                for k,v in biz_counts[pair[1]].items():
                    #k is group label
                    random_p_two[k] = []
                    #v is # of elements to add
                    for el in range(0,v):
                        random_p_two[k].append(bids[curr])
                        curr = curr + 1
                assert curr == len(bids)
                
                nmirtrial = nmi.nmi(0,0,0,0,0,True,random_p_one,random_p_two)
                nmirsum = nmirsum + nmirtrial 

            nmir = nmirsum/float(num_trials)
            yelp_nmi = pair_yelp_nmi_biz[(pair[0],pair[1])]
            diff = float(yelp_nmi)-(nmir)
            outline = 'business ' + pair[0] + ' ' + pair[1] + ' ' + str(yelp_nmi) + ' ' + str(nmir) + ' ' + str(diff) + '\n'
            output.write(outline)
            print outline
                

        output.close()

                    
                    
if __name__ == "__main__":    

    #state constants
    states = ['NC','OH']
    counts_random(states)
    
    
    
