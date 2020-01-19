module MediaItemUnitTests exposing (suite)

import Expect as Expect
import Experiment.Brush.Editor.Dialect.MediaItem as MediaItem exposing (MediaItem)
import Fuzz exposing (bool)
import Fuzzing exposing (identifier)
import Parser exposing (run)
import Test exposing (Test, describe, fuzz3)

suite : Test
suite =
    describe "The MediaItem Module"
        [ describe "parse"
            [ fuzz3 identifier bool bool "should parse valid media item" <|
                \id trash preserve ->
                    MediaItem.toString (MediaItem id trash preserve)
                        |> run MediaItem.parser
                        |> Expect.equal (Ok (MediaItem id trash preserve))
            ]
        ]
