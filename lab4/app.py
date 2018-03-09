from datetime import date

from model import Wallet
from model import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class User():
    def __init__(self):
        self.engine = create_engine('sqlite:///assignment2.db')
        Base.metadata.create_all(self.engine)
        

    def session_factory(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        return session


    def create_wallets(self):
        session = self.session_factory()
        walletA = wallet(address="0x12345",balance=1000,public_key="345w24qc4a4t34raert")
        walletB = wallet(address="0x67890",balance=2000,public_key="345w24qc4a4t34rhhjjk") 
        session.add(walletA)
        session.add(walletB)
        session.commit()
        session.close()

    def get_wallets(self):
        session = self.session_factory()
        wallet_query = session.query(Wallet)
        session.close()
        return wallet_query.all()

    def  update_wallets(self):
        session = self.session_factory()
        wallet_query = session.query(Wallet)
        wallets = wallet_query.all()
        for wal in wallets:
            #print(wal.balance)
            wal.balance = (wal.balance + 500)
        session.commit()
        session.close()
        wallets = wallet_query.all()
        return wallets

if __name__ == '__main__':
    usr = User() 
    wallets = usr.get_wallets()
    if len(wallets) == 0:
        usr.create_wallets()
    
    wallets = usr.get_wallets()
    print("get method call")
    print("id" + " " +"public_key       " + " " + "address  " + " " + "balance")
    for wallet in wallets:
        print(str(wallet.id) + " " + str(wallet.public_key) + " " + str(wallet.address) + " " + str(wallet.balance))
    
    print("\nafter update")
    print("id" + " " +"public_key       " + " " + "address  " + " " + "balance")
    wal = usr.update_wallets()
    for w in wal:
        print(str(w.id) + " " + str(wallet.public_key) + " " + str(w.address) + " " + str(w.balance))
