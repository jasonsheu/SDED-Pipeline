import c2mAPI
import pandas as pd


class RagicMailer:

    def __init__(self, file, username, password):
        self.df = pd.read_csv(file)
        self.username = username
        self.password = password


    def send_all_mail(self, filename, path):
        c2m = c2mAPI.c2mAPIBatch(self.username, self.password, "0") #change to 1 for production
        c2m.setFileName(filename, path) #set the name ane file path for batch
        
        #change to appropriate address and options
        po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on Separate Page','Full Color','White 24#','Printing both sides','First Class','#10 Double Window')
        ad = c2mAPI.returnAddress("Jason Sheu","SDED","3855 Nobel Drive","apt 2101","La Jolla","CA","92122")

        addList = [] #field names cannot change
        for i in range(len(self.df)):
            addList.append(self.df.iloc[i].to_dict())

        return addList

#         c2m.addJob("1","2",po,ad,addList)
#         print(c2m.runAll().text)

    def send_specific(self, name, organization , address1, address2 , address3 , city, state, postalCode, country, filename, path):
        c2m = c2mAPI.c2mAPIBatch(self.username, self.password, "1") #change to 1 for production
        c2m.setFileName(filename, path) #set the name ane file path for batch

        #change to appropriate address and options
        po = c2mAPI.printOptions('Letter 8.5 x 11','Next Day','Address on Separate Page','Full Color','White 24#','Printing both sides','First Class','#10 Double Window')
        ad = c2mAPI.returnAddress("Jason Sheu","SDED","3855 Nobel Drive","apt 2101","La Jolla","CA","92122")

        addList = []
        address = {'name': name,
                   'organization': organization,
                   'address1': address1,
                   'address2': address2,
                   'address3': address3,
                   'city': city,
                   'state': state,
                   'postalCode': postalCode,
                   'country':country}
        addList.append(address)
        c2m.addJob("1","2",po,ad,addList) # start page, stop page

        #this line sends the mail through the api
        print(c2m.runAll().text)
