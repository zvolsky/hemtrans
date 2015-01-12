# -*- coding: utf-8 -*-

@auth.requires_membership('admin')
def sedadla():
    form = SQLFORM.factory(
            Field('typ_vozidla_id', db.typ_vozidla, requires = IS_IN_DB(db, db.typ_vozidla, db.typ_vozidla._format)),
            Field('leve', 'integer', default=1),
            Field('prave', 'integer', default=2),
            Field('predni', 'integer', default=175),
            Field('krok', 'integer', default=77),
            Field('zadni', 'integer'),
            Field('rad', 'integer', default=1),
            Field('cisla', 'string', comment='oddělit mezerami'),
            Field('cisluj', 'string', length=1, default='L', comment='L | R | None'),
            Field('nabizeno', 'boolean', comment='None: podle cisluj'),
            )
    if form.process().accepted:
        form.vars.pop('id')
        form.vars.cisla = form.vars.cisla.split() if form.vars.cisla else None
        form.vars.nabizeno = form.vars.nabizeno if form.vars.nabizeno else (True if form.vars.cisluj else False)
        insert_problem = sedadla_func(**form.vars)
        if insert_problem:
            return insert_problem
        redirect(URL('sedadla', 'situace', args=form.vars.typ_vozidla_id))
    return dict(form=form)

def sedadla_func(typ_vozidla_id, leve, prave, predni, krok=77, zadni=None, rad=1,
            cisla=None, cisluj='L', nabizeno=None,
            umisteni=(-100, -50, 0, 50, 100)):
    """
    leve 1..5  pozice na sirku
    prave 1..5 pozice na sirku
     napr. 1,2-dvojsedačka vlevo, 4,5-dvojsedačka vpravo, 1,5 pětisedačka, 4,4 single sedadlo vpravo od uličky
    predni     distance[cm] přední řady
    krok       rozestup řad[cm] (je-li zadáno zadni, krok se ignoruje a spočte znovu podle zadni/predni)
    zadni      distance[cm] zadní řady (None: řady se posouvají o krok; not None: krok se určí podle zadni/predni)
    rad        kolik rad za sebou vytvořit
    cisla      list přidělených čísel (None: sestaví se automaticky podle cisluj a posledního přiděleného)
    cisluj 'L'|'R'|None - zleva, zprava, nečíslovat
    nabizeno   zda je nabízeno (False|True|None, None: podle cisluj)
    umisteni   umístění pozic 1..5 vzhledem k podélné ose
    """

    if nabizeno is None:
        nabizeno = True if cisluj else False
    v_rade = prave - leve + 1
    pocet = rad * v_rade
    if cisluj and cisla is None:
        cisluj = cisluj.upper()
        max = db.sedadlo.cislo.max()
        posledni = db(db.sedadlo.typ_vozidla_id==typ_vozidla_id).select(max).first()[max] or 0
        cisla = []
        for rada in xrange(rad):
            predchozi = posledni + rada * v_rade
            for ktere in xrange(v_rade):
                if cisluj in ('R', 'P'):
                    dalsi = predchozi + v_rade - ktere
                else:
                    dalsi = predchozi + ktere + 1
                cisla.append(dalsi)
    if rad>1 and zadni:
        krok = (zadni - predni) / (rad - 1)

    # kontrola parametrů
    if cisluj and len(cisla)<pocet:
        return 'chybí čísla sedadel'
    if leve not in range(1, 6) or prave not in range(1, 6) or prave<leve:
        return 'chybné pozice leve-prave'
    if predni<30:
        return 'příliš vepředu'
    if not 0<rad<20:
        return 'chybný počet řad'

    kolikate = 0
    for rada in xrange(rad):
        for ktere in xrange(leve - 1, prave):
            db.sedadlo[0] = dict(
                    typ_vozidla_id = typ_vozidla_id,
                    cislo = cisla[kolikate] if cisluj else None,
                    nabizeno = nabizeno,
                    odpredu = predni + rada * krok,
                    od_osy = umisteni[ktere]
                    )
            kolikate += 1

    return None     # Ok
