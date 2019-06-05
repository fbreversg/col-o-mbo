""" Modulo de persistencia en Neo4J"""
from neo4j import GraphDatabase
import os
import random

OUTPUT_FOLDER = '/Users/f.brevers.gomez/Documents/col-o-mbo/output/'

_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345"))

QUERY_ALL = "MATCH (n)" \
            "RETURN n"

QUERY_SUSPECTS = "MATCH (s:sospechoso) return s.imagen as imagen"
QUERY_ASASSIN = "MATCH (w:arma {nombre:'Burocracia'})<-[:TIENE_ACCESO_A]-(s:sospechoso)" \
                "-[:ESTABA_EN]-(:lugar {nombre:'Office'}) return s.imagen AS `imagen`"
UPDATE_TEMP_ASSASSIN = "MATCH (w:arma {nombre:{arma}.nombre}), (s:sospechoso {imagen: {imagen}})" \
                     "DELETE (s"


CREATE_SUSPECT = "MATCH (w:arma {nombre: {arma}.nombre}), (r:lugar {nombre: {lugar}.nombre})" \
                 "MERGE (s:sospechoso {imagen: {imagen}})" \
                 "MERGE (s)-[:TIENE_ACCESO_A]->(w)" \
                 "MERGE (s)-[:ESTABA_EN]->(r)"
CREATE_WEAPON = "CREATE (w:arma {nombre: {arma}.nombre, peso: {arma}.peso})"
CREATE_ROOM = "CREATE (r:lugar {nombre: {lugar}.nombre})"

#TODO: CREATE COMPLICES

#TODO: Ver como asignar un caption por defecto.
weapons = [{"nombre": "Impresora 3D", "peso": "15 Kg"}, {"nombre": "Cable RJ45", "peso": "0.3 Kg"},
           {"nombre": "Planta ZZ", "peso": "8 Kg"}, {"nombre": "Semaforo sistemas", "peso": "15 Tm"},
           {"nombre": "Burocracia", "peso": "15 Tm"}]

rooms = [{"nombre": "Hall"}, {"nombre": "Sala Mafalda"}, {"nombre": "CPD"}, {"nombre": "Sala Ada Lovelace"},
         {"nombre": "Office"}, {"nombre": "Patio"}]


def create_suspects():

    for sospechoso in os.listdir(OUTPUT_FOLDER):
        _create_suspect(sospechoso)


def create_weapons():

    for weapon in weapons:
        _create_weapon(weapon)


def create_rooms():

    for room in rooms:
        _create_room(room)


def _create_suspect(suspect_image):

    with _driver.session() as session:
        session.run(CREATE_SUSPECT, imagen=suspect_image, arma=random.choice(weapons), lugar=random.choice(rooms) )


def _create_weapon(weapon):

    with _driver.session() as session:
        session.run(CREATE_WEAPON, arma=weapon)


def _create_room(room):
    with _driver.session() as session:
        session.run(CREATE_ROOM, lugar=room)


def query_asassin():
    with _driver.session() as session:
        records = session.run(QUERY_ASASSIN)
        print(records.data())
        if records.detach() > 1:
            # Tenemos varios asesinos asi que dejamos uno xD
            for temp_ass in records.data()[:-1]:
                data = session.run(UPDATE_TEMP_ASSASSIN, arma=random.choice(weapons[:-1]), imagen=temp_ass['imagen'])
                print(data.data())

if __name__ == "__main__":

    #create_weapons()
    #create_rooms()
    #create_suspects()
    query_asassin()


'''
from neo4j import GraphDatabase

class Application(object):

    def __init__(self, uri, user, password)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

'''
