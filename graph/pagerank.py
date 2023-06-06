import pprint
from session_helper import create_session

session = create_session()

# Printing query results and summary 
def print_query_results(records, summary):
    pp = pprint.PrettyPrinter(indent = 4)
    
    print("The query `{query}` returned {records_count} records in {time} ms.".format(
        query = summary.query, records_count = len(records),
        time = summary.result_available_after,
    ))

    for record in records:
        pp.pprint(record.data())
        print()

def create_advisors_rating(session):
    session.run(
        """MATCH () - [r:consulted] -> (advisor:Advisors)
            WITH advisor, COALESCE(SUM(r.rating)) as total
            SET advisor.star = toInteger(total)"""
    )

def query_simulate_pagerank_algorithm(session):
    print('Dropping the graph from cypher catalog, only if exists')
    session.run("""CALL gds.graph.drop('pageRankGraph',false);""")

    print('Project the graph')
    session.run(
        """CALL gds.graph.project('pageRankGraph', 'Advisors', 'consulted');"""
    )

    print('Running the page rank algorithm for the stored graph')
    result = session.run(
        """CALL gds.pageRank.stream('pageRankGraph')
            YIELD nodeId, score
            WITH gds.util.asNode(nodeId) AS advisor, score AS score
            RETURN advisor.name AS advisor_name, ROUND((advisor.star * score), 2) AS advisor_rank
            ORDER BY advisor_rank DESC LIMIT 5;"""
    )
    records = list(result)
    summary = result.consume()
    return records, summary
print('Creating advisors total rating...')
session.execute_write(create_advisors_rating)

print('Use case 1: Finding top consulted advisors...')
records, summary = session.execute_read(query_simulate_pagerank_algorithm)
print_query_results(records, summary)

session.close()