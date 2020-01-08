module RangeParamsUnitTests exposing (..)

import Expect exposing (Expectation)
import Fuzz exposing (Fuzzer, int, intRange, list, string, constant, oneOf)
import Test exposing (..)
import Experiment.Brush.Editor.Settings.RangeParam as RangeParam exposing(RangeParam)
import Parser exposing(run)
import Fuzzing exposing(oneRangeParamId, rangeNumber)

suite : Test
suite =
    describe "The RangeParam Module"
    [
        describe "parse"
        [
            fuzz2 oneRangeParamId rangeNumber "should parse valid range" <|
                \paramId value ->
                    RangeParam.toString (RangeParam paramId value) |> run RangeParam.parser
                        |> Expect.equal (Ok (RangeParam paramId value))
        ]

    ]