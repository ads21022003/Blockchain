
import random
import time
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto import Random
import os
class Transaction :
    def __init__(self,id ,payer,payee , amount):
            self.payer =payer
            self.payee =payee
            self.amount =amount
            self.id  = id
            self.signature = 0
    def __str__(self)->str :
         return f'{self.id} {self.payee.export_key(format="DER").hex()[50:100]}  {self.payer.export_key(format="DER").hex()[50:100]} {self.amount} '
    def serialize(self):
         return f'{self.id} {self.payee.export_key(format="DER").hex()}  {self.payer.export_key(format="DER").hex()} {self.amount} '
    def get_hash(self):
        a = f'{self.id} {self.payee} {self.payer} {self.amount}'
        return SHA256.new(a.encode('utf-8'))
class Block:
   
    def __init__(self,index,prevHash , transactions ):
        self.nonce  = 0
        self.transactions =transactions
        self.time = time.time()
        self.prevHash = prevHash
        self.index = index
        self.hash=-1

    def __str__(self) -> str:
        a=  f'{self.index} {str(self.prevHash)[:10] } {self.nonce} {datetime.fromtimestamp(self.time).strftime("%Y-%m-%d %H:%M:%S")}  \n'
        for i in self.transactions:
            a+=str(i)+"\n"
        return a      
    def get_hash(self):
         a = a=  f'{self.index} {self.prevHash } {self.nonce} {self.time} \n'
         for i in self.transactions:
            a+=i.serialize()+"\n"
         
         return SHA256.new(str(self).encode('utf-8'))

         
class Blockchain:
    def __init__(self):
          self.blockchain=[]
          #genisis block
          self.blockchain.append(Block(0,0,[]))
          self.blockchain[0].hash = self.blockchain[0].get_hash().hexdigest()
    def get_lastBlock (self)->Block:
         return self.blockchain[-1]
    def add_block(self,new_block:Block)->bool:
         last_block_hash = self.get_lastBlock().get_hash().hexdigest()
         if (new_block.prevHash==last_block_hash):
              hash_value = new_block.get_hash().hexdigest()
              if (hash_value[:2]=="00"):
                   for transaction in new_block.transactions:
                        public_payer = transaction.payer
                        try:
                           
                            pkcs1_15.new(public_payer).verify(transaction.get_hash(),transaction.signature)
                        except:
                             print("invalid Transaction")
                             break
                   else:
                        self.blockchain.append(new_block)
                        return True
         else :
              print("Previous hash didn't match")
              return False
         return False
 
class User:
     def __init__(self):
          random_generator = Random.get_random_bytes
          self.private_key =      RSA.generate(1024,randfunc=os.urandom)     
          self.key = self.private_key.publickey()
          self.pending_transaction=[]
     def send_money (self  , payee , amount):
          id =(int) (9999999999*random.random())
          trasaction = Transaction(id, self.key, payee,amount)
          signer = pkcs1_15.new(self.private_key)
          #print(signer)
          #print(trasaction.get_hash())
          trasaction.signature = signer.sign(trasaction.get_hash())
          self.pending_transaction.append(trasaction)
     def mine(self,blockchain:Blockchain)->bool:
          if (len(self.pending_transaction)==0):
               print("No transaction to add")
               return 1
          last_block = blockchain.get_lastBlock()
          new_index = last_block.index+1
          prevHash = last_block.hash
          new_block = Block(new_index , prevHash , self.pending_transaction)
          new_block.hash = new_block.get_hash().hexdigest()
          while (new_block.hash[:2]!="00"):
               new_block.nonce+=1
               new_block.hash = new_block.get_hash().hexdigest()
          print("Mining Completed")
          blockchain.add_block(new_block)
          print("BlockChain Updated")
          self.pending_transaction=[]

          


          
    
     

    









if __name__ =="__main__" :
    roony = User()
    tom = User()
    jhonny = User()
    blockchain = Blockchain()
    roony.send_money(tom.key,100)
    roony.send_money(jhonny.key,890)
    roony.mine(blockchain)
    roony.send_money(jhonny.key,1890)
    roony.send_money(tom.key,45100)
    roony.mine(blockchain)
    print(blockchain.blockchain[0])
    print(blockchain.blockchain[1])
    print(blockchain.blockchain[2])