module FractionUnitTests exposing (..)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.FractionUnit as FractionUnit exposing (Fraction)
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
                    FractionUnit.toString fn |> run FractionUnit.parser
                        |> Expect.equal (Ok fn)
        ]

    ]