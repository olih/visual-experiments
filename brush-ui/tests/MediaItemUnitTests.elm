module MediaItemUnitTests exposing (suite)

import Expect as Expect
import Experiment.Brush.Editor.Dialect.MediaItem as MediaItem exposing (MediaItem)
import Fuzz exposing (bool, tuple)
import Fuzzing exposing (positiveNumber, identifier)
import Parser exposing (run)
import Test exposing (Test, describe, fuzz3)
import Tuple exposing (first, second)


suite : Test
suite =
    describe "The MediaItem Module"
        [ describe "parse"
            [ fuzz3 identifier positiveNumber (tuple ( bool, bool )) "should parse valid media item" <|
                \id gen duo ->
                    MediaItem.toString (MediaItem id gen (first duo) (second duo))
                        |> run MediaItem.parser
                        |> Expect.equal (Ok (MediaItem id gen (first duo) (second duo)))
            ]
        ]
