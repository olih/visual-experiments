module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.Dialect.Section as Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushContent as BrushContent exposing (BrushContent)
import Experiment.Brush.Editor.Dialect.BrushStrokeContent exposing (BrushStrokeContent)
import Experiment.Brush.Editor.Dialect.RangeContent exposing (RangeContent)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure)
import Experiment.Brush.Editor.Dialect.SectionList as SectionList
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing (Identifier)
import Experiment.Brush.Editor.Dialect.SectionTypeId exposing(SectionTypeId(..))
type alias Model =
    {   idx: Identifier
        , generation: Identifier
        , latestGeneration: Identifier
        , showTrash: Bool
        , sections: List Section
        , maybeBrushContent: Maybe BrushContent
        , maybeRangeContent: Maybe RangeContent
        , maybeBrushStrokeContent: Maybe BrushStrokeContent
        , failure : Maybe Failure
    }

reset: Model
reset = {
        idx = Identifier.notFound
        , generation = Identifier.notFound
        , latestGeneration = Identifier.notFound
        , showTrash = False
        , sections = []
        , failure = Nothing
        , maybeBrushContent = Nothing
        , maybeRangeContent = Nothing
        , maybeBrushStrokeContent = Nothing
    }

fromString: String -> Model -> Model
fromString content model =
    let
        perhapsSections = SectionList.fromString content
        sections = Result.withDefault [] perhapsSections
        failure = Failing.fromResult perhapsSections "section"

        latestGeneration = Section.getLatestGeneration sections
        
        maybeBrushContent = sections 
            |> List.filter (Section.bySectionType BrushesSection)
            |> List.filter (Section.byId latestGeneration)
            |> List.head
            |> Maybe.map BrushContent.fromSection

    in
        { model | 
            sections = sections
            , failure = failure
            , latestGeneration = latestGeneration
            , generation = latestGeneration
            , maybeBrushContent = maybeBrushContent
        }   