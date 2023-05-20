from rdflib import Graph, BNode, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD, DCAT, DCTERMS

NS = Namespace("https://alexandorful.github.io/datacube/ontology#")
NSR = Namespace("https://alexandorful.github.io/datacube/resources/")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
EUROVOC = Namespace("http://eurovoc.europa.eu/")
EUA = Namespace("http://publications.europa.eu/resource/authority/")
SPDX = Namespace("http://spdx.org/rdf/terms#")


def define_dataset(g: Graph):
    dataset = NSR.DataCubePopulationInstance

    g.add((dataset, RDF.type, DCAT.Dataset))
    g.add((dataset, DCTERMS.title, Literal("Population 2021", lang="en")))

    g.add((dataset, DCTERMS.description,
           Literal("Population statistics for Czech counties and regions",
                   lang="en")))
    g.add((dataset, DCTERMS.publisher, Literal("https://github.com/alexandorful", datatype=XSD.anyURI)))
    g.add((dataset, DCTERMS.creator, Literal("https://github.com/alexandorful", datatype=XSD.anyURI)))

    g.add((dataset, DCAT.keyword, Literal("mean population", lang="en")))
    g.add((dataset, DCAT.keyword, Literal("population count", lang="en")))
    g.add((dataset, DCAT.theme, EUROVOC["3300"]))
    g.add((dataset, DCAT.theme, EUROVOC["4259"]))
    g.add((dataset, DCTERMS.spatial, EUA["country/CZE"]))
    g.add((dataset, DCAT.distribution, NSR["dataset/PopulationData/distribution/rdf-turtle"]))

    time = BNode()
    g.add((dataset, DCTERMS.temporal, time))
    g.add((time, RDF.type, DCTERMS.PeriodOfTime))
    g.add((time, DCAT.startDate, Literal("2021-01-01", datatype=XSD.date)))
    g.add((time, DCAT.endDate, Literal("2021-12-31", datatype=XSD.date)))

    g.add((dataset, DCTERMS.accrualPeriodicity, EUA["frequency/IRREG"]))


def create_distribution(g: Graph):
    distribution = NSR.CubeDistribution

    g.add((distribution, RDF.type, DCAT.Distribution))
    g.add((distribution, DCAT.accessURL, URIRef("https://github.com/alexandorful/data_engineering")))
    g.add((distribution, DCTERMS.format, EUA["file-type/RDF_TURTLE"]))
    g.add((distribution, DCAT.mediaType, URIRef("https://www.iana.org/assignments/media-types/text/turtle")))


def create_dataset():
    g = Graph(bind_namespaces="rdflib")
    define_dataset(g)
    create_distribution(g)
    g.serialize("population-dataset.ttl", format="turtle")


if __name__ == "__main__":
    create_dataset()
