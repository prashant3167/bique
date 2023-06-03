from session_helper import create_session, clean_session

session = create_session()
session = clean_session(session)

def load_node_users(session):
    session.run(
        """LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS line
            CREATE (:Users {
                id: line.id,
                name: line.name
        })"""
    )


def load_node_advisors(session):
    session.run(
        """LOAD CSV WITH HEADERS FROM 'file:///final_advisors.csv' AS line
            CREATE (:Advisors {
                id: line.id,
                name: line.name,
                jobcount: line.jobcount,
                charge: line.charge
        })"""
    )

def load_relation_users_advisors(session):
    session.run(
            """LOAD CSV WITH HEADERS FROM 'file:///mapping.csv' AS line
                MATCH (user:Users {id: line.user_id})
                WITH user, line
                MATCH (advisor:Advisors {id: line.advisor_id})
                CREATE (user) - [r:consulted] -> (advisor)
                SET r.rating = toInteger(line.rating),
                    r.date = date(line.date)"""
    )

print('Creating and loading the nodes and relations into the database...')
session.execute_write(load_node_users)
session.execute_write(load_node_advisors)
session.execute_write(load_relation_users_advisors)

session.close()
