import os
import pandas
import matplotlib

# opinions = os.listdir('Opinions')

# for index, i in enumerate(opinions):
#     opinions[index] = opinions[index].split('.')[0]
#     print(opinions[index])
    
# print(opinions)

# print([filename.removesuffix(".json") for filename in os.listdir('Opinions')])

print(*list(map(lambda x: x. removesuffix(".json"), os.listdir("Opinions"))), sep='\n')

productCode = input('Podaj kod produktu: ')

opinions = pandas.read_json(f'Opinions/{productCode}.json')
# converting score from 4,5/5 format to float
opinions.iloc[:, 3] = opinions.iloc[:, 3].apply(lambda x: float(x.split('/')[0].replace(',', '.')))
print(opinions)

stats = {
    'opinionsCount' : len(opinions),
    'prosCount' : len(list(filter(lambda x: len(x) > 0, opinions.iloc[:, 10]))),
    'consCount' : len(list(filter(lambda x: len(x) > 0, opinions.iloc[:, 11]))),
    'averageScore' : round(opinions.iloc[:, 3].mean(), 2)
}

print(f"""Dla produktu o identyfikatorze {productCode}
pobrano {stats['opinionsCount']} opinii.
Dla {stats['prosCount']} opinni podana została lista zalet produktu
a dla {stats["consCount"]} opini podana została lista jego wad
Średnia ocena poduktu to {stats["averageScore"]}.""")