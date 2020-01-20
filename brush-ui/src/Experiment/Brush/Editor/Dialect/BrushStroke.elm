module Experiment.Brush.Editor.Dialect.BrushStroke exposing (BrushStroke, parser, toString, fromStringList)

import Parser exposing ((|.), (|=), Parser, keyword, spaces, succeed, Trailing(..), run, DeadEnd)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Experiment.Brush.Editor.Dialect.RelativePoint as RelativePoint exposing (RelativePoint)
import Experiment.Brush.Editor.Dialect.Fraction as Fraction exposing (Fraction)
type alias BrushStroke =
    { id : Identifier
    , position: RelativePoint
    , scale: Fraction
    , rotation: Fraction
    }

parser : Parser BrushStroke
parser =
    succeed BrushStroke
        |. keyword "BrushStroke"
        |. spaces
        |= Identifier.parser
        |. spaces
        |. keyword "P"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |. keyword "S"
        |. spaces
        |= Fraction.parser
        |. spaces
        |. keyword "R"
        |. spaces
        |= Fraction.parser


toString : BrushStroke -> String
toString value =
    [ "BrushStroke"
    , Identifier.toString value.id
    , "P"
    , RelativePoint.toString value.position
    , "S"
    , Fraction.toString value.scale
    , "R"
    , Fraction.toString value.rotation
    ]
        |> String.join " "

fromString: String -> (String, Result (List DeadEnd) BrushStroke)
fromString line  =
    (line, run parser line)

fromStringList: List String -> List (String, Result (List DeadEnd) BrushStroke)
fromStringList lines =
    List.map fromString lines
