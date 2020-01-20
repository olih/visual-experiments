module Experiment.Brush.Editor.Dialect.Section exposing (Section, fromString, toString, getLatestGeneration)

import Parser exposing (DeadEnd, Problem(..), run)
import Experiment.Brush.Editor.Dialect.SectionHeader as SectionHeader exposing(SectionHeader)
import Experiment.Brush.Editor.Dialect.SectionTypeId exposing(SectionTypeId(..))
import Experiment.Brush.Editor.Dialect.Identifier as Identifier


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

getLatestGeneration: List Section -> Maybe Int
getLatestGeneration sections =
    sections 
    |> List.filter (\section -> section.header.sectionType == BrushesSection)
    |> List.map (\section -> section.header.id |> Identifier.toInt)
    |> List.maximum

