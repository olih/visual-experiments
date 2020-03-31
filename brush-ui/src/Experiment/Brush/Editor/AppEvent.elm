module Experiment.Brush.Editor.AppEvent exposing (Msg(..))

import Experiment.Brush.Editor.Dialect.RangeParamId exposing (RangeParamId)
import Http

type Msg = 
    OnNext
    | OnPrevious
    | OnFirst
    | OnLast
    | OnTrash
    | OnPreserve
    | OnSave
    | OnChangeParam RangeParamId String
    | GotText (Result Http.Error String)

