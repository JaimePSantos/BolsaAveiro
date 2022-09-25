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
        assert runTests(
            "[1,2] + [3,4] + [5,6]*[5,6]") == interpVarValues[2]

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
        assert runTests(
            "[1,2] < [2,3] AND [2,3] > [1,2]") == interpVarValues[12]

    def test_formula14(self):
        assert runTests(
            "!(x < [2,3] AND y > [1,2])") == interpVarValues[13]

    def test_formula15(self):
        assert runTests(
            "!(x < [2,3] AND y > [1,2]) AND $ z IN (z + z*z)") == interpVarValues[14]

    def test_formula16(self):
        assert runTests(
            "[1,2] < [2,3] AND x > [1,2] OR y/[5,6] + x*z") == interpVarValues[15]

    def test_formula17(self):
        assert runTests(
            "x := [5,6] ; (y := [1,2]) -> x > y") == interpVarValues[16]

    def test_formula18(self):
        assert runTests("[{ x>y }](x > y)") == interpVarValues[17]

    def test_formula19(self):
        assert runTests(
            "<{ x := [1,2]+[3,4] }> x>y") == interpVarValues[18]

    def test_formula20(self):
        assert runTests(
            "y>[1,3]-[1,1] -> [{ x>[1,2]*[2,2] }] (x > y)") == interpVarValues[19]

    def test_formula20(self):
        assert runTests(
            "y>[1,3]-[1,1] -> [{ x>[1,2]*[2,2] }] (x > y)") == interpVarValues[19]

    def test_formula21(self):
        assert runTests("x < [1,2]") == interpVarValues[20]

    def test_formula22(self):
        assert runTests(
            "x < [1,2] AND y < [1,2]") == interpVarValues[21]

    def test_formula23(self):
        assert runTests(
            "x < [1,2] AND y < [1,2] AND z < [3,5]") == interpVarValues[22]

    def test_formula24(self):
        assert runTests(
            "!(x < [2,3] AND y > [1,2])") == interpVarValues[23]

    def test_formula25(self):
        assert runTests("x:=[1,2]") == interpVarValues[24]

    def test_formula26(self):
        assert runTests("?(x >y AND i>j)") == interpVarValues[25]

    def test_formula27(self):
        assert runTests("?(x >[1,2] AND i>j)") == interpVarValues[26]

    def test_formula28(self):
        assert runTests(
            "x'=[1,2] & (x>y AND i>j)") == interpVarValues[27]

    def test_formula29(self):
        assert runTests(
            "x:=y ; x'=[1,2] & (x>z AND i>j AND w > l) ; y' = [3,4] & (x > y)") == interpVarValues[28]

    def test_formula30(self):
        assert runTests(
            "x:=y || x := z ; x'=[1,2]") == interpVarValues[29]

    def test_formula31(self):
        assert runTests(
            "(  x:=y ; x:=z ; ( [{(x:=k)**}](x>y)))**") == interpVarValues[30]

    def test_formula32(self):
        assert runTests(
            "x<=[1,3] -> [{x'=[1,2]}] x>[1,1]") == interpVarValues[31]

    def test_formula33(self):
        assert runTests("?(x > 0 AND x>y)") == interpVarValues[32]

    def test_formula34(self):
        assert runTests("? (x > y)") == interpVarValues[33]

    def test_formula35(self):
        assert runTests(
            "? (x > 0) ; (x'=-x, y'=-y & (0<x))") == interpVarValues[34]

    def test_formula36(self):
        assert runTests(
            "?(2<x AND x<4 AND 0<y AND y<2);( x'= 5-x , y'=-y ; (2 < x AND x < 4 AND 0<y AND y<2))") == interpVarValues[35]

    def test_formula37(self):
        assert runTests(
            "[{x'=1}] ( [{ y'=1 }] ( x>y ) ) -> x > y") == interpVarValues[36]

    def test_formula38(self):
        assert runTests(
            "[{x:=[1,2]; y:=[0,1] ; {x'=x - 1}}] (x>0 AND  y>=0)") == interpVarValues[37]

    def test_formula39(self):
        assert runTests(
            "[{x:=[1,2]+[2,3]; y:=[0,1] * ([6,6]/[3,3]) ; {x'=x - 1}}] (x>0 AND  y>=0)") == interpVarValues[38]

    def test_formula40(self):
        assert runTests(
            "[{x:=[1,2]; y:=[0,1] ;{x'=x-1}}] (x>0 AND y>=0)") == interpVarValues[39]

    def test_formula41(self):
        assert runTests("[{x:=[5,6];y:=[3,4] }] [{ {?(x > 0) ; {x'=-x, y'=-y & 0<x } || ?(2<x AND x<4 AND 0<y AND y<2); { x'= 5-x , y'=-y & (2 < x AND x < 4 AND 0<y AND y<2)} || ?( 4 < x AND 0<y AND y<2 ) ; { x'=5-x , y'=3-y & ( 4<x AND 0 <y AND y < 2 ) } || ?( 2 < x AND x < 4 AND 2 < y ) ; { x' = -x , y' = -y & ( 2 < x AND x < 4 AND 2 < y )} || ?( 4 < x AND 2 < y ) ; { x' = -x , y'=3 - y & ( 4 < x AND 2 < y )}}**}] ( x>2 )") == interpVarValues[40]
