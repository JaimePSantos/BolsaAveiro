from iddl.RunProgram import runTests
from tests.TestVariables.InterpVar import (
    interpVarValues,
)

class TestInterpreter(object):
    def test_formula1(self):
        assert runTests("[1,2] + [3,4] - [5,6]") == interpVarValues[0]
    def test_formula2(self):
        assert runTests("[3,4]") == interpVarValues[1]
    def test_formula3(self):
        assert runTests("[1,2] + [3,4] + [5,6]*[5,6]") == interpVarValues[2]
    def test_formula4(self):
        assert runTests("[1,2] - [3,4]") == interpVarValues[3]
    def test_formula5(self):
        assert runTests("x-[1,2]") == interpVarValues[4]
    def test_formula6(self):
        assert runTests("[1,2] / [3,4]") == interpVarValues[5]
    def test_formula7(self):
        assert runTests("x / [1,2]") == interpVarValues[6]
    def test_formula8(self):
        assert runTests("x / [1,2] + [3,4]") == interpVarValues[7]
    def test_formula9(self):
        assert runTests("[1,2] < [2,3]") == interpVarValues[8]
    def test_formula10(self):
        assert runTests("[1,2] <= [2,3]") == interpVarValues[9]
    def test_formula11(self):
        assert runTests("[2,3] > [1,2]") == interpVarValues[10]
    def test_formula12(self):
        assert runTests("[2,3] >= [1,2]") == interpVarValues[11]
    def test_formula13(self):
        assert runTests("[1,2] < [2,3] AND [2,3] > [1,2]") == interpVarValues[12]
    def test_formula14(self):
        assert runTests("!(x < [2,3] AND y > [1,2])") == interpVarValues[13]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula16(self):
        assert runTests("[1,2] < [2,3] AND x > [1,2] OR y/[5,6] + x*z") == interpVarValues[15]
    def test_formula17(self):
        assert runTests("x := [5,6] ; (y := [1,2]) -> x > y") == interpVarValues[16]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]
    def test_formula15(self):
        assert runTests("!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]