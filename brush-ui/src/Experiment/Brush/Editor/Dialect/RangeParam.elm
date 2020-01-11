module Experiment.Brush.Editor.Dialect.RangeParam exposing(RangeParam, parser, toString, setValue)

import Parser exposing ((|.), (|=), Parser, chompWhile, getChompedString, int, map, run, spaces, succeed, symbol, keyword, oneOf)
import Experiment.Brush.Editor.Dialect.RangeParamId as RangeParamId exposing(RangeParamId)
type alias RangeParam = {
    id: RangeParamId
    , value: Int
    }

setValue: Int -> RangeParam -> RangeParam
setValue value param =
    { param | value = value}

parser : Parser RangeParam
parser =
    succeed RangeParam
        |. keyword "SETTINGS"
        |. spaces
        |. keyword "RANGE"
        |. spaces
        |= RangeParamId.parser
        |. spaces
        |= int

toString: RangeParam -> String
toString value =
    [
    "SETTINGS", "RANGE"
    , RangeParamId.toString value.id
    , String.fromInt value.value
    ]
    |> String.join " "