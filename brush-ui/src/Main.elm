module Main exposing (Document, Model, init, main, subscriptions, update, view)

import Browser
import Html exposing (Html, div, section, i, button, span, h1, text, p, nav)
import Html.Attributes as Attr exposing(attribute)
import Html.Events exposing (onClick)
import Http
import Svg exposing (svg)
import Svg.Attributes exposing (xlinkHref, viewBox)
import Experiment.Brush.Editor.AppEvent as AppEvent exposing (Msg(..))
import Experiment.Brush.Editor.Applicative as App
import Experiment.Brush.Editor.Dialect.Failing as Failing exposing (Failure, FailureKind(..))
import Experiment.Brush.Editor.Dialect.RangeContent as RangeContent
import Experiment.Brush.Editor.Dialect.Identifier as Identifier
import Experiment.Brush.Editor.Dialect.BrushContent as BrushContent
import Experiment.Brush.Editor.Dialect.BrushStrokeContent as BrushStrokeContent

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
subscriptions _ =
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



viewRangeParamSection:  App.Model -> Html AppEvent.Msg
viewRangeParamSection appModel =
    section [ Attr.class "section" ]
        [ div [ Attr.class "container" ]
            [ h1 [ Attr.class "title" ]
                [ text "Genetic Parameters" ]
                , appModel.rangeContent |> RangeContent.view
            ]
        ]
viewIconButton: String -> Msg -> Html AppEvent.Msg
viewIconButton name action =
    button [ Attr.class "button", onClick action]
            [ span [ Attr.class "icon is-small" ]
                [ i [ Attr.class <| (["fas fa-", name] |> String.concat) ]
                    []
            ]
            ]


getFlipFlopClass: Bool -> String
getFlipFlopClass onOff =
    if onOff then "button is-success" else  "button"

viewFlipFlopButton: String -> Bool -> Msg -> Html AppEvent.Msg
viewFlipFlopButton name state action =
    button [ Attr.class <| getFlipFlopClass state, onClick action]
            [ span [ Attr.class "icon is-small" ]
                [ i [ Attr.class <| (["fas fa-", name] |> String.concat) ]
                    []
            ]
            ]

viewControlSection:  App.Model -> Html AppEvent.Msg
viewControlSection appModel =
    section [ Attr.class "section" ]
        [ div [ Attr.class "container" ]
            [ p [ Attr.class "buttons" ]
                [
                    viewIconButton "fast-backward" OnFirst
                    , viewIconButton "caret-left" OnPrevious
                    ,  viewIconButton "caret-right" OnNext
                    ,  viewIconButton "fast-forward" OnLast
                    , viewFlipFlopButton "trash" (App.isTrash appModel) OnTrash
                    , viewFlipFlopButton "star" (App.isPreserve appModel) OnPreserve
                    , viewIconButton "save" OnSave
                ]
            ]   
        ]


viewLevelItem: String -> String -> Html AppEvent.Msg
viewLevelItem desc value =
    div [ Attr.class "level-item has-text-centered" ]
            [ div []
                [ p [ Attr.class "heading" ]
                    [ text desc ]
                , p [ Attr.class "title" ]
                    [ text value ]
                ]
            ]

viewLevelSection:  App.Model -> Html AppEvent.Msg
viewLevelSection appModel =
    section [ Attr.class "section" ]
        [ nav [ Attr.class "level" ]
                [
                    viewLevelItem "Brush"  <| Identifier.toString appModel.idx
                    , viewLevelItem "Generation"  <| Identifier.toString appModel.generation
                    , viewLevelItem "Brushes"  <|  String.fromInt <| List.length <| appModel.brushContent.brushes.values 
                ]
        ]

viewBrushPreviewSection: App.Model -> Html AppEvent.Msg
viewBrushPreviewSection appModel =
    section [ Attr.class "section" ]
        [ div [ Attr.class "container" ]
            [ 
                svg [ attribute "xmlns:xlink" "http://www.w3.org/1999/xlink", viewBox "0 0 1000 1000"] 
                <| BrushContent.view appModel.idx appModel.brushContent
                :: BrushStrokeContent.view appModel.brushStrokeContent
            ]   
        ]


viewLoaded : App.Model -> Document AppEvent.Msg
viewLoaded appModel =
    { title = "Brush UI"
    , body =
        [ div []
            [ h1 [] [ text "Brush UI" ]
            , viewLevelSection appModel
            , viewBrushPreviewSection appModel
            , viewControlSection appModel
            , viewRangeParamSection appModel
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
    case uiEvent of
        OnFirst -> App.goFirst appModel
        OnLast -> App.goLast appModel
        OnNext -> App.goNext appModel
        OnPrevious -> App.goPrevious appModel
        OnTrash -> App.trash appModel
        OnPreserve -> App.preserve appModel
        OnChangeParam id value -> App.changeParam id value appModel
        OnSave -> appModel -- should properly save
        GotText _ -> appModel