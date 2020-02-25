from flask import Flask, escape, request, jsonify
#from flask_graphql import GraphQLView
from ariadne.constants import PLAYGROUND_HTML
from ariadne import QueryType, graphql_sync, make_executable_schema,load_schema_from_path, ObjectType
import resolver as r

type_defs = load_schema_from_path('schema.graphql')
query = QueryType()
mut = ObjectType('Mutation')
student = ObjectType('student')
clas = ObjectType('clas')

fakeDatabase = {}
app = Flask(__name__)
query.set_field('student_details', r.student_details)
query.set_field('class_details', r.class_details)
mut.set_field('add_student',r.add_student)
mut.set_field('add_class',r.add_class)
mut.set_field('update_class',r.update_class)
schema = make_executable_schema(type_defs, [student,clas,query,mut])

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
    
@app.route("/graphql", methods=["GET"])
def graphql_playgroud():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200
  
@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code