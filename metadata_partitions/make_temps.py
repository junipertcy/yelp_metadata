#state constant
states = ['OH']

for state in states:
    #Test with encoding
    start = open(state + '_network.gml','r')
    esc_lines = []
    for line in start:
        a = line.decode('utf-8')
        #This work-around replaces non-ascii characters with '?', for now.
        b = a.encode('ascii','replace')
        esc_lines.append(b)
    start.close()
    new_file = open(state+ '_network_temp.gml','w')
    new_file.truncate()
    new_file.writelines(esc_lines)
    new_file.close()
    print "created temp file for " + state
