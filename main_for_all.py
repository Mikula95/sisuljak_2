from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate/<question>', methods=['POST'])
def calculate(question):
    if question == 'A1':
        return calculate_a1()
    elif question == 'A2':
        return calculate_a2()
    elif question == 'A3':
        return calculate_a3()
    elif question == 'B1':
        return calculate_b1()
    elif question == 'B2':
        return calculate_b2()

def calculate_a1():
    column_names = ["#Taxid", "Ensembl_protein", "Gn", "Mean-copy-number"]
    df = pd.read_csv("./inputs/9606_abund.csv", sep='\t', names=column_names, comment="#")
    unique_values = df.drop_duplicates(subset=['Gn', 'Mean-copy-number']).shape[0]
    return jsonify(result=unique_values)
# 
def calculate_a2():
    column_names = ["#Taxid", "Ensembl_protein", "Gn", "Mean-copy-number"]
    df = pd.read_csv("./inputs/9606_abund.csv", sep='\t', names=column_names, comment="#")    
    grouped = df.groupby('Gn')['Mean-copy-number'].agg(['mean', 'std']).reset_index()
    grouped = grouped.fillna("Not available")
    result = grouped.to_dict(orient='records')

    return jsonify(result=result)
 

def calculate_a3():
    column_names = ["#Taxid", "Ensembl_protein", "Gn", "Mean-copy-number"]
    df = pd.read_csv("./inputs/9606_abund.csv", sep='\t', names=column_names, comment="#")
    df_unique = df.drop_duplicates(subset=['Gn'])
    df_unique['Percentile'] = df_unique['Mean-copy-number'].rank(pct=True)
    result = df_unique[['Gn', 'Percentile']].to_dict(orient='records')

    return jsonify(result=result)

def calculate_b1():
    column_names = ["#Taxid", "Ensembl_protein", "Gn", "Mean-copy-number"]
    column_names_a = ["Gn","Domain","Start","End","Eval"]
    abund_df = pd.read_csv('./inputs/9606_abund.csv', sep='\t', names=column_names, comment='#')
    domains_df = pd.read_csv('./inputs/9606_gn_dom.csv', sep='\t', names=column_names_a, comment='#')
    merged_df = pd.merge(domains_df, abund_df, on='Gn')
    grouped = merged_df.groupby('Domain')['Mean-copy-number'].mean()
    highest_abundance_value = grouped.max()
    
    return jsonify(result=highest_abundance_value)

def calculate_b2():
    column_names = ["#Taxid", "Ensembl_protein", "Gn", "Mean-copy-number"]
    column_names_a = ["Gn","Domain","Start","End","Eval"]
    abund_df = pd.read_csv('./inputs/9606_abund.csv', sep='\t', names=column_names, comment='#')
    domains_df = pd.read_csv('./inputs/9606_gn_dom.csv', sep='\t', names=column_names_a, comment='#')
    abund_df.rename(columns={'#Taxid': 'Taxid'}, inplace=True)
    merged_df = pd.merge(domains_df, abund_df, on='Gn')
    domain_stats = merged_df.groupby(['Gn', 'Domain'])['Mean-copy-number'].agg(['mean', 'std']).reset_index()
    domain_stats['mean_percentile'] = domain_stats['mean'].rank(pct=True) * 100
    domain_stats['std_percentile'] = domain_stats['std'].rank(pct=True) * 100
    mean_table = domain_stats[['Gn', 'Domain', 'mean', 'mean_percentile']]
    std_table = domain_stats[['Gn', 'Domain', 'std', 'std_percentile']]

    data = {
        'mean_table': mean_table.to_dict(orient='records'),
        'std_table': std_table.to_dict(orient='records')
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
