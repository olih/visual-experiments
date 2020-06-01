module Experiment.Brush.Editor.Dialect.SectionTypeId exposing (SectionTypeId(..), parser, toString)

import Parser exposing ((|.), Parser, keyword, oneOf, succeed)

type SectionTypeId
    = SettingsSection
    | BrushesSection
    | MonochromeSection


parser : Parser SectionTypeId
parser =
    oneOf
        [ succeed SettingsSection
            |. keyword "section:settings"
        , succeed BrushesSection
            |. keyword "section:brushes"
        , succeed MonochromeSection
            |. keyword "section:monochrome"
        ]


toString : SectionTypeId -> String
toString value =
    case value of
        SettingsSection ->
            "section:settings"

        BrushesSection ->
            "section:brushes"

        MonochromeSection ->
            "section:monochrome"
