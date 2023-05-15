import pandas as pd
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF, SKOS


NS = Namespace("https://alexandorful.github.io/datacube/ontology#")
NSR = Namespace("https://alexandorful.github.io/datacube/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")


def clean_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    data_frame = data_frame[["Okres", "OkresCode", "Kraj", "KrajCode", "OborPece"]].dropna()
    return data_frame


def set_hierarchy(graph_instance: Graph) -> Graph:
    graph_instance.add((URIRef("http://eurovoc.europa.eu/3300"), RDF.type, SKOS.ConceptScheme))
    graph_instance.add((URIRef("http://eurovoc.europa.eu/3300"), SKOS.prefLabel, Literal("geographical distribution of the population", lang="en")))
    graph_instance.add((URIRef("http://eurovoc.europa.eu/3300"), SKOS.hasTopConcept, NS.region))
    graph_instance.add((URIRef("http://eurovoc.europa.eu/3300"), SKOS.hasTopConcept, NS.county))
    graph_instance.add((URIRef("http://eurovoc.europa.eu/3300"), SKOS.notation, Literal("3300")))

    graph_instance.add((NS.region, RDF.type, SKOS.ConceptScheme))
    graph_instance.add((NS.region, SKOS.inScheme, URIRef("http://eurovoc.europa.eu/3300")))
    graph_instance.add((NS.region, SKOS.prefLabel, Literal("Kraj", lang="cs")))
    graph_instance.add((NS.region, SKOS.prefLabel, Literal("Region", lang="en")))

    graph_instance.add((NS.county, RDF.type, SKOS.ConceptScheme))
    graph_instance.add((NS.county, SKOS.inScheme, URIRef("http://eurovoc.europa.eu/3300")))
    graph_instance.add((NS.county, SKOS.prefLabel, Literal("Okres", lang="cs")))
    graph_instance.add((NS.county, SKOS.prefLabel, Literal("County", lang="en")))

    return graph_instance

def add_entries_to_hierarchy(data_frame: pd.DataFrame, graph_instance: Graph) -> Graph:
    for _, row in data_frame[["Okres", "OkresCode", "Kraj", "KrajCode"]].drop_duplicates().dropna().iterrows():
        graph_instance.add((NSR[row["OkresCode"]], RDF.type, SKOS.Concept))
        graph_instance.add((NSR[row["OkresCode"]], SKOS.prefLabel, Literal(str(row["Okres"]), lang="cs")))
        graph_instance.add((NSR[row["OkresCode"]], SKOS.notation, Literal(str(row["OkresCode"]))))
        graph_instance.add((NS.region, SKOS.hasTopConcept, NSR[row["OkresCode"]]))

        graph_instance.add((NSR[row["OkresCode"]], SKOS.inScheme, NS.region))

        graph_instance.add((NSR[row["KrajCode"]], RDF.type, SKOS.Concept))
        graph_instance.add((NSR[row["KrajCode"]], SKOS.prefLabel, Literal(str(row["Kraj"]), lang="cs")))
        graph_instance.add((NSR[row["KrajCode"]], SKOS.notation, Literal(str(row["KrajCode"]))))
        graph_instance.add((NS.county, SKOS.hasTopConcept, NSR[row["KrajCode"]]))
        graph_instance.add((NSR[row["KrajCode"]], SKOS.inScheme, NS.county))

        graph_instance.add((NSR[row["KrajCode"]], SKOS.narrower, NSR[row["OkresCode"]]))
        graph_instance.add((NSR[row["OkresCode"]], SKOS.broader, NSR[row["KrajCode"]]))

        return graph_instance

def main() -> None:
    data = "Care providers - Data.csv"

    df = pd.read_csv(data, low_memory=False)
    df = clean_data(df)

    g = Graph()
    g = set_hierarchy(g)
    g = add_entries_to_hierarchy(df, g)

    print(g.serialize(format="ttl", destination="Region_County SKOS.ttl"))
    print("-" * 80)

if __name__ == "__main__":
    main()
