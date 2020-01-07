import re
grim = open('grimms.txt', 'r') 

#read all stopwords into a list, more time/space efficient
stopword = []
stopwords = open('stopwords.txt', 'r')
for line in stopwords:
    word = line.strip()
    stopword.append(word)

#creating a word dictionary with indexing title
w2v = {}
ln = 0
for line in grim:
    ln = ln + 1
    line = line.strip()
    if ln > 123 and ln < 9207:
        if line.isupper() and line[0].isalpha():
            title = line
            continue
        line = re.sub(r'[^a-zA-Z0-9 ]', '', line)
        words = line.split()
        for word in words:
            word = word.lower()
            if word not in stopword:
                #match = re.search(r'[a-z0-9 ]+',word)
                #if match:
                w2v.setdefault(word, {}).setdefault(title, []).append(ln)

# function to iterate through the file and print the line by index list
# word transformation included
def print_line(list, wd):
    f = open('grimms.txt', 'r')
    l = 0
    for line in f:
        new = ''
        l = l + 1
        if l in list:
            line = line.strip()
            words = line.split(wd)
            for word in words:
                if words.index(word) != len(words) - 1:
                    new = new + word + '**' + wd.upper() + '**'
                else:
                    new += word
            print('    ', l, ' ', new)

# THE MAIN SEARCHING SYSTEM BEGINS：
print("Welcome to the Grimms' Fairy Tales search system!\n")
print('Please enter your query:')
x = input()
while(x != 'qquit'):
    print('query = ' + x)
    query = x.split()
    
    #1.single query
    if(len(query) == 1):
        if w2v.get(query[0]) == None:
            print('  --')
        else:
            for title in w2v[query[0]]:
                print('  ' + title)
                print_line(w2v[query[0]][title], query[0])

    #2. two-word-query contains 'or'            
    elif 'or' in query:
        #here is another method using set(list) union to do 'or'
        '''if w2v.get(query[0])!=None and w2v.get(query[2])!=None:
            titles = list(set(w2v[query[0]]).union(set(w2v[query[2]])))
            for title in titles:
                print("  "+title)
                print('   ',query[0])
                if title in w2v[query[0]]:
                    print_line(w2v[query[0]][title],query[0])
                else: print('   --')
                if title in w2v[query[2]]:
                    print_line(w2v[query[2]][title],query[2])
                else: print('   --')
        else if w2v.get(query[0])==None:
            if w2v.get(query[2])==None：
                print('   --')
            else:
                for title in w2v[query[2]]:
                    print("  "+title)
                    print('   ',query[0])
                    print('   --')
                    print('   ',query[2])
                    print_line(w2v[query[2]][title],query[2])'''

        titles = []
        if w2v.get(query[0]) != None:
            for title in w2v[query[0]]:
                titles.append(title)
                print('  ' + title)
                print('   ', query[0])
                print_line(w2v[query[0]][title], query[0])
                print('   ', query[2])
                if w2v.get(query[2]) != None and title in w2v[query[2]]:
                    print_line(w2v[query[2]][title], query[2])
                else: print('   --')
        if w2v.get(query[2]) != None:
            for title in w2v[query[2]]:
                if title not in titles:
                    print('  ' + title)
                    print('   ', query[0])
                    print('   --')
                    print('   ', query[2])
                    print_line(w2v[query[2]][title], query[2])

    #3. two-word-query contains 'and'
    elif 'and' in query:
        if w2v.get(query[0]) != None and w2v.get(query[2]) != None:
            titles = [i for i in w2v[query[0]] if i in w2v[query[2]]]
            if titles != []:
                for title in titles:
                    print('  ' + title)
                    print('   ', query[0])
                    print_line(w2v[query[0]][title], query[0])
                    print('   ', query[2])
                    print_line(w2v[query[2]][title], query[2])
        elif titles == []:
            print('   --')
        else:
            print('   --')

    #4. 'more than' query, default the query word has appeared at least once
    # if no result found, no output
    elif 'morethan' in query:
        for title in w2v[query[0]]:
            if query[2].isdigit() == True:
               if len(w2v[query[0]][title]) > int(query[2]):
                      print("  " + title)
            else:
                if w2v[query[2]].get(title) == None:
                    print("  " + title)
                elif len(w2v[query[0]][title]) > len(w2v[query[2]][title]):
                      print("  " + title)

    #5.'near' query,if no result found, no output
    elif 'near' in query:
        if w2v.get(query[0]) != None and w2v.get(query[2]) != None:
            titles = [i for i in w2v[query[0]] if i in w2v[query[2]]]
            if titles != []:
                for title in titles:
                    for m in w2v[query[0]][title]:
                        for n in w2v[query[2]][title]:
                            if abs(m-n) <= 1:
                                print('  ' + title)

    #6.any-length-query by logical and
    else:
        if w2v.get(query[0]) != None:
            titles = w2v[query[0]]
            for word in query:
                if w2v.get(word) == None:
                    titles = []
                    break;
                else:
                    titles = [i for i in titles if i in w2v[word]]
            if titles != []:
                for title in titles:
                    print('  '+title)
                    for word in query:
                        print('   ', word)
                        print_line(w2v[word][title], word)
            else: print('   --')
        else: print('   --')
            
        
    print('Please enter your query:')
    x = input()
    
quit()


