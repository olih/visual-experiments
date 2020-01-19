module Experiment.Brush.Editor.Dialect.RangeParam exposing (RangeParam, parser, setValue, toString)

import Experiment.Brush.Editor.Dialect.RangeParamId as RangeParamId exposing (RangeParamId)
import Parser exposing ((|.), (|=), Parser, int, keyword, spaces, succeed, end)


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
