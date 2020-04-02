module Experiment.Brush.Editor.Dialect.Brush exposing (Brush, byId, fromStringList, parser, toString, toStringList, togglePreserve, togglePreserveForId, toggleTrash, toggleTrashForId, view)

import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing (Identifier)
import Experiment.Brush.Editor.Dialect.VectorialSegment as VectorialSegment exposing (VectorialSegment)
import Html exposing (Html)
import Parser exposing ((|.), (|=), DeadEnd, Parser, Trailing(..), keyword, oneOf, run, spaces, succeed)
import Svg exposing (path,  symbol)
import Svg.Attributes exposing (d, id, viewBox)


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


fromString : String -> ( String, Result (List DeadEnd) Brush )
fromString line =
    ( line, run parser line )


fromStringList : List String -> List ( String, Result (List DeadEnd) Brush )
fromStringList lines =
    List.map fromString lines


toStringList : List Brush -> List String
toStringList brushes =
    List.map toString brushes


byId : Identifier -> Brush -> Bool
byId id brush =
    brush.id == id


toggleTrashForId : Identifier -> List Brush -> List Brush
toggleTrashForId id list =
    list
        |> List.map
            (\brush ->
                if brush.id == id then
                    toggleTrash brush

                else
                    brush
            )


togglePreserveForId : Identifier -> List Brush -> List Brush
togglePreserveForId id list =
    list
        |> List.map
            (\brush ->
                if brush.id == id then
                    togglePreserve brush

                else
                    brush
            )


asPathString : Brush -> String
asPathString brush =
    brush.segments
        |> List.map VectorialSegment.toSvgString
        |> (++) [ "z" ]
        |> String.join " "


view : Brush -> Html a
view brush =
    symbol [ viewBox "0 0 600 600", id "brush" ]
        [ path [ d <| asPathString brush ]
            []
        ]
