module Fuzzing exposing (invalidMediaItemString, invalidRangeParamString, mediaItemString, oneOfList, oneRangeParamId, positiveNumber, rangeNumber, rangeParamString, fraction)

import Fuzz exposing (Fuzzer, intRange)
import Random as Random
import Shrink as Shrink
import Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId(..))
import Experiment.Brush.Editor.Dialect.FractionUnit exposing (Fraction)


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