#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
import pandas as pd
import re

catalog = pd.read_csv("Product-Catalogue.csv")


# In[3]:


barcodes = [str(a) for a in catalog.loc[:,"BARCODE"]]
sku = [b for b in catalog.loc[:,"SKU"]]
product = [c for c in catalog.loc[:,"PRODUCT"]]
product = sorted(product)

barsku = dict() # barcode: SKU
barproduct = dict() # barcode: product
skuproduct = dict() # SKU: product


for i in range(len(sku)):
    barsku[barcodes[i]]=sku[i]

for i in range(len(sku)):
    barproduct[barcodes[i]]=product[i]
    
for i in range(len(sku)):
    skuproduct[sku[i]]=product[i]    


# In[8]:


# manual input csv --> dictionary --> dataframe

print("System Activated. Welcome User!")
print("Date Today: " + str(datetime.datetime.now()))
print("Please Select An Option")

catalog2 = pd.read_csv("Product-Catalogue.csv")
mf = pd.read_csv("HDB-Master-File.csv")

command = "1"
while(True):
    valid_entry = False
    while (not valid_entry):
        try:
            command = int(input("Options: 1-Event Log, 2-Running Balance, 3-Inventory History, 0-Quit "))
            valid_entry = True
        except ValueError:
            print("Non-numeric data entered. Please enter valid option.") 
    if (int(command)==1):
        el_options = 1
        while(True):
            valid_entry = False
            while (not valid_entry):
                try:
                    el_option= int(input("Options: 1-Existing, 2-Add New Product, 0-Back "))
                    valid_entry = True
                except ValueError:
                    print("Non-numeric data entered. Please enter valid option.") 
            if (int(el_option)==1):
                #refreshing all files
                mf = pd.read_csv("HDB-Master-File.csv")
                catalog = pd.read_csv("Product-Catalogue.csv")
                barcodes = [str(a) for a in catalog.loc[:,"BARCODE"]]
                sku = [b for b in catalog.loc[:,"SKU"]]
                product = [c for c in catalog.loc[:,"PRODUCT"]]
                product = sorted(product)

                barsku = dict() # barcode: SKU
                barproduct = dict() # barcode: product
                skuproduct = dict() # SKU: product


                for i in range(len(sku)):
                    barsku[barcodes[i]]=sku[i]

                for i in range(len(sku)):
                    barproduct[barcodes[i]]=product[i]

                for i in range(len(sku)):
                    skuproduct[sku[i]]=product[i]  
                
                options = 1
                while(True):
                    valid_entry = False
                    while (not valid_entry):
                        try:
                            options = int(input("Options: 1-Log Inflow, 2-Log Outflow, 0-Back "))
                            valid_entry = True
                        except ValueError:
                            print("Non-numeric data entered. Please enter valid option.") 
                    if (int(options)==1):
                        start = datetime.datetime.now()
                        currentdate = start.strftime("%m/%d/%Y") 
                        currenttime = start.strftime("%H:%M")
                        skuInput = input("SKU: ").upper()
                        while(skuInput not in sku):
                            print("Please enter valid SKU.")
                            skuInput = input("SKU: ")
                        valid_entry = False
                        while (not valid_entry):
                            try:
                                inflow = int(input("Enter Quantity: "))
                                valid_entry = True
                            except ValueError:
                                print("Non-numeric data entered.") 

        

                        mf = mf.append({"DATE":currentdate,"TIME":currenttime,"PRODUCT":skuproduct[skuInput],"SKU":skuInput,"INFLOW":int(inflow),"OUTFLOW":0},ignore_index=True)
                        new_mf = pd.DataFrame(mf)
                        new_mf.to_csv("HDB-Master-File.csv", sep=',',index=False)
                        mf = pd.read_csv("HDB-Master-File.csv")

                    if (int(options)==2):
                        print("Current Option: Log Outflow \n Note: \n - file must be in .csv \n - header of CSV is 'barcode' \n - CSV file must be in the same folder as inventory system program")
                        inputfile = input("Filename: ")
                        master = pd.read_csv(inputfile)
                        barcode_tally = {}

                        for k in barcodes:
                            barcode_tally[k] = 0

                        for i in master.loc[:,"barcode"]:
                            if str(i)[-1:]=="x":
                                continue
                            else:
                                barcode_tally[str(i)] += 1

                        start = datetime.datetime.now()
                        currentdate = start.strftime("%m/%d/%Y") 
                        currenttime = start.strftime("%H:%M")

                        for i in barcode_tally:
                            if barcode_tally[i]!=0:
                                mf = mf.append({"DATE":currentdate,"TIME":currenttime,"PRODUCT":barproduct[i],"SKU":barsku[i],"INFLOW":0,"OUTFLOW":barcode_tally[i]},ignore_index=True)

                        finalDF = pd.DataFrame(mf)
                        finalDF.to_csv("HDB-Master-File.csv", sep=',',index=False)

                        precount = [str(i) for i in master.loc[:,"barcode"]]
                        postcount = []

                        for i in precount:
                            if i[-1:]=="x":
                                postcount.append(i)
                            else:
                                i += "x"
                                postcount.append(i)

                        master.loc[:,"barcode"] = [i for i in postcount]
                        newScans = pd.DataFrame(master)
                        newScans.to_csv(inputfile, sep=',',index=False)
                        
                    if (int(options)==0):
                        break
                    

            if (int(el_option)==2):
                start = datetime.datetime.now()
                currentdate = start.strftime("%m/%d/%Y") 
                currenttime = start.strftime("%H:%M")
                newbar = input("New Barcode: ")
                while(newbar in barcodes):
                    print("Barcode already exists. Please enter new barcode.")
                    newbar = (input("Barcode: "))
                newsku = input("New SKU: ").upper()
                while(newsku in sku):
                    print("SKU already exists.Please enter new SKU.")
                    newsku = input("SKU: ")
                newproduct = (input("New Product: ")).title()
                while(newproduct in product):
                    print("Product name already exists.Please enter new product name.")
                    newproduct = input("Product Name: ")
                catalog2 = catalog2.append({"BARCODE":newbar,"SKU":newsku,"PRODUCT":newproduct},ignore_index=True)
                newcatalog = pd.DataFrame(catalog2)
                newcatalog.to_csv("Product-Catalogue.csv", sep=',',index=False)
                catalog2 = pd.read_csv("Product-Catalogue.csv")

                mf = mf.append({"DATE":currentdate,"TIME":currenttime,"PRODUCT":newproduct,"SKU":newsku,"INFLOW":0,"OUTFLOW":0},ignore_index=True)
                new_mf = pd.DataFrame(mf)
                new_mf.to_csv("HDB-Master-File.csv", sep=',',index=False)
                mf = pd.read_csv("HDB-Master-File.csv")

            if (int(el_option)==0):
                break
                
            
    if (int(command)==2):
        pc_option =1
        while(True):
            valid_entry = False
            while (not valid_entry):
                try:
                    pc_option = int(input("Options: 1-All, 2-Specific Product, 0-Back "))
                    valid_entry = True
                except ValueError:
                    print("Non-numeric data entered. Please enter valid option.")
            if (int(pc_option)==1):
                skudictmany = dict()

                for i in sku:
                    mf2 = mf.loc[mf.loc[:,"SKU"]==i]
                    balance = mf2.loc[:,"INFLOW"].sum()-mf2.loc[:,"OUTFLOW"].sum()
                    skudictmany[i]=balance

                for i in skudictmany:
                    print (" ")
                    print("Running Balance of "+skuproduct[i]+": "+str(skudictmany[i]))

            if (int(pc_option)==2):

                targetsku = input("SKU: ").upper()
                while(targetsku not in sku):
                    print("SKU does not exist. Please enter existing SKU.")
                    targetsku = input("SKU: ")
                
                mf0 = mf.loc[mf.loc[:,"SKU"]==targetsku]
                balance = mf0.loc[:,"INFLOW"].sum()-mf0.loc[:,"OUTFLOW"].sum()

                print("Running Balance of "+skuproduct[targetsku]+": "+str(balance))
            
            if (int(pc_option)==0):
                break
            

    if (int(command)==3):
        ih_option = 1
        while(True):
            valid_entry = False
            while (not valid_entry):
                try:
                    ih_option = int(input("Options: 1-By Date, 2-By Product, 0-Back "))
                    valid_entry = True
                except ValueError:
                    print("Non-numeric data entered. Please enter valid option.")           

            if(int(ih_option)==1):
                ih_date = 0
                ih_date = input("Date '(MM/DD/YYYY)': ")
                date_pattern = r'[0-1][0-9]/[0-3][0-9]/[0-9][0-9][0-9][0-9]'
                while re.search(date_pattern, ih_date)==None:
                    ih_date = input("Wrong date format. Try again: '(MM/DD/YYYY)': ")
                date_match = str(re.search(date_pattern,str(ih_date)).group())
                dates = mf.set_index('DATE').filter(regex=date_match,axis=0)
                print("")
                print(dates)
                print("")
                
            if(int(ih_option)==2):
                ih_product_sku = input("Product SKU: ").upper()
                while(ih_product_sku not in sku):
                    print("SKU does not exist. Please enter existing SKU.")
                    ih_product_sku = input("SKU: ")
                
                specific_product = mf.loc[mf.loc[:,"SKU"]==str(ih_product_SKU)]
                print(specific_product)
                print("Specific Product")
                print("")
            
            if(int(ih_option)==0):
                break

              
    if(int(command)==0):
        print("Quit")
        break


# In[ ]:




