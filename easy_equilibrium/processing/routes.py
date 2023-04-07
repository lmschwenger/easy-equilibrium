import os

import numpy as np
import plotly.graph_objects as go
from flask import request, Blueprint, render_template

from easy_equilibrium.processing.helper_functions import get_pka_data, chemical_equilibrium

equilibrium_page = Blueprint('equilibrium_page', __name__)


@equilibrium_page.route('/', methods=['GET', 'POST'])
def graph_page():
    pKa2 = None
    pH_range = np.array([round(val, 2) for val in np.arange(0, 14.1, 0.1)])
    pka_dict = get_pka_data()

    # Get the selected dropdown value
    selected_category = request.form.get('dropdown', default=list(pka_dict.keys())[0])

    # Create the layout
    layout = go.Layout(title='Graphs for ' + selected_category,
                       xaxis=dict(range=[0, 14]),
                       yaxis=dict(range=[0, 1])
                       )

    # Combine the plots and layout into a figure
    fig = go.Figure(layout=layout)

    compound = pka_dict[selected_category]
    # Create the plots
    if len(compound.values()) > 1:

        acid_name = selected_category
        conj1_name = list(compound.keys())[0]
        conj2_name = list(compound.keys())[1]

        pKa1 = list(compound.values())[0]
        pKa2 = list(compound.values())[1]

        K1 = 10 ** (-pKa1)
        K2 = 10 ** (-pKa2)

        chemical_conc = 1
        H_conc = 10 ** (-pH_range)
        # Calculate the concentrations of the species at each pH value
        # Calculate the concentrations of H2S, HS-, and S2- at each pH value

        acid = ((H_conc ** 2) /
                (H_conc ** 2 + K1 * H_conc + K1 * K2)) * chemical_conc
        conj1 = ((K1 * H_conc) /
                 (H_conc ** 2 + K1 * H_conc + K1 * K2)) * chemical_conc
        conj2 = (K1 * K2 /
                 (H_conc ** 2 + K1 * H_conc + K1 * K2)) * chemical_conc

        curves = {acid_name: acid,
                  conj1_name: conj1,
                  conj2_name: conj2}

    else:
        acid_name = selected_category
        conj_name = list(compound.keys())[0]
        pKa1 = list(compound.values())[0]
        acid, conj = chemical_equilibrium(pKa1, pH_range=pH_range)
        curves = {acid_name: acid,
                  conj_name: conj}

    for name, curve in curves.items():
        fig.add_trace(go.Scatter(x=pH_range, y=curve, name=name, mode='lines'))

    headers = ['pH']
    list_of_values = [list(pH_range)]
    pka_values = [pKa1] if not pKa2 else [pKa1, pKa2]
    for name, values in curves.items():
        headers.append(name)
        list_of_values.append([round(val, 3) for val in values])

    zipped = list(zip(*list_of_values))

    path_to_here = os.path.dirname(__file__)
    filepath = os.path.join(path_to_here, os.pardir, 'static', 'data', f"{selected_category}.txt")

    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(','.join(headers) + '\n')
            for row in zipped:
                row_str = ','.join(str(val) for val in row) + '\n'
                f.write(row_str)

    # Render the HTML template with the dropdown menu and graph
    return render_template('easy_equilibrium.html', options=pka_dict.keys(), graph=fig.to_html(), headers=headers,
                           data=zipped, pka_values=pka_values)
