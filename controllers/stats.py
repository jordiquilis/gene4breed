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
    try:
        int(request.vars.specie_id)
        int(request.vars.species_types)
    except:
        redirect(URL('stats', 'datapoints_and_plants'))
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


@auth.requires_membership('manager')
def genotype_comparison():
    species = db(db.species).select()
    return dict(species=species)


@auth.requires_membership('manager')
def plant_genotype_comparison():
    try:
        int(request.vars.specie_id)
        int(request.vars.species_types)
    except:
        redirect(URL('stats', 'plant_genotype_comparison'))
    specie = db(db.species.id == request.vars.specie_id).select().first()
    specie_type = db(db.species_types.id == request.vars.species_types).select().first()
    plants = [row for row in db((db.plants.plant_line==db.plant_lines.id) &
                                (db.plant_lines.species_type==specie_type.id)).select(db.plants.id, db.plants.name, groupby=db.plants.name)]
    comparison = None
    if request.vars.plants_to_compare and request.vars.reference_plant:
        reference_markers_raw = db(db.exp_plant_marker.plant == request.vars.reference_plant).select()
        reference_markers = {}
        for row in reference_markers_raw:
            reference_markers[row['exp_plant_marker.marker']] = row['exp_plant_marker.marker_value']
        to_compare = []
        plant_ids = []
        if isinstance(request.vars.plants_to_compare, list):
            plant_ids = request.vars.plants_to_compare
        else:
            plant_ids.append(request.vars.plants_to_compare)

        for plant_id in plant_ids:
            raw = db(db.exp_plant_marker.plant == plant_id).select()
            values = {}
            for row in raw:
                values[row['exp_plant_marker.marker']] = row['exp_plant_marker.marker_value']
            to_compare.append(values)
        results = {}
        for i, plant_id in enumerate(plant_ids):
            id = int(plant_id)
            results[id] = {'score': 0}
            for marker in reference_markers.keys():
                if to_compare[i].has_key(marker):
                    if reference_markers[marker] == to_compare[i][marker]:
                        results[id]['score'] += 2
                    else:
                        if reference_markers[marker] == 'H' or to_compare[i][marker] == 'H':
                            results[id]['score'] += 1
        num_markers = len(reference_markers)
        for i, plant_id in enumerate(plant_ids):
            plant_id = int(plant_id)
            for plant in plants:
                if plant.id == plant_id:
                    results[plant_id]['plant_name'] = plant.name
                    results[plant_id]['score'] = float(results[plant_id]['score'])/(num_markers*2.)

        comparison = {'results': results, 'reference:': request.vars.reference_plant, 'to_compare': request.vars.plants_to_compare}
    return dict(specie=specie, specie_type=specie_type, plants=plants, comparison=comparison)

