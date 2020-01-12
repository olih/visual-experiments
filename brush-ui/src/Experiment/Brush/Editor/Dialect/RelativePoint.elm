module Experiment.Brush.Editor.Dialect.RelativePoint exposing
    ( RelativePoint
    , parser
    , toString
    )

import Experiment.Brush.Editor.Dialect.Fraction as Fraction exposing (Fraction)
import Parser exposing ((|.), (|=), Parser, spaces, succeed)


type alias RelativePoint =
    { dx : Fraction
    , dy : Fraction
    }

parser : Parser RelativePoint
parser =
    succeed RelativePoint
        |= Fraction.parser
        |. spaces
        |= Fraction.parser


toString : RelativePoint -> String
toString value =
    Fraction.toString value.dx ++ " " ++ Fraction.toString value.dy
