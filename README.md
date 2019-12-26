# CSV2PDF

Das Skript 'report.py' liest Daten mit Verlaufszahlen aus der Datei 'jahresuebersicht.csv' ein, 
berechnet welche Kunden und welche Produkte die besten/ schlechtesten Verkaufszahlen haben und erzeugt Diagramme  
um die Daten zu visualisieren.
Die berechneten Daten und Diagramme werden mit der Templating-Engine Jinja in die Latexvorlage 'report_template.txt' eingefügt und dann 
mit pdflatex kompiliert um ein PDF Report über die Verkaufszahlen zu erzeugen. 

Das jupyter notebook 'report.ipynb' kann genutzt werden um mit den Daten zu experimentieren. 

![](https://github.com/HannesBenne/CSV2PDF/blob/master/img/rme.PNG)
