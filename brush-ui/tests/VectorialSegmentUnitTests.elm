module VectorialSegmentUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.VectorialSegment as VectorialSegment
import Fuzzing exposing (vectorialSegmentString)
import Parser exposing(run)

suite : Test
suite =
    describe "The VectorialSegment Module"
    [
        describe "parse"
        [
            fuzz vectorialSegmentString "should parse valid vectorial segment" <|
                \segment ->
                    run VectorialSegment.parser segment
                    |> Result.map VectorialSegment.toString
                        |> Expect.equal (Ok segment)
        ]

    ]