from rdflib import Graph, Literal, Namespace, URIRef, BNode
from rdflib.namespace import RDF, RDFS, FOAF, XSD, PROV
from datetime import datetime

NSR = Namespace("https://alexandorful.github.io/resources/")
NSP = Namespace("https://alexandorful.github.io/provenance#")

def create_graph() -> Graph:
    result = Graph(bind_namespaces="rdflib")

    create_entities(result)
    create_agents(result)
    create_activities(result)

    result.add((NSP.Creator, RDF.type, PROV.Role))

    return result


def create_entities(collector: Graph):
    data_cube = NSR.CareProvidersDataCube
    collector.add((data_cube, RDF.type, PROV.Entity))
    collector.add((data_cube, RDFS.label, Literal('care_providers_cube', lang='en')))
    collector.add((data_cube, PROV.wasGeneratedBy, NSP.CareProvidersScript))
    collector.add((data_cube, PROV.wasDerivedFrom, NSP.CareProvidersDataset))
    collector.add((data_cube, PROV.wasAttributedTo, NSP.CareProvidersScript))

    dataset = NSP.CareProvidersDataset
    collector.add((dataset, RDF.type, PROV.Entity))
    collector.add((dataset, RDFS.label, Literal('care_providers_data', lang='en')))


def create_agents(collector: Graph):
    uni = NSR.MFF
    collector.add((uni, RDF.type, PROV.Agent))
    collector.add((uni, RDF.type, PROV.Organization))
    collector.add((uni, FOAF.name, Literal("Faculty of Mathematics and Physics")))

    author = NSR.AlexanderDore
    collector.add((author, RDF.type, PROV.Agent))
    collector.add((author, RDF.type, PROV.Person))
    collector.add((author, FOAF.firstName, Literal("Alexander")))
    collector.add((author, FOAF.surname, Literal("Dore")))

    script = NSR.CareProvidersScript
    collector.add((script, RDF.type, PROV.Agent))
    collector.add((script, RDF.type, PROV.SoftwareAgent))
    collector.add((script, FOAF.name, Literal("data_cube_dag.py")))
    collector.add((script, PROV.atLocation, URIRef("data_cube_dag.py")))


def create_activities(collector: Graph):
    activity = NSP.CreateCareProvidersDataCube
    collector.add((activity, RDF.type, PROV.Activity))
    collector.add((activity, PROV.startedAtTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    collector.add((activity, PROV.endedAtTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    collector.add((activity, PROV.used, NSP.CareProvidersDataset))
    collector.add((activity, PROV.wasAssociatedWith, NSP.AlexanderDore))

    bnode = BNode()
    collector.add((activity, PROV.qualifiedUsage, bnode))
    collector.add((bnode, RDF.type, PROV.Usage))
    collector.add((bnode, PROV.entity, NSP.CareProvidersDataset))
    collector.add((bnode, PROV.hadRole, NSP.Creator))


def create_prov_data():

    prov_data = create_graph()
    prov_data.serialize(format="trig", destination="./care-providers-provenance.trig")


if __name__ == "__main__":
    create_prov_data()


