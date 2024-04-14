from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from typing import List
from ..model.agency import Agency
from ..model.editors import Editor
from .newspaperNS import paper_model
from ..model.newspaper import Newspaper

from .newspaperNS import issue_model
from ..model.issue import Issue


editors_ns = Namespace("editor", description="Editor related operations")

editor_model = editors_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
            help='The unique identifier of an editor'),
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address'),
    'list_of_newspapers': fields.List(fields.Nested(paper_model), required=True,
            help='list_of_newspapers'),
    "list_of_issues": fields.List(fields.Nested(issue_model), required=True,
            help='list_of_issues'),
    "payment": fields.Float(required=True,help = "payment")
   })

editor_model2 = editors_ns.model('EditorModel2', {
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address')
   })


paper = Newspaper(1, "The Standards", 1, 7)
@editors_ns.route('/')
class EditorAPI(Resource):
    @editors_ns.doc(description="Create a new editor")
    @editors_ns.expect(editor_model2, validate=True)
    @editors_ns.marshal_with(editor_model, envelope='editor')
    def post(self):
        # editor_id = len(Agency.get_instance().editors) + 20
        # TODO: this is not smart! you should find a better way to generate a unique ID!
        editor_id = max([0] + [i.editor_id for i in Agency.get_instance().editors], default=0) + 1
        new_editor = Editor(editor_id=editor_id,
                              name=editors_ns.payload['name'],
                              address=editors_ns.payload['address'])
        Agency.get_instance().add_editor(new_editor)
        return new_editor

    @editors_ns.marshal_list_with(editor_model, envelope='editor')
    @editors_ns.doc(description="List all editors in the agency")
    def get(self):
        return Agency.get_instance().editors

@editors_ns.route('/<int:editor_id>')
class EditorID(Resource):
    @editors_ns.marshal_list_with(editor_model, envelope='editor')
    @editors_ns.doc(description="Get an editor's information")
    def get(self,editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        else:
            return targeted_editor


    @editors_ns.doc(description="Delete an editor")
    def delete(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        Agency.get_instance().remove_editor(targeted_editor)
        return jsonify(f"Editor with ID {editor_id} was removed")
        # if Agency.editors <1:
        #     return "no editors left"
        # if Agency.editors == 1:
        #     return "no editors left"
        # Agency.add_editor(Editor[editor_id1])



    @editors_ns.doc(description="Update an editor's information")
    @editors_ns.expect(editor_model, validate=True)
    @editors_ns.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_newspaper(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        else:
            targeted_editor.name = editors_ns.payload['name']
            targeted_editor.address = editors_ns.payload['address']
            targeted_editor.list_of_newspapers = editors_ns.payload['list_of_newspapers']
        # Agency.get_instance().update_editor(targeted_editor)
        return targeted_editor


@editors_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    @editors_ns.marshal_list_with(issue_model, envelope='issue')
    @editors_ns.doc(description="Return a list of newspaper issues that the editor was responsible for")
    def get(self,editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found")
        else:
            targeted_issues = targeted_editor.list_of_issues
            if not targeted_issues:
                return jsonify(f"No issues found for editor with ID {editor_id}")
            return targeted_issues

