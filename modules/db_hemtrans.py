# -*- coding: utf-8 -*-

from gluon import Field

def get_db(db, auth):
    db.define_table('typ_vozidla',
        Field('typ', 'string', length=64),
        Field('mist', 'integer'),
        Field('delka', 'integer'),
        format='%(typ)s'
        )

    db.define_table('sedadlo',
        Field('typ_vozidla_id', db.typ_vozidla),
        Field('cislo', 'integer'),
        Field('nabizeno', 'boolean'),
        Field('odpredu', 'integer'),
        Field('od_osy', 'integer'),
        format='%(cislo)s'
        )
