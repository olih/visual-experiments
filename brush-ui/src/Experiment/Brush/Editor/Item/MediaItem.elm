module Experiment.Brush.Editor.Item.MediaItem exposing(MediaItem, parser, toString)

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
        |. keyword "ID"
        |. spaces
        |= int
        |. spaces
        |. keyword "G"
        |. spaces
        |= int
        |. spaces
        |= trashParser
        |= preserveParser

toString: MediaItem -> String
toString value =
    [
    "ID", String.fromInt value.id
    ,"G", String.fromInt value.generation
    , if value.trash then "T" else "_"
    , if value.preserve then "P" else "_"
    ]
    |> String.join " "