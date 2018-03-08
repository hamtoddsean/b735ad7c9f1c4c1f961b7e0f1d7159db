import uuid
import time

import requests
from decimal import *
	
import re,os,zlib,json,time,csv

class Client(object):
    def __init__(self, url, public_key, secret):
        self.url = url + "/api/2"
        self.session = requests.session()
        self.session.auth = (public_key, secret)

    def get_symbol(self, symbol_code):
        """Get symbol."""
        return self.session.get("%s/public/symbol/%s" % (self.url, symbol_code)).json()

    def get_orderbook(self, symbol_code):
        """Get orderbook. """
        return self.session.get("%s/public/orderbook/%s" % (self.url, symbol_code)).json()

    def get_address(self, currency_code):
        """Get address for deposit."""
        return self.session.get("%s/account/crypto/address/%s" % (self.url, currency_code)).json()

    def get_account_balance(self):
        """Get main balance."""
        return self.session.get("%s/account/balance" % self.url).json()

    def get_trading_balance(self):
        """Get trading balance."""
        return self.session.get("%s/trading/balance" % self.url).json()

    def transfer(self, currency_code, amount, to_exchange):
        return self.session.post("%s/account/transfer" % self.url, data={
                'currency': currency_code, 'amount': amount,
                'type': 'bankToExchange' if to_exchange else 'exchangeToBank'
            }).json()

    def new_order(self, client_order_id, symbol_code, side, quantity, price=None):
        """Place an order."""
        data = {'symbol': symbol_code, 'side': side, 'type': 'market','timeInForce': 'FOK', 'quantity': quantity}

        if price is not None:
            data['price'] = price

        return self.session.put("%s/order/%s" % (self.url, client_order_id), data=data).json()

    def get_order(self, client_order_id, wait=None):
        """Get order info."""
        data = {'wait': wait} if wait is not None else {}

        return self.session.get("%s/order/%s" % (self.url, client_order_id), params=data).json()

    def cancel_order(self, client_order_id):
        """Cancel order."""
        return self.session.delete("%s/order/%s" % (self.url, client_order_id)).json()

    def withdraw(self, currency_code, amount, address, network_fee=None):
        """Withdraw."""
        data = {'currency': currency_code, 'amount': amount, 'address': address}

        if network_fee is not None:
            data['networkfee'] = network_fee

        return self.session.post("%s/account/crypto/withdraw" % self.url, data=data).json()

    def get_transaction(self, transaction_id):
        """Get transaction info."""
        return self.session.get("%s/account/transactions/%s" % (self.url, transaction_id)).json()
        
    def showtime(self,v):
        tva= 'Timer-'
        va= ''
        if v< 60:
            va= tva+str(v)+'-seconds'
        if v> 59 and v< 3600:
            v= v/60
            v= round(v,3)
            va= tva+str(v)+'-minutes'
        if v> 3599 and v< 86399:
            v= v/3600
            v= round(v,3)
            va= tva+str(v)+'-hours'
        if v> 86399:
            v= v/86400
            v= round(v,3)
            va= tva+str(v)+'-days'
        return va

    def talcal(self,t,p):
        qp=''
        pp=t-p
        if pp> 0:
            qp=pp/p
            qp=qp*100
        return qp

    def buy(self,aamt,abid):
        #import hitbtc
        import uuid
        import decimal
        abtc_usd= self.get_symbol('ETHUSD')
        aorder=''
        aclient_order_id = uuid.uuid4().hex
        abest = abid
        abet = None
        acamt = aamt
        nooz=''
        print('fetching buy order')
        aorder = self.new_order(aclient_order_id, 'ETHUSD', 'buy', aamt, abet)
        if 'error' in aorder:
            for iv in range(10):
                acamt=acamt-0.001
                round(acamt,3)
                aclient_order_idd = uuid.uuid4().hex
                aorder = self.new_order(aclient_order_idd, 'ETHUSD', 'buy', acamt, abet)
                if 'status' in aorder:
                    break
        print('done')
        print(aorder)
        return aorder

    def sell(self,eamt,ebid):
        #import hitbtc
        import uuid
        import decimal
        ebtc_usd= self.get_symbol('ETHUSD')
        eorder=''
        eclient_order_id = uuid.uuid4().hex
        ebest = ebid
        ebet = None
        ecamt = eamt
        print('fetching sell order')
        eorder = self.new_order(eclient_order_id, 'ETHUSD', 'sell', eamt, ebet)
        if 'error' in eorder:
            for tfi in range(10):
                ecamt=ecamt-0.001
                round(ecamt,3)
                eclient_order_idd = uuid.uuid4().hex
                eorder = self.new_order(eclient_order_idd, 'ETHUSD', 'sell', ecamt, ebet)
                if 'status' in eorder:
                    break
        print('done')
        print(eorder)
        return eorder

    def srun(self,juj,stoptime,pathh):
        import os,zlib,json,time,csv,re,datetime
        time=datetime.datetime.now()
        time=str(time)
        mo=re.compile(r'(\d+-\d+-\d+)')
        ma=re.compile(r'(\d+):(\d+):(\d+)')
        mmo=re.compile(r'(\d+)(.)(\d+)')


        baa=ma.findall(time)
        aa=int(baa[0][0])
        bb=int(baa[0][1])
        cc=int(baa[0][2])
        aa=aa*3600
        bb=bb*60
        cc=aa+bb+cc

        ba=mo.findall(time)
        e=(str(ba[0]))
        kb=''
        bid=''
        ask=''
        bbid=''
        aask=''
        count=''
        dg=[]
        ded=1
        plist=''
        stoptimee= stoptime
        
        if ded==1:
            cpl=json.loads(juj)
            if cpl['bid']!=None:
    
                bid=float(cpl['bid'])
                ask=float(cpl['ask'])
    
    # print(cpl)
                bbab=mmo.findall(str(bid))
                bbaa=mmo.findall(str(ask))
                bbid=float(bbab[0][0])
                aask=float(bbaa[0][0])
                        

                plist=pathh
      
                count=len(plist['count'])

                if plist['list']==[]:
                    if ask-bid <=0.7:
                        plist['list']=[bid,ask]

                if plist['list'] !=[]:
                    if ask==float(plist['list'][1]):
                        if bid==float(plist['list'][0]):
                            plist['count'].append(1)
  
                if plist['list'] !=[]:
                    if ask<plist['list'][1] or ask>plist['list'][1]:
                        plist['list']=[bid,ask]
                        plist['count']=dg


                if plist['store']!=[]:
                    if plist['store'][-1]!= ask:
                        plist['store'].append(ask)
                if plist['store']==[]:
                    plist['store'].append(ask)

########

                if len(plist['store'])>= 20:
                    ab=len(plist['store'])- 20
                    slist=plist['store'][ab::]
                    for ji in range(0,len(slist)-1):
                        if plist['store'][ji]- plist['store'][ji+1]>= 25 or plist['store'][ji+1]- plist['store'][ji]<= -25:
                            plist['counter'].append(1)
                    if len(plist['counter'])>= 19:
                        plist['tab']=['switch']
                        plist['store']=slist
                    else:
                        plist['store']=[]
                        plist['tab']=['d']
                        plist['counter']=[]

################

                if plist['tab'][0]=='switch':

################
#watchdiff=''
                    if ask-bid>=25 and plist['status']!='sell':
                        plist['ww']=[bid,ask]
                        plist['w']=[bid,ask]
  
####fix lower
                    if ask- bid<=7:
                        if plist['ww']!=[]:
                            if ask<=plist['ww'][1]:
                                if count>1:
                                    plist['lowert']=[bid,ask]
                                    plist['lower']=[bid,ask]
####@#####

#####buy
                    if plist['ww']!=[] and plist['status']!='sell':
                        if ask<= plist['ww'][0]:
                            if ask- plist['ww'][1]>=25:
                                kplacebuy=self.buy(float(plist['qty'])+0.001,ask)
                                if 'status' in kplacebuy:
                                    if kplacebuy['status']=='filled':
                                        plist['buyp'].append(float(kplacebuy['tradesReport'][0]['price']))
                                        tick=0.1/100
                                        tick=float(kplacebuy['tradesReport'][0]['price'])* tick
                                        tick=float(kplacebuy['tradesReport'][0]['price'])- tick
                            
                                     
                                        plist['buy'].append(tick)
                                        plist['BUY'].append(float(kplacebuy['tradesReport'][0]['price']))
                                        plist['status']='sell'
                                        plist['qty']=kplacebuy['quantity']
                                        pathh['keeprecord'].append(kplacebuy)

#########
    ########sellll 1
                    if plist['status']=='sell':
                        if bid> plist['buyp'][-1]:
                            if bid-plist['buyp'][-1]>= 25:
                                kcttick=0.1/100
                                kcttick=bid* kcttick
                                kcttick=bid- kcttick
                
                                qq=self.talcal(kcttick,float(plist['buy'][-1]))
                                if qq> 0.09:
                                    kkplacesell=self.sell(float(plist['qty']),bid)
                                    if 'status' in kkplacesell:
                                        if kkplacesell['status']=='filled':
                                            plist['sellp'].append(float(kkplacesell['tradesReport'][0]['price']))
                                            kcttick=float(kkpacesell['tradesReport'][0]['price'])-kcttick
                                            plist['sell'].append(kcttick)
                                            plist['SELL'].append(float(kkplcesell['tradesReport'][0]['price']))
                                            plist['status']='buy'
                                            plist['lower']=[]
                                            plist['lowert']=[]
                                            plist['w']=[]
                                            plist['ww']=[]
                                            plist['qty']=kkplacesell['quantity']
                                            pathh['keeprecord'].append(kkplacesell)


                    if len(plist['buy'])==len(plist['sell']) and len(plist['sell']) !=0:
                        aaa=sum(plist['buy'])
                        bbb=sum(plist['sell'])
                        ccc=bbb-aaa
                        ddd=ccc/plist['buy'][0]
                        ddd=ddd*100
                        if ccc>0:
                            pprof='%profit'+'-'+str(ddd)+'-'+str(ccc)
                            plist['profit']=pprof
                        if ccc==0:
                            pprof='%even'+'-'+str(ddd)+'-'+str(ccc)
                            plist['profit']=pprof
                        if ccc<0:
                            pprof='%loss'+'-'+str(ddd)+'-'+str(ccc)
                            plist['profit']=pprof
                        plist['even']='yes'
                        print(pprof)
                    else:
                        plist['even']='no'
                    print(plist)
                    pathh=plist
       # ddouup.writerow([plist])




###################



                else:
#watchdiff=''
                    if ask-bid>=0.7 and plist['status']!='sell':
                        plist['ww']=[bid,ask]
                        plist['w']=[bid,ask]
  
####fix lower
                    if ask- bid<=0.7 and plist['status']!= 'sell':
                        if plist['ww']!=[]:
                            if aask<=plist['ww'][1]:
                                if count>1:
                                    plist['lowert']=[bid,ask]
                                    plist['lower']=[bid,ask]

#####buy
                    if plist['lowert']!=[] and plist['status']!='sell':
                        if ask> 0:
                            if ask> plist['lowert'][1]:
    ###place buyorder
                                placebuy=self.buy(float(plist['qty'])+0.001,ask)
                                if 'status' in placebuy:
                                    if placebuy['status']=='filled':
                                        plist['buyp'].append(float(placebuy['tradesReport'][0]['price']))
                                        ttick=0.1/100
                                        ttick=float(placebuy['tradesReport'][0]['price'])* ttick
                                        ttick=float(placebuy['tradesReport'][0]['price'])- ttick

                                        plist['buy'].append(ttick)
                                        plist['BUY'].append(float(placebuy['tradesReport'][0]['price']))
                                        plist['status']='sell'
                                        plist['qty']=placebuy['quantity']
                                        pathh['keeprecord'].append(placebuy)

#########

    ########sellll 1
                    if plist['status']=='sell':
                        if bid> plist['buyp'][-1]:
                            if bid-plist['buyp'][-1]> 0.9:
                                cttick=0.1/100
                                cttick=bid* cttick
                                cttick=bid- cttick

                                q=self.talcal(cttick,float(plist['buy'][-1]))
                                if q> 0.09:
                                    placesell=self.sell(float(plist['qty']),bid)
                                    if 'status' in placesell:
                                        if placesell['status']=='filled':
                                            plist['sellp'].append(float(placesell['tradesReport'][0]['price']))
                                            cttick=float(placesell['tradesReport'][0]['price'])-cttick
                                            plist['sell'].append(cttick)
                                            plist['SELL'].append(float(placesell['tradesReport'][0]['price']))
                                            plist['status']='buy'
                                            plist['lower']=[]
                                            plist['lowert']=[]
                                            plist['w']=[]
                                            plist['ww']=[]
                                            plist['qty']=placesell['quantity']
                                            pathh['keeprecord'].append(placesell)

####@@@@
                    if len(plist['buy'])==len(plist['sell']) and len(plist['sell']) !=0:
                        aa=sum(plist['buy'])
                        bb=sum(plist['sell'])
                        cc=bb-aa
                        dd=cc/plist['buy'][0]
                        dd=dd*100
                        if cc>0:
                            prof='%profit'+'-'+str(dd)+'-'+str(cc)
                            plist['profit']=prof
                        if cc==0:
                            prof='%even'+'-'+str(dd)+'-'+str(cc)
                            plist['profit']=prof
                        if cc<0:
                            prof='%loss'+'-'+str(dd)+'-'+str(cc)
                            plist['profit']=prof
                        plist['even']='yes'
                        print(prof)
                    else:
                        plist['even']='no'
                    print(plist)
                    pathh= plist
      #  douup.writerow([plist])

      #def


                if cc> stoptimee and plist['even']=='yes':
                    plist['pleven']='yes'
       #pleven='yes'
                    pathh= plist
                    print('over and out')




if __name__ == "__main__":
    public_key = "cc2bf5e7ed2ba3dab76115b76d4ccbdc"
    secret = "14c806cfba09cdfbce048e7086232623"

    client = Client("https://api.hitbtc.com", public_key, secret)
    
    clist={'keeprecord':[],'go':'','qty':'0.007','pleven':'','ggo':'yes','list':[],'buyp':[],'sellp':[],'BUY':[],'SELL':[],'even':'','count':[],'status':'','buy':[],'sell':[],'lower':[],'lowert':[],'uppert':[],'upper':[],'w':[],'ww':[],'counter':[],'store':[],'tab':['d'],'watch':''}
    url='http://api.hitbtc.com/api/2/public/ticker/ETHUSD'
    
    stoptime=432000
    showt= ''


    for vii in range(439200):
        time.sleep(1)
        showt= client.showtime(vii)
        print(showt)

        countpl=clist['pleven']


        if vii< stoptime or countpl != 'yes':
            r = requests.get(url)
            if r.status_code== 200:
                s=r.json()
                print(r)
                ss=json.dumps(s)
                print(ss)
                client.srun(ss,stoptime,clist)

        else:
            print(showt)
            print('logged out')
            print(clist)
