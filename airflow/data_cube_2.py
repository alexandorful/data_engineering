import pandas as pd
import datetime

from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import QB, RDF, XSD, SKOS, DCTERMS

NS = Namespace("https://alexandorful.github.io/datacube/ontology#")
NSR = Namespace("https://alexandorful.github.io/datacube/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")

SDMX_CONCEPT = Namespace("http://purl.org/linked-data/sdmx/2009/concept#")
SDMX_MEASURE = Namespace("http://purl.org/linked-data/sdmx/2009/measure#")
SDMX_CODE = Namespace("http://purl.org/linked-data/sdmx/2009/code#")


def process_population(output_path = "/opt/airflow/dags/"):
    population = load_data("Population - data.csv")
    codelist = load_data("Codelist.csv")

    data_cube = as_data_cube(population, codelist)
    data_cube.serialize(format="ttl", destination = output_path.rstrip("/") + "/population.ttl")
    print("-" * 80)


def load_data(file_path):
    return pd.read_csv(file_path, low_memory=False)


def find_county(code: int, codelist: pd.DataFrame) -> str:
    return codelist[(codelist["CHODNOTA2"] == code)].iloc[0]["CHODNOTA1"]


def as_data_cube(data, codelist: pd.DataFrame):
    result = Graph()
    dimensions = create_dimensions(result)
    measures = create_measure(result)
    structure = create_structure(result, dimensions, measures)
    dataset = create_dataset(result, structure)

    data = data[(data["vuk"] == "DEM0004") & (data["vuzemi_cis"] == 101)]
    create_observations(result, dataset, data, codelist)
    create_resources(result, data, codelist)

    return result


def create_dimensions(collector: Graph):

    county = NS.county
    collector.add((county, RDF.type, RDFS.Property))
    collector.add((county, RDF.type, QB.DimensionProperty))
    collector.add((county, RDF.type, QB.CodedProperty))
    collector.add((county, RDFS.label, Literal("CountyCode", lang="en")))
    collector.add((county, RDFS.range, XSD.string))
    collector.add((county, QB.concept, SDMX_CONCEPT.refArea))

    region = NS.region
    collector.add((region, RDF.type, RDFS.Property))
    collector.add((region, RDF.type, QB.DimensionProperty))
    collector.add((region, RDF.type, QB.CodedProperty))
    collector.add((region, RDFS.label, Literal("RegionCode", lang="en")))
    collector.add((region, RDFS.range, XSD.string))
    collector.add((region, QB.concept, SDMX_CONCEPT.refArea))

    return [county, region]


def create_measure(collector: Graph):
    mean_population = NS.meanPopulation
    collector.add((mean_population, RDF.type, RDFS.Property))
    collector.add((mean_population, RDF.type, QB.MeasureProperty))
    collector.add((mean_population, RDFS.label, Literal("Mean population count", lang="en")))
    collector.add((mean_population, RDFS.label, Literal("Střední stav obyvatel - počet", lang="cs")))
    collector.add((mean_population, RDFS.subPropertyOf, SDMX_MEASURE.obsValue))
    collector.add((mean_population, RDFS.range, XSD.integer))

    return [mean_population]


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
    collector.add((dataset, RDFS.label, Literal("Obyvatelé v okresech 2021", lang="cs")))
    collector.add((dataset, RDFS.label, Literal("Population 2021", lang="en")))
    curr_date = datetime.date.today().isoformat()
    collector.add((dataset, DCTERMS.issued, Literal("2023-03-11", datatype=XSD.date)))
    collector.add((dataset, DCTERMS.modified, Literal(curr_date, datatype=XSD.date)))
    collector.add((dataset, DCTERMS.publisher, Literal("https://github.com/alexandorful")))
    collector.add((dataset, DCTERMS.license, Literal("https://github.com/alexandorful/NDBI046/blob/main/LICENSE")))
    collector.add((dataset, QB.structure, structure))

    return dataset


def create_resources(collector: Graph, data: pd.DataFrame, codelist: pd.DataFrame):
    for _, row in data.iterrows():
        code = find_county(row.vuzemi_kod, codelist)
        collector.add((NSR[code], RDF.type, NS.county))
        collector.add((NSR[code], SKOS.prefLabel, Literal(row.vuzemi_txt, lang="cs")))

    regions = load_data("Care providers - Data.csv")
    for _, row in regions[["KrajCode", "Kraj"]].drop_duplicates().dropna().iterrows():
        region = row["KrajCode"]
        collector.add((NSR[region], RDF.type, NS.region))
        collector.add((NSR[region], SKOS.prefLabel, Literal(row["Kraj"], lang="cs")))


def create_observations(collector: Graph, dataset: URIRef, data: pd.DataFrame, code: pd.DataFrame):
    regions = load_data("Care providers - Data.csv")
    code_map = {}
    for _, row in (
        regions[["KrajCode", "OkresCode"]].drop_duplicates().dropna().iterrows()
    ):
        code_map[row["OkresCode"]] = row["KrajCode"]

    for index, row in data.iterrows():
        resource = NSR["observation-" + str(index).zfill(4)]
        collector.add((resource, RDF.type, QB.Observation))
        collector.add((resource, QB.dataSet, dataset))
        collector.add((resource, QB.dataSet, dataset))

        county = find_county(row.vuzemi_kod, code)
        collector.add((resource, NS.county, NSR[county]))
        collector.add((resource, NS.region, NSR[code_map[county]]))

        collector.add(
            (resource, NS.mean_population, Literal(row.hodnota, datatype=XSD.integer))
        )


if __name__ == "__main__":
    process_population()


