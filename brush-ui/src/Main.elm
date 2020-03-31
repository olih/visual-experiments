module Main exposing (Document, Model, init, main, subscriptions, update, view)

import Browser
import Experiment.Brush.Editor.AppEvent as AppEvent exposing (Msg(..))
import Experiment.Brush.Editor.Applicative as App
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure, FailureKind(..))
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http


type Model
    = Unloadable Failure
    | Loading
    | Loaded App.Model


main =
    Browser.document
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


init : () -> ( Model, Cmd Msg )
init _ =
    ( Loading, fetchGeneticBrushes )



-- UPDATE


noCmd : Model -> ( Model, Cmd Msg )
noCmd model =
    ( model, Cmd.none )


update : AppEvent.Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotText result ->
            case result of
                Ok fullContent ->
                    case App.fromString fullContent of
                        Ok appModel ->
                            Loaded appModel |> noCmd

                        Err failure ->
                            Unloadable failure |> noCmd

                Err _ ->
                    Unloadable (Failing.create "whole content" InvalidFormatFailure "fetching /brushes.gen.txt did not work") |> noCmd

        _ ->
            case model of
                Loaded appModel ->
                    processEvent msg appModel |> Loaded |> noCmd

                _ ->
                    model |> noCmd



-- SUBSCRIPTIONS


subscriptions : Model -> Sub AppEvent.Msg
subscriptions model =
    Sub.none



-- VIEW


type alias Document msg =
    { title : String
    , body : List (Html msg)
    }


viewLoading : Document AppEvent.Msg
viewLoading =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Loading Brush UI" ]
            ]
        ]
    }


viewUnloadable : Failure -> Document AppEvent.Msg
viewUnloadable failure =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Loading Brush UI failed" ]
            , p [] [ text failure.source ]
            , p [] [ text failure.message ]
            ]
        ]
    }


viewLoaded : App.Model -> Document AppEvent.Msg
viewLoaded appModel =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Loading Brush UI" ]
            , button [ onClick OnNext] [ text "Next" ]
            ]
        ]
    }


view : Model -> Document AppEvent.Msg
view model =
    case model of
        Loading ->
            viewLoading

        Unloadable failure ->
            viewUnloadable failure

        Loaded appModel ->
            viewLoaded appModel


fetchGeneticBrushes : Cmd AppEvent.Msg
fetchGeneticBrushes =
    Http.get
        { url = "/brushes.gen.txt"
        , expect = Http.expectString GotText
        }

processEvent: Msg -> App.Model -> App.Model
processEvent uiEvent appModel =
    appModel