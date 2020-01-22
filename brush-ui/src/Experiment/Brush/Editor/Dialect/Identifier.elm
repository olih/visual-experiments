module Experiment.Brush.Editor.Dialect.Identifier exposing (Identifier(..), parser, toString, toInt, fromInt)

import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)

type Identifier = IntIdentifier Int

parser : Parser Identifier
parser =
    succeed IntIdentifier
        |. symbol "i:"
        |. spaces
        |= int


toString : Identifier -> String
toString value =
    case value of
       IntIdentifier n ->
        String.concat["i:", String.fromInt n]
toInt : Identifier -> Int
toInt value =
    case value of
       IntIdentifier n ->
        n

fromInt : Int -> Identifier
fromInt value =
    IntIdentifier value