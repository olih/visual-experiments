module Experiment.Brush.Editor.Dialect.Section exposing (Section, fromString, toString, getLatestGeneration, byId, bySectionType, getIdsByType)

import Parser exposing (DeadEnd, Problem(..), run)
import Experiment.Brush.Editor.Dialect.SectionHeader as SectionHeader exposing(SectionHeader)
import Experiment.Brush.Editor.Dialect.SectionTypeId exposing(SectionTypeId(..))
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)


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

getIdsByType: SectionTypeId -> List Section -> List Identifier
getIdsByType sectionType sections =
    sections 
    |> List.filter (\section -> section.header.sectionType == sectionType)
    |> List.map (\section -> section.header.id)

getLatestGeneration: List Section -> Maybe Identifier
getLatestGeneration sections =
    getIdsByType BrushesSection sections
    |> List.map Identifier.toInt
    |> List.maximum
    |> Maybe.map Identifier.fromInt

byId: Identifier -> Section -> Bool
byId id section =
    section.header.id == id

bySectionType: SectionTypeId -> Section -> Bool
bySectionType typeId section =
    section.header.sectionType == typeId
