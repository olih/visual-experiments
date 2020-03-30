module Experiment.Brush.Editor.Dialect.BrushContent exposing (BrushContent, fromSection, setBrushes, asBrushesIn, setValues)

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

setBrushes: Content Brush -> BrushContent -> BrushContent
setBrushes brushes content =
    { content | brushes = brushes }

asBrushesIn: BrushContent -> Content Brush -> BrushContent
asBrushesIn content brushes  =
    { content | brushes = brushes }

setValues : List Brush -> BrushContent -> BrushContent
setValues values content =
    Content.setValues values (Brush.toStringList values) content.brushes |> asBrushesIn content