module Fuzzing exposing (invalidMediaItemString, invalidRangeParamString, mediaItemString, oneOfList, oneRangeParamId, positiveNumber, rangeNumber, rangeParamString, fraction, vectorialPathString, identifier)

import Fuzz exposing (Fuzzer, intRange)
import Random as Random
import Shrink as Shrink
import Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId(..))
import Experiment.Brush.Editor.Dialect.Fraction exposing (Fraction)
import Experiment.Brush.Editor.Dialect.Identifier exposing(Identifier(..))


oneOfList : List a -> Fuzzer a
oneOfList list =
    List.map Fuzz.constant list |> Fuzz.oneOf


oneRangeParamId : Fuzzer RangeParamId
oneRangeParamId =
    oneOfList [ CrossoverRangeId, MutationRangeId, PopulationRangeId ]


rangeNumber : Fuzzer Int
rangeNumber =
    intRange 1 1000


positiveNumber : Fuzzer Int
positiveNumber =
    intRange 1 1000000000

identifier : Fuzzer Identifier
identifier =
    positiveNumber |> Fuzz.map IntIdentifier

mediaItemString : Fuzzer String
mediaItemString =
    positiveNumber
        |> Fuzz.map (\n -> String.concat [ "ID ", String.fromInt n, " G 7 T P" ])


rangeParamString : Fuzzer String
rangeParamString =
    positiveNumber
        |> Fuzz.map (\n -> String.concat [ "SETTINGS RANGE MUTATION ", String.fromInt n ])


invalidMediaItemString : Fuzzer String
invalidMediaItemString =
    positiveNumber
        |> Fuzz.map (\n -> String.concat [ "ID ", String.fromInt n, " wrong" ])


invalidRangeParamString : Fuzzer String
invalidRangeParamString =
    oneOfList [ "SETTINGS RANGE MUTATION", "SETTINGS RANGE WRONG" ]

fraction: Fuzzer Fraction
fraction =
    Fuzz.custom
            (Random.map2 Fraction (Random.int 0 1000000000) (Random.int 1 1000000000))
            (\{ numerator, denominator } -> Shrink.map Fraction (Shrink.int numerator) |> Shrink.andMap (Shrink.int denominator))

fractionString : Fuzzer String
fractionString =
    Fuzz.map2 (\n d -> String.concat[String.fromInt n, "/", String.fromInt d]) (intRange 0 1000000000) (intRange 1 1000000000)

relativePointString : Fuzzer String
relativePointString =
    Fuzz.map2 (\dx dy -> String.join " " [dx, dy]) fractionString fractionString

horizontalString : Fuzzer String
horizontalString =
    fractionString
        |> Fuzz.map (\f -> String.concat [ "h ", f])

verticalString : Fuzzer String
verticalString =
    fractionString
        |> Fuzz.map (\f -> String.concat [ "v ", f])

lineToString : Fuzzer String
lineToString =
    relativePointString
        |> Fuzz.map (\pt1 -> String.join " " [ "l", pt1])

cubicCurveToString : Fuzzer String
cubicCurveToString =
    Fuzz.map3 (\pt1 pt2 pt3 -> String.join " " [ "c", pt1, pt2, pt3]) relativePointString relativePointString relativePointString

smoothCubicCurveToString : Fuzzer String
smoothCubicCurveToString =
    Fuzz.map2 (\pt1 pt2 -> String.join " " [ "s", pt1, pt2]) relativePointString relativePointString

quadraticCurveToString : Fuzzer String
quadraticCurveToString =
    Fuzz.map2 (\pt1 pt2 -> String.join " " [ "q", pt1, pt2]) relativePointString relativePointString

smoothQuadraticCurveToString : Fuzzer String
smoothQuadraticCurveToString =
    Fuzz.map (\pt1 -> String.join " " [ "t", pt1]) relativePointString

vectorialPathString: Fuzzer String
vectorialPathString =
    Fuzz.oneOf [
        lineToString
        , horizontalString
        , verticalString
        , cubicCurveToString
        , smoothCubicCurveToString
        , quadraticCurveToString
        , smoothQuadraticCurveToString
    ]