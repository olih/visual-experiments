module Experiment.Brush.Editor.Dialect.Section exposing (Section, fromString, toString)

import Parser exposing (DeadEnd, Problem(..), run)
import Experiment.Brush.Editor.Dialect.SectionHeader as SectionHeader exposing(SectionHeader)

type alias Section =
    { header : SectionHeader
    , lines : List String
    }

fromString: String -> Result (List DeadEnd) Section
fromString content =
    case content |> String.lines of
        headerStr :: lines ->
            run SectionHeader.parser headerStr
                |> Result.map (\header -> Section header lines)
        _ ->
            Err (Problem "The first line should be a section header" |> DeadEnd 0 0 |> List.singleton)
         

toString : Section -> String
toString value =
    (value.header |> SectionHeader.toString) :: value.lines
    |> String.join "\n"
