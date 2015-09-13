# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport

import csv_util
import file_util


@auth.requires_membership('manager')
def index():
    return dict()


@auth.requires_membership('manager')
def contact():
    grid = SQLFORM.smartgrid(db.contact)
    return dict(grid=grid)


@auth.requires_membership('manager')
def news():
    grid = SQLFORM.smartgrid(db.news)
    return dict(grid=grid)


@auth.requires_membership('manager')
def species():
    grid = SQLFORM.smartgrid(db.species)
    return dict(grid=grid)


@auth.requires_membership('manager')
def species_types():
    grid = SQLFORM.smartgrid(db.species_types)
    return dict(grid=grid)


@auth.requires_membership('manager')
def traits():
    grid = SQLFORM.smartgrid(db.traits)
    return dict(grid=grid)


@auth.requires_membership('manager')
def lines():
    grid = SQLFORM.smartgrid(db.plant_lines)
    return dict(grid=grid)


@auth.requires_membership('manager')
def experiments():
    grid = SQLFORM.smartgrid(db.experiments)
    return dict(grid=grid)


@auth.requires_membership('manager')
def users():
    grid = SQLFORM.smartgrid(db.auth_user)
    return dict(grid=grid)


@auth.requires_membership('manager')
def markers():
    grid = SQLFORM.smartgrid(db.markers)
    return dict(grid=grid)


@auth.requires_membership('manager')
def marker_values():
    grid = SQLFORM.smartgrid(db.exp_plant_marker)
    return dict(grid=grid)


@auth.requires_membership('manager')
def trait_values():
    grid = SQLFORM.smartgrid(db.exp_plant_trait)
    return dict(grid=grid)


@auth.requires_membership('manager')
def plants():
    grid = SQLFORM.smartgrid(db.plants)
    return dict(grid=grid)



def process_import_traits(form):
    file_name = form.vars.traits_csv_file.filename
    extension = file_util.get_file_extension(file_name)
    if extension not in ['.csv']:
        form.errors.traits_csv_file = 'Wrong file extension'
        return False
    return True


@auth.requires_membership('manager')
def import_traits():
    traits = []
    traits_errors = []
    traits_form = FORM(
                        INPUT(_name='traits_csv_file', _type='file'),
                        INPUT(_name='submit', _type='submit', _value='Import traits data')
                      )
    if traits_form.process(onvalidation=process_import_traits).accepted:
        traits = csv_util.parse_traits(traits_form.vars.traits_csv_file.file)
        for trait in traits:
            try:
                specie = db(db.species.name == trait['traits.species']).select().first()
                db.traits.insert(name=trait['traits.name'], species=specie.id, 
                            acronym=trait['traits.acronym'], genetic_control=trait['traits.genetic_control'], 
                            dominance=trait['traits.dominance'], related_markers=trait['traits.related_markers'], 
                            description=trait['traits.description'], project=trait['traits.project'])
            except:
                traits_errors.append(trait)
        if len(traits_errors):
            response.flash = 'Data imported with errors'
        else:
            response.flash = 'Data successfully imported'
    elif traits_form.errors:
        response.flash = 'Error in provided data'
    else:
        pass
                                                                     
    return dict(form=traits_form, traits=traits, traits_errors=traits_errors)


@auth.requires_membership('manager')
def import_markers():
    return dict()


@auth.requires_membership('manager')
def import_experiment_data():
    return dict()
