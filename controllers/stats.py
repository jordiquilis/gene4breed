# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport

import fasta_util
import clustal_util
import os


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
        # Let's check parameters
        int(request.vars.specie_id)
        int(request.vars.species_types)
    except:
        redirect(URL('stats', 'datapoints_and_plants'))

    # Get specie and specie type
    specie = db(db.species.id == request.vars.specie_id).select().first()
    specie_type = db(db.species_types.id == request.vars.species_types).select().first()
    # Stats is a dictionary that will be shown in the view
    stats = {}
    stats['Total DPs'] = db((db.exp_plant_marker.plant==db.plants.id) & 
                                            (db.plants.plant_line==db.plant_lines.id) &
                                            (db.plant_lines.species_type==specie_type.id)).count()
    stats['Useful DPs'] = db((db.exp_plant_marker.plant==db.plants.id) &              
                            (db.plants.plant_line==db.plant_lines.id) &
                            (db.plant_lines.species_type==specie_type.id) & 
                            (db.exp_plant_marker.marker_value!='nd')).count()
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
    # Arguments check
    try:
        int(request.vars.specie_id)
        int(request.vars.species_types)
    except:
        redirect(URL('stats', 'plant_genotype_comparison'))
    # Get specie, specie type and the plants of this type
    specie = db(db.species.id == request.vars.specie_id).select().first()
    specie_type = db(db.species_types.id == request.vars.species_types).select().first()
    plants = [row for row in db((db.plants.plant_line==db.plant_lines.id) &
                                (db.plant_lines.species_type==specie_type.id)).select(db.plants.id, db.plants.name, groupby=db.plants.name)]
    reference_plant = None
    # Markers parsing
    comparison = None
    if request.vars.plants_to_compare and request.vars.reference_plant:
        reference_plant = db(db.plants.id == request.vars.reference_plant).select().first()
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
        # For each plant, we get their markers
        for plant_id in plant_ids:
            raw = db(db.exp_plant_marker.plant == plant_id).select()
            values = {}
            for row in raw:
                values[row['exp_plant_marker.marker']] = row['exp_plant_marker.marker_value']
            to_compare.append(values)

        # Here we calculate the score depending if they're equal or not
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
        # We prepare the results to be displayed in the view
        num_markers = len(reference_markers)
        for i, plant_id in enumerate(plant_ids):
            plant_id = int(plant_id)
            for plant in plants:
                if plant.id == plant_id:
                    results[plant_id]['plant_name'] = plant.name
                    results[plant_id]['score'] = float(results[plant_id]['score'])/(num_markers*2.)

        comparison = {'results': results, 'reference:': request.vars.reference_plant, 'to_compare': request.vars.plants_to_compare}
    return dict(specie=specie, specie_type=specie_type, plants=plants, comparison=comparison, reference=reference_plant)


@auth.requires_membership('manager')
def bio_genotype_comparison():
    species = db(db.species).select()
    return dict(species=species)


@auth.requires_membership('manager')
def bio_plant_genotype_comparison():
    try:
        int(request.vars.specie_id)
        int(request.vars.species_types)
    except:
        redirect(URL('stats', 'bio_genotype_comparison'))
    specie = db(db.species.id == request.vars.specie_id).select().first()
    specie_type = db(db.species_types.id == request.vars.species_types).select().first()
    plants = [row for row in db((db.plants.plant_line==db.plant_lines.id) &
                                (db.plant_lines.species_type==specie_type.id)).select(db.plants.id, db.plants.name, groupby=db.plants.name)]
    comparison = None
    if request.vars.plants_to_compare:
        plant_ids = []
        if isinstance(request.vars.plants_to_compare, list):
            plant_ids = request.vars.plants_to_compare
        else:
            redirect(URL('stats', 'bio_genotype_comparison'))
        
        to_compare = []
        for plant_id in plant_ids:
            # Get plant
            plant = db(db.plants.id == plant_id).select().first()
            # Get markers
            raw_markers = db(db.exp_plant_marker.plant == plant_id).select()
            markers = {}
            for row in raw_markers:
                markers[row['exp_plant_marker.marker']] = row['exp_plant_marker.marker_value']
            to_compare.append({'plant_id': plant.id, 'plant_name': plant.name, 'markers': markers})

        # Create the FASTA file
        fasta_file = fasta_util.create_fasta_file(to_compare)
        # Create the tree using clustalw
        tree_file = clustal_util.get_phylo_tree(fasta_file)
        tree_representation = None
        if tree_file:
            # Here we parse the tree from Phylo.draw_ascii function to be pretty in HTML format
            with open(tree_file) as input:
                lines = input.readlines()
                tree_representation = ''.join(lines)
                tree_repesentation = tree_representation.replace(' ', '&nbsp;')
            try:
                os.remove(tree_file)
            except:
                pass

        comparison = {'to_compare': to_compare, 'fasta_file':fasta_file, 'tree_file':tree_file, 'tree':tree_representation }

    return dict(specie=specie, specie_type=specie_type, plants=plants, comparison=comparison)

