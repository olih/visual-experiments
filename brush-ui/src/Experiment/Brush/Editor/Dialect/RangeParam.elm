module Experiment.Brush.Editor.Dialect.RangeParam exposing (RangeParam, parser, setValue, toString, fromStringList)

import Experiment.Brush.Editor.Dialect.RangeParamId as RangeParamId exposing (RangeParamId)
import Parser exposing ((|.), (|=), Parser, int, keyword, spaces, succeed, end, run, DeadEnd)


type alias RangeParam =
    { id : RangeParamId
    , value : Int
    }


setValue : Int -> RangeParam -> RangeParam
setValue value param =
    { param | value = value }


parser : Parser RangeParam
parser =
    succeed RangeParam
        |. keyword "Range"
        |. spaces
        |= RangeParamId.parser
        |. spaces
        |= int
        |.end


toString : RangeParam -> String
toString value =
    [ "Range"
    , RangeParamId.toString value.id
    , String.fromInt value.value
    ]
        |> String.join " "

fromString: String -> (String, Result (List DeadEnd) RangeParam)
fromString line  =
    (line, run parser line)

fromStringList: List String -> List (String, Result (List DeadEnd) RangeParam)
fromStringList lines =
    List.map fromString lines