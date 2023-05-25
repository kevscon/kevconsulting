from flask import Flask, render_template, request, jsonify, send_file
from app import app
import json, os


@app.route('/', methods=['GET', 'POST'])
def home():
    from app.app.nbi_search.forms import SearchForm
    form = SearchForm()
    from app.app.nbi_search.route_funcs import get_states
    state_options = get_states()
    form.state_postal.choices = state_options

    if request.method == 'POST':
        state_postal = request.form['state_postal']
        from app.app.nbi_search.route_funcs import filter_bridges
        bridge_list = filter_bridges()
        return render_template(
			'filtered-bridges.html',
            state_postal=state_postal,
            bridge_list=bridge_list
			)
    return render_template('home.html', form=form)


@app.route('/<state_postal>/counties', methods=['GET'])
def county_options(state_postal):
    from app.app.nbi_search.route_funcs import filter_counties
    county_names = sorted(filter_counties(state_postal))
    return jsonify({'county_names': county_names})


@app.route('/<state_postal>/<structure_number>', methods=['GET'])
def bridge_data(state_postal, structure_number):
    from app.app.nbi_search.route_funcs import return_bridge_properties
    bridge_data = return_bridge_properties(state_postal, structure_number)
    return render_template('bridge-data.html', bridge_data=bridge_data)


@app.route('/download')
def download_file():
    import os
    path = os.getcwd() + '/app/app/nbi_search/data/nbi_output.xlsx'
    return send_file(path, as_attachment=True, cache_timeout=0)

# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'),404
#
#
# @app.errorhandler(500)
# def internal_error(error):
#     return render_template('500.html'),500
