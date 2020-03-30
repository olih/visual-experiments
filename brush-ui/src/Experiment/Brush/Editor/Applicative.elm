module Experiment.Brush.Editor.Applicative exposing(Model, fromString, trash)

import Experiment.Brush.Editor.Dialect.Section as Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushContent as BrushContent exposing (BrushContent)
import Experiment.Brush.Editor.Dialect.Brush as Brush
import Experiment.Brush.Editor.Dialect.BrushStrokeContent as BrushStrokeContent exposing (BrushStrokeContent)
import Experiment.Brush.Editor.Dialect.RangeContent as RangeContent exposing (RangeContent)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure, FailureKind(..))
import Experiment.Brush.Editor.Dialect.SectionList as SectionList
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing (Identifier)
import Experiment.Brush.Editor.Dialect.SectionTypeId exposing(SectionTypeId(..))
type alias Model =
    {   idx: Identifier
        , idxList: List Identifier
        , generation: Identifier
        , latestGeneration: Identifier
        , sections: List Section
        , brushContent: BrushContent
        , rangeContent: RangeContent
        , brushStrokeContent: BrushStrokeContent
    }

create: List Identifier -> Identifier -> List Section -> BrushContent -> RangeContent -> BrushStrokeContent -> Model
create idxList latestGeneration sections brushContent rangeContent brushStrokeContent =
  {   idx = idxList |> List.head |> Maybe.withDefault (Identifier.notFound)
        , idxList = idxList
        , generation = latestGeneration
        , latestGeneration = latestGeneration
        , sections = sections
        , brushContent = brushContent
        , rangeContent = rangeContent
        , brushStrokeContent = brushStrokeContent
    }  

fromString: String -> Result Failure Model
fromString content =
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
        
        in
            Maybe.map3 (\ brush range brushStroke -> create idxList latestGeneration sections brush range brushStroke |> Ok) maybeBrushContent maybeRangeContent maybeBrushStrokeContent
            |> Maybe.withDefault (Maybe.map identity failure |> Maybe.withDefault (Failing.create "whole content" InvalidFormatFailure "A section is missing") |> Err)

trash: Model -> Model
trash model =
    { model | brushContent =  BrushContent.setValues (Brush.toggleTrashForId model.idx model.brushContent.brushes.values) model.brushContent }