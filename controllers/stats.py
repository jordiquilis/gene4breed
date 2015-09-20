# -*- coding: utf-8 -*-

if 0:
    from __init__ import *  # @UnusedWildImport


@auth.requires_membership('manager')
def index():
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
