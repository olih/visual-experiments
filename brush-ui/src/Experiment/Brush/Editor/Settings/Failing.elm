module Experiment.Brush.Editor.Settings.Failing exposing (FailureKind(..), Failure, fromDeadEndList, create, createMessage)

import Parser exposing(DeadEnd, Problem(..), (|.), (|=), Parser, oneOf, andThen, chompWhile, getChompedString, int, variable, map, run, spaces, succeed, symbol, keyword, chompUntilEndOr, problem)

type FailureKind =
    InvalidLengthFailure
    | InvalidFormatFailure

type alias Failure = {
    kind: FailureKind
    , source: String --source of the failure
    , message: String --human readable message
    }

deadEndToString: DeadEnd -> String
deadEndToString deadEnd =
    case deadEnd.problem of
        Problem str ->
            str
        Expecting str ->
            "Expecting " ++ str
        ExpectingSymbol str ->
            "Expecting symbol " ++ str
        ExpectingKeyword str ->
            "Expecting keyword " ++ str
        UnexpectedChar ->
            "Unexpected character"
        ExpectingInt ->
            "Expecting Int"
        ExpectingHex ->
            "Expecting Hex"
        ExpectingOctal ->
            "Expecting Octal"
        ExpectingBinary ->
            "Expecting Binary"
        ExpectingFloat ->
            "Expecting Float"
        ExpectingNumber ->
            "Expecting Number"
        ExpectingVariable ->
            "Expecting Variable"
        ExpectingEnd ->
            "Expecting End"
        BadRepeat ->
            "Bad Repeat"


failureKindParser : Parser FailureKind
failureKindParser =
  oneOf
    [succeed InvalidFormatFailure
        |. keyword "(753c7eba)"
     , succeed InvalidLengthFailure
        |. keyword "(a799245c)"   
    ]

createMessage: FailureKind -> String -> String
createMessage failureKind message =
    case failureKind of
        InvalidFormatFailure -> "(753c7eba) " ++ message
        InvalidLengthFailure -> "(a799245c) " ++ message

create: String -> FailureKind -> String -> Failure
create source failureKind message =
    {
    kind = failureKind
    , source = source
    , message = createMessage failureKind message
    }

parseFailureKind : String -> FailureKind
parseFailureKind str =
    case run failureKindParser str of
        Ok failureKind ->
            failureKind

        Err msg ->
            InvalidFormatFailure

deadEndToFailureKind: DeadEnd -> FailureKind
deadEndToFailureKind deadEnd =
    case deadEnd.problem of
        Problem str ->
            parseFailureKind str
        otherwise ->
            InvalidFormatFailure 

fromDeadEndList: List DeadEnd -> String -> Failure
fromDeadEndList deadEnds source =
    let
        message = deadEnds |> List.map deadEndToString |> String.join "; "
        failureKind = deadEnds |> List.head |> Maybe.map deadEndToFailureKind |> Maybe.withDefault InvalidFormatFailure
    in
        Failure failureKind source message
