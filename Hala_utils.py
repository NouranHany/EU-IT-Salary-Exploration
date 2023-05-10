german_cities=['Munich', 'Berlin', 'Hamburg', 'Wolfsburg', 'Stuttgart',
       'Schleswig-Holstein','Konstanz area', 'Frankfurt',
       'Cologne', 'Kempten', 'Münster', 'Erlangen','Rosenheim', 'Mannheim ', 'Boeblingen', 'Düsseldorf', 'Ingolstadt',
       'Nürnberg', 'Ansbach', 'Leipzig','Tuttlingen', 'Bonn','Koblenz','Heidelberg', 'Karlsruhe', 'Köln',
       'Aachen', 'Dusseldorf','Würzburg','Braunschweig ', 'Dresden','Stuttgart ','Lübeck', 'Nuremberg ', 'Bodensee', 'Paderborn',
       'Konstanz', 'Ulm', 'Düsseldorf ','Bölingen','Hannover','Siegen','Nuremberg', 'Friedrichshafen', 'Walldorf','Regensburg','Heilbronn',
       'Dortmund', 'Jena','Brunswick','Bielefeld','Hildesheim', 'Heidelberg ', 'Murnau am Staffelsee ','Hildesheim ','Dusseldurf','Darmstadt',
        'Duesseldorf','Ingolstadt ','Saarbrücken']



def write_category_freq(column_name, file_name,df):
    value_counts=df[column_name].value_counts()
    with open(file_name, 'w', encoding='utf-8') as f:
        # Loop through unique values and their counts
        for val, count in zip(value_counts.index, value_counts.values):
            # Write value and count to file
            f.write(f'{val}: {count}\n')