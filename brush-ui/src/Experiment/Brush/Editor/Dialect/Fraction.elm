module Experiment.Brush.Editor.Dialect.Fraction exposing (Fraction, asFloatString, parser, toString)

import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)


type alias Fraction =
    { numerator : Int
    , denominator : Int
    }


parser : Parser Fraction
parser =
    succeed Fraction
        |. spaces
        |= int
        |. symbol "/"
        |= int
        |. spaces


toString : Fraction -> String
toString value =
    String.fromInt value.numerator ++ "/" ++ String.fromInt value.denominator


asFloatString : Fraction -> String
asFloatString fraction =
    toFloat fraction.numerator / toFloat fraction.denominator
    |> String.fromFloat
