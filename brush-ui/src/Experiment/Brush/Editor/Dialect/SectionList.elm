module Experiment.Brush.Editor.Dialect.SectionList exposing (fromString, toString)

import Parser exposing (DeadEnd, Problem(..), run)
import Experiment.Brush.Editor.Dialect.Section as Section exposing (Section)

sectionMarker: String
sectionMarker =
    String.concat["\n",String.repeat 8 "-", "\n"]

fromString: String -> Result (List DeadEnd) (List Section)
fromString content =
    content 
        |> String.split sectionMarker
        |> List.map Section.fromString
        |> List.foldr (Result.map2 (::)) (Ok []) --flatten results       

toString : List Section -> String
toString sections =
    sections 
    |> List.map Section.toString
    |> String.join sectionMarker
