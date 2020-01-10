module Fuzzing exposing(oneOfList, oneRangeParamId, rangeNumber, positiveNumber, mediaItemString, rangeParamString, invalidMediaItemString, invalidRangeParamString)

import Fuzz exposing (Fuzzer, int, list, string, intRange)
import Experiment.Brush.Editor.Settings.RangeParamId exposing(RangeParamId(..))

oneOfList: List a -> Fuzzer a
oneOfList list =
    List.map Fuzz.constant list |> Fuzz.oneOf

oneRangeParamId: Fuzzer RangeParamId
oneRangeParamId = oneOfList [CrossoverRangeId, MutationRangeId, PopulationRangeId]

rangeNumber : Fuzzer Int
rangeNumber = 
    intRange 1 1000

positiveNumber : Fuzzer Int
positiveNumber = 
    intRange 1 1000000000

mediaItemString : Fuzzer String
mediaItemString =
    positiveNumber 
    |> Fuzz.map (\n -> String.concat ["ID ", String.fromInt n, " G 7 T P"])

rangeParamString : Fuzzer String
rangeParamString =
    positiveNumber 
    |> Fuzz.map (\n -> String.concat ["SETTINGS RANGE MUTATION ", String.fromInt n])

invalidMediaItemString : Fuzzer String
invalidMediaItemString =
    positiveNumber 
    |> Fuzz.map (\n -> String.concat ["ID ", String.fromInt n, " wrong"])

invalidRangeParamString : Fuzzer String
invalidRangeParamString =
    oneOfList ["SETTINGS RANGE MUTATION", "SETTINGS RANGE WRONG"]
