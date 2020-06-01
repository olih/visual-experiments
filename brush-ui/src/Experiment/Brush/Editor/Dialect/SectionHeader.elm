module Experiment.Brush.Editor.Dialect.SectionHeader exposing (SectionHeader, parser, toString)

import Parser exposing ((|.), (|=), Parser, spaces, succeed, keyword, end)
import Experiment.Brush.Editor.Dialect.SectionTypeId as SectionTypeId exposing(SectionTypeId)
import Experiment.Brush.Editor.Dialect.Identifier as Identifier exposing(Identifier)

type alias SectionHeader =
    { id : Identifier
      , sectionType : SectionTypeId
    }


parser : Parser SectionHeader
parser =
    succeed SectionHeader
        |. keyword "Section"
        |. spaces
        |= Identifier.parser
        |. spaces
        |= SectionTypeId.parser
        |. end


toString : SectionHeader -> String
toString value =
    String.join " " ["Section", value.id |> Identifier.toString, value.sectionType |> SectionTypeId.toString]
