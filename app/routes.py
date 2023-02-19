from flask import Flask, render_template, request, send_file, jsonify
from app import app
import os, json
import pandas as pd


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/steel-shapes', methods=['GET', 'POST'])
def steel_shapes():
    from app.app.steel_shapes.forms import InputForm
    form = InputForm()
    if request.method == 'POST':
        from app.app.steel_shapes.route_funcs import process_form
        output_dict = process_form()
        return render_template(
			'steel-shape-properties.html',
            output_dict=output_dict
			)
    return render_template('steel-shape-search.html', form=form)

@app.route('/<shape_section>/shape-designations')
def shape_designation_options(shape_section):
    from app.app.steel_shapes.route_funcs import filter_designations
    shape_designations = filter_designations(shape_section)
    return jsonify({'shape_designations': shape_designations})

@app.route('/<shape_section>/<shape_designation>/shape-labels')
def shape_label_options(shape_section, shape_designation):
    from app.app.steel_shapes.route_funcs import filter_labels
    shape_labels = filter_labels(shape_section, shape_designation)
    return jsonify({'shape_labels': shape_labels})

@app.route('/download')
def download_file():
    import os
    path = os.getcwd() + '/app/app/steel_shapes/shape_properties.xlsx'
    return send_file(path, as_attachment=True, cache_timeout=0)


@app.route('/historic-steel-shapes', methods=['GET', 'POST'])
def historic_steel_shapes():
    from app.app.steel_shapes.forms import HistoricInputForm
    form = HistoricInputForm()
    if request.method == 'POST':
        from app.app.steel_shapes.route_funcs import process_historic_form
        output_dict = process_historic_form()
        return render_template(
			'historic-steel-shape-properties.html',
            output_dict=output_dict
			)
    return render_template('historic-steel-shape-search.html', form=form)

@app.route('/<edition>/<shape_type>/historic-shape-sections')
def historic_shape_section_options(edition, shape_type):
    from app.app.steel_shapes.route_funcs import filter_historic_sections
    shape_sections = filter_historic_sections(edition, shape_type)
    return jsonify({'shape_sections': shape_sections})

@app.route('/<edition>/<shape_section>/historic-shape-labels')
def historic_shape_label_options(edition, shape_section):
    from app.app.steel_shapes.route_funcs import filter_historic_labels
    shape_labels = filter_historic_labels(edition, shape_section)
    return jsonify({'shape_labels': shape_labels})


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500
