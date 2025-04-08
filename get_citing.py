import json
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode

CONFIG = json.loads(sys.argv[1])
SNAPSHOT = CONFIG["snapshot"]
INPUT = CONFIG["input"]
OUTPUT = CONFIG["output"]


spark = SparkSession.builder.config(
    "spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.8.5"
).getOrCreate()


def cited_dois(work):
    references = work.get("reference", [])
    return [r["DOI"].lower() for r in references if "DOI" in r]


data = spark.sparkContext.textFile(SNAPSHOT, minPartitions=10000)
data = data.map(lambda line: json.loads(line))

citations = data.map(lambda work: (work["DOI"].lower(), cited_dois(work)))
citations = spark.createDataFrame(citations, ["doi", "cited_dois"])
citations = citations.select(
    citations.doi.alias("citing"), explode(citations.cited_dois).alias("cited")
)

cited = spark.sparkContext.textFile(INPUT)
cited = cited.map(lambda x: (x.lower(),))
cited = spark.createDataFrame(cited, ["cited"])

citing = cited.join(citations, "cited", "inner")
citing = citing.select(citations.citing, citing.cited)
citing.write.format("csv").save(OUTPUT)
