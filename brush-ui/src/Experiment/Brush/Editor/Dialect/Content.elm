module Experiment.Brush.Editor.Dialect.Content exposing (Content, toContent)

import Experiment.Brush.Editor.Dialect.Failing exposing (Failure)

type alias Content a =
    { 
    values : List a
    , failures : List Failure
    }

addValue: a -> Content a -> Content a
addValue value content =
    { content | values = value :: content.values}

addFailure: Failure -> Content a -> Content a
addFailure failure content =
    { content | failures = failure :: content.failures}

add: Result Failure a -> Content a -> Content a
add rs content =
    case rs of
        Ok v ->
            addValue v content

        Err v ->
            addFailure v content
toContent : List (Result Failure a) -> Content a
toContent list =
    List.foldr
        add
        { values = [] , failures = []}
        list