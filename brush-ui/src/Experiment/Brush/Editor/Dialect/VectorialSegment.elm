module Experiment.Brush.Editor.Dialect.VectorialSegment exposing (VectorialSegment, parser, toString)

import Parser exposing ((|.), (|=), Parser, int, keyword, oneOf, spaces, succeed)
import Experiment.Brush.Editor.Dialect.Fraction as Fraction exposing (Fraction)
import Experiment.Brush.Editor.Dialect.RelativePoint as RelativePoint exposing(RelativePoint)

-- all positions are relative

type VectorialSegment =
    LineTo RelativePoint
    | Horizontal Fraction
    | Vertical Fraction
    | CubicCurve RelativePoint RelativePoint RelativePoint
    | SmoothCubicCurve RelativePoint RelativePoint
    | QuadraticCurve RelativePoint RelativePoint
    | SmoothQuadraticCurve RelativePoint


lineParser : Parser VectorialSegment
lineParser =
    succeed LineTo
        |. keyword "l"
        |. spaces
        |= RelativePoint.parser

horizontalParser : Parser VectorialSegment
horizontalParser =
    succeed Horizontal
        |. keyword "h"
        |. spaces
        |= Fraction.parser

verticalParser : Parser VectorialSegment
verticalParser =
    succeed Vertical
        |. keyword "v"
        |. spaces
        |= Fraction.parser

cubicCurveParser : Parser VectorialSegment
cubicCurveParser =
    succeed CubicCurve
        |. keyword "c"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

smoothCubicCurveParser : Parser VectorialSegment
smoothCubicCurveParser =
    succeed SmoothCubicCurve
        |. keyword "s"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

quadraticCurveParser : Parser VectorialSegment
quadraticCurveParser =
    succeed QuadraticCurve
        |. keyword "q"
        |. spaces
        |= RelativePoint.parser
        |. spaces
        |= RelativePoint.parser

smoothQuadraticCurveParser : Parser VectorialSegment
smoothQuadraticCurveParser =
    succeed SmoothQuadraticCurve
        |. keyword "t"
        |. spaces
        |= RelativePoint.parser

parser: Parser VectorialSegment
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

toString: VectorialSegment -> String
toString path =
    case path of
        LineTo pt -> 
            String.join " " ["l", RelativePoint.toString pt]
        Horizontal f ->
             String.join " " ["h", Fraction.toString f]
        Vertical f ->
            String.join " " ["v", Fraction.toString f]
        CubicCurve pt1 pt2 pt3 -> 
            String.join " " ["c", RelativePoint.toString pt1, RelativePoint.toString pt2, RelativePoint.toString pt3]
        SmoothCubicCurve pt1 pt2 -> 
            String.join " " ["s", RelativePoint.toString pt1, RelativePoint.toString pt2]
        QuadraticCurve pt1 pt2 -> 
            String.join " " ["q", RelativePoint.toString pt1, RelativePoint.toString pt2]
        SmoothQuadraticCurve pt1 -> 
            String.join " " ["t", RelativePoint.toString pt1]
