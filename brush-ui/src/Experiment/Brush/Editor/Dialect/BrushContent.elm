module Experiment.Brush.Editor.Dialect.BrushContent exposing (BrushContent, fromSection)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.Brush as Brush exposing (Brush)

type alias BrushContent =
    { 
        section: Section
        , brushes: Content Brush
    }

fromSection: Section -> BrushContent
fromSection section =
    BrushContent section (Brush.fromStringList section.lines |> Content.toContent)