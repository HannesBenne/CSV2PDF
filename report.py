import os
import subprocess
import codecs
import pandas as pd
import codecs
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import locale
from locale import atof
from jinja2 import Template
import jinja2

data = pd.read_csv('jahresuebersicht.csv', delimiter=';', thousands='.', encoding = "ISO-8859-1")
data.dropna(axis=1, inplace=True)

locale.setlocale(locale.LC_NUMERIC, '')
data['Preis'] = data['Preis'].apply(atof)
data['Einheit'] = data['Einheit'].apply(int)

#Monate als Kategorie festlegen damit sie nicht alphabetisch sondern nach Reihenfolge im Kalender sortiert werden
months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
data['Monat'] = pd.Categorical(data['Monat'], categories=months, ordered=True)
data['Umsatz'] = data['Einheit'] * data['Preis']

profit_data = data.groupby('Monat').sum()[['Einheit','Umsatz']]
profit_data.sort_index()
min_sales_mon = profit_data.Umsatz.idxmin()
min_sales_val = profit_data.Umsatz.min()
max_sales_mon = profit_data.Umsatz.idxmax()
max_sales_val = profit_data.Umsatz.max()
sales_year = profit_data.Umsatz.sum()

rcParams['figure.figsize'] = 14.7,8.27
sns.set()
month_sales_plot = sns.lineplot(data = data, x = 'Monat', y = 'Umsatz', palette = 'Blues_d', ci = None)
month_sales_plot.set_xlabel("Monat",fontsize=16)
month_sales_plot.set_ylabel("Umsatz in €",fontsize=15)
month_sales_plot.tick_params(labelsize=14)
month_sales_plot.figure.savefig(r"img\jahresumsatz.png")

customer_data = data.groupby('Kunde').Einheit.sum()
customer_data = customer_data.sort_values(ascending=False)
top_customer = (customer_data.index[0], customer_data[0])
second_customer = (customer_data.index[1], customer_data[1])
third_customer = (customer_data.index[2], customer_data[2])
flop_costomer = (customer_data.index[-1], customer_data[-1])
max_3 = sorted(list(customer_data.sort_values(ascending = False).iloc[0:3].index))

top_customer_plot = sns.barplot(data = data[data['Kunde'].isin(max_3)], x = 'Kunde', y = 'Umsatz', palette = 'Blues_d', ci=None)
top_customer_plot.set_xlabel("Kunde",fontsize=16)
top_customer_plot.set_ylabel("Umsatz in €",fontsize=15)
top_customer_plot.tick_params(labelsize=14)
top_customer_plot.figure.savefig(r'img\top_kunden.png')

product_data = data.groupby('Warengruppe').Umsatz.sum()
product_data.sort_values(ascending=False, inplace=True)

top_product = (product_data.index[0], product_data[0])
flop_product = (product_data.index[-1], product_data[-1])

top_data = data[data.Warengruppe == top_product[0]].groupby('Monat').sum()
top_data['Monatsnummer'] = range(1,13)

flop_data = data[data.Warengruppe == flop_product[0]].groupby('Monat').sum()
flop_data['Monatsnummer'] = range(1,13)

fig, axes = plt.subplots(1, 2)
fig.set_size_inches(14, 4)
p1 = sns.regplot(data = flop_data[flop_data.Umsatz !=0], x = 'Monatsnummer', y = 'Umsatz', ax=axes[0]).set_title("Flop Produkt: " + flop_product[0])
p2 = sns.regplot(data = top_data, x = 'Monatsnummer', y = 'Umsatz', ax=axes[1]).set_title("Top Produkt: " + top_product[0])
fig.savefig(r'img\flopundtop.png')

latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.')))

template = latex_jinja_env.get_template('report_template.tex')
texfile = template.render(Gesamtumsatz = int(sales_year),
                      Maxmonat = max_sales_mon,
                      Maxumsatz = int(max_sales_val),
                      Minmonat = min_sales_mon,
                      Minumsatz = int(min_sales_val),
                      Kunde1 = top_customer[0],
                      Umsatz1 = int(top_customer[1]),
                      Kunde2 = second_customer[0],
                      Umsatz2 = int(second_customer[1]),
                      Kunde3 = third_customer[0],
                      Umsatz3 = int(third_customer[1]),
                      Topprodukt = top_product[0],
                      Topumsatz = int(top_product[1]),
                      Flopprodukt = flop_product[0],
                      Flopumsatz = int(flop_product[1])
                     )

with codecs.open('report.tex', 'w', 'utf-8') as file:
    file.write(texfile)

return_value = subprocess.call(['pdflatex', 'report.tex'], shell=False)
if(return_value):
    print('Fehler beim compilieren der tex Datei')

