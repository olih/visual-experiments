module Experiment.Brush.Editor.Dialect.Identifier exposing (Identifier(..), parser, toString, toInt, fromInt, notFound)

import Parser exposing ((|.), (|=), Parser, int, spaces, succeed, symbol)

type Identifier = IntIdentifier Int | NotFoundIdenfifier

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
       NotFoundIdenfifier ->
        "i:nf"

toInt : Identifier -> Int
toInt value =
    case value of
       IntIdentifier n ->
            n
       NotFoundIdenfifier ->
            -1
fromInt : Int -> Identifier
fromInt value =
    IntIdentifier value

notFound: Identifier
notFound = NotFoundIdenfifier