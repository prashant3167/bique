from neo4j import GraphDatabase
from neo4j.time import Date
from datetime import datetime

class Neo4jDataRetriever:
    def __init__(self, uri="bolt://10.4.41.51:7687", username="neo4j", password="bique123"):
        self.uri = uri
        self.username = username
        self.password = password

    def retrieve_data(self, id):
        cypher_query = f"MATCH (n:Users {{id:'{id}'}})-[c:consulted]-(p:Advisors) RETURN p.name AS name, p.id AS id, c.date AS date, c.rating AS rating ORDER BY date DESC"
        data = []
        with GraphDatabase.driver(self.uri, auth=(self.username, self.password)) as driver:
            with driver.session() as session:
                result = session.run(cypher_query)

                for record in result:
                    item = record.data()
                    if "date" in item:
                        date = item["date"]
                        if isinstance(date, Date):
                            item["date"] = date.to_native().strftime("%Y-%m-%d")
                    data.append(item)
        
        return data