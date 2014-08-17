import math
from flask import session
from easypc.database import db


class Character():

    def __init__(self, name):
        self.pc = db.pcs.find_one({"name": name, "owner": session['user']})

    @property
    def name(self):
        return self.pc.get("name")

    @property
    def race(self):
        return self.pc.get("race")

    @property
    def attributes(self):
        return self.pc.get("attributes")

    @classmethod
    def list_all(cls):
        return db.pcs.find({"owner": session['user']})

    @classmethod
    def create(cls, name):
        db.pcs.insert({
            "owner": session['user'],
            "name": name,
            "race": None,
            "age": None,
            "attributes": {
                "strength": 0,
                "dexterity": 0,
                "constitution": 0,
                "intelligence": 0,
                "wisdom": 0,
                "charisma": 0
            },
            "alignment": None,
            "physical_desc": {
                "gender": None,
                "height": None,
                "weight": None,

                "eyes": None,
                "hair": None
            },
            "traits": [],
            "languages": ["Common"]
        })
        return cls(name)

    def update(self, update_args):

        def _update(attr, parent):
            if(attr in update_args):
                if(isinstance(parent, list)):
                    if(isinstance(update_args[attr], list)):
                        for item in update_args[attr]:
                            if item not in parent:
                                parent.append(item)
                    else:
                        if update_args[attr] not in parent:
                            parent.append(update_args[attr])

                elif(isinstance(parent, dict)):
                    parent[attr] = update_args[attr]

        _update("race", self.pc)
        _update("alignment", self.pc)

        _update("gender", self.pc['physical_desc'])
        _update("height", self.pc['physical_desc'])
        _update("weight", self.pc['physical_desc'])
        _update("eyes", self.pc['physical_desc'])
        _update("hair", self.pc['physical_desc'])

        _update("strength", self.pc['attributes'])
        _update("dexterity", self.pc['attributes'])
        _update("constitution", self.pc['attributes'])
        _update("intelligence", self.pc['attributes'])
        _update("wisdom",  self.pc['attributes'])
        _update("charisma",  self.pc['attributes'])

        _update("traits", self.pc["traits"])
        _update("languages", self.pc["languages"])

        if('age' in update_args):
            self.update_age(update_args['age'])

        self.save()

    def update_age(self, new_age):
        # TODO: attr modifications for venerable and such
        self.pc['age'] = new_age

    def save(self):
        db.pcs.save(self.pc)

    def get_modifier(self, attr):
        return (math.floor(int(self.pc['attributes'][attr])/2) - 5)
