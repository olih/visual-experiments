module IdentifierUnitTests exposing (suite)

import Expect as Expect
import Test exposing (Test, describe, fuzz)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Fuzzing exposing (identifier)
import Parser exposing(run)

suite : Test
suite =
    describe "The Identifier Module"
    [
        describe "parse"
        [
            fuzz identifier "should parse valid identifier" <|
                \id ->
                    Identifier.toString id |> run Identifier.parser
                        |> Expect.equal (Ok id)
        ]

    ]