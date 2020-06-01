module Tags exposing (toTags, reset, toListWithoutOne)

import Set exposing (Set)
import Json.Decode as Decode exposing (Decoder, list, string)
import Set exposing(Set)
toSetDecoder : Decoder (List comparable) -> Decoder (Set comparable)
toSetDecoder listDecoder =
    Decode.map Set.fromList listDecoder

toTags: Decoder (Set String)
toTags =
    list string |> toSetDecoder

reset: Set String
reset =
    Set.empty

toListWithoutOne: String -> Set String -> List String
toListWithoutOne tag tags =
    Set.remove tag tags
    |> Set.toList
    |> List.sort