import ast
import types
from uuid import uuid4

import pytest
from langflow.interface.custom.base import CustomComponent
from langflow.interface.custom.code_parser.code_parser import CodeParser, CodeSyntaxError
from langflow.interface.custom.custom_component.component import Component, ComponentCodeNullError
from langflow.interface.custom.utils import build_custom_component_template
from langflow.services.database.models.flow import Flow, FlowCreate

code_default = """
from langflow import Prompt
from langflow.interface.custom.custom_component import CustomComponent

from langchain.llms.base import BaseLLM
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import Document

import requests

class YourComponent(CustomComponent):
    display_name: str = "Your Component"
    description: str = "Your description"
    field_config = { "url": { "multiline": True, "required": True } }

    def build(self, url: str, llm: BaseLLM, template: Prompt) -> Document:
        response = requests.get(url)
        prompt = PromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        result = chain.run(response.text[:300])
        return Document(page_content=str(result))
"""


def test_code_parser_init():
    """
    Test the initialization of the CodeParser class.
    """
    parser = CodeParser(code_default)
    assert parser.code == code_default


def test_code_parser_get_tree():
    """
    Test the __get_tree method of the CodeParser class.
    """
    parser = CodeParser(code_default)
    tree = parser.get_tree()
    assert isinstance(tree, ast.AST)


def test_code_parser_syntax_error():
    """
    Test the __get_tree method raises the
    CodeSyntaxError when given incorrect syntax.
    """
    code_syntax_error = "zzz import os"

    parser = CodeParser(code_syntax_error)
    with pytest.raises(CodeSyntaxError):
        parser.get_tree()


def test_component_init():
    """
    Test the initialization of the Component class.
    """
    component = Component(code=code_default, _function_entrypoint_name="build")
    assert component.code == code_default
    assert component._function_entrypoint_name == "build"


def test_component_get_code_tree():
    """
    Test the get_code_tree method of the Component class.
    """
    component = Component(code=code_default, _function_entrypoint_name="build")
    tree = component.get_code_tree(component.code)
    assert "imports" in tree


def test_component_code_null_error():
    """
    Test the get_function method raises the
    ComponentCodeNullError when the code is empty.
    """
    component = Component(code="", _function_entrypoint_name="")
    with pytest.raises(ComponentCodeNullError):
        component.get_function()


# TODO: Validate if we should remove this
# def test_component_function_entrypoint_name_null_error():
#     """
#     Test the get_function method raises the ComponentFunctionEntrypointNameNullError
#     when the function_entrypoint_name is empty.
#     """
#     component = Component(code=code_default, _function_entrypoint_name="")
#     with pytest.raises(ComponentFunctionEntrypointNameNullError):
#         component.get_function()


def test_custom_component_init():
    """
    Test the initialization of the CustomComponent class.
    """
    function_entrypoint_name = "build"

    custom_component = CustomComponent(code=code_default, function_entrypoint_name=function_entrypoint_name)
    assert custom_component.code == code_default
    assert custom_component.function_entrypoint_name == function_entrypoint_name


def test_custom_component_build_template_config():
    """
    Test the build_template_config property of the CustomComponent class.
    """
    custom_component = CustomComponent(code=code_default, function_entrypoint_name="build")
    config = custom_component.template_config
    assert isinstance(config, dict)


def test_custom_component_get_function():
    """
    Test the get_function property of the CustomComponent class.
    """
    custom_component = CustomComponent(code="def build(): pass", function_entrypoint_name="build")
    my_function = custom_component.get_function
    assert isinstance(my_function, types.FunctionType)


def test_code_parser_parse_imports_import():
    """
    Test the parse_imports method of the CodeParser
    class with an import statement.
    """
    parser = CodeParser(code_default)
    tree = parser.get_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            parser.parse_imports(node)
    assert "requests" in parser.data["imports"]


def test_code_parser_parse_imports_importfrom():
    """
    Test the parse_imports method of the CodeParser
    class with an import from statement.
    """
    parser = CodeParser("from os import path")
    tree = parser.get_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            parser.parse_imports(node)
    assert ("os", "path") in parser.data["imports"]


def test_code_parser_parse_functions():
    """
    Test the parse_functions method of the CodeParser class.
    """
    parser = CodeParser("def test(): pass")
    tree = parser.get_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            parser.parse_functions(node)
    assert len(parser.data["functions"]) == 1
    assert parser.data["functions"][0]["name"] == "test"


def test_code_parser_parse_classes():
    """
    Test the parse_classes method of the CodeParser class.
    """
    parser = CodeParser("class Test: pass")
    tree = parser.get_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            parser.parse_classes(node)
    assert len(parser.data["classes"]) == 1
    assert parser.data["classes"][0]["name"] == "Test"


def test_code_parser_parse_global_vars():
    """
    Test the parse_global_vars method of the CodeParser class.
    """
    parser = CodeParser("x = 1")
    tree = parser.get_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            parser.parse_global_vars(node)
    assert len(parser.data["global_vars"]) == 1
    assert parser.data["global_vars"][0]["targets"] == ["x"]


def test_component_get_function_valid():
    """
    Test the get_function method of the Component
    class with valid code and function_entrypoint_name.
    """
    component = Component(code="def build(): pass", _function_entrypoint_name="build")
    my_function = component.get_function()
    assert callable(my_function)


def test_custom_component_get_function_entrypoint_args():
    """
    Test the get_function_entrypoint_args
    property of the CustomComponent class.
    """
    custom_component = CustomComponent(code=code_default, function_entrypoint_name="build")
    args = custom_component.get_function_entrypoint_args
    assert len(args) == 4
    assert args[0]["name"] == "self"
    assert args[1]["name"] == "url"
    assert args[2]["name"] == "llm"


def test_custom_component_get_function_entrypoint_return_type():
    """
    Test the get_function_entrypoint_return_type
    property of the CustomComponent class.
    """
    from langchain.schema import Document

    custom_component = CustomComponent(code=code_default, function_entrypoint_name="build")
    return_type = custom_component.get_function_entrypoint_return_type
    assert return_type == [Document]


def test_custom_component_get_main_class_name():
    """
    Test the get_main_class_name property of the CustomComponent class.
    """
    custom_component = CustomComponent(code=code_default, function_entrypoint_name="build")
    class_name = custom_component.get_main_class_name
    assert class_name == "YourComponent"


def test_custom_component_get_function_valid():
    """
    Test the get_function property of the CustomComponent
    class with valid code and function_entrypoint_name.
    """
    custom_component = CustomComponent(code="def build(): pass", function_entrypoint_name="build")
    my_function = custom_component.get_function
    assert callable(my_function)


def test_code_parser_parse_arg_no_annotation():
    """
    Test the parse_arg method of the CodeParser class without an annotation.
    """
    parser = CodeParser("")
    arg = ast.arg(arg="x", annotation=None)
    result = parser.parse_arg(arg, None)
    assert result["name"] == "x"
    assert "type" not in result


def test_code_parser_parse_arg_with_annotation():
    """
    Test the parse_arg method of the CodeParser class with an annotation.
    """
    parser = CodeParser("")
    arg = ast.arg(arg="x", annotation=ast.Name(id="int", ctx=ast.Load()))
    result = parser.parse_arg(arg, None)
    assert result["name"] == "x"
    assert result["type"] == "int"


def test_code_parser_parse_callable_details_no_args():
    """
    Test the parse_callable_details method of the
    CodeParser class with a function with no arguments.
    """
    parser = CodeParser("")
    node = ast.FunctionDef(
        name="test",
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
        body=[],
        decorator_list=[],
        returns=None,
    )
    result = parser.parse_callable_details(node)
    assert result["name"] == "test"
    assert len(result["args"]) == 0


def test_code_parser_parse_assign():
    """
    Test the parse_assign method of the CodeParser class.
    """
    parser = CodeParser("")
    stmt = ast.Assign(targets=[ast.Name(id="x", ctx=ast.Store())], value=ast.Num(n=1))
    result = parser.parse_assign(stmt)
    assert result["name"] == "x"
    assert result["value"] == "1"


def test_code_parser_parse_ann_assign():
    """
    Test the parse_ann_assign method of the CodeParser class.
    """
    parser = CodeParser("")
    stmt = ast.AnnAssign(
        target=ast.Name(id="x", ctx=ast.Store()),
        annotation=ast.Name(id="int", ctx=ast.Load()),
        value=ast.Constant(n=1),
        simple=1,
    )
    result = parser.parse_ann_assign(stmt)
    assert result["name"] == "x"
    assert result["value"] == "1"
    assert result["annotation"] == "int"


def test_code_parser_parse_function_def_not_init():
    """
    Test the parse_function_def method of the
    CodeParser class with a function that is not __init__.
    """
    parser = CodeParser("")
    stmt = ast.FunctionDef(
        name="test",
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
        body=[],
        decorator_list=[],
        returns=None,
    )
    result, is_init = parser.parse_function_def(stmt)
    assert result["name"] == "test"
    assert not is_init


def test_code_parser_parse_function_def_init():
    """
    Test the parse_function_def method of the
    CodeParser class with an __init__ function.
    """
    parser = CodeParser("")
    stmt = ast.FunctionDef(
        name="__init__",
        args=ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]),
        body=[],
        decorator_list=[],
        returns=None,
    )
    result, is_init = parser.parse_function_def(stmt)
    assert result["name"] == "__init__"
    assert is_init


def test_component_get_code_tree_syntax_error():
    """
    Test the get_code_tree method of the Component class
    raises the CodeSyntaxError when given incorrect syntax.
    """
    component = Component(code="import os as", _function_entrypoint_name="build")
    with pytest.raises(CodeSyntaxError):
        component.get_code_tree(component.code)


def test_custom_component_get_code_tree_syntax_error():
    """
    Test the get_code_tree method of the CustomComponent class
    raises the CodeSyntaxError when given incorrect syntax.
    """
    custom_component = CustomComponent(code="import os as", function_entrypoint_name="build")
    with pytest.raises(CodeSyntaxError):
        custom_component.get_code_tree(custom_component.code)


def test_custom_component_get_function_entrypoint_args_no_args():
    """
    Test the get_function_entrypoint_args property of
    the CustomComponent class with a build method with no arguments.
    """
    my_code = """
class MyMainClass(CustomComponent):
    def build():
        pass"""

    custom_component = CustomComponent(code=my_code, function_entrypoint_name="build")
    args = custom_component.get_function_entrypoint_args
    assert len(args) == 0


def test_custom_component_get_function_entrypoint_return_type_no_return_type():
    """
    Test the get_function_entrypoint_return_type property of the
    CustomComponent class with a build method with no return type.
    """
    my_code = """
class MyClass(CustomComponent):
    def build():
        pass"""

    custom_component = CustomComponent(code=my_code, function_entrypoint_name="build")
    return_type = custom_component.get_function_entrypoint_return_type
    assert return_type == []


def test_custom_component_get_main_class_name_no_main_class():
    """
    Test the get_main_class_name property of the
    CustomComponent class when there is no main class.
    """
    my_code = """
def build():
    pass"""

    custom_component = CustomComponent(code=my_code, function_entrypoint_name="build")
    class_name = custom_component.get_main_class_name
    assert class_name == ""


def test_custom_component_build_not_implemented():
    """
    Test the build method of the CustomComponent
    class raises the NotImplementedError.
    """
    custom_component = CustomComponent(code="def build(): pass", function_entrypoint_name="build")
    with pytest.raises(NotImplementedError):
        custom_component.build()


def test_build_config_no_code():
    component = CustomComponent(code=None)

    assert component.get_function_entrypoint_args == []
    assert component.get_function_entrypoint_return_type == []


@pytest.fixture
def component(client, active_user):
    return CustomComponent(
        user_id=active_user.id,
        field_config={
            "fields": {
                "llm": {"type": "str"},
                "url": {"type": "str"},
                "year": {"type": "int"},
            }
        },
    )


@pytest.fixture(scope="session")
def test_flow(db):
    flow_data = {
        "nodes": [{"id": "1"}, {"id": "2"}],
        "edges": [{"source": "1", "target": "2"}],
    }

    # Create flow
    flow = FlowCreate(id=uuid4(), name="Test Flow", description="Fixture flow", data=flow_data)

    # Add to database
    db.add(flow)
    db.commit()

    yield flow

    # Clean up
    db.delete(flow)
    db.commit()


@pytest.fixture(scope="session")
def db(app):
    # Setup database for tests
    yield app.db

    # Teardown
    app.db.drop_all()


def test_list_flows_return_type(component):
    flows = component.list_flows()
    assert isinstance(flows, list)


def test_list_flows_flow_objects(component):
    flows = component.list_flows()
    assert all(isinstance(flow, Flow) for flow in flows)


def test_build_config_return_type(component):
    config = component.build_config()
    assert isinstance(config, dict)


def test_build_config_has_fields(component):
    config = component.build_config()
    assert "fields" in config


def test_build_config_fields_dict(component):
    config = component.build_config()
    assert isinstance(config["fields"], dict)


def test_build_config_field_keys(component):
    config = component.build_config()
    assert all(isinstance(key, str) for key in config["fields"])


def test_build_config_field_values_dict(component):
    config = component.build_config()
    assert all(isinstance(value, dict) for value in config["fields"].values())


def test_build_config_field_value_keys(component):
    config = component.build_config()
    field_values = config["fields"].values()
    assert all("type" in value for value in field_values)


def test_create_and_validate_component_valid_code(test_component_code):
    component = CustomComponent(code=test_component_code)
    assert isinstance(component, CustomComponent)


def test_build_langchain_template_custom_component_valid_code(test_component_code):
    component = CustomComponent(code=test_component_code)
    frontend_node = build_custom_component_template(component)
    assert isinstance(frontend_node, dict)
    template = frontend_node["template"]
    assert isinstance(template, dict)
    assert "param" in template
    param_options = template["param"]["options"]
    # Now run it again with an update field
    frontend_node = build_custom_component_template(component, update_field="param")
    new_param_options = frontend_node["template"]["param"]["options"]
    assert param_options != new_param_options


def test_build_langchain_template_custom_component_templatefield(test_component_with_templatefield_code):
    component = CustomComponent(code=test_component_with_templatefield_code)
    frontend_node = build_custom_component_template(component)
    assert isinstance(frontend_node, dict)
    template = frontend_node["template"]
    assert isinstance(template, dict)
    assert "param" in template
    param_options = template["param"]["options"]
    # Now run it again with an update field
    frontend_node = build_custom_component_template(component, update_field="param")
    new_param_options = frontend_node["template"]["param"]["options"]
    assert param_options != new_param_options
