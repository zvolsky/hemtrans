# -*- coding: utf-8 -*-

SED_SIRKA = 46
SED_VYSKA = 32

drift_sirka = SED_SIRKA / 2
drift_vyska = 125 - SED_VYSKA / 2

@auth.requires_membership('admin')
def situace():
    if len(request.args)<1:
        redirect(URL('default', 'index'))
    vozidlo = db(db.typ_vozidla.id==request.args[0]).select().first()
    sedadla = db(db.sedadlo.typ_vozidla_id==request.args[0]).select()
    img_vozidlo = DIV(_id="vozidlo", _style="position: relative; width: 300px; height: %spx; background-color: grey; overflow: hidden" % (vozidlo.delka/2))
    for sedadlo in sedadla:
        img_vozidlo.append(DIV(sedadlo.cislo, _class="sedadlo", _id="s%s" % sedadlo.cislo,
                _style="position: absolute; background-color: yellow; width: 46px; height: 32px; top: %spx; left:%spx" % (sedadlo.odpredu/2 - drift_vyska, sedadlo.od_osy + drift_sirka)))
    return dict(img=img_vozidlo)
