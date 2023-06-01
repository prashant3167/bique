from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://localhost:3000"])

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = [
        {
            'image': 'team2.jpg',
            'name': 'John Michael',
            'email': 'john@creative-tim.com',
            'job': 'Manager',
            'org': 'Organization',
            'status': 'online',
            'employedDate': '23/04/18'
        },
        {
            'image': 'team3.jpg',
            'name': 'Alexa Liras',
            'email': 'alexa@creative-tim.com',
            'job': 'Programator',
            'org': 'Developer',
            'status': 'offline',
            'employedDate': '11/01/19'
        },
        {
            'image': 'team4.jpg',
            'name': 'Laurent Perrier',
            'email': 'laurent@creative-tim.com',
            'job': 'Executive',
            'org': 'Projects',
            'status': 'online',
            'employedDate': '19/09/17'
        },
        {
            'image': 'team3.jpg',
            'name': 'Michael Levi',
            'email': 'michael@creative-tim.com',
            'job': 'Programator',
            'org': 'Developer',
            'status': 'online',
            'employedDate': '24/12/08'
        },
        {
            'image': 'team2.jpg',
            'name': 'Richard Gran',
            'email': 'richard@creative-tim.com',
            'job': 'Manager',
            'org': 'Executive',
            'status': 'offline',
            'employedDate': '04/10/21'
        },
        {
            'image': 'team4.jpg',
            'name': 'Miriam Eric',
            'email': 'miriam@creative-tim.com',
            'job': 'Programtor',
            'org': 'Developer',
            'status': 'offline',
            'employedDate': '14/09/20'
        }
    ]
    response = jsonify(authors)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run()
