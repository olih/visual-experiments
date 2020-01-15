module Experiment.Brush.Editor.Dialect.RangeParam exposing (RangeParam, parser, setValue, toString)

import Experiment.Brush.Editor.Dialect.RangeParamId as RangeParamId exposing (RangeParamId)
import Parser exposing ((|.), (|=), Parser, int, keyword, spaces, succeed)


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
        |. keyword "Settings"
        |. spaces
        |. keyword "Range"
        |. spaces
        |= RangeParamId.parser
        |. spaces
        |= int


toString : RangeParam -> String
toString value =
    [ "Settings"
    , "Range"
    , RangeParamId.toString value.id
    , String.fromInt value.value
    ]
        |> String.join " "
