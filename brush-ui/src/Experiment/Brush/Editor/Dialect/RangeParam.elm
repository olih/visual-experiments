module Experiment.Brush.Editor.Dialect.RangeParam exposing (RangeParam, parser, setValue, toString, fromStringList, view)

import Experiment.Brush.Editor.Dialect.RangeParamId as RangeParamId exposing (RangeParamId)
import Parser exposing ((|.), (|=), Parser, int, keyword, spaces, succeed, end, run, DeadEnd)

import Html exposing (Html, label, input, text, div)
import Html.Attributes as Attr
import Experiment.Brush.Editor.AppEvent exposing (Msg(..))
import Html.Events exposing (onInput)
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


viewOption: RangeParamId -> Int -> Html a
viewOption rgParamId value =
    label [ Attr.class "radio" ]
            [ input [ Attr.name <| RangeParamId.toString rgParamId, Attr.type_ "radio", Attr.value <| String.fromInt value ]
                []
            , text <| String.fromInt value
            ]

view : RangeParam -> Html Msg
view rgParam =
    [1, 2, 3]
    |> List.map (viewOption rgParam.id)
    |> div [ Attr.class "control", onInput <| OnChangeParam rgParam.id]