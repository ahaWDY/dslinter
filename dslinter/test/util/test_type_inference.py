"""Class which tests the TypeInference util class."""
import astroid

from dslinter.util.type_inference import TypeInference


class TestTypeInference:
    """Class which tests the TypeInference util class."""

    def test_add_reveal_type_calls(self):
        """Test the add_reveal_type_calls() method with a single expression."""
        code = "a = b.c(d)"
        nodes = [astroid.parse(code).body[0].value]

        result = TypeInference.add_reveal_type_calls(code, nodes, lambda node: node.func.expr.name)
        assert result == "a = b.c(d); reveal_type(b)"

    def test_add_reveal_type_calls_multiple(self):
        """Test the add_reveal_type_calls() method with multiple expressions."""
        code = "a = b.c(d)\nx = 5 \ne = f.g()"
        tree = astroid.parse(code)
        nodes = [tree.body[0].value, tree.body[2].value]

        result = TypeInference.add_reveal_type_calls(code, nodes, lambda node: node.func.expr.name)
        assert result == "a = b.c(d); reveal_type(b)\nx = 5 \ne = f.g(); reveal_type(f)"

    def test_run_mypy_success(self):
        """Test if mypy is ran successfully on some correct code."""
        result = TypeInference.run_mypy("a = 5")
        assert result == "Success: no issues found in 1 source file\n"

    def test_run_mypy_error(self):
        """Test if mypy returns an error when code is incorrect."""
        result = TypeInference.run_mypy("a: str = 5")
        assert result.splitlines()[1] == "Found 1 error in 1 file (checked 1 source file)"
