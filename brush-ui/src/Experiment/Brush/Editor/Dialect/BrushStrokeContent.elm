module Experiment.Brush.Editor.Dialect.BrushStrokeContent exposing (BrushStrokeContent, fromSection)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.BrushStroke as BrushStroke exposing (BrushStroke)

type alias BrushStrokeContent =
    { 
        section: Section
        , strokes: Content BrushStroke
    }

fromSection: Section -> BrushStrokeContent
fromSection section =
    BrushStrokeContent section (BrushStroke.fromStringList section.lines |> Content.toContent)