module Experiment.Brush.Editor.Dialect.VectorialPath exposing (VectorialPath, parser, toString)

import Parser exposing ((|.), (|=), Parser, int, keyword, oneOf, spaces, succeed)
import Experiment.Brush.Editor.Dialect.FractionUnit as FractionUnit exposing (Fraction)
import Experiment.Brush.Editor.Dialect.RelativePoint as RelativePoint exposing(RelativePoint)

-- all positions are relative

type VectorialPath =
    LineTo RelativePoint
    | Horizontal Fraction
    | Vertical Fraction
    | CubicCurve RelativePoint RelativePoint RelativePoint
    | SmoothCubicCurve RelativePoint RelativePoint
    | QuadraticCurve RelativePoint RelativePoint
    | SmoothQuadraticCurve RelativePoint


lineParser : Parser VectorialPath
lineParser =
    succeed LineTo
        |. keyword "l"
        |. spaces
        |= RelativePoint.parser

horizontalParser : Parser VectorialPath
horizontalParser =
    succeed Horizontal
        |. keyword "h"
        |. spaces
        |= FractionUnit.parser

verticalParser : Parser VectorialPath
verticalParser =
    succeed Vertical
        |. keyword "v"
        |. spaces
        |= FractionUnit.parser

cubicCurveParser : Parser VectorialPath
cubicCurveParser =
    succeed CubicCurve
        |. keyword "c"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

smoothCubicCurveParser : Parser VectorialPath
smoothCubicCurveParser =
    succeed SmoothCubicCurve
        |. keyword "s"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

quadraticCurveParser : Parser VectorialPath
quadraticCurveParser =
    succeed QuadraticCurve
        |. keyword "q"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

smoothQuadraticCurveParser : Parser VectorialPath
smoothQuadraticCurveParser =
    succeed SmoothQuadraticCurve
        |. keyword "t"
        |. spaces
        |= RelativePoint.parser

parser: Parser VectorialPath
parser =
    oneOf [
        lineParser
        , horizontalParser
        , verticalParser
        , cubicCurveParser
        , smoothCubicCurveParser
        , quadraticCurveParser
        , smoothQuadraticCurveParser
    ]

toString: VectorialPath -> String
toString path =
    case path of
        LineTo pt -> 
            String.join " " ["l", RelativePoint.toString pt]
        Horizontal f ->
             String.join " " ["h", Fraction.toString f]        Horizontal f ->
        Vertical f ->
            String.join " " ["v", Fraction.toString f]
        CubicCurve pt1 pt2 pt3 -> 
            String.join " " ["c", RelativePoint.toString pt1, RelativePoint.toString pt2, RelativePoint.toString pt3]
        SmoothCubicCurve pt1 pt2 -> 
            String.join " " ["s", RelativePoint.toString pt1, RelativePoint.toString pt2]
        QuadraticCurve pt1 pt2 -> 
            String.join " " ["q", RelativePoint.toString pt1, RelativePoint.toString pt2]
        SmoothQuadraticCurve pt1 pt2 -> 
            String.join " " ["t", RelativePoint.toString pt1]
