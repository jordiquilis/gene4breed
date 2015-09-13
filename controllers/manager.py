# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport


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


@auth.requires_membership('manager')
def import_traits():
    return dict()


@auth.requires_membership('manager')
def import_markers():
    return dict()


@auth.requires_membership('manager')
def import_experiment_data():
    return dict()
