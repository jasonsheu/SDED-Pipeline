class Address:
    def __init__(self, properties: dict):
        std_plist = ['First_name', 'Last_name', 'Organization', 'Address1', 'Address2', 'Address3', 'City', 'State', 'Zip', 'Country_non-US']

        # for p in std_plist:
        #     print(f"self.{p} = properties['{p}']")

        self.first_name = properties['First_name']
        self.last_name = properties['Last_name']
        self.organization = properties['Organization']
        self.address1 = properties['Address1']
        self.address2 = properties['Address2']
        self.address3 = properties['Address3']
        self.city = properties['City']
        self.state = properties['State']
        self.zip = properties['Zip']
        self.country = properties['Country_non-US']
        


        self.plist = [properties[p] for p in std_plist]

    def __str__(self) -> str:
        return str(self.plist)

    def __repr__(self) -> str:
        return str(self)
    
    def __iter__(self):
        return iter(self.plist)

    def __next__(self):
        return next(self.plist)
