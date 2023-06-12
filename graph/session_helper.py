from neo4j import GraphDatabase

def delete_and_detach_all_nodes(session):
    session.run(
        "MATCH (n) DETACH DELETE n"
    )

def create_session():
    username = 'neo4j'
    password = 'bique123'

    print('Creating a connection with neo4j...')
    driver = GraphDatabase.driver("neo4j://10.4.41.51:7687", auth=(username, password))

    session = driver.session()
    print('Session Initiated....')

    return session

def clean_session(session):
    
    print('Deleting and detaching all the previous nodes in the database.')
    session.execute_write(delete_and_detach_all_nodes)
    return session
