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

def load_node_skills(session):
    session.run(
                """LOAD CSV WITH HEADERS FROM 'file:///skills.csv' AS line
                CREATE (:Skills {
                id: line.id,
                skill: line.skill
        })"""
    )

def load_relation_advisors_skills(session):
    session.run(
            """LOAD CSV WITH HEADERS FROM 'file:///skill_mappings.csv' AS line
                MATCH (advisor:Advisors {id: line.advisor_id})
                WITH advisor, line
                MATCH (skill:Skills {id: line.skill_id})
                CREATE (advisor) - [r:has] -> (skill)"""
    )

print('Creating and loading the nodes and relations into the database...')
session.execute_write(load_node_users)
session.execute_write(load_node_advisors)
session.execute_write(load_node_skills)
session.execute_write(load_relation_users_advisors)
session.execute_write(load_relation_advisors_skills)

session.close()
