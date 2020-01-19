module Experiment.Brush.Editor.Dialect.Brush exposing (Brush, parser, toString)

import Parser exposing ((|.), (|=), Parser, keyword, spaces, succeed, Trailing(..))
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Experiment.Brush.Editor.Dialect.VectorialSegment as VectorialSegment exposing (VectorialSegment)

type alias Brush =
    { id : Identifier
    , segments : List VectorialSegment
    }


segmentsParser : Parser (List VectorialSegment)
segmentsParser =
    Parser.sequence
    { start = "["
    , separator = ","
    , end = "]"
    , spaces = spaces
    , item = VectorialSegment.parser
    , trailing = Optional
    }
parser : Parser Brush
parser =
    succeed Brush
        |. keyword "Brush"
        |. spaces
        |= Identifier.parser
        |. spaces
        |= segmentsParser


toString : Brush -> String
toString value =
    [ "Brush"
    , Identifier.toString value.id
    , "["
    , value.segments |> List.map VectorialSegment.toString |> String.join ","
    , "]"
    ]
        |> String.join " "
