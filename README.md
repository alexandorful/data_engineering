# Data Engineering - Assignment 1
## https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02-data-cube.html

## System Requirements
- Python 3 (developed with Python 3.10)
- Modules (declared in [requirements.txt](1-Data-Cube/requirements.txt)):
  - [Pandas](https://pandas.pydata.org/)
  - [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html)
 
 ## Installation instructions
1. Clone the repository
2. Install Pandas and RDFLib libraries
3. Generate the respective datacubes by running 'data_cube_1.py' and 'data_cube_2.py'
4. See the generated files: "Care_Providers.ttl" and "Population_2021.ttl"
5. Check integrity constraints by running `integrity_constraints.py`

## Information
### Care providers datacube
- Script located in `cubes/data_cube_1.py`
- The script generates a datacube using data from the [Národní registr poskytovatelů zdravotních služeb](https://data.gov.cz/datov%C3%A1-sada?iri=https://data.gov.cz/zdroj/datov%C3%A9-sady/https---opendata.mzcr.cz-api-3-action-package_show-id-nrpzs) dataset.
- The generated datacube has the following dimensions:
  - county
  - region
  - field of care
- and has the measure:
  - number of care providers
- The generated datacube file: "Care_Providers.ttl"

### Population 2021 data cube
- Script located in `cubes/data_cube_2.pyy`
- The script generates a datacube using data from the [Pohyb obyvatel za ČR, kraje, okresy, SO ORP a obce - rok 2021](https://data.gov.cz/datov%C3%A1-sada?iri=https%3A%2F%2Fdata.gov.cz%2Fzdroj%2Fdatov%C3%A9-sady%2F00025593%2F12032e1445fd74fa08da79b14137fc29) dataset
- Uses dataset from care providers data cube to map counties to regions
- The generated datacube has the following dimensions:
  - county
  - region
- and has the measure:
  - mean population
- The generated datacube file: "Population_2021.ttl"

### Integrity constraints
- Script `integrity constraints.py` checks whether the generated datacubes comply to the constraints.
- If the file passes all the constraints, then the datacube is valid.

# Data Engineering - Assignment 2
## [https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/02-data-cube.html](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/03-airflow.html)

## System Requirements
- Python 3 (developed with Python 3.10)
- Docker (Minimum of 4GB memory)
- Modules (declared in [requirements.txt](1-Data-Cube/requirements.txt)):
  - [Pandas](https://pandas.pydata.org/)
  - [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html)
  - [Requests](https://requests.readthedocs.io/en/latest/)
 
 ## Installation instructions
1. Clone the repository
2. Run `docker compose up --build`
3. open localhost:8080 and enter - username: airflow, password: airflow
5. Run data_cube_dag where, in the configuration, the"output_path" parameter is set to absolute path in linux filesystem ({"output_path": "/opt/airflow/dags/"})

## Information
The scripts for data_cube_1 and data_cube_2 are largely unchanged. Some functionality was added by a few changes to the main() function, which allowed them to function with Docker

# Data Engineering - Assignment 3
## https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/04-provenance.html#/1/1

## System Requirements
- Python 3 (developed with Python 3.10)
- [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html)
 
 ## Installation instructions
1. Clone the repository
2. Install rdflib
3. Run the Provenance-care-providers and Provenance-population Python files to generate the 2 respective .trig files

## Information
The scripts use PROV to generate RDF TriG files. 

# Data Engineering - Assignment 4
## https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/05-vocabulary.html#/2

Run the file SKOS-builder to generate the SKOS hierarchy, with respects to region and County. Then run the file 'population_dcat' to generate the DCAT dataset for the Population Cube.

# Data Engineering - Assignment 5
## [https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/05-vocabulary.html#/2](https://skoda.projekty.ms.mff.cuni.cz/ndbi046/seminars/06-public.html)

You can find the GitHub pages index here: https://alexandorful.github.io/data_engineering

Indexed files are certificate.crt, data-catalog.sha256.sign and Population_2021.ttl





