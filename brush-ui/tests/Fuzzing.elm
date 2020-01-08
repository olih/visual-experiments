module Fuzzing exposing(oneOfList, oneRangeParamId, rangeNumber, positiveNumber)

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