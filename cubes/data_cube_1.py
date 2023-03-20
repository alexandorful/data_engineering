import pandas as pd
import datetime

from rdflib import Graph, BNode, Literal, Namespace
from rdflib.namespace import QB, RDF, XSD, SKOS, DCTERMS

NS = Namespace("https://alexandorful.github.io/datacube/ontology#")
NSR = Namespace("https://alexandorful.github.io/datacube/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
SDMX_CODE = Namespace("http://purl.org/linked-data/sdmx/2009/code#")

County = "Okres"
CountyCode = "OkresCode"
Region = "Kraj"
RegionCode = "KrajCode"
Field = "OborPece"

def main():
    data_as_csv = load_csv_file_as_object("Care providers - Data.csv")
    data_cube = as_data_cube(data_as_csv)
    print(data_cube.serialize(format="ttl", destination="Care_Providers.ttl"))
    print("-" * 80)


def load_csv_file_as_object(file_path: str):
    result = pd.read_csv(file_path, low_memory=False)
    return result

def as_data_cube(data):
    result = Graph()
    dimensions = create_dimensions(result)
    measures = create_measure(result)
    structure = create_structure(result, dimensions, measures)
    dataset = create_dataset(result, structure)
    create_observations(result, dataset, data)
    create_resources(result, data)

    return result


def create_dimensions(collector: Graph):

    county = NS.county
    collector.add((county, RDF.type, RDFS.Property))
    collector.add((county, RDF.type, QB.DimensionProperty))
    collector.add((county, RDFS.label, Literal("CountyCode", lang="en")))
    collector.add((county, RDFS.range, XSD.string))
    collector.add((county, QB.concept, SDMX_CONCEPT.refArea))

    region = NS.region
    collector.add((region, RDF.type, RDFS.Property))
    collector.add((region, RDF.type, QB.DimensionProperty))
    collector.add((region, RDFS.label, Literal("RegionCode", lang="en")))
    collector.add((region, RDFS.range, XSD.string))
    collector.add((region, QB.concept, SDMX_CONCEPT.refArea))

    field = NS.field
    collector.add((field, RDF.type, RDFS.Property))
    collector.add((field, RDF.type, QB.DimensionProperty))
    collector.add((field, RDFS.label, Literal("Field", lang="en")))
    collector.add((field, RDFS.range, XSD.string))

    return [county, region, field]


def create_measure(collector: Graph):

    number = NS.NumberofProviders
    collector.add((number, RDF.type, QB.MeasureProperty))
    collector.add((number, RDF.type, RDFS.Property))
    collector.add((number, RDFS.label, Literal("Number of care providers", lang="en")))
    collector.add((number, RDFS.range, XSD.integer))
    collector.add((number, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))


    return [number]


def create_structure(collector: Graph, dimensions, measures):

    structure = NS.structure
    collector.add((structure, RDF.type, QB.DataStructureDefinition))

    for dimension in dimensions:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.dimension, dimension))

    for measure in measures:
        component = BNode()
        collector.add((structure, QB.component, component))
        collector.add((component, QB.measure, measure))

    return structure


def create_dataset(collector: Graph, structure):
    dataset = NSR.dataCubeInstance
    collector.add((dataset, RDF.type, QB.DataSet))
    collector.add((dataset, RDFS.label, Literal("Poskytovatelé zdravotních služeb", lang="cs")))
    collector.add((dataset, RDFS.label, Literal("HealthCare Providers", lang="en")))
    curr_date = datetime.date.today().isoformat()
    collector.add((dataset, DCTERMS.issued, Literal("2023-03-11", datatype=XSD.date)))
    collector.add((dataset, DCTERMS.modified, Literal(curr_date, datatype=XSD.date)))
    collector.add((dataset, DCTERMS.publisher, Literal("https://github.com/alexandorful")))
    collector.add((dataset, DCTERMS.license, Literal("https://github.com/alexandorful/NDBI046/blob/main/LICENSE")))
    collector.add((dataset, QB.structure, structure))

    return dataset


def create_observations(collector: Graph, dataset, data: pd.DataFrame):
    grouped = data.groupby(["OkresCode", "KrajCode", "OborPece"]).size().reset_index(name="PocetPoskytovaluPece")
    for index, row in grouped.iterrows():
        resource = NSR["observation-" + str(index).zfill(4)]
        create_observation(collector, dataset, resource, row)


def create_observation(collector: Graph, dataset, resource, data: pd.DataFrame):

    collector.add((resource, RDF.type, QB.Observation))
    collector.add((resource, QB.dataSet, dataset))
    collector.add((resource, NS.county, Literal(data["OkresCode"])))
    collector.add((resource, NS.region, Literal(data["KrajCode"])))
    collector.add((resource, NS.field, Literal(data["OborPece"])))
    collector.add((resource, NS.numberOfCareProviders, Literal(data["PocetPoskytovaluPece"])))




def create_resources(collector: Graph, data: pd.DataFrame):
    for _, row in data[[County, CountyCode]].drop_duplicates().dropna().iterrows():
        county = serialize_to_string(row[CountyCode])
        collector.add((NSR[county], RDF.type, NS.county))
        collector.add((NSR[county], SKOS.prefLabel, Literal(str(row[County]), lang="cs")))

    for _, row in data[[Region, RegionCode]].drop_duplicates().dropna().iterrows():
        region = serialize_to_string(row[RegionCode])
        collector.add((NSR[region], RDF.type, NS.region))
        collector.add((NSR[region], SKOS.prefLabel, Literal(str(row[Region]), lang="cs")))

    for _, row in data[[Field]].drop_duplicates().dropna().iterrows():
        field = serialize_to_string(row[Field])
        collector.add((NSR[field], RDF.type, NS.field_of_care))
        collector.add(
            (NSR[field], SKOS.prefLabel, Literal(str(row[Field]), lang="cs"))
        )

def serialize_to_string(obj: any) -> str:
    return str(obj).strip().replace(", ", ",").replace(" ", "_").lower()

if __name__ == "__main__":
    main()


