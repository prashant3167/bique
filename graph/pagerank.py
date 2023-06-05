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

def create_advisors_average_rating(session):
    session.run(
        """MATCH () - [r:consulted] -> (advisor:Advisors)
            WITH advisor, COALESCE(SUM(r.rating), 1) as total
            SET advisor.star = toInteger(total)"""
    )

def get_advisor_ranking(session):
    result = session.run(
        """MATCH () - [r] -> (advisor:Advisors)
            WITH advisor, COUNT(r) * advisor.star AS rank
            ORDER BY rank DESC
            RETURN advisor.name, rank         
            LIMIT 25   
        """
    )
    
    records = list(result)
    summary = result.consume()
    return records, summary

session.execute_write(create_advisors_average_rating)
records, summary = session.execute_read(get_advisor_ranking)
print_query_results(records, summary)

session.close()