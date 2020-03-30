module Main exposing (Document, Model, Msg(..), init, main, subscriptions, update, view)

import Browser
import Experiment.Brush.Editor.AppEvent as AppEvent exposing (UIEvent(..))
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


type Msg
    = OnUIEvent UIEvent
    | GotText (Result Http.Error String)


noCmd : Model -> ( Model, Cmd Msg )
noCmd model =
    ( model, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
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

        OnUIEvent event ->
            case model of
                Loaded appModel ->
                    AppEvent.processEvent event appModel |> Loaded |> noCmd

                _ ->
                    model |> noCmd



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


type alias Document msg =
    { title : String
    , body : List (Html msg)
    }


viewLoading : Document Msg
viewLoading =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Loading Brush UI" ]
            ]
        ]
    }


viewUnloadable : Failure -> Document Msg
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


viewLoaded : App.Model -> Document Msg
viewLoaded appModel =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Loading Brush UI" ]
            , button [ onClick (OnUIEvent OnNext)] [ text "Next" ]
            ]
        ]
    }


view : Model -> Document Msg
view model =
    case model of
        Loading ->
            viewLoading

        Unloadable failure ->
            viewUnloadable failure

        Loaded appModel ->
            viewLoaded appModel


fetchGeneticBrushes : Cmd Msg
fetchGeneticBrushes =
    Http.get
        { url = "/brushes.gen.txt"
        , expect = Http.expectString GotText
        }
