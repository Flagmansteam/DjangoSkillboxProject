from io import TextIOWrapper
from csv import DictReader

def save_csv_products(file, encoding):
    #из байт получаем строчки
    csv_file = TextIOWrapper(
        file,
        encoding=encoding,
    )
    reader = DictReader(csv_file)

    products =[Product(**row) for row in reader]
    Product.objects.bulk_create(products)
    #создаём несколько объектов сразу с помощью bulk_create

    return products