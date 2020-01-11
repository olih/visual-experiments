module MediaItemUnitTests exposing (..)

import Expect exposing (Expectation)
import Tuple exposing (first, second)
import Fuzz exposing (Fuzzer, int, bool, intRange, list, string, constant, oneOf, tuple)
import Test exposing (..)
import Experiment.Brush.Editor.Dialect.MediaItem as MediaItem exposing(MediaItem)
import Parser exposing(run)
import Fuzzing exposing(positiveNumber)

suite : Test
suite =
    describe "The MediaItem Module"
    [
        describe "parse"
        [
            fuzz3 positiveNumber positiveNumber (tuple (bool, bool)) "should parse valid media item" <|
                \id gen duo ->
                    MediaItem.toString (MediaItem id gen (first duo) (second duo)) |> run MediaItem.parser
                        |> Expect.equal (Ok (MediaItem id gen (first duo) (second duo)))
        ]

    ]