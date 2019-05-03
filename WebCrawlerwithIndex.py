#page = contents use get_page

#Test github in atom

def get_page(url):
	try: import urllib
		return urllib.urlopen(url).read()
	except:
		return

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None,0
    else:
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
	while True:
		url, endpos=get_next_target(page)
		links=[]
		if url:
			links.append(url)
			page=page[endpos:]
		else:
			break
	return links

#def add_to_index(index, keyword, url):
    #for entry in index:
        #if entry[0] == keyword:
            #entry[1].append(url)
            #return
    #index.append([keyword, [url]])

def add_to_index(index, keyword, url):
	if keyword in index:
		index[keyword].append(url)
	else:
		index[keyword] = [url]

#def lookup(index, keyword):
    #for entry in index:
        #if entry[0] == keyword:
            #return entry[1]
    #return []

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def hashtable_get_bucket(htable,keyword):
    return htable[hash_string(keyword,len(htable))]

def hash_string(keyword,buckets):
    result=0
    for letter in keyword:
        result = (result+ ord(letter))%buckets
    return result

def make_hashtable(nbuckets):
    hashtable = []
    for unused in range(0,nbuckets):
    	hashtable.append([])
    return hashtable

def crawl_web(seed):
	tocrawl=[seed]
	crawled =[]
	index = {}
	graph ={}
	while tocrawl:
		page=tocrawl.pop()
		if page not in crawled and len(crawled)<max_pages:
			content = get_page(page)
			add_page_to_index(index,page,content)
			outlinks=get_all_links(get_page(page))
			tocrawl.extend(outlinks)
			#union(tocrawl,outlinks)
			crawled.append(page)
	return index,graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank= newrank + d*(ranks[node]/len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks

print_all_links(get_page('url'))
