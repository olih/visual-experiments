module BrushUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.Brush as Brush
import Fuzzing exposing (brushString)
import Parser exposing(run)

suite : Test
suite =
    describe "The Brush Module"
    [
        describe "parse"
        [
            fuzz brushString "should parse valid brush" <|
                \path ->
                    run Brush.parser path
                    |> Result.map Brush.toString
                        |> Expect.equal (Ok path)
        ]

    ]