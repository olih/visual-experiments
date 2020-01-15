module Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId(..), parser, toString)

import Parser exposing ((|.), Parser, keyword, oneOf, succeed)

-- Predefined list now but open to evolution

type RangeParamId
    = CrossoverRangeId
    | MutationRangeId
    | PopulationRangeId


parser : Parser RangeParamId
parser =
    oneOf
        [ succeed CrossoverRangeId
            |. keyword "range:crossover"
        , succeed MutationRangeId
            |. keyword "range:mutation"
        , succeed PopulationRangeId
            |. keyword "range:population"
        ]


toString : RangeParamId -> String
toString value =
    case value of
        CrossoverRangeId ->
            "range:crossover"

        MutationRangeId ->
            "range:mutation"

        PopulationRangeId ->
            "range:population"
