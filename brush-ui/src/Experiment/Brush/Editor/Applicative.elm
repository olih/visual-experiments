module Experiment.Brush.Editor.Applicative exposing(reset, fromString)

import Experiment.Brush.Editor.Dialect.Section as Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushContent as BrushContent exposing (BrushContent)
import Experiment.Brush.Editor.Dialect.Brush as Brush
import Experiment.Brush.Editor.Dialect.BrushStrokeContent as BrushStrokeContent exposing (BrushStrokeContent)
import Experiment.Brush.Editor.Dialect.RangeContent as RangeContent exposing (RangeContent)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure)
import Experiment.Brush.Editor.Dialect.SectionList as SectionList
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing (Identifier)
import Experiment.Brush.Editor.Dialect.SectionTypeId exposing(SectionTypeId(..))
type alias Model =
    {   idx: Identifier
        , idxList: List Identifier
        , generation: Identifier
        , latestGeneration: Identifier
        , sections: List Section
        , maybeBrushContent: Maybe BrushContent
        , maybeRangeContent: Maybe RangeContent
        , maybeBrushStrokeContent: Maybe BrushStrokeContent
        , failure : Maybe Failure
    }

reset: Model
reset = {
        idx = Identifier.notFound
        , idxList = []
        , generation = Identifier.notFound
        , latestGeneration = Identifier.notFound
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
        
        maybeRangeContent = sections 
            |> List.filter (Section.bySectionType SettingsSection)
            |> List.filter (Section.byId latestGeneration)
            |> List.head
            |> Maybe.map RangeContent.fromSection

        maybeBrushStrokeContent = sections 
            |> List.filter (Section.bySectionType MonochromeSection)
            |> List.head
            |> Maybe.map BrushStrokeContent.fromSection

        idxList = maybeBrushContent 
            |> Maybe.map (.brushes >> .values)
            |> Maybe.withDefault []
            |> List.map .id
        
        idx = idxList |> List.head |> Maybe.withDefault (Identifier.notFound)

    in
        { model | 
            sections = sections
            , failure = failure
            , latestGeneration = latestGeneration
            , generation = latestGeneration
            , maybeBrushContent = maybeBrushContent
            , maybeRangeContent = maybeRangeContent
            , maybeBrushStrokeContent = maybeBrushStrokeContent
            , idxList = idxList
            , idx = idx
        }

trash: Model -> Model
trash model =
    let
        maybeNewBrush = model.maybeBrushContent 
            |> Maybe.map (.brushes >> .values) 
            |> Maybe.withDefault []
            |> List.filter (Brush.byId model.idx)
            |> List.head
            |> Maybe.map Brush.toggleTrash
        

    in
        model