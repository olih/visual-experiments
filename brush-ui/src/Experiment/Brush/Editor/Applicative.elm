module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.Dialect.MultiContent as MultiContent exposing(MultiContent)

type alias Model =
    {   idx: Int
        , generation: Int
        , showTrash: Bool
        , multiContent : MultiContent
    }

reset: Model
reset = {
        idx = 0
        , generation = 0
        , showTrash = False
        , multiContent = MultiContent.reset
    }
