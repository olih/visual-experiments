module RangeParamsUnitTests exposing (suite)

import Expect
import Experiment.Brush.Editor.Dialect.RangeParam as RangeParam exposing (RangeParam)
import Fuzzing exposing (oneRangeParamId, rangeNumber)
import Parser exposing (run)
import Test exposing (Test, describe, fuzz2)


suite : Test
suite =
    describe "The RangeParam Module"
        [ describe "parse"
            [ fuzz2 oneRangeParamId rangeNumber "should parse valid range" <|
                \paramId value ->
                    RangeParam.toString (RangeParam paramId value)
                        |> run RangeParam.parser
                        |> Expect.equal (Ok (RangeParam paramId value))
            ]
        ]
