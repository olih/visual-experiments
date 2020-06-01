module FractionUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.Fraction as Fraction
import Fuzzing exposing (fraction)
import Parser exposing(run)

suite : Test
suite =
    describe "The FractionUnit Module"
    [
        describe "parse"
        [
            fuzz fraction "should parse valid fraction" <|
                \fn ->
                    Fraction.toString fn |> run Fraction.parser
                        |> Expect.equal (Ok fn)
        ]

    ]