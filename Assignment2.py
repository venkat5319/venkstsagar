from flask import request, Flask, jsonify
from py2neo import Graph, Node, NodeMatcher
app = Flask(__name__)
graph = Graph('neo4j+s://170c0f3b.databases.neo4j.io', auth=('neo4j', 'opzAKaG9t0bvmGb3KGX8bXSzOiSWHBw_hwPGjMEr6rg'))
transaction = graph.begin()
@app.route('/show', methods=['GET','POST'])
def post_show():
    try:
        show = request.get_json()
        matcher = NodeMatcher(graph)
        shows = matcher.match(title=show['title'])
        if len(shows) > 0:
            return jsonify({"status" : "Duplicate Show Title"})

        node = Node("IMDB",
                    show_id=show['show_id'],
                    type=show['type'],
                    title=show['title'],
                    director=show['director'],
                    cast=show['cast'],
                    genres=show['genres'],
                    date_added=show['date_added'],
                    release_year=show['release_year'],
                    rating=show['rating'],
                    duration=show['duration'],
                    description=show['description'])
        transaction.create(node)
        graph.commit(transaction)
        return jsonify({"status": "Show Added"})
    except Exception as e:
        print(e)
        return jsonify({"Error": "Something went wrong"})
@app.route('/show/<title>', methods=['GET','PATCH'])
def patch_show(title):
    show = request.get_json()
    matcher = NodeMatcher(graph)
    shows_nodes = matcher.match(title=title)
    for show_node in shows_nodes:
        show_node.update(title=show['title'],
                         description=show['description'],
                         rating=show['rating'])
        graph.push(show_node)
        return jsonify({"status" : "Show Updated"})
    return jsonify({"status": "Show Title Not Available"})

@app.route('/show/<title>', methods=['GET','DELETE'])
def delete_show(title):
    matcher = NodeMatcher(graph)
    shows_nodes = matcher.match(title=title)
    transaction = graph.begin()
    for show_node in shows_nodes:
        transaction.delete(show_node)
        graph.commit(transaction)
        return jsonify({"status": "Show Deleted"})
    return jsonify({"status": "Show Title Not Available"})

@app.route('/show', methods=['GET'])
def get_shows():
    matcher = NodeMatcher(graph)
    shows_nodes = matcher.match('IMDB')
    shows = []
    for show_node in shows_nodes:
        show = {"show_id": show_node['show_id'],
                 "type": show_node['type'],
                 "title": show_node['title'],
                 "director": show_node['director'],
                 "cast": show_node['cast'],
                 "genres": show_node['genres'],
                 "date_added": show_node['date_added'],
                 "release_year": show_node['release_year'],
                 "rating": show_node['rating'],
                 "duration": show_node['duration'],
                 "description": show_node['description']}
        shows.append(show)
    return jsonify({"shows": shows})

@app.route('/show/<title>', methods=['GET'])
def get_movie(title):
    headers = {'Content-Type': 'application/json'}
    matcher = NodeMatcher(graph)
    shows_nodes = matcher.match(title=title)
    for show_node in shows_nodes:
        show = {"Ids": show_node['show_id'],
                 "Genre": show_node['type'],
                 "Title": show_node['title'],
                 "Director": show_node['director'],
                 "Actors": show_node['cast'],
                 "Votes": show_node['genres'],
                 "Revenue": show_node['date_added'],
                 "Year": show_node['release_year'],
                 "Rating": show_node['rating'],
                 "Runtime": show_node['duration'],
                 "Description": show_node['description']}
        return jsonify(show)
    return jsonify({"status": "Show Title Not Available"})

if __name__ == '__main__':
    app.run(debug=True)