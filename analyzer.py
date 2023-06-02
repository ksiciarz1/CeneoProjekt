import os
import pandas
import json
from matplotlib import pyplot as plt
import numpy as np

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
opinions.iloc[:, 3] = opinions.iloc[:, 3].apply(
    lambda x: float(x.split('/')[0].replace(',', '.')))

# counts number of unique values and fill empty
stars = opinions.stars.value_counts().reindex(
    np.arange(0, 5, 0.5), fill_value=0)

recommendations = opinions['recommendation'].value_counts(
    dropna=True).reindex()

# bar
for index, value in enumerate(stars):
    plt.text(index, value+0.5, str(value), ha="center")

stars.plot.bar(color=['red', 'red', 'red', 'red', 'red',
               'blue', 'blue', 'blue', 'green', 'green'])

plt.title(label='Opinie')
plt.xlabel("Gwiazdki")
plt.ylabel("Liczba")
plt.xticks(rotation="horizontal")

for index, value in enumerate(stars):
    plt.text(index, value+0.5, str(value), ha="center")

plt.savefig(f"Charts/{productCode}_stars.png")
# plt.show()
plt.close()

# pie
recommendations.plot.pie(autopct='%1.2f%%', labels=["Polecam", "Nie polecam"])

plt.savefig(f"Charts/{productCode}_recommendations.png")
# plt.show()
plt.close()

stats = {
    'opinionsCount': len(opinions),
    'prosCount': len(list(filter(lambda x: len(x) > 0, opinions.iloc[:, 10]))),
    'consCount': len(list(filter(lambda x: len(x) > 0, opinions.iloc[:, 11]))),
    'averageScore': round(opinions.iloc[:, 3].mean(), 2)
}

output = [stats, stars.to_dict(), recommendations.to_dict()]


with open(f"Stats/{productCode}.json", "w", encoding='utf-8') as outfile:
    outfile.write(json.dumps(output, indent=4, ensure_ascii=False))

# print(f"""Dla produktu o identyfikatorze {productCode}
# pobrano {stats['opinionsCount']} opinii.
# Dla {stats['prosCount']} opinni podana została lista zalet produktu
# a dla {stats["consCount"]} opini podana została lista jego wad
# Średnia ocena poduktu to {stats["averageScore"]}.""")
