module Experiment.Brush.Editor.Dialect.BrushStroke exposing (BrushStroke, parser, toString, fromStringList, view)

import Parser exposing ((|.), (|=), Parser, keyword, spaces, succeed, Trailing(..), run, DeadEnd)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)
import Experiment.Brush.Editor.Dialect.RelativePoint as RelativePoint exposing (RelativePoint)
import Experiment.Brush.Editor.Dialect.Fraction as Fraction exposing (Fraction)
import Html exposing (Html)
import Svg exposing (use, g)
import Svg.Attributes exposing (transform, fill, xlinkHref)
import Experiment.Brush.Editor.Dialect.PixelSqDim as PixelSqDim

type alias BrushStroke =
    { id : Identifier
    , position: RelativePoint
    , scale: Fraction
    , rotation: Fraction
    }

parser : Parser BrushStroke
parser =
    succeed BrushStroke
        |. keyword "BrushStroke"
        |. spaces
        |= Identifier.parser
        |. spaces
        |. keyword "P"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |. keyword "S"
        |. spaces
        |= Fraction.parser
        |. spaces
        |. keyword "R"
        |. spaces
        |= Fraction.parser


toString : BrushStroke -> String
toString value =
    [ "BrushStroke"
    , Identifier.toString value.id
    , "P"
    , RelativePoint.toString value.position
    , "S"
    , Fraction.toString value.scale
    , "R"
    , Fraction.toString value.rotation
    ]
        |> String.join " "

fromString: String -> (String, Result (List DeadEnd) BrushStroke)
fromString line  =
    (line, run parser line)

fromStringList: List String -> List (String, Result (List DeadEnd) BrushStroke)
fromStringList lines =
    List.map fromString lines

toPix: Fraction -> String
toPix fraction =
    PixelSqDim.fromFraction 1000 fraction |> String.fromFloat

toDeg: Fraction -> String
toDeg fraction =
    PixelSqDim.fromFraction 360 fraction |> String.fromFloat

asTransformString: BrushStroke -> String
asTransformString brushStroke =
    [
        "rotate("
        , toDeg brushStroke.rotation
        , ")"
        , "scale("
        , Fraction.asFloatString brushStroke.scale
        , ")"
        ,"translate("
        , toPix brushStroke.position.dx
        , toPix brushStroke.position.dy
        , ")"
    ] |> String.join " "

view : BrushStroke -> Html a
view brushStroke =
    g [ transform <| asTransformString brushStroke ] [
    use [
    fill "black"
    , xlinkHref "#brush"
    ]
        []
    ]