module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.MultiContent as MultiContent exposing(MultiContent)

type alias Model =
    {   count: Int
        , idx: Int
        , generation: Int
        , showTrash: Bool
        , multiContent : MultiContent
    }

reset: Model
reset = {
        count = 0
        , idx = 0
        , generation = 0
        , showTrash = False
        , multiContent = MultiContent.reset
    }
