""" Modulo de persistencia en Neo4J"""
from neo4j import GraphDatabase
import os
import random

OUTPUT_FOLDER = '/Users/f.brevers.gomez/Documents/col-o-mbo/output/'

_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345"))

QUERY_ALL = "MATCH (n)" \
            "RETURN n"

QUERY_SUSPECTS = "MATCH (s:sospechoso) return s.imagen as imagen"
QUERY_ASASSIN = "MATCH (w:arma {nombre:'1 Tm de burocracia'})<-[:TIENE_ACCESO_A]-(s:sospechoso)" \
                "-[:ESTABA_EN]-(:lugar {nombre:'Office'}) return s.imagen AS `imagen`"
UPDATE_TEMP_ASSASSIN = "MATCH (w:arma {nombre:{arma}.nombre}), " \
                       "(s:sospechoso {imagen: {imagen}})-[r:TIENE_ACCESO_A]-()" \
                       "DELETE r " \
                       "MERGE (s)-[:TIENE_ACCESO_A]->(w)"


CREATE_SUSPECT = "MATCH (w:arma {nombre: {arma}.nombre}), (r:lugar {nombre: {lugar}.nombre})" \
                 "MERGE (s:sospechoso {imagen: {imagen}})" \
                 "MERGE (s)-[:TIENE_ACCESO_A]->(w)" \
                 "MERGE (s)-[:ESTABA_EN]->(r)"
CREATE_WEAPON = "CREATE (w:arma {nombre: {arma}.nombre, peso: {arma}.peso})"
CREATE_ROOM = "CREATE (r:lugar {nombre: {lugar}.nombre})"

FOCK_IT = "MATCH (n) DETACH DELETE n"

weapons = [{"nombre": "Impresora 3D"}, {"nombre": "Cable RJ45"},
           {"nombre": "Planta ZZ"}, {"nombre": "Semaforo sistemas"},
           {"nombre": "1 Tm de burocracia"}]

rooms = [{"nombre": "Hall"}, {"nombre": "Sala Mafalda"}, {"nombre": "CPD"}, {"nombre": "Sala Ada Lovelace"},
         {"nombre": "Office"}, {"nombre": "Patio"}]


def create_scenario():

    _create_weapons()
    _create_rooms()
    _create_suspects()


def _create_suspects():

    for sospechoso in os.listdir(OUTPUT_FOLDER):
        if sospechoso is not '.DS_Store':
            __create_suspect(sospechoso)
    __check_asassin()


def _create_weapons():

    for weapon in weapons:
        __create_weapon(weapon)


def _create_rooms():

    for room in rooms:
        __create_room(room)


def __create_suspect(suspect_image):

    with _driver.session() as session:
        session.run(CREATE_SUSPECT, imagen=suspect_image, arma=random.choice(weapons), lugar=random.choice(rooms) )


def __create_weapon(weapon):

    with _driver.session() as session:
        session.run(CREATE_WEAPON, arma=weapon)


def __create_room(room):
    with _driver.session() as session:
        session.run(CREATE_ROOM, lugar=room)


def __fockit():
    with _driver.session() as session:
        session.run(FOCK_IT)


def __check_asassin():
    with _driver.session() as session:
        records = session.run(QUERY_ASASSIN)
        temp_asassins = records.data()
        if len(temp_asassins) > 1:
            # Tenemos varios asesinos asi que dejamos uno xD
            for temp_ass in temp_asassins[:-1]:
                session.run(UPDATE_TEMP_ASSASSIN, arma=random.choice(weapons[:-1]), imagen=temp_ass['imagen'])
                print("Eliminado asesino innecesario")
        elif len(temp_asassins) == 0:
            print("NO HAY sospechosos")
            __fockit()
            print("Regenerando escenario")
            create_scenario()


if __name__ == "__main__":

    _create_weapons()
    _create_rooms()
    _create_suspects()
