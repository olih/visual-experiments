module Experiment.Brush.Editor.Applicative exposing(reset)

import Experiment.Brush.Editor.MultiContent exposing(MultiContent)

type alias Model =
    {   count: Int
        , lines: List String
        , idx: Int
        , generation: Int
        , showTrash: Bool
        , multiContent : MultiContent
        , generationIndexes: List (Int, Int)
    }

reset: Model
reset = {
        count = 0
        , idx = 0
        , generation = 0
        , showTrash = False
        , items = []
        , generationIndexes = []
    }
