module Experiment.Brush.Editor.Dialect.Content exposing (Content, toContent, setValues, asValuesIn)
import Parser exposing (DeadEnd)
import Tuple exposing (first, second)
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure)

type alias Content a =
    { 
    lines: List String    
    , values : List a
    , failures : List Failure
    }

addValue: String -> a -> Content a -> Content a
addValue line value content =
    { content |
     values = value :: content.values
     , lines = line :: content.lines }

addFailure: String -> List DeadEnd -> Content a -> Content a
addFailure line deads content =
    { content | failures = (Failing.fromDeadEndList deads line) :: content.failures}

add: (String, Result (List DeadEnd) a) -> Content a -> Content a
add lineAndResult content =
    case second lineAndResult of
        Ok v ->
            addValue (first lineAndResult) v content

        Err v ->
            addFailure (first lineAndResult) v content
toContent : List (String, Result (List DeadEnd) a) -> Content a
toContent list =
    List.foldr
        add
        { lines = [], values = [] , failures = []}
        list

setValues: List a -> List String -> Content a -> Content a
setValues values lines content =
    { content | values = values, lines = lines}

asValuesIn: Content a -> List a -> List String  -> Content a
asValuesIn content values lines =
    { content | values = values, lines = lines}