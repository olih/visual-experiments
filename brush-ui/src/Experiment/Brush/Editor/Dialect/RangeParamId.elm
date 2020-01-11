module Experiment.Brush.Editor.Dialect.RangeParamId exposing(RangeParamId(..), parser, toString)

import Parser exposing ((|.), (|=), Parser, chompWhile, getChompedString, int, map, run, spaces, succeed, symbol, keyword, oneOf)
type RangeParamId = CrossoverRangeId | MutationRangeId | PopulationRangeId

parser : Parser RangeParamId
parser =
  oneOf
    [ succeed CrossoverRangeId
        |. keyword "CROSSOVER"
    , succeed MutationRangeId
        |. keyword "MUTATION"
    , succeed PopulationRangeId
        |. keyword "POPULATION"
    ]

toString: RangeParamId -> String
toString value =
    case value of
       CrossoverRangeId -> "CROSSOVER"
       MutationRangeId -> "MUTATION"
       PopulationRangeId -> "POPULATION"