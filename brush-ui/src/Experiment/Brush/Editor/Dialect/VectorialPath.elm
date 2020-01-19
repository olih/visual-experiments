module Experiment.Brush.Editor.Dialect.VectorialPath exposing (VectorialPath, parser, toString)

import Parser exposing ((|.), (|=), Parser, keyword, spaces, succeed, Trailing(..))
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Experiment.Brush.Editor.Dialect.VectorialSegment as VectorialSegment exposing (VectorialSegment)

type alias VectorialPath =
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
parser : Parser VectorialPath
parser =
    succeed VectorialPath
        |. keyword "Path"
        |. spaces
        |= Identifier.parser
        |. spaces
        |= segmentsParser


toString : VectorialPath -> String
toString value =
    [ "Path"
    , Identifier.toString value.id
    , "["
    , value.segments |> List.map VectorialSegment.toString |> String.join ","
    , "]"
    ]
        |> String.join " "
