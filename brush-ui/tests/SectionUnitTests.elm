module SectionUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.Section as Section
import Fuzzing exposing (sectionString)
import Parser exposing(run)

suite : Test
suite =
    describe "The Section Module"
    [
        describe "parse"
        [
            fuzz sectionString "should parse valid brush" <|
                \section ->
                    Section.fromString section
                    |> Result.map Section.toString
                        |> Expect.equal (Ok section)
        ]

    ]