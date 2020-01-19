module Experiment.Brush.Editor.Dialect.Brush exposing (Brush, parser, toString, toggleTrash, togglePreserve, fromStringList)

import Parser exposing ((|.), (|=), Parser, keyword, spaces, succeed, Trailing(..), oneOf, run, DeadEnd)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Experiment.Brush.Editor.Dialect.VectorialSegment as VectorialSegment exposing (VectorialSegment)

type alias Brush =
    { id : Identifier
    , trash : Bool
    , preserve : Bool
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

toggleTrash : Brush -> Brush
toggleTrash item =
    { item | trash = not item.trash }


togglePreserve : Brush -> Brush
togglePreserve item =
    { item | preserve = not item.preserve }

trashParser : Parser Bool
trashParser =
    oneOf
        [ succeed True
            |. keyword "T"
        , succeed False
            |. keyword "_"
        ]


preserveParser : Parser Bool
preserveParser =
    oneOf
        [ succeed True
            |. keyword "P"
        , succeed False
            |. keyword "_"
        ]

parser : Parser Brush
parser =
    succeed Brush
        |. keyword "Brush"
        |. spaces
        |= Identifier.parser
        |. spaces
        |= trashParser
        |. spaces
        |= preserveParser
        |. spaces
        |= segmentsParser


toString : Brush -> String
toString value =
    [ "Brush"
    , Identifier.toString value.id
    , if value.trash then
        "T"
      else
        "_"
    , if value.preserve then
        "P"
      else
        "_"
    , "["
    , value.segments |> List.map VectorialSegment.toString |> String.join ","
    , "]"
    ]
        |> String.join " "

fromString: String -> (String, Result (List DeadEnd) Brush)
fromString line  =
    (line, run parser line)

fromStringList: List String -> List (String, Result (List DeadEnd) Brush)
fromStringList lines =
    List.map fromString lines
