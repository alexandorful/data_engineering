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
    data_cube = NSR.PopulationDataCube
    collector.add((data_cube, RDF.type, PROV.Entity))
    collector.add((data_cube, RDFS.label, Literal('population_cube', lang='en')))
    collector.add((data_cube, PROV.wasGeneratedBy, NSP.PopulationScript))
    collector.add((data_cube, PROV.wasDerivedFrom, NSP.PopulationDataset))
    collector.add((data_cube, PROV.wasAttributedTo, NSP.PopulationScript))

    populationdataset = NSP.PopulationDataset
    collector.add((populationdataset, RDF.type, PROV.Entity))
    collector.add((populationdataset, RDFS.label, Literal('population_data', lang='en')))

    care_providers_dataset = NSP.CareProvidersDataset
    collector.add((care_providers_dataset, RDF.type, PROV.Entity))
    collector.add((populationdataset, RDFS.label, Literal('care_provider_data', lang='en')))

    codelist = NSP.CountyCodelist
    collector.add((codelist, RDF.type, PROV.Entity))
    collector.add((populationdataset, RDFS.label, Literal('codelist_data', lang='en')))


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
    activity = NSP.CreatePopulationDataCube
    collector.add((activity, RDF.type, PROV.Activity))
    collector.add((activity, PROV.startedAtTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    collector.add((activity, PROV.endedAtTime, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    collector.add((activity, PROV.used, NSP.PopulationDataset))
    collector.add((activity, PROV.wasAssociatedWith, NSP.AlexanderDore))

    bnode = BNode()
    collector.add((activity, PROV.qualifiedUsage, bnode))
    collector.add((bnode, RDF.type, PROV.Usage))
    collector.add((bnode, PROV.entity, NSP.PopulationDataset))
    collector.add((bnode, PROV.hadRole, NSP.Creator))

    bnode2 = BNode()
    collector.add((activity, PROV.qualifiedUsage, bnode))
    collector.add((bnode2, RDF.type, PROV.Usage))
    collector.add((bnode2, PROV.entity, NSP.CareProvidersDataset))
    collector.add((bnode2, PROV.hadRole, NSP.Creator))

    bnode3 = BNode()
    collector.add((activity, PROV.qualifiedUsage, bnode))
    collector.add((bnode3, RDF.type, PROV.Usage))
    collector.add((bnode3, PROV.entity, NSP.CountyCodelist))
    collector.add((bnode3, PROV.hadRole, NSP.Creator))


def create_prov_data():

    prov_data = create_graph()
    prov_data.serialize(format="trig", destination="./population-provenance.trig")


if __name__ == "__main__":
    create_prov_data()


