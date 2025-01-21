import hash_table as ht
class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    class Node:
        def __init__(self,book_name,texts):
            self.name=book_name
            self.text=texts
            self.distinct=[]
            
    def __init__(self, book_titles, texts):
        self.library=[]
        books=book_titles[:]
        text=[i[:] for i in texts]
        for i in range(len(books)):
            self.library.append(self.Node(books[i],text[i]))
            node=self.library[-1]
            self.sort(node.text,0,len(node.text)-1)
            for j in node.text:
                if len(node.distinct)==0 or node.distinct[-1]!=j:
                    node.distinct.append(j)
        self.sort(self.library,0,len(self.library)-1)                   
                    
    def compare(self,a,b):
        if type(a)==self.Node and type(b)==self.Node: return a.name<b.name
        return a<b
    
    def merge(self,arr, s, e):
        mid = s + (e - s) // 2
        len1 = mid - s + 1
        len2 = e - mid
        arr1 = arr[s:mid + 1]
        arr2 = arr[mid + 1:e + 1]
        ansindex = s
        i = 0
        j = 0
        while i < len1 and j < len2:
            if self.compare(arr1[i], arr2[j]):
                arr[ansindex] = arr1[i]
                i += 1
            else:
                arr[ansindex] = arr2[j]
                j += 1
            ansindex += 1
        while i < len1:
            arr[ansindex] = arr1[i]
            i += 1
            ansindex += 1
        while j < len2:
            arr[ansindex] = arr2[j]
            j += 1
            ansindex += 1

    def sort(self,arr, s, e):
        if s >= e: return
        mid = s + (e - s) // 2
        self.sort(arr, s, mid)
        self.sort(arr, mid + 1, e)
        self.merge(arr, s, e)

    def search(self,arr, s, e, key):
        if s > e: return -1
        mid = s + (e - s) // 2
        if arr[mid].name == key: return mid
        elif arr[mid].name < key: return self.search(arr, mid + 1, e, key)
        else: return self.search(arr, s, mid - 1, key)
        
    def distinct_words(self, book_title):
        index=self.search(self.library,0,len(self.library)-1,book_title)
        return self.library[index].distinct
    
    def count_distinct_words(self, book_title):
        index=self.search(self.library,0,len(self.library)-1,book_title)
        return len(self.library[index].distinct)
    
    def search_keyword(self, keyword):
        return [i.name for i in self.library if keyword in i.distinct]
    
    def print_books(self):
        for i in self.library:
            s=" | ".join(j for j in i.distinct)
            print(f"{i.name}: {s}")
            
class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        if name=="Jobs": self.hash_map=ht.HashMap("Chain", params)
        elif name=="Gates": self.hash_map=ht.HashMap("Linear", params)
        else: self.hash_map=ht.HashMap("Double", params)
        self.books=[]
            
    def add_book(self, book_title, text):
        val=ht.HashSet(self.hash_map.collision_type,self.hash_map.params)
        for i in text: val.insert(i)
        self.hash_map.insert((book_title,val))
        self.books.append((book_title,val))
    
    def distinct_words(self, book_title):
        val=self.hash_map.find(book_title)        
        if self.hash_map.collision_type=="Chain": return [j for lis in val.table if lis is not None for j in lis]
        else: return [i for i in val.table if i is not None]
    
    def count_distinct_words(self, book_title):
        return self.hash_map.find(book_title).size
    
    def search_keyword(self, keyword):
        return [i[0] for i in self.books if i[1].find(keyword)]   
    
    def print_books(self):
        for i in self.books: 
            print(f"{i[0]}: {i[1].__str__()}")