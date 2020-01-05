module Experiment.Brush.Editor.Schema exposing(MediaItem, parser, toString)

import Parser exposing ((|.), (|=), Parser, chompWhile, getChompedString, int, map, run, spaces, succeed, symbol, keyword, oneOf)

type alias MediaItem = {
    id: Int
    , generation: Int
    , trash: Bool
    , preserve: Bool
    }

toggleTrash: MediaItem -> MediaItem
toggleTrash item =
    { item | trash = not item.trash}

togglePreserve: MediaItem -> MediaItem
togglePreserve item =
    { item | preserve = not item.preserve}

trashParser : Parser Bool
trashParser =
  oneOf
    [ succeed True
        |. keyword "T"
    , succeed False
        |. keyword "t"
    ]
preserveParser : Parser Bool
preserveParser =
  oneOf
    [ succeed True
        |. keyword "P"
    , succeed False
        |. keyword "p"
    ]
parser : Parser MediaItem
parser =
    succeed MediaItem
        |. keyword "ID"
        |. symbol "="
        |= int
        |. spaces
        |. keyword "G"
        |. symbol "="
        |= int
        |. spaces
        |= trashParser
        |= preserveParser

toString: MediaItem -> String
toString value =
    [
    "ID=",String.fromInt value.id
    ,"G=", String.fromInt value.generation
    , if value.trash then "T" else "t"
    , if value.preserve then "P" else "p"
    ]
    |> String.join " "