class Perfume:
    description = ''
    usage = ''
    country = ''

    def __init__(self, href, item, name, price):
        self.href = href
        self.item = item
        self.name = name
        self.price = price

    def set_inner_data(self, description, usage, country):
        self.description = description
        self.usage = usage
        self.country = country

    def __repr__(self):
        return f'{self.item} - {self.name}'

    def get_params(self):
        return self.href, self.item, self.name, self.price, self.description, self.usage, self.country
