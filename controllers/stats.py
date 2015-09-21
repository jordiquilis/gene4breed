# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport


@auth.requires_membership('manager')
def index():
    return dict()


@auth.requires_membership('manager')
def datapoints_and_plants():
    species = db(db.species).select()
    return dict(species=species)


@auth.requires_membership('manager')
def species_options():
    session.forget(response)
    species = db().select(db.species.name, distinct=True, orderby=db.species.name)
    return dict(species=species)
 

@auth.requires_membership('manager')
def species_types():
    session.forget(response)
    try:
        species_types = db(db.species_types.species==request.vars.specie_id).select()
    except:
        species_types = []
    return dict(species_types=species_types)


@auth.requires_membership('manager')
def specie_type_stats():
    specie = db(db.species.id == request.vars.specie_id).select().first()
    specie_type = db(db.species_types.id == request.vars.species_types).select().first()
    stats = {}
    stats['Total DPs'] = db((db.exp_plant_marker.plant==db.plants.id) & 
                                            (db.plants.plant_line==db.plant_lines.id) &
                                            (db.plant_lines.species_type==specie_type.id)).count()
    stats['Useful DPs'] = db((db.exp_plant_marker.plant==db.plants.id) &              
                            (db.plants.plant_line==db.plant_lines.id) &
                            (db.plant_lines.species_type==specie_type.id) & 
                            (db.exp_plant_marker.marker_value=='nd')).count()
    stats['% Useful DPs'] = str(round((float(stats['Useful DPs']) / float(stats['Total DPs']))*100., 2)) + '%'
    stats['Total Number of Markers'] = len(db((db.exp_plant_marker.plant==db.plants.id) &
                                           (db.plants.plant_line==db.plant_lines.id) &
                                           (db.plant_lines.species_type==specie_type.id)).select(groupby=db.exp_plant_marker.marker))
    stats['Total Number of Plants'] = len(db((db.exp_plant_marker.plant==db.plants.id) &
                                         (db.plants.plant_line==db.plant_lines.id) &
                                         (db.plant_lines.species_type==specie_type.id)).select(groupby=db.plants.name))
    return dict(specie=specie, specie_type=specie_type, stats=stats)
