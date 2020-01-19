module Experiment.Brush.Editor.Dialect.MediaItem exposing (MediaItem, parser, toString, toggleTrash, togglePreserve)

import Parser exposing ((|.), (|=), Parser, keyword, oneOf, spaces, succeed)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)

type alias MediaItem =
    { id : Identifier
    , trash : Bool
    , preserve : Bool
    }


toggleTrash : MediaItem -> MediaItem
toggleTrash item =
    { item | trash = not item.trash }


togglePreserve : MediaItem -> MediaItem
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


parser : Parser MediaItem
parser =
    succeed MediaItem
        |. keyword "Media"
        |. spaces
        |= Identifier.parser
        |. spaces
        |= trashParser
        |. spaces
        |= preserveParser


toString : MediaItem -> String
toString value =
    [ "Media"
    , Identifier.toString value.id
    , if value.trash then
        "T"
      else
        "_"
    , if value.preserve then
        "P"
      else
        "_"
    ]
        |> String.join " "
