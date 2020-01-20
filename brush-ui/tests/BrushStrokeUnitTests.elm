module BrushStrokeUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.BrushStroke as BrushStroke
import Fuzzing exposing (brushStrokeString)
import Parser exposing(run)

suite : Test
suite =
    describe "The BrushStroke Module"
    [
        describe "parse"
        [
            fuzz brushStrokeString "should parse valid brush stroke" <|
                \stroke ->
                    run BrushStroke.parser stroke
                    |> Result.map BrushStroke.toString
                        |> Expect.equal (Ok stroke)
        ]

    ]