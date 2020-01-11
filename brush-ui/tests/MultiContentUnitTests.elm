module MultiContentUnitTests exposing (..)

import Expect as Expect
import Fuzz exposing (Fuzzer, int, intRange, list, string, constant, oneOf)
import Test exposing (Test, describe, fuzz2)
import Experiment.Brush.Editor.Dialect.MultiContent as MultiContent exposing (MultiContent)
import Fuzzing exposing(mediaItemString, rangeParamString, invalidMediaItemString, invalidRangeParamString)

suite : Test
suite =
    describe "The MultiContent Module"
    [
        describe "conversion from amd to list of string"
        [
            fuzz2 (list mediaItemString) (list rangeParamString) "should convert valid values" <|
                \mediaItems rangeParams ->
                    MultiContent.fromStringList (mediaItems ++ rangeParams)
                    |> MultiContent.toStringList
                        |> Expect.equal (mediaItems ++ rangeParams)
            , fuzz2 (list invalidMediaItemString) (list invalidRangeParamString) "should not convert invalid values" <|
                \mediaItems rangeParams ->
                    MultiContent.fromStringList (mediaItems ++ rangeParams)
                    |> .failures
                    |> List.map .source
                        |> Expect.equal (mediaItems ++ rangeParams)
        ]

    ]