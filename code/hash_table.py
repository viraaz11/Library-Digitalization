from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        if collision_type=="Double": self.z1,self.z2,self.c2,self.table_size=params
        elif collision_type=="Chain": self.z,self.table_size=params 
        else: self.z,self.table_size=params
        self.table = [None] * self.table_size
        self.size = 0 
        self.params=params
        self.collision_type = collision_type
    
    def polynomial_hash(self, key, z):
        m = self.table_size
        if self.collision_type=="Double" and self.z2==z: m=self.c2
        hash_value = 0
        power = 1
        for char in key:
            if char>="a" and char<="z": hash_value = (hash_value + (ord(char) - ord('a')) * power) % m
            else: hash_value = (hash_value + (ord(char) - ord('A') + 26) * power) % m
            power = (power * z) % m
        if self.collision_type=="Double" and self.z2==z: return self.c2-hash_value
        return hash_value
    
    def double_insert(self,x):
        if self.size==self.table_size: raise Exception("Table is Full")
        h1=h2=0
        if type(x)==tuple:
            if self.find(x[0]) != None and self.find(x[0]) !=False: return 
            h1=self.polynomial_hash(x[0],self.z1)
            h2=self.polynomial_hash(x[0],self.z2)            
        else:
            if self.find(x) !=False and self.find(x) != None: return 
            h1=self.polynomial_hash(x,self.z1)
            h2=self.polynomial_hash(x,self.z2)
        index=h1
        i = 1
        first=True
        while self.table[index] is not None and self.table[index]!=x:
            if not(first) and index==h1: raise Exception("Table is Full") 
            index = (h1 + i * h2) % self.table_size
            i+=1
            first=False
        if self.table[index] is None:
            self.table[index] = x     
            self.size+=1       

    def chain_insert(self,x): 
        index=0
        if type(x)==tuple:   
            if self.find(x[0]) != None and self.find(x[0]) !=False: return
            index=self.polynomial_hash(x[0],self.z)          
        else: 
            if self.find(x) !=False and self.find(x) != None: return 
            index=self.polynomial_hash(x,self.z)
        if self.table[index] is None:
            self.table[index]=[x]
            self.size+=1
        elif x not in self.table[index]: 
            self.table[index].append(x)
            self.size+=1
    
    def linear_insert(self,x):  
        if self.size==self.table_size: raise Exception("Table is Full") 
        index = 0
        if type(x)==tuple:   
            if self.find(x[0]) != None and self.find(x[0]) !=False: return
            index=self.polynomial_hash(x[0],self.z)          
        else: 
            if self.find(x) !=False and self.find(x) != None: return 
            index=self.polynomial_hash(x,self.z)
        start=index
        first=True
        while self.table[index] is not None and self.table[index]!=x:
            if not(first) and index==start: raise Exception("Table is Full")
            index = (index + 1) % self.table_size
            first=False
        if self.table[index] is None:
            self.table[index] = x     
            self.size+=1
        
    def insert(self, x):
        if self.collision_type=="Double": self.double_insert(x)
        elif self.collision_type=="Chain": self.chain_insert(x)
        else: self.linear_insert(x)
    
    def chain_search(self,key):
        index=self.polynomial_hash(key,self.z)
        if self.table[index] is None: return None
        for i in self.table[index]: 
            if i==key or (i[0]==key and type(i) is tuple): return i
        return None
    
    def linear_search(self,key):
        index = self.polynomial_hash(key,self.z)
        start=index
        first=True
        while self.table[index] is not None:
            if not(first) and index==start: break
            if key == self.table[index] or (key == self.table[index][0] and type(self.table[index]) is tuple): return self.table[index]
            index = (index + 1) % self.table_size
            first=False
        return None
    
    def double_search(self,key):
        h1 = self.polynomial_hash(key,self.z1)
        h2 = self.polynomial_hash(key,self.z2)
        index = h1
        i=1
        first=True
        while self.table[index] is not None:
            if key == self.table[index] or (key == self.table[index][0] and type(self.table[index]) is tuple): return self.table[index]
            if not(first) and index==h1: break
            index = (h1 + i * h2) % self.table_size
            i+=1
            first=False
        return None
    
    def find(self, key):
        if self.collision_type == "Chain": return self.chain_search(key)            
        elif self.collision_type == "Linear": return self.linear_search(key)
        else: return self.double_search(key)
        
    def get_slot(self, key):
        if self.collision_type == "Chain" or self.collision_type == "Linear": return self.polynomial_hash(key,self.z)
        else: return self.polynomial_hash(key,self.z1)
        
    def get_load(self):
        return self.size/self.table_size
    
    def __str__(self):
        if self.collision_type=="Chain": return " | ".join(" ; ".join(f"({j[0]},{j[1]})" if type(j) is tuple else f"{j}" for j in i) if i is not None else "<EMPTY>" for i in self.table)
        else: return  " | ".join(f"({i[0]},{i[1]})" if i is not None and type(i) is tuple  else ( f"{i}" if i is not None and type(i) is str else f"<EMPTY>") for i in self.table)
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        l=[]
        if self.collision_type=="Chain":
            for i in self.table:
                if i is not None: l.extend(i)
        else: l=[i for i in self.table if i is not None]
        self.table_size=get_next_size()
        self.table=[None]*self.table_size
        self.size=0
        for i in l:
            self.insert(i)
        
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
    
    def insert(self, key):
        super().insert(key)
        
    def find(self, key):
        val=super().find(key)
        if val is not None: return True
        return False
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type,params)
    
    def insert(self, x):
        # x = (key, value)
        super().insert(x)
    
    def find(self, key):
        val=super().find(key)
        if val is None : return None
        return val[1]
    
    def get_slot(self, key):
        return super().get_slot(key)
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        return super().__str__()