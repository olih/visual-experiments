module SectionUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz, fuzz2)
import Experiment.Brush.Editor.Dialect.Section as Section
import Fuzzing exposing (sectionString, brushSectionsString)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier
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
        ], 
        describe "getLatestGeneration"
        [
            fuzz2 sectionString brushSectionsString "should get latest generation" <|
                \i7 sections ->
                    (i7 :: "Section i:20 section:brushes\nA\nB" :: sections |> List.filterMap (Section.fromString >> Result.toMaybe))
                    |> Section.getLatestGeneration
                    |> Expect.equal (Identifier.fromInt 20)
        ]

    ]