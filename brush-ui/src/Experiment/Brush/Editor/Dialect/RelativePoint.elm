module Experiment.Brush.Editor.Dialect.RelativePoint exposing
    ( RelativePoint
    , parser
    , toString
    )

import Experiment.Brush.Editor.Dialect.FractionUnit as FractionUnit exposing (Fraction)
import Parser exposing ((|.), (|=), Parser, spaces, succeed)


type alias RelativePoint =
    { dx : Fraction
    , dy : Fraction
    }

parser : Parser RelativePoint
parser =
    succeed RelativePoint
        |= FractionUnit.parser
        |. spaces
        |= FractionUnit.parser


toString : RelativePoint -> String
toString value =
    FractionUnit.toString value.dx ++ " " ++ FractionUnit.toString value.dy
