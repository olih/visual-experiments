module VectorialPathUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.VectorialPath as VectorialPath
import Fuzzing exposing (vectorialPathString)
import Parser exposing(run)

suite : Test
suite =
    describe "The VectorialPath Module"
    [
        describe "parse"
        [
            fuzz vectorialPathString "should parse valid vectorial path" <|
                \path ->
                    run VectorialPath.parser path
                    |> Result.map VectorialPath.toString
                        |> Expect.equal (Ok path)
        ]

    ]