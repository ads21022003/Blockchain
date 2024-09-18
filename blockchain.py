
import random
import time
from hashlib import sha256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
class Transaction :
    def __init__(self,id ,payer,payee , amount):
            self.payer =payer
            self.payee =payee
            self.amount =amount
            self.id  = id
            self.signature = 0
    def __str__(self) :
         return f'{self.id} {self.payee} {self.payer} {self.amount} {self.id} {self.signature}'
    def get_hash(self):
        a = f'{self.id} {self.payee} {self.payer} {self.amount}'
        sha256(a.encode('utf-8')).hexdigest()
class block:
   
    def __init__(self,index,prevHash , transactions ):
        self.nonce  = 0
        self.transactions =transactions
        self.time = time.time()
        self.prevHash = prevHash
        self.index = index
        self.hash=-1

    def __str__(self) -> str:
        a=  f'{self.index} {self.prevHash } {self.nonce} {self.time} {self.prevHash}'
        for i in self.transactions:
            a+=" "+str(i)
        return a      
    def get_hash(self):
         return sha256(str(self).encode('utf-8')).hexdigest()

         
class Blockchain:
    def __init__(self):
          self.blockchain=[]
          #genisis block
          self.blockchain.append(block(0,0,[]))
          self.blockchain[0].hash = self.blockchain[0].get_hash()
    def get_lastBlock (self):
         return self.blockchain[-1]
    def add_block(self,new_block):
         last_block_hash = self.get_lastBlock().get_hash()
         if (new_block.prevHash==last_block_hash):
              hash_value = new_block.get_hash()
              if (hash_value[:2]=="00"):
                   for transaction in new_block.transactions:
                        public_payer = transaction.payer
                        try:
                           
                            pkcs1_15.new(public_payer).verify(transaction.get_hash(),transaction.signature)
                        except:
                             print("invalid Transaction")
                             break
                   else:
                        self.append(new_block)

         else :
              print("Previous hash didn't match")
 
class User:
     def __init__(self):
          self.private_key =      RSA.generate(1024)     
          self.key = self.__key.publickey()
          self.pending_transaction=[]
     def send_money (self  , payee , amount):
          id =(int) (9999999999*random.random())
          trasaction = Transaction(id, self.key, payee,amount)
          signer = pkcs1_15.new(self.private_key)

          trasaction.signature = signer.sign(trasaction.get_hash())
          self.pending_transaction.append(trasaction)
     def mine(self):
          
          


          
    
     

    









if __name__ =="__main__" :
    print("hello world")