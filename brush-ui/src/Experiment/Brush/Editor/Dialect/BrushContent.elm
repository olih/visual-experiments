module Experiment.Brush.Editor.Dialect.BrushContent exposing (BrushContent, fromSection, setBrushes, asBrushesIn, setValues, getBrush, view)

import Experiment.Brush.Editor.Dialect.Content as Content exposing (Content)
import Experiment.Brush.Editor.Dialect.Section exposing (Section)
import Experiment.Brush.Editor.Dialect.Brush as Brush exposing (Brush)
import Experiment.Brush.Editor.Dialect.Identifier exposing(Identifier)
import Html exposing (Html)
import Svg exposing (svg)
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

getBrush: Identifier -> BrushContent -> Maybe Brush
getBrush identifier content =
    content.brushes.values 
    |> List.filter (\brush -> brush.id == identifier)
    |> List.head

view : Identifier -> BrushContent ->  Html a
view identifier content =
   getBrush identifier content
   |> Maybe.map Brush.view
   |> Maybe.withDefault (svg [][])
   