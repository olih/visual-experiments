module Experiment.Brush.Editor.Dialect.BrushStrokeContent exposing (BrushStrokeContent, fromSection, view)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushStroke as BrushStroke exposing (BrushStroke)
import Html exposing (Html)
import Svg exposing (g)

type alias BrushStrokeContent =
    { 
        section: Section
        , strokes: Content BrushStroke
    }

fromSection: Section -> BrushStrokeContent
fromSection section =
    BrushStrokeContent section (BrushStroke.fromStringList section.lines |> Content.toContent)

view : BrushStrokeContent -> List (Html a)
view content =
    content.strokes.values 
    |> List.map BrushStroke.view